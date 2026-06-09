"""Application constants and configuration."""

# Colors
CANVAS_BG = "#2b2b2b"
TOOLBAR_BG = "#f0f0f0"
STATUS_BG = "#e0e0e0"
SEPARATOR_COLOR = "#999999"
CROP_OUTLINE = "red"
OVERLAY_COLOR = "#000000"
OVERLAY_ALPHA = 128

# Sizes
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
TOOLBAR_BUTTON_WIDTH = 8

# Image processing
MAX_HISTORY = 20
MIN_ZOOM = 0.1
MAX_ZOOM = 5.0
ZOOM_STEP = 0.1
JPEG_QUALITY = 90

# File types
SUPPORTED_OPEN_EXTENSIONS = (
    ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp"),
    ("All files", "*.*")
)
SUPPORTED_SAVE_EXTENSIONS = (
    ("PNG files", "*.png"),
    ("JPEG files", "*.jpg *.jpeg"),
    ("All files", "*.*")
)

# Crop
CROP_DASH_PATTERN = (5, 5)
CROP_LINE_WIDTH = 2

# Checkerboard pattern for transparency
CHECKERBOARD_SIZE = 20
