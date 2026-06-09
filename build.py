#!/usr/bin/env python3
"""Build script for creating standalone executables."""

import sys
import os
import subprocess
import shutil


def clean_build():
    """Remove previous build artifacts."""
    for path in ["build", "dist"]:
        if os.path.exists(path) and os.path.isdir(path):
            shutil.rmtree(path)
    for f in os.listdir("."):
        if f.endswith(".spec"):
            os.remove(f)
    print("Cleaned previous build artifacts.")


def build():
    """Run PyInstaller to build the executable."""
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "ImageEditor",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        # Critical: include all Pillow plugins
        "--collect-all", "PIL",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "PIL.ImageFilter",
        "--hidden-import", "PIL.ImageOps",
        "--hidden-import", "PIL.ImageEnhance",
        "--hidden-import", "PIL.ImageDraw",
        "--hidden-import", "PIL.ImageTk",
        "--hidden-import", "PIL.PngImagePlugin",
        "--hidden-import", "PIL.JpegImagePlugin",
        "--hidden-import", "PIL.GifImagePlugin",
        "--hidden-import", "PIL.BmpImagePlugin",
        "--hidden-import", "PIL.TiffImagePlugin",
        "--hidden-import", "PIL.WebPImagePlugin",
        "main.py"
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print("Build failed!")
        sys.exit(1)
    print("Build completed successfully!")
    print(f"Executable: {os.path.abspath('dist/ImageEditor')}")


def main():
    clean_build()
    build()


if __name__ == "__main__":
    main()
