"""Clipboard operations for image loading."""

from PIL import Image as PILImage
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication


def load_image_from_clipboard() -> PILImage.Image:
    """Load image from system clipboard.

    Returns:
        PIL Image object

    Raises:
        ValueError: If clipboard does not contain image data
    """
    clipboard = QApplication.clipboard()
    qimage = clipboard.image()

    if qimage.isNull():
        raise ValueError("No image data in clipboard. Copy an image and try again.")

    return qimage_to_pil(qimage)


def qimage_to_pil(qimage: QImage) -> PILImage.Image:
    """Convert QImage to PIL Image.

    Args:
        qimage: Qt QImage object

    Returns:
        PIL Image object
    """
    # Convert to RGB888 format if not already
    if qimage.format() != QImage.Format.Format_RGB888:
        qimage = qimage.convertToFormat(QImage.Format.Format_RGB888)

    width = qimage.width()
    height = qimage.height()
    ptr = qimage.constBits()
    bytes_per_line = qimage.bytesPerLine()  # Account for stride/padding

    # Create PIL Image from bytes with proper stride
    img = PILImage.frombytes("RGB", (width, height), ptr.tobytes(), "raw", "RGB", bytes_per_line, 1)
    return img


def pil_to_qimage(pil_img: PILImage.Image) -> QImage:
    """Convert PIL Image to QImage.

    Args:
        pil_img: PIL Image object

    Returns:
        Qt QImage object
    """
    # Convert to RGB if needed
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")

    data = pil_img.tobytes("raw", "RGB")
    bytes_per_line = 3 * pil_img.width  # RGB = 3 bytes per pixel
    qimage = QImage(
        data, pil_img.width, pil_img.height, bytes_per_line, QImage.Format.Format_RGB888
    )

    # Make a copy to avoid data being freed
    return qimage.copy()
