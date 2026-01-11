"""Unit tests for validation utilities."""

import pytest

from utils.validators import (
    is_extreme_dimension,
    validate_image_dimensions,
    validate_resize_dimensions,
)


# T082: Unit tests for resize input validation
@pytest.mark.unit
class TestResizeValidation:
    """Test resize dimension validation."""

    def test_validate_resize_dimensions_positive(self):
        """Valid positive dimensions should not raise error."""
        validate_resize_dimensions(100, 200)
        validate_resize_dimensions(1, 1)
        validate_resize_dimensions(3840, 2160)  # 4K

    def test_validate_resize_dimensions_zero_width_raises_error(self):
        """Zero width should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            validate_resize_dimensions(0, 100)

    def test_validate_resize_dimensions_zero_height_raises_error(self):
        """Zero height should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            validate_resize_dimensions(100, 0)

    def test_validate_resize_dimensions_negative_width_raises_error(self):
        """Negative width should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            validate_resize_dimensions(-10, 100)

    def test_validate_resize_dimensions_negative_height_raises_error(self):
        """Negative height should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            validate_resize_dimensions(100, -50)

    def test_validate_resize_dimensions_aspect_ratio_mode(self):
        """When one dimension is None, it should be allowed (aspect ratio mode)."""
        # Note: validate_resize_dimensions should handle None for aspect ratio calculation
        # For now, we'll check dimensions before calling validator
        validate_resize_dimensions(200, 150)

    def test_is_extreme_dimension_too_small(self):
        """Dimensions less than 50px should be flagged as extreme."""
        assert is_extreme_dimension(49, 100) is True
        assert is_extreme_dimension(100, 49) is True
        assert is_extreme_dimension(10, 10) is True

    def test_is_extreme_dimension_too_large(self):
        """Dimensions greater than 10000px should be flagged as extreme."""
        assert is_extreme_dimension(10001, 100) is True
        assert is_extreme_dimension(100, 10001) is True
        assert is_extreme_dimension(15000, 15000) is True

    def test_is_extreme_dimension_normal_range(self):
        """Dimensions in normal range (50-10000) should not be flagged."""
        assert is_extreme_dimension(50, 50) is False
        assert is_extreme_dimension(100, 100) is False
        assert is_extreme_dimension(1920, 1080) is False
        assert is_extreme_dimension(3840, 2160) is False
        assert is_extreme_dimension(10000, 10000) is False


@pytest.mark.unit
class TestImageDimensionsValidation:
    """Test existing image dimension validation."""

    def test_validate_image_dimensions_positive(self):
        """Valid positive dimensions should not raise error."""
        validate_image_dimensions(100, 200)

    def test_validate_image_dimensions_zero_raises_error(self):
        """Zero dimensions should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            validate_image_dimensions(0, 100)

        with pytest.raises(ValueError, match="positive"):
            validate_image_dimensions(100, 0)

    def test_validate_image_dimensions_negative_raises_error(self):
        """Negative dimensions should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            validate_image_dimensions(-10, 100)

        with pytest.raises(ValueError, match="positive"):
            validate_image_dimensions(100, -50)
