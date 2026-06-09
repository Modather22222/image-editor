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

## CI/CD & Releases

This project uses **GitHub Actions** with two separate workflows following best practices.

### CI Workflow (`ci.yml`)

Runs automatically on every push to `main` and on pull requests.

- **Lint & Test**: Runs unit tests to verify nothing is broken
- **Build Artifacts**: Compiles executables for Linux, Windows, and macOS
- **No Release Created**: CI only validates builds; it does not publish releases

View CI runs: **Actions → CI**

### Release Workflow (`release.yml`)

Creates a **GitHub Release** with downloadable executables. This only runs when you intentionally publish a version.

#### How to Create a Release

**Option 1: Push a Version Tag (Recommended)**

This follows [Semantic Versioning](https://semver.org/):

```bash
# For bug fixes
git tag v0.1.1
git push origin v0.1.1

# For new features
git tag v0.2.0
git push origin v0.2.0

# For stable releases
git tag v1.0.0
git push origin v1.0.0
```

**Option 2: Manual Trigger via GitHub UI**

1. Go to **Actions → Release → Run workflow**
2. Enter a version tag (e.g., `v1.0.0`)
3. Click **Run workflow**

#### What Happens During a Release

1. Builds executables for all 3 platforms in parallel
2. Creates a GitHub Release with that exact version tag
3. Attaches `ImageEditor` (Linux), `ImageEditor.exe` (Windows), `ImageEditor` (macOS)
4. Auto-generates release notes from commits since the last tag
5. Includes SHA256 checksums for verification

### Semantic Versioning Guide

| Tag Format | When to Use | Example |
|------------|-------------|---------|
| `v0.1.0` | Initial release | First public version |
| `v0.2.0` | New features | Added brightness/contrast dialog |
| `v0.2.1` | Bug fix only | Fixed crop coordinate bug |
| `v1.0.0` | Stable / production | API stable, major milestone |
| `v2.0.0` | Breaking changes | Redesigned UI, removed features |

### Viewing Releases

All published releases are available at:
```
https://github.com/Modather22222/image-editor/releases
```

## Project Structure

```
image_editor/
├── .github/
│   └── workflows/
│       ├── ci.yml           # Build & test on push/PR
│       └── release.yml      # Create release on tag push
├── image_editor/
│   ├── core/
│   │   ├── history_manager.py   # 20-step undo/redo (Command Pattern)
│   │   └── image_processor.py   # PIL filter/transform operations
│   ├── ui/
│   │   ├── main_window.py       # Root window & menu bar
│   │   ├── toolbar.py           # Emoji + text button toolbar
│   │   ├── canvas_view.py       # Scrollable image canvas + crop logic
│   │   ├── status_bar.py        # Bottom info bar
│   │   └── dialogs.py           # Brightness/Contrast & Resize dialogs
│   ├── utils/
│   │   └── constants.py         # App constants & defaults
│   └── app.py                 # Main controller wiring UI to core
├── tests/
│   ├── test_image_processor.py
│   └── test_history_manager.py
├── main.py                    # Entry point
├── build.py                   # Local PyInstaller build script
├── requirements.txt           # Pillow>=9.0.0
└── CHANGELOG.md             # Version history
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and run tests: `python -m unittest discover tests -v`
4. Commit: `git commit -m "feat: add new feature"`
5. Push: `git push origin feature/my-feature`
6. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) for details.
