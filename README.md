# Image Viewer & Editor

A cross-platform desktop image viewer and editor built with Python, Tkinter, and Pillow.

## Features

- View images (JPG, PNG, GIF, BMP, TIFF, WebP)
- Basic editing: crop, resize, rotate 90°
- Filters: grayscale, sepia, blur, sharpen, edge detect, invert
- Brightness & Contrast (real-time preview)
- Zoom & pan
- Undo (20 steps)
- Fullscreen mode (F11)

## Quick Start

### Option 1: Pre-built Executable (Recommended)

Download the latest release for your platform from [Releases](../../releases).

- **Windows**: Run `ImageEditor.exe`
- **macOS**: Run `./ImageEditor` (may need `chmod +x`)
- **Linux**: Run `./ImageEditor` (may need `chmod +x`)

### Option 2: Run from Source

Requires Python 3.13+.

```bash
# Clone the repository
git clone <repo-url>
cd image_editor

# Create virtual environment
python3.13 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Option 3: Build from Source

```bash
# Activate venv first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install build dependencies
pip install pyinstaller

# Build
python build.py
```

The executable will be created in the `dist/` directory.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O | Open image |
| Ctrl+S | Save |
| Ctrl+Shift+S | Save As |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| + / - | Zoom in/out |
| Ctrl+0 | Fit to window |
| Ctrl+1 | Actual size |
| C | Toggle crop mode |
| Enter | Apply crop |
| Esc | Cancel crop / Exit fullscreen |
| R | Rotate 90° CW |
| Shift+R | Rotate 90° CCW |
| F11 | Toggle fullscreen |

## Building for All Platforms

This repository includes a GitHub Actions workflow (`.github/workflows/build.yml`) that automatically builds executables for Windows, macOS, and Linux on every push to `main`.

To trigger a build manually, go to **Actions → Build Cross-Platform Executables → Run workflow**.
