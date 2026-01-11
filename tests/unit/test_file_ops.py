"""Unit tests for file operations module."""

from pathlib import Path

import pytest
from PIL import Image as PILImage


class TestFileOperations:
    """Test file I/O operations."""

    @pytest.fixture
    def sample_png(self, tmp_path):
        """Create sample PNG file."""
        img_path = tmp_path / "test.png"
        img = PILImage.new("RGB", (200, 150), color="green")
        img.save(img_path, "PNG")
        return img_path

    @pytest.fixture
    def sample_jpg(self, tmp_path):
        """Create sample JPG file."""
        img_path = tmp_path / "test.jpg"
        img = PILImage.new("RGB", (200, 150), color="yellow")
        img.save(img_path, "JPEG")
        return img_path

    @pytest.fixture
    def sample_bmp(self, tmp_path):
        """Create sample BMP file."""
        img_path = tmp_path / "test.bmp"
        img = PILImage.new("RGB", (200, 150), color="cyan")
        img.save(img_path, "BMP")
        return img_path

    # T019: Unit tests for load_image_from_file()
    @pytest.mark.unit
    def test_load_png_returns_pil_image(self, sample_png):
        """Load PNG file returns PIL Image object."""
        from core.file_ops import load_image_from_file

        img = load_image_from_file(sample_png)

        assert isinstance(img, PILImage.Image)
        assert img.size == (200, 150)
        assert img.mode in ("RGB", "RGBA")

    @pytest.mark.unit
    def test_load_jpg_returns_pil_image(self, sample_jpg):
        """Load JPG file returns PIL Image object."""
        from core.file_ops import load_image_from_file

        img = load_image_from_file(sample_jpg)

        assert isinstance(img, PILImage.Image)
        assert img.size == (200, 150)

    @pytest.mark.unit
    def test_load_bmp_returns_pil_image(self, sample_bmp):
        """Load BMP file returns PIL Image object."""
        from core.file_ops import load_image_from_file

        img = load_image_from_file(sample_bmp)

        assert isinstance(img, PILImage.Image)
        assert img.size == (200, 150)

    @pytest.mark.unit
    def test_load_nonexistent_file_raises_error(self):
        """Load nonexistent file raises FileNotFoundError."""
        from core.file_ops import load_image_from_file

        with pytest.raises(FileNotFoundError):
            load_image_from_file(Path("does_not_exist.png"))

    @pytest.mark.unit
    def test_load_invalid_image_raises_error(self, tmp_path):
        """Load invalid image file raises ValueError."""
        from core.file_ops import load_image_from_file

        bad_file = tmp_path / "not_an_image.png"
        bad_file.write_text("Not an image")

        with pytest.raises((ValueError, PILImage.UnidentifiedImageError)):
            load_image_from_file(bad_file)

    @pytest.mark.unit
    def test_load_converts_to_rgb(self, tmp_path):
        """Load ensures image is in RGB or RGBA mode."""
        from core.file_ops import load_image_from_file

        # Create grayscale image
        gray_path = tmp_path / "gray.png"
        gray_img = PILImage.new("L", (100, 100), color=128)
        gray_img.save(gray_path, "PNG")

        img = load_image_from_file(gray_path)

        # Should be converted to RGB or RGBA
        assert img.mode in ("RGB", "RGBA")
