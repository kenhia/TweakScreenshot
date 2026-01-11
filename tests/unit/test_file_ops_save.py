"""Unit tests for save operations in file_ops module."""

from pathlib import Path

import pytest
from PIL import Image as PILImage


class TestSaveImageToFile:
    """Test save_image_to_file() function."""

    @pytest.fixture
    def sample_image(self):
        """Create sample PIL Image for testing."""
        return PILImage.new("RGB", (100, 100), color="green")

    # T038: Unit test for save_image_to_file()
    @pytest.mark.unit
    def test_save_png_creates_file(self, sample_image, tmp_path):
        """Saving PNG creates valid file."""
        from core.file_ops import save_image_to_file

        output_path = tmp_path / "test.png"
        save_image_to_file(sample_image, output_path, format_str="PNG")

        assert output_path.exists()
        saved_img = PILImage.open(output_path)
        assert saved_img.format == "PNG"
        assert saved_img.size == (100, 100)

    @pytest.mark.unit
    def test_save_jpg_with_quality(self, sample_image, tmp_path):
        """Saving JPG with quality parameter works."""
        from core.file_ops import save_image_to_file

        output_path = tmp_path / "test.jpg"
        save_image_to_file(sample_image, output_path, format_str="JPEG", quality=85)

        assert output_path.exists()
        saved_img = PILImage.open(output_path)
        assert saved_img.format == "JPEG"

    @pytest.mark.unit
    def test_save_bmp_creates_file(self, sample_image, tmp_path):
        """Saving BMP creates valid file."""
        from core.file_ops import save_image_to_file

        output_path = tmp_path / "test.bmp"
        save_image_to_file(sample_image, output_path, format_str="BMP")

        assert output_path.exists()
        saved_img = PILImage.open(output_path)
        assert saved_img.format == "BMP"

    @pytest.mark.unit
    def test_save_to_nonexistent_directory_creates_dir(self, sample_image, tmp_path):
        """Saving to nonexistent directory creates parent directories."""
        from core.file_ops import save_image_to_file

        output_path = tmp_path / "nested" / "dir" / "test.png"
        save_image_to_file(sample_image, output_path, format_str="PNG")

        assert output_path.exists()

    @pytest.mark.unit
    def test_save_unsupported_format_raises_error(self, sample_image, tmp_path):
        """Saving with unsupported format raises ValueError."""
        from core.file_ops import save_image_to_file

        output_path = tmp_path / "test.gif"

        with pytest.raises(ValueError, match="Unsupported format"):
            save_image_to_file(sample_image, output_path, format_str="GIF")


class TestCheckDiskSpace:
    """Test check_disk_space() function."""

    # T039: Unit test for check_disk_space()
    @pytest.mark.unit
    def test_check_disk_space_sufficient_returns_true(self, tmp_path):
        """Check disk space returns True when sufficient space available."""
        from core.file_ops import check_disk_space

        # Small file size (1 KB) should always have space
        result = check_disk_space(tmp_path, required_bytes=1024)

        assert result is True

    @pytest.mark.unit
    def test_check_disk_space_insufficient_returns_false(self, tmp_path):
        """Check disk space returns False when insufficient space."""
        from core.file_ops import check_disk_space

        # Extremely large file size (1 PB) should trigger False
        result = check_disk_space(tmp_path, required_bytes=1024**5)

        assert result is False

    @pytest.mark.unit
    def test_check_disk_space_nonexistent_path_raises_error(self):
        """Check disk space with nonexistent path raises ValueError."""
        from core.file_ops import check_disk_space

        with pytest.raises(ValueError, match="does not exist"):
            check_disk_space(Path("/nonexistent/path"), required_bytes=1024)


class TestEstimateFileSize:
    """Test estimate_file_size() function."""

    @pytest.mark.unit
    def test_estimate_png_file_size(self):
        """Estimate file size for PNG returns reasonable value."""
        from core.file_ops import estimate_file_size

        # 1920x1080 image should estimate reasonable PNG size
        estimated = estimate_file_size(1920, 1080, "PNG")

        # PNG typically 10-30 KB per megapixel for screenshots
        # 1920x1080 = 2.07 MP, expect ~20-60 KB
        assert 10_000 < estimated < 100_000

    @pytest.mark.unit
    def test_estimate_jpg_file_size(self):
        """Estimate file size for JPG returns reasonable value."""
        from core.file_ops import estimate_file_size

        # 1920x1080 image should estimate smaller JPG size
        estimated = estimate_file_size(1920, 1080, "JPEG")

        # JPG typically 5-15 KB per megapixel with quality 90
        assert 5_000 < estimated < 50_000

    @pytest.mark.unit
    def test_estimate_file_size_for_large_image(self):
        """Estimate file size for 4K image returns reasonable value."""
        from core.file_ops import estimate_file_size

        # 3840x2160 = 8.3 MP
        estimated = estimate_file_size(3840, 2160, "PNG")

        # Should be roughly 4x larger than 1080p
        assert 40_000 < estimated < 400_000
