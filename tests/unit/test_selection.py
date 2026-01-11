"""Unit tests for Selection model."""

import pytest


class TestSelectionModel:
    """Test Selection model validation and bounds checking."""

    # T056: Unit test for Selection model validation
    @pytest.mark.unit
    def test_selection_valid_region(self):
        """Selection with valid region is created successfully."""
        from models.selection import Selection

        selection = Selection(x=10, y=20, width=100, height=50)

        assert selection.x == 10
        assert selection.y == 20
        assert selection.width == 100
        assert selection.height == 50

    @pytest.mark.unit
    def test_selection_negative_coordinates_raises_error(self):
        """Selection with negative coordinates raises ValueError."""
        from models.selection import Selection

        with pytest.raises(ValueError, match="negative"):
            Selection(x=-10, y=20, width=100, height=50)

    @pytest.mark.unit
    def test_selection_zero_width_raises_error(self):
        """Selection with zero width raises ValueError."""
        from models.selection import Selection

        with pytest.raises(ValueError, match="positive"):
            Selection(x=10, y=20, width=0, height=50)

    @pytest.mark.unit
    def test_selection_zero_height_raises_error(self):
        """Selection with zero height raises ValueError."""
        from models.selection import Selection

        with pytest.raises(ValueError, match="positive"):
            Selection(x=10, y=20, width=100, height=0)

    @pytest.mark.unit
    def test_selection_bounds_check_within_image(self):
        """Selection within image bounds passes validation."""
        from models.selection import Selection

        selection = Selection(x=10, y=10, width=50, height=50)

        # Image is 100x100
        assert selection.is_within_bounds(100, 100) is True

    @pytest.mark.unit
    def test_selection_bounds_check_outside_image(self):
        """Selection outside image bounds fails validation."""
        from models.selection import Selection

        selection = Selection(x=80, y=80, width=50, height=50)

        # Selection extends beyond 100x100 image
        assert selection.is_within_bounds(100, 100) is False

    @pytest.mark.unit
    def test_selection_to_tuple(self):
        """Selection can be converted to tuple for PIL crop."""
        from models.selection import Selection

        selection = Selection(x=10, y=20, width=100, height=50)

        # PIL crop expects (left, upper, right, lower)
        assert selection.to_tuple() == (10, 20, 110, 70)

    @pytest.mark.unit
    def test_selection_area(self):
        """Selection calculates area correctly."""
        from models.selection import Selection

        selection = Selection(x=10, y=20, width=100, height=50)

        assert selection.area() == 5000
