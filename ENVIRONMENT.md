# ImageOrganizer Environment Setup

## 1. Overview

This project is a Python-based image and video organizer.
It scans a source folder, determines the file date from EXIF metadata or file modified time, and then moves or copies files into a date-based directory structure.


## 2. Recommended Environment

- Operating system: Windows 10 or Windows 11
- Python: 3.10 or later
- Terminal: PowerShell or Command Prompt

This project has been developed as a simple local script project.
It does not require a database, web server, or external service.


## 3. Required Python Dependency

The project requires the following third-party package:

- `Pillow`

`Pillow` is used to read EXIF metadata from image files.


## 4. Create a Virtual Environment

From the project root directory, create a virtual environment:

```powershell
python -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If you use Command Prompt:

```cmd
venv\Scripts\activate.bat
```


## 5. Install Dependencies

After activating the virtual environment, install the required package:

```powershell
pip install Pillow
```

Optional check:

```powershell
pip show Pillow
```


## 6. Verify Python Environment

You can verify Python and pip with:

```powershell
python --version
pip --version
```

You can also verify that Pillow is available:

```powershell
python -c "from PIL import Image; print('Pillow OK')"
```


## 7. Project Structure

Main folders and files:

- `main.py`
  Entry point of the script.
- `core/`
  EXIF reading and date classification logic.
- `services/`
  File organization logic.
- `locales/`
  Language resource files for `zh`, `en`, and `ja`.
- `log/`
  Generated log files after each run.


## 8. Run the Script

Basic example:

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos
```

Copy mode example:

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --mode copy
```

Japanese UI example:

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang ja
```


## 9. Runtime Parameters

- `--src`
  Source directory. Required.
- `--dst`
  Destination directory. Required.
- `--mode`
  `move` or `copy`. Default is `move`.
- `--lang`
  `zh`, `en`, or `ja`. Default is `zh`.


## 10. Output and Logs

The script automatically creates a `log` folder in the project directory.

Each run generates a log file like:

```text
organize_log_YYYYMMDD_HHMMSS.txt
```

The script prints the final log path after execution.


## 11. Common Setup Problems

### Python is not recognized

If `python` is not recognized, make sure Python is installed and added to your system `PATH`.

### PowerShell blocks activation

If PowerShell refuses to activate the virtual environment, run:

```powershell
Set-ExecutionPolicy -Scope Process RemoteSigned
```

Then activate the environment again.

### Pillow is missing

If you see an import error related to `PIL`, install or reinstall Pillow:

```powershell
pip install --upgrade Pillow
```


## 12. Recommended Workflow

1. Open a terminal in the project root directory.
2. Create and activate a virtual environment.
3. Install `Pillow`.
4. Run the script with `--src` and `--dst`.
5. Check the generated `log` file after execution.
