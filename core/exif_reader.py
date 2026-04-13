from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime

# Read the capture time from the image EXIF metadata.
def get_exif_datetime(path: str) -> datetime | None:
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif:
            return None

        for tag, value in exif.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "DateTimeOriginal":
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

        return None
    except Exception:
        return None

# Use the file modification time when EXIF data is unavailable.
def get_file_datetime(path: str) -> datetime:
    stat = os.stat(path)
    return datetime.fromtimestamp(stat.st_mtime)
