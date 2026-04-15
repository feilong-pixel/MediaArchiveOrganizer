import argparse
import os
import sys
from datetime import datetime
from locales import get_texts
from services.organizer import organize_images


def configure_console_encoding() -> None:
    # Force UTF-8 console output so localized help text renders correctly on Windows.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def build_log_path() -> str:
    # Store run logs in a dedicated folder next to the script.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "log")
    os.makedirs(log_dir, exist_ok=True)

    # Use a timestamped file name so each run keeps its own log record.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(log_dir, f"organize_log_{timestamp}.txt")


def validate_paths(src_dir: str, dst_dir: str, texts: dict[str, str]) -> tuple[str, str]:
    # Normalize both paths first so validation works with relative inputs as well.
    src_abs = os.path.abspath(src_dir)
    dst_abs = os.path.abspath(dst_dir)

    if not os.path.isdir(src_abs):
        raise ValueError(texts["src_not_found"].format(path=src_abs))

    # Only compare nested paths when both locations are on the same drive.
    src_drive = os.path.splitdrive(src_abs)[0].lower()
    dst_drive = os.path.splitdrive(dst_abs)[0].lower()
    if src_drive == dst_drive:
        # Prevent the destination from being the source itself or any child of it.
        common_path = os.path.commonpath([src_abs, dst_abs])
        if common_path == src_abs:
            raise ValueError(texts["dst_inside_src"].format(src=src_abs, dst=dst_abs))

    return src_abs, dst_abs


def main():
    configure_console_encoding()

    # Parse the language early so argparse help text can be localized.
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument("--lang", choices=("zh", "en", "ja"), default="en")
    base_args, _ = base_parser.parse_known_args()
    texts = get_texts(base_args.lang)

    # Build the main parser after the localized text bundle is available.
    parser = argparse.ArgumentParser(description=texts["app_description"])
    parser.add_argument("--src", required=True, help=texts["src_help"])
    parser.add_argument("--dst", required=True, help=texts["dst_help"])
    parser.add_argument("--mode", choices=("move", "copy"), default="move", help=texts["mode_help"])
    parser.add_argument(
        "--duplicate-detection",
        choices=("off", "phash", "strict"),
        default="phash",
        help=texts["duplicate_detection_help"],
    )
    parser.add_argument(
        "--phash-threshold",
        type=int,
        default=4,
        help=texts["phash_threshold_help"],
    )
    parser.add_argument("--lang", choices=("zh", "en", "ja"), default="en", help=texts["lang_help"])

    args = parser.parse_args()
    texts = get_texts(args.lang)
    src_dir, dst_dir = validate_paths(args.src, args.dst, texts)

    log_path = build_log_path()

    print(texts["start_message"])
    print(texts["mode_selected"].format(mode=args.mode))
    print(texts["duplicate_detection_selected"].format(mode=args.duplicate_detection, threshold=args.phash_threshold))

    organize_images(
        src_dir,
        dst_dir,
        log_path,
        args.mode,
        texts,
        args.duplicate_detection,
        args.phash_threshold,
    )

    print(texts["done_message"].format(log_path=log_path))


if __name__ == "__main__":
    main()
