# sanitized-mac

A Python application designed to clean up cluttered folders on macOS by identifying, categorizing, and organizing files.

Sanitized Mac helps keep your filesystem organized by distinguishing supported file types from temporary, hidden, and unrecognized files.

> **Platform support:** Sanitized Mac is developed for macOS. Support for Windows has been discontinued.

## Features

- Identify and categorize files based on their extensions.
- Recognize common document, image, audio, video, and archive formats.
- Detect temporary and incomplete download files.
- Ignore hidden macOS and Unix files, such as `.DS_Store`.
- Identify files with unsupported or missing extensions.
- Support case-insensitive file extension matching.

## Installation

Sanitized Mac is distributed as a precompiled application for macOS. No Python installation, compilation, or additional dependencies are required.

### 1. Download the application

Visit the [GitHub Releases](../../releases/latest) page and download the latest version of Sanitized Mac for macOS.

Select the appropriate release asset for your Mac.

### 2. Install the application

If the downloaded file is a `.dmg`, open it and follow the installation instructions.

If the downloaded file is a `.zip`, extract its contents and move the application to your Applications folder, if applicable.

### 3. Launch Sanitized Mac

Open the application from your Applications folder or the location where you extracted it.

**macOS security notice:** If macOS prevents the application from opening because it cannot verify the developer, open System Settings → Privacy & Security and review the option to open the application.

Only approve applications you have downloaded from a trusted source.

## Usage

1. Launch Sanitized Mac.
2. Select the folder you want to observe and clean e.g. Downloads.
3. [sanitize] option will scan the selected folder and clean the selected folder.
4. [start] option will enable polling and observation of the '.sort' folder so that you may drag files into it, which will function similar to sanitizing.

**Important:** Back up important files before performing cleanup operations. Avoid selecting macOS system directories or folders containing files that are currently in use.

## Platform Compatibility

| Operating System | Support                  |
| ---------------- | ------------------------ |
| macOS            | Supported                |
| Windows          | Discontinued             |
| Linux            | Not officially supported |

Sanitized Mac is developed and distributed for macOS. Windows support has been discontinued, and no new Windows releases are planned.

## Supported file types

Sanitized Mac recognizes several categories of files based on their extensions.

| Category | Supported extensions |
|----------|----------------------|
| Documents | `.pdf`, `.txt`, `.doc`, `.docx`, `.rtf`, `.odt`, `.md` |
| Spreadsheets | `.csv`, `.xls`, `.xlsx`, `.ods` |
| Presentations | `.ppt`, `.pptx`, `.odp` |
| Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.heic`, `.bmp`, `.tiff`, `.tif`, `.svg` |
| Audio | `.mp3`, `.wav`, `.aac`, `.flac`, `.m4a`, `.ogg`, `.opus` |
| Video | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.m4v` |
| Archives | `.zip`, `.tar`, `.gz`, `.rar`, `.7z`, `.bz2`, `.xz` |
| Installers | `.dmg`, `.pkg`, `.exe`, `.msi`, `.deb`, `.rpm` |

You may add additional categories or supported extensions in the configuration menu. 

### Temporary files

The following extensions are recognized as temporary files:

| Extension | Description |
|-----------|-------------|
| `.crdownload` | Incomplete Chromium-based browser download |
| `.download` | Incomplete or temporary download |
| `.part` | Partial file or incomplete download |
| `.partial` | Partially downloaded or written file |
| `.tmp` | Temporary file |
| `.temp` | Temporary file |

Files beginning with a period (`.`) are also ignored by the temporary-item detection function.

This includes hidden macOS and Unix files such as `.DS_Store`.

### Unknown file types

A file is classified as `unknown` when its extension is not included in the supported file types or when it has no extension.

File classification is based on the filename extension rather than the actual contents of the file.

## Important considerations

Sanitized Mac is intended to help organize cluttered directories. File classification alone does not determine whether a file is safe to delete.

Before performing cleanup operations:

- Back up important files.
- Avoid cleaning system directories.
- Review unfamiliar files before deleting or moving them.
- Avoid interrupting active downloads or other file operations.

Temporary files and incomplete downloads may still be in use by other applications.

## Development

To contribute to the project, fork the repository and clone your fork locally.

Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

After making your changes, commit them:

```bash
git add .
git commit -m "Describe your changes"
```

Push your branch:

```bash
git push origin feature/your-feature-name
```

Open a pull request describing your changes and their purpose.

Contributions related to file classification, filesystem safety, performance, and macOS compatibility are welcome.

## License

See the [LICENSE](LICENSE) file for licensing information.