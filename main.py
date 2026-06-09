#!/usr/bin/env python3
"""Entry point for the Image Viewer & Editor application."""

import sys
import os

# CRITICAL: Pre-load all PIL plugins so PyInstaller bundles them correctly.
# Without this, Image.open() will fail in the built executable
# because Pillow loads plugins dynamically at runtime.
try:
    from PIL import Image
    import PIL.PngImagePlugin
    import PIL.JpegImagePlugin
    import PIL.GifImagePlugin
    import PIL.BmpImagePlugin
    import PIL.TiffImagePlugin
    import PIL.WebPImagePlugin
except ImportError:
    pass  # If any plugin is missing, Pillow will still try to handle it

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_pil(image_path: str) -> bool:
    """Test if PIL can open the given image."""
    try:
        img = Image.open(image_path)
        print(f"[TEST OK] Opened: {image_path}")
        print(f"  Size: {img.size}, Mode: {img.mode}, Format: {img.format}")
        return True
    except Exception as e:
        print(f"[TEST FAILED] Could not open: {image_path}")
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main() -> None:
    # Check for --test-pil flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test-pil":
        test_path = sys.argv[2] if len(sys.argv) > 2 else "test_image.png"
        success = test_pil(test_path)
        sys.exit(0 if success else 1)
    
    from image_editor.app import ImageEditorApp
    app = ImageEditorApp()
    app.run()


if __name__ == "__main__":
    main()
