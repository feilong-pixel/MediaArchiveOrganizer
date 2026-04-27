import os
import shutil
import csv
from datetime import datetime
from core.date_classifier import get_target_date, build_date_path
from core.duplicate_detector import compute_file_hash, compute_phash
from core.hash_db import load_hash_db, save_hash_db, add_hash_record, get_valid_original_paths
import platform

SUPPORTED_EXT = (".jpg", ".jpeg", ".png", ".mp4", ".mov")

def is_windows():
    return platform.system() == "Windows"

def timestamp():
    # Keep log timestamps human-readable for quick troubleshooting.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Transfer the file while preserving timestamps. Windows doesn't preserve 
# creation time by default, so we need to set it explicitly.
def transfer_file(src, dst, mode):
    st = os.stat(src)
    atime, mtime, ctime = st.st_atime, st.st_mtime, st.st_ctime

    if mode == "copy":
        shutil.copy2(src, dst)
    else:
        shutil.move(src, dst)

    if not is_windows():
        return

    try:
        import pywintypes
        import win32file
        import win32con
    except ImportError:
        return

    handle = win32file.CreateFile(
        dst,
        win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL,
        None
    )

    win32file.SetFileTime(
        handle,
        pywintypes.Time(ctime),  # CreationTime
        pywintypes.Time(atime),  # AccessTime
        pywintypes.Time(mtime)   # ModifyTime
    )

    handle.close()


def get_unique_path(directory: str, filename: str) -> str:
    # Append a numeric suffix to avoid overwriting an existing file.
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(directory, filename)
    counter = 1

    while os.path.exists(candidate):
        candidate = os.path.join(directory, f"{base}_{counter}{ext}")
        counter += 1

    return candidate


def get_duplicate_path(original_path: str) -> str:
    # Keep duplicates beside the retained file using an explicit duplicate suffix.
    directory = os.path.dirname(original_path)
    base, ext = os.path.splitext(os.path.basename(original_path))
    counter = 1
    candidate = os.path.join(directory, f"{base}_dup{counter}{ext}")

    while os.path.exists(candidate):
        counter += 1
        candidate = os.path.join(directory, f"{base}_dup{counter}{ext}")

    return candidate


def build_duplicate_report_path(log_path: str) -> str:
    log_dir = os.path.dirname(os.path.abspath(log_path))
    return os.path.join(log_dir, "duplicate_report.csv")


def append_duplicate_report_rows(report_path: str, rows: list[dict[str, str]]) -> None:
    if not rows:
        return

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    fieldnames = [
        "original_name",
        "original_path",
        "kept_path",
        "duplicate_method",
        "hash",
        "duplicate_path",
    ]
    write_header = not os.path.exists(report_path)

    with open(report_path, "a", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def resolve_duplicate_hash(path: str, duplicate_detection: str) -> tuple[str, str] | None:
    # Select the requested duplicate detection method for the current file.
    if duplicate_detection == "off":
        return None

    if duplicate_detection == "strict":
        return "strict", compute_file_hash(path)

    phash_value = compute_phash(path)
    if phash_value is None:
        return None

    return "phash", phash_value


def organize_images(
    src_dir: str,
    dst_dir: str,
    log_path: str,
    mode: str = "move",
    lang=None,
    duplicate_detection: str = "phash",
    phash_threshold: int = 4,
):
    os.makedirs(dst_dir, exist_ok=True)
    log_lines = []
    duplicate_rows = []

    # Load the persisted hash database once per run.
    hash_db = load_hash_db()

    for root, _, files in os.walk(src_dir):
        for name in files:
            path = os.path.join(root, name)

            # Ignore files outside the supported media extensions.
            if not name.lower().endswith(SUPPORTED_EXT):
                continue

            try:
                duplicate_info = resolve_duplicate_hash(path, duplicate_detection)
                valid_paths = []

                if duplicate_info is not None:
                    method, hash_value = duplicate_info
                    # Only treat matches inside the current destination root as duplicates.
                    valid_paths = get_valid_original_paths(
                        hash_db,
                        method,
                        hash_value,
                        dst_dir,
                        threshold=phash_threshold,
                    )

                if valid_paths:
                    original_path = valid_paths[0]
                    target_path = get_duplicate_path(original_path)
                    transfer_file(path, target_path, mode)
                    duplicate_rows.append(
                        {
                            "original_name": os.path.basename(path),
                            "original_path": path,
                            "kept_path": original_path,
                            "duplicate_method": method,
                            "hash": hash_value,
                            "duplicate_path": target_path,
                        }
                    )

                    log_lines.append(
                        f"{timestamp()} | DUP | {method}={hash_value} | {path} -> {target_path} | original={original_path}"
                    )

                else:
                    dt = get_target_date(path)
                    target_dir = build_date_path(dst_dir, dt)
                    os.makedirs(target_dir, exist_ok=True)

                    target_path = get_unique_path(target_dir, name)
                    transfer_file(path, target_path, mode)

                    log_lines.append(
                        f"{timestamp()} | OK | {mode.upper()} | {path} -> {target_path}"
                    )

                if duplicate_info is not None:
                    method, hash_value = duplicate_info
                    add_hash_record(hash_db, method, hash_value, target_path)

            except Exception as e:
                log_lines.append(
                    f"{timestamp()} | ERR | {type(e).__name__} | {path} | {str(e)}"
                )

    # Persist the updated hash database after the run completes.
    save_hash_db(hash_db)
    append_duplicate_report_rows(build_duplicate_report_path(log_path), duplicate_rows)

    # Write one log entry per processed file so each run can be audited later.
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
