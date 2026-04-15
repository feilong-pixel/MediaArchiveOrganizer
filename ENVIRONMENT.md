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

This command creates a folder named `venv` under the current project root.

For example, if your project is located at:

```text
D:\ImageOrganizer
```

then the virtual environment is created at:

```text
D:\ImageOrganizer\venv
```

Common locations:

- Virtual environment folder: `D:\ImageOrganizer\venv`
- Python inside the virtual environment: `D:\ImageOrganizer\venv\Scripts\python.exe`
- pip inside the virtual environment: `D:\ImageOrganizer\venv\Scripts\pip.exe`

In other words, project dependencies are not installed next to `main.py`.
They are installed into the Python environment inside `venv`.
As long as you use `venv\Scripts\python.exe` or activate this `venv`, dependencies will be loaded from that environment.

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If you use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

After activation, your terminal prompt usually shows something like `(venv)`, which means you are using this project's virtual environment.

If you want to confirm which Python is currently active, run:

```powershell
Get-Command python
```

or:

```powershell
python -c "import sys; print(sys.executable)"
```

The result should point to:

```text
your-project-path\venv\Scripts\python.exe
```


## 5. Install Dependencies

After activating the virtual environment, install the required package:

```powershell
pip install Pillow
```

This installs `Pillow` into the currently active virtual environment.

If you want to avoid installing into the wrong Python environment, use the more explicit command:

```powershell
.\venv\Scripts\python.exe -m pip install Pillow
```

This guarantees that the package is installed into this project's `venv`, not into the global Python installation or some other virtual environment.

Optional check:

```powershell
pip show Pillow
```

More explicit check:

```powershell
.\venv\Scripts\python.exe -m pip show Pillow
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

If you want to completely avoid ambiguity about which Python is being used, run:

```powershell
.\venv\Scripts\python.exe -c "from PIL import Image; print('Pillow OK')"
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

Please note that `main.py` is located in the project root.
You should enter the project root directory before running the script.

For example:

```powershell
cd D:\ImageOrganizer
```

If you have already activated this project's `venv`, you can run:

```powershell
python .\main.py --src D:\InputPhotos --dst D:\SortedPhotos
```

If you do not want to depend on whether activation succeeded, it is recommended to run the script with the full Python path inside the virtual environment:

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos
```

This is clearer and less error-prone.
It helps avoid these common problems:

- the terminal is not in the project root, so `main.py` cannot be found
- the current Python is not the project's `venv`, so `Pillow` cannot be found
- it is unclear where `venv` is located

Basic example:

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos
```

Copy mode example:

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --mode copy
```

Japanese UI example:

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang ja
```

Recommended order:

1. `cd` into the project root
2. Confirm that `venv` exists under `.\venv`
3. Prefer `.\venv\Scripts\python.exe .\main.py ...` when running the script

This makes dependency and path issues much easier to diagnose.


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
.\venv\Scripts\python.exe -m pip install --upgrade Pillow
```

If you are still unsure whether the terminal is using the correct environment, run:

```powershell
python -c "import sys; print(sys.executable)"
.\venv\Scripts\python.exe -m pip show Pillow
```


## 12. Recommended Workflow

1. Open a terminal in the project root directory, for example: `cd D:\ImageOrganizer`
2. Run `python -m venv venv` and confirm that the virtual environment was created in `your-project-path\venv`
3. Prefer `.\venv\Scripts\python.exe -m pip install Pillow` to install dependencies
4. Run the script with `.\venv\Scripts\python.exe .\main.py --src ... --dst ...`
5. Check the generated `log` file after execution
