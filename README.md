# NotePad

A clean, modern rich-text NotePad desktop application built with Python and PyQt5.

## Features
- **Rich Text Editing**: Bold, Italic, Underline, Font Family, and Font Size controls.
- **Color Customization**: Text color and background highlight picker.
- **Alignment**: Align Left, Center, Right, and Justify.
- **Document Management**: Create new files, Open, Save, and Save As with UTF-8 encoding.
- **Export & Print**: Direct PDF export, Print Preview, and Print support.
- **Quick Inserts**: Insert current date and timestamp with a click.
- **Cross-Platform**: Standalone `.dmg` installer for macOS (Apple Silicon & Intel) and `.exe` portable executable for Windows.

---

## Downloads & Releases

Pre-compiled standalone binaries are generated automatically via GitHub Actions:
- **macOS (Apple Silicon)**: `NotePad-macOS-arm64.dmg` (Drag-and-drop installer)
- **Windows**: `NotePad-Windows-x64.exe` (Single-file portable executable)

---

## Building from Source

### Prerequisites
- Python 3.10, 3.11, or 3.12
- PyQt5 & PyInstaller:
  ```bash
  pip install pyqt5 pyinstaller
  ```

### Build on macOS (.dmg & .app)
Run the automated build script:
```bash
chmod +x build_macos.sh
./build_macos.sh
```
Output will be located in:
- `dist/NotePad.app` (macOS Application bundle)
- `dist/NotePad-macOS-arm64.dmg` (macOS Disk Image installer)

### Build on Windows (.exe)
Run the batch script:
```cmd
build_windows.bat
```
Or build directly with PyInstaller:
```cmd
python -m PyInstaller --clean --noconfirm NotePad.spec
```
Output will be located at `dist\NotePad.exe`.

---

## Automated CI/CD
GitHub Actions (`.github/workflows/build.yml`) builds both the Windows `.exe` and macOS `.dmg` on every push to `main` and on tag release.
