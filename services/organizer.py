import os
import shutil
from datetime import datetime
from core.date_classifier import get_target_date, build_date_path

SUPPORTED_EXT = (".jpg", ".jpeg", ".png", ".mp4", ".mov")


def timestamp():
    # Keep log timestamps human-readable for quick troubleshooting.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def transfer_file(src, dst, mode):
    # Dispatch to copy or move based on the selected organization mode.
    if mode == "copy":
        shutil.copy2(src, dst)
    else:
        shutil.move(src, dst)


def organize_images(src_dir: str, dst_dir: str, log_path: str, mode: str = "move", lang=None):
    os.makedirs(dst_dir, exist_ok=True)
    log_lines = []

    for root, _, files in os.walk(src_dir):
        for name in files:
            path = os.path.join(root, name)

            # Ignore files outside the supported media extensions.
            if not name.lower().endswith(SUPPORTED_EXT):
                continue

            try:
                dt = get_target_date(path)
                target_dir = build_date_path(dst_dir, dt)
                os.makedirs(target_dir, exist_ok=True)

                target_path = os.path.join(target_dir, name)

                # Add a numeric suffix to avoid overwriting an existing file.
                counter = 1
                base, ext = os.path.splitext(name)
                while os.path.exists(target_path):
                    target_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
                    counter += 1

                transfer_file(path, target_path, mode)

                log_lines.append(
                    f"{timestamp()} | OK | {mode.upper()} | {path} -> {target_path}"
                )

            except Exception as e:
                log_lines.append(
                    f"{timestamp()} | ERR | {type(e).__name__} | {path} | {str(e)}"
                )

    # Write one log entry per processed file so each run can be audited later.
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
