"""Tests for image processing operations."""

import unittest
from PIL import Image

from image_editor.core.image_processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        self.rgb_image = Image.new("RGB", (100, 100), color=(128, 64, 32))
        self.rgba_image = Image.new("RGBA", (100, 100), color=(128, 64, 32, 200))

    def test_grayscale(self):
        result = self.processor.grayscale(self.rgb_image)
        self.assertEqual(result.mode, "RGB")
        self.assertEqual(result.size, (100, 100))

    def test_sepia(self):
        result = self.processor.sepia(self.rgb_image)
        self.assertEqual(result.mode, "RGB")
        self.assertEqual(result.size, (100, 100))

    def test_blur(self):
        result = self.processor.blur(self.rgb_image)
        self.assertEqual(result.mode, "RGB")
        self.assertEqual(result.size, (100, 100))

    def test_sharpen(self):
        result = self.processor.sharpen(self.rgb_image)
        self.assertEqual(result.mode, "RGB")
        self.assertEqual(result.size, (100, 100))

    def test_edge_detect(self):
        result = self.processor.edge_detect(self.rgb_image)
        self.assertEqual(result.mode, "RGB")
        self.assertEqual(result.size, (100, 100))

    def test_invert(self):
        result = self.processor.invert(self.rgb_image)
        self.assertEqual(result.mode, "RGB")
        self.assertEqual(result.size, (100, 100))

    def test_rotate_cw(self):
        result = self.processor.rotate_90_cw(self.rgb_image)
        self.assertEqual(result.size, (100, 100))

    def test_rotate_ccw(self):
        result = self.processor.rotate_90_ccw(self.rgb_image)
        self.assertEqual(result.size, (100, 100))

    def test_resize(self):
        result = self.processor.resize(self.rgb_image, 50, 50)
        self.assertEqual(result.size, (50, 50))

    def test_crop(self):
        result = self.processor.crop(self.rgb_image, (10, 10, 50, 50))
        self.assertEqual(result.size, (40, 40))

    def test_adjust_brightness(self):
        result = self.processor.adjust_brightness(self.rgb_image, 1.5)
        self.assertEqual(result.size, (100, 100))

    def test_adjust_contrast(self):
        result = self.processor.adjust_contrast(self.rgb_image, 1.5)
        self.assertEqual(result.size, (100, 100))

    def test_rgba_conversion(self):
        result = self.processor.invert(self.rgba_image)
        self.assertEqual(result.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
