import os
from datetime import datetime
from .exif_reader import get_exif_datetime, get_file_datetime

# Resolve the target date using EXIF first and file time as a fallback.
def get_target_date(path: str) -> datetime:
    exif_time = get_exif_datetime(path)
    if exif_time:
        return exif_time
    return get_file_datetime(path)


# Build the destination folder path in YYYY/MM/DD format.
def build_date_path(base_dir: str, dt: datetime) -> str:
    year = f"{dt.year:04d}"
    month = f"{dt.month:02d}"
    day = f"{dt.day:02d}"
    return os.path.join(base_dir, year, month, day)
