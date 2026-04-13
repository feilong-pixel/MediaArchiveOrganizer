# ImageOrganizer Disclaimer

## 1. Risk Notice

This tool is intended to automatically organize image and video files.
During use, the program may move or copy files and create new directory structures in the destination folder.

Although the tool follows its designed rules as closely as possible, actual use may still be affected by file permissions, incorrect paths, disk conditions, file locks, unexpected interruptions, invalid time metadata, or other unforeseen factors.
As a result, the following situations may occur:

- Organized results do not match expectations
- Files are moved to unintended folders
- Duplicate file names are automatically renamed
- Some files fail to process
- Log records are incomplete
- In extreme cases, data loss, overwrite, or unrecoverable issues may occur


## 2. User Responsibility

Before running this tool, the user is responsible for confirming the following:

- The source and destination paths are correct
- Important files have been backed up in advance
- There is sufficient disk space
- The difference between `move` mode and `copy` mode is fully understood
- The expected destination folder structure is understood

If you need to preserve the original files, use `--mode copy` whenever possible.


## 3. Special Notice for Move Mode

When using the default `move` mode, files are moved from the source directory to the destination directory.
This means the original files may no longer remain in the source folder after processing.

Therefore, when using the tool for the first time, processing important files, or when you are unsure whether the output will match your expectations, it is strongly recommended to:

- Test with a small set of files first
- Prefer `--mode copy`
- Review the log output before full-scale processing


## 4. Note on Date Detection

This tool reads image EXIF time first.
If EXIF time cannot be read, it uses the file's modified time as a fallback.

Therefore, the final organization result depends on whether the file's date metadata is accurate.
If the original EXIF data is missing or incorrect, or if the file modified time has changed, the final date folder may not match the true capture date.


## 5. Note on Logs

The tool generates a log file for each run, but logs are intended only for troubleshooting and record keeping.
Logs do not guarantee completeness, accuracy, or recoverability of the organization result.

After important processing, users should manually verify:

- Whether the log contains `ERR`
- Whether the number of files in the destination matches expectations
- Whether the destination folder structure is correct


## 6. Limitation of Liability

This tool is provided "as is" without any express or implied warranty.

The developer or provider is not liable for:

- Direct or indirect losses caused by using or being unable to use this tool
- Misplaced, overwritten, deleted, or lost files caused by misuse
- Failures caused by the operating system, permissions, hardware, disk conditions, third-party libraries, or runtime environment
- Losses caused by users not backing up important data


## 7. Recommended Safe Usage

To reduce risk, it is recommended to use this tool as follows:

1. Test with a small number of files first
2. Prefer `--mode copy` to verify the result
3. Back up original files before full processing
4. Review both the log file and destination folders
5. Proceed with large-scale organization only after confirming the result is correct


## 8. Final Statement

By running this tool, you acknowledge and accept the risks and limitations described above.
