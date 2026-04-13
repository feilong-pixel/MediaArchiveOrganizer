# ImageOrganizer

A Python tool for organizing image and video files by date.

The program reads image EXIF time first. If EXIF time is unavailable, it falls back to the file's modified time.
Organized files are placed into the target directory using a `year\month\day` folder structure.


## Features

- Recursively scans subfolders in the source directory
- Organizes images and videos by date automatically
- Uses `move` mode by default
- Supports `copy` mode to keep original files
- Supports Chinese, English, and Japanese UI
- Generates a separate log file for each run
- Automatically appends a numeric suffix for duplicate file names


## Supported File Types

- `.jpg`
- `.jpeg`
- `.png`
- `.mp4`
- `.mov`


## Environment

- Windows 10 or Windows 11
- Python 3.10 or later
- Dependency: `Pillow`

Install dependency:

```powershell
pip install Pillow
```

For detailed environment setup, see:

- [ENVIRONMENT.md](./ENVIRONMENT.md)
- [环境配置说明.md](./环境配置说明.md)
- [環境設定ガイド.md](./環境設定ガイド.md)


## Basic Usage

Open a terminal in the project root and run:

```powershell
python main.py --src SOURCE_DIR --dst TARGET_DIR
```

Example:

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos
```


## Arguments

### `--src`

Source directory. Required.

### `--dst`

Destination directory. Required.

### `--mode`

Organization mode:

- `move`: move files, default
- `copy`: copy files and keep originals

Example:

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --mode copy
```

### `--lang`

Interface language:

- `zh`: Chinese
- `en`: English
- `ja`: Japanese

Example:

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang en
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang ja
```


## Common Examples

### Move files by default

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos
```

### Copy files and keep originals

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --mode copy
```

### Use English UI

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang en
```

### Use Japanese UI

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang ja
```


## Logs

The program automatically creates or reuses the `log` folder under the script directory.

Log file names use this format:

```text
organize_log_YYYYMMDD_HHMMSS.txt
```

Example:

```text
organize_log_20260413_135222.txt
```

After execution, the program prints the full path of the generated log file.


## Organization Rules

- Recursively scans all subfolders in the source directory
- Uses image EXIF time first
- Falls back to file modified time when EXIF is unavailable
- Outputs files to `target\year\month\day\`
- Adds a numeric suffix if a file with the same name already exists

Duplicate name example:

```text
photo.jpg
photo_1.jpg
photo_2.jpg
```


## Project Structure

- `main.py`
  Program entry point
- `core/`
  Date detection and EXIF reading logic
- `services/`
  File organization logic
- `locales/`
  Chinese, English, and Japanese UI texts
- `log/`
  Log output folder for each run


## Notes

- Make sure the source and destination paths are correct
- Default `move` mode removes files from the source directory
- Use `--mode copy` if you need to keep original files
- It is recommended to test with a small number of files first
- Back up important files before large batch processing


## Common Failure Causes

- File is in use and cannot be moved or copied
- File permission is insufficient
- Image EXIF data is invalid
- Destination directory is not writable


## Disclaimer

This tool is intended to automatically organize image and video files.
In actual use, the result may still differ from expectations due to incorrect paths, permission problems, file locks, disk issues, invalid time metadata, interrupted execution, or other unforeseen factors.

Please note:

- Default `move` mode moves original files
- Duplicate file names are automatically renamed
- If EXIF time or file time is inaccurate, the destination date folder may not match the real capture date
- Logs are only for assistance and do not guarantee completeness of results

To reduce risk:

1. Test with a small set of files first
2. Prefer `--mode copy` for verification
3. Back up important data before full processing
4. Check both the log and destination folders after execution

For the full disclaimer, see:

- [免责声明.md](./免责声明.md)
