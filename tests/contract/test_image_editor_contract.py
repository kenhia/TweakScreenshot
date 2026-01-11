"""Contract tests for ImageEditor public interface."""

from pathlib import Path

import pytest
from PIL import Image as PILImage


class TestImageEditorContract:
    """Test the public API contract of ImageEditor class."""

    @pytest.fixture
    def image_editor(self):
        """Create ImageEditor instance for testing."""
        from core.image_editor import ImageEditor

        return ImageEditor()

    @pytest.fixture
    def sample_png_path(self, tmp_path):
        """Create a sample PNG file for testing."""
        img_path = tmp_path / "test.png"
        img = PILImage.new("RGB", (100, 100), color="red")
        img.save(img_path, "PNG")
        return img_path

    @pytest.fixture
    def sample_jpg_path(self, tmp_path):
        """Create a sample JPG file for testing."""
        img_path = tmp_path / "test.jpg"
        img = PILImage.new("RGB", (100, 100), color="blue")
        img.save(img_path, "JPEG")
        return img_path

    # T017: Contract test for load_from_file()
    @pytest.mark.contract
    def test_load_from_file_valid_png(self, image_editor, sample_png_path):
        """Contract: Valid PNG file loads successfully."""
        image_editor.load_from_file(sample_png_path)

        assert image_editor.has_image() is True
        assert image_editor.get_current_image() is not None
        assert image_editor.has_unsaved_changes() is False
        assert len(image_editor.get_edit_history()) == 0

    @pytest.mark.contract
    def test_load_from_file_valid_jpg(self, image_editor, sample_jpg_path):
        """Contract: Valid JPG file loads successfully."""
        image_editor.load_from_file(sample_jpg_path)

        assert image_editor.has_image() is True
        assert image_editor.get_current_image() is not None

    @pytest.mark.contract
    def test_load_from_file_invalid_path(self, image_editor):
        """Contract: Invalid file path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            image_editor.load_from_file(Path("nonexistent.png"))

    @pytest.mark.contract
    def test_load_from_file_corrupted_image(self, image_editor, tmp_path):
        """Contract: Corrupted image file raises appropriate exception."""
        bad_path = tmp_path / "corrupted.png"
        bad_path.write_text("This is not an image")

        with pytest.raises((ValueError, PILImage.UnidentifiedImageError)):
            image_editor.load_from_file(bad_path)

    @pytest.mark.contract
    def test_load_from_file_postcondition_images_identical(self, image_editor, sample_png_path):
        """Contract: After load, current and original images are identical."""
        image_editor.load_from_file(sample_png_path)

        current = image_editor.get_current_image()
        original = image_editor.get_original_image()

        assert current.size == original.size
        assert current.mode == original.mode

    # T018: Contract test for load_from_clipboard()
    @pytest.mark.contract
    def test_load_from_clipboard_with_image(self, image_editor, qtbot):
        """Contract: Clipboard with image loads successfully."""
        from PySide6.QtGui import QImage
        from PySide6.QtWidgets import QApplication

        # Create test image and put in clipboard
        qimage = QImage(50, 50, QImage.Format.Format_RGB888)
        qimage.fill(0xFF0000)  # Red

        clipboard = QApplication.clipboard()
        clipboard.setImage(qimage)

        image_editor.load_from_clipboard()

        assert image_editor.has_image() is True
        assert image_editor.get_current_image() is not None
        assert image_editor.get_file_path() is None  # Clipboard has no file path
        assert image_editor.has_unsaved_changes() is False

    @pytest.mark.contract
    def test_load_from_clipboard_without_image(self, image_editor, qtbot):
        """Contract: Clipboard without image raises ValueError with clear message."""
        from PySide6.QtWidgets import QApplication

        # Clear clipboard
        clipboard = QApplication.clipboard()
        clipboard.clear()

        with pytest.raises(ValueError, match="clipboard.*image"):
            image_editor.load_from_clipboard()

    @pytest.mark.contract
    def test_has_image_initially_false(self, image_editor):
        """Contract: has_image() returns False for new ImageEditor."""
        assert image_editor.has_image() is False

    @pytest.mark.contract
    def test_get_current_image_initially_none(self, image_editor):
        """Contract: get_current_image() returns None for new ImageEditor."""
        assert image_editor.get_current_image() is None
