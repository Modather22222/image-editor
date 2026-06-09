# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Full image viewer/editor built with Tkinter and Pillow
- Open/Save support for PNG, JPEG, GIF, BMP, TIFF, WebP
- Filters: Grayscale, Sepia, Blur, Sharpen, Edge Detect, Invert
- Brightness & Contrast adjustment with real-time slider preview
- Crop tool with visual selection overlay and dimming
- Resize dialog with aspect ratio lock
- 90° clockwise and counter-clockwise rotation
- Zoom & pan (mouse wheel, fit-to-window, actual size)
- Fullscreen mode (F11 toggle)
- 20-step undo history using Command Pattern
- Keyboard shortcuts (Ctrl+O, Ctrl+S, Ctrl+Z, +, -, etc.)
- Cross-platform executable builds via PyInstaller
- GitHub Actions CI/CD for automated Windows, macOS, and Linux builds
- Automated GitHub Releases triggered by version tags
- Unit tests for image processor and history manager
