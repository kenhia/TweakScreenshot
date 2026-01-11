"""Unit tests for clipboard operations."""

import pytest
from PIL import Image as PILImage


class TestClipboardOperations:
    """Test clipboard image operations."""

    # T020: Unit tests for load_image_from_clipboard()
    @pytest.mark.unit
    def test_load_from_clipboard_returns_pil_image(self, qtbot):
        """Load image from clipboard returns PIL Image."""
        from PySide6.QtGui import QImage
        from PySide6.QtWidgets import QApplication

        from core.clipboard import load_image_from_clipboard

        # Create and set clipboard image
        qimage = QImage(100, 100, QImage.Format.Format_RGB888)
        qimage.fill(0x00FF00)  # Green

        clipboard = QApplication.clipboard()
        clipboard.setImage(qimage)

        img = load_image_from_clipboard()

        assert isinstance(img, PILImage.Image)
        assert img.size == (100, 100)
        assert img.mode in ("RGB", "RGBA")

    @pytest.mark.unit
    def test_load_from_empty_clipboard_raises_error(self, qtbot):
        """Load from empty clipboard raises ValueError."""
        from PySide6.QtWidgets import QApplication

        from core.clipboard import load_image_from_clipboard

        # Clear clipboard
        clipboard = QApplication.clipboard()
        clipboard.clear()

        with pytest.raises(ValueError, match="clipboard.*image"):
            load_image_from_clipboard()

    @pytest.mark.unit
    def test_qimage_to_pil_conversion(self, qtbot):
        """QImage to PIL Image conversion works correctly."""
        from PySide6.QtGui import QImage

        from core.clipboard import qimage_to_pil

        qimage = QImage(50, 50, QImage.Format.Format_RGB888)
        qimage.fill(0xFF0000)  # Red

        pil_img = qimage_to_pil(qimage)

        assert isinstance(pil_img, PILImage.Image)
        assert pil_img.size == (50, 50)
        assert pil_img.mode in ("RGB", "RGBA")

    @pytest.mark.unit
    def test_pil_to_qimage_conversion(self):
        """PIL Image to QImage conversion works correctly."""
        from PySide6.QtGui import QImage

        from core.clipboard import pil_to_qimage

        pil_img = PILImage.new("RGB", (75, 75), color="blue")
        qimage = pil_to_qimage(pil_img)

        assert isinstance(qimage, QImage)
        assert qimage.width() == 75
        assert qimage.height() == 75

    @pytest.mark.unit
    def test_round_trip_conversion(self):
        """QImage -> PIL -> QImage preserves dimensions."""
        from PySide6.QtGui import QImage

        from core.clipboard import pil_to_qimage, qimage_to_pil

        original = QImage(120, 80, QImage.Format.Format_RGB888)
        original.fill(0x0000FF)

        pil_img = qimage_to_pil(original)
        converted_back = pil_to_qimage(pil_img)

        assert converted_back.width() == original.width()
        assert converted_back.height() == original.height()
