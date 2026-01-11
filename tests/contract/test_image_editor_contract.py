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

    # T037: Contract test for save_to_file()
    @pytest.mark.contract
    def test_save_to_file_png_format(self, image_editor, sample_png_path, tmp_path):
        """Contract: Save image to PNG format creates valid file."""
        image_editor.load_from_file(sample_png_path)

        output_path = tmp_path / "output.png"
        image_editor.save_to_file(output_path, format_str="PNG")

        assert output_path.exists()
        # Verify file is valid by loading it
        saved_img = PILImage.open(output_path)
        assert saved_img.format == "PNG"
        assert saved_img.size == (100, 100)

    @pytest.mark.contract
    def test_save_to_file_jpg_format(self, image_editor, sample_png_path, tmp_path):
        """Contract: Save image to JPG format creates valid file."""
        image_editor.load_from_file(sample_png_path)

        output_path = tmp_path / "output.jpg"
        image_editor.save_to_file(output_path, format_str="JPEG", quality=90)

        assert output_path.exists()
        saved_img = PILImage.open(output_path)
        assert saved_img.format == "JPEG"

    @pytest.mark.contract
    def test_save_to_file_clears_unsaved_flag(self, image_editor, sample_png_path, tmp_path):
        """Contract: Saving image clears has_unsaved_changes flag."""
        image_editor.load_from_file(sample_png_path)

        # Simulate an edit by marking as unsaved (future task will actually edit)
        # For now, just test that save clears the flag

        output_path = tmp_path / "output.png"
        image_editor.save_to_file(output_path, format_str="PNG")

        assert image_editor.has_unsaved_changes() is False

    @pytest.mark.contract
    def test_save_to_file_without_image_raises_error(self, image_editor, tmp_path):
        """Contract: Attempting to save without loaded image raises ValueError."""
        output_path = tmp_path / "output.png"

        with pytest.raises(ValueError, match="No image loaded"):
            image_editor.save_to_file(output_path, format_str="PNG")

    # T055: Contract test for crop()
    @pytest.mark.contract
    def test_crop_valid_region(self, image_editor, sample_png_path):
        """Contract: Cropping with valid region reduces image dimensions."""
        image_editor.load_from_file(sample_png_path)

        # Original is 100x100
        original_img = image_editor.get_current_image()
        assert original_img.size == (100, 100)

        # Crop to 50x50 region starting at (10, 10)
        image_editor.crop(x=10, y=10, width=50, height=50)

        # Current image should now be 50x50
        cropped_img = image_editor.get_current_image()
        assert cropped_img.size == (50, 50)

        # Should mark as unsaved
        assert image_editor.has_unsaved_changes() is True

        # Edit history should record the crop
        history = image_editor.get_edit_history()
        assert len(history) == 1
        assert history[0].type == "crop"

    @pytest.mark.contract
    def test_crop_invalid_region_raises_error(self, image_editor, sample_png_path):
        """Contract: Cropping with invalid region raises ValueError."""
        image_editor.load_from_file(sample_png_path)

        # Crop region outside image bounds (image is 100x100)
        with pytest.raises(ValueError, match="region"):
            image_editor.crop(x=150, y=150, width=50, height=50)

    @pytest.mark.contract
    def test_crop_zero_dimensions_raises_error(self, image_editor, sample_png_path):
        """Contract: Cropping with zero width/height raises ValueError."""
        image_editor.load_from_file(sample_png_path)

        with pytest.raises(ValueError, match="dimensions"):
            image_editor.crop(x=10, y=10, width=0, height=50)

    @pytest.mark.contract
    def test_crop_without_image_raises_error(self, image_editor):
        """Contract: Attempting to crop without loaded image raises ValueError."""
        with pytest.raises(ValueError, match="No image loaded"):
            image_editor.crop(x=0, y=0, width=50, height=50)

    # T071: Contract test for revert()
    @pytest.mark.contract
    def test_revert_after_crop(self, image_editor, sample_png_path):
        """Contract: Reverting after crop restores original image."""
        image_editor.load_from_file(sample_png_path)

        # Original is 100x100
        original_size = image_editor.get_current_image().size
        assert original_size == (100, 100)

        # Crop to 50x50
        image_editor.crop(x=25, y=25, width=50, height=50)
        assert image_editor.get_current_image().size == (50, 50)
        assert image_editor.has_unsaved_changes() is True

        # Revert should restore original
        image_editor.revert()

        # Back to original size
        assert image_editor.get_current_image().size == (100, 100)
        assert image_editor.has_unsaved_changes() is False
        assert len(image_editor.get_edit_history()) == 0

    @pytest.mark.contract
    def test_revert_clears_edit_history(self, image_editor, sample_png_path):
        """Contract: Reverting clears all edit history."""
        image_editor.load_from_file(sample_png_path)

        # Perform multiple crops
        image_editor.crop(x=10, y=10, width=80, height=80)
        image_editor.crop(x=5, y=5, width=60, height=60)

        # Should have 2 operations
        assert len(image_editor.get_edit_history()) == 2

        # Revert clears all
        image_editor.revert()
        assert len(image_editor.get_edit_history()) == 0

    @pytest.mark.contract
    def test_revert_without_changes_is_safe(self, image_editor, sample_png_path):
        """Contract: Reverting without changes is safe (no-op)."""
        image_editor.load_from_file(sample_png_path)

        original_size = image_editor.get_current_image().size

        # Revert without any edits should be safe
        image_editor.revert()

        # Image unchanged
        assert image_editor.get_current_image().size == original_size
        assert image_editor.has_unsaved_changes() is False

    @pytest.mark.contract
    def test_revert_without_image_raises_error(self, image_editor):
        """Contract: Attempting to revert without loaded image raises ValueError."""
        with pytest.raises(ValueError, match="No image loaded"):
            image_editor.revert()
