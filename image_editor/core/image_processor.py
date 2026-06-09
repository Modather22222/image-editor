"""Pure image processing operations (no GUI)."""

from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from typing import Tuple


class ImageProcessor:
    """Stateless image processing utility methods."""

    @staticmethod
    def grayscale(img: Image.Image) -> Image.Image:
        result = ImageOps.grayscale(img)
        if result.mode != 'RGB':
            result = result.convert('RGB')
        return result

    @staticmethod
    def sepia(img: Image.Image) -> Image.Image:
        img = ImageOps.grayscale(img)
        img = img.convert('RGB')
        pixels = img.load()
        for i in range(img.width):
            for j in range(img.height):
                r, g, b = pixels[i, j]
                tr = min(255, int(0.393 * r + 0.769 * g + 0.168 * b))
                tg = min(255, int(0.349 * r + 0.686 * g + 0.131 * b))
                tb = min(255, int(0.272 * r + 0.534 * g + 0.189 * b))
                pixels[i, j] = (tr, tg, tb)
        return img

    @staticmethod
    def blur(img: Image.Image, radius: float = 2.0) -> Image.Image:
        return img.filter(ImageFilter.GaussianBlur(radius=radius))

    @staticmethod
    def sharpen(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.SHARPEN)

    @staticmethod
    def edge_detect(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.FIND_EDGES)

    @staticmethod
    def invert(img: Image.Image) -> Image.Image:
        return ImageOps.invert(img.convert('RGB'))

    @staticmethod
    def adjust_brightness(img: Image.Image, factor: float) -> Image.Image:
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(factor)

    @staticmethod
    def adjust_contrast(img: Image.Image, factor: float) -> Image.Image:
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(factor)

    @staticmethod
    def rotate_90_cw(img: Image.Image) -> Image.Image:
        return img.rotate(-90, expand=True)

    @staticmethod
    def rotate_90_ccw(img: Image.Image) -> Image.Image:
        return img.rotate(90, expand=True)

    @staticmethod
    def resize(img: Image.Image, width: int, height: int) -> Image.Image:
        return img.resize((width, height), Image.Resampling.LANCZOS)

    @staticmethod
    def crop(img: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image:
        """Crop image to the given box (left, top, right, bottom)."""
        return img.crop(box)

    @staticmethod
    def ensure_rgb(img: Image.Image) -> Image.Image:
        """Convert image to RGB mode if necessary."""
        if img.mode in ('RGBA', 'P', 'LA', 'L'):
            return img.convert('RGB')
        return img
