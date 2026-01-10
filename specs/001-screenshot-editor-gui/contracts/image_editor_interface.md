# Contract: ImageEditor Interface

**Purpose**: Define the public API for core image editing operations  
**Module**: `src/core/image_editor.py`  
**Contract Type**: Class Interface

## ImageEditor Class

**Responsibility**: Orchestrate image loading, editing operations (crop, resize, revert), and provide access to current image state.

### Constructor

```python
def __init__(self) -> None:
    """Initialize image editor with empty state."""
```

**Postconditions**:
- `has_image()` returns `False`
- `get_current_image()` returns `None`

---

### load_from_file

```python
def load_from_file(self, file_path: Path) -> None:
    """Load image from file system.
    
    Args:
        file_path: Path to image file (PNG, JPG, BMP)
        
    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file is not a valid image or format not supported
        PIL.UnidentifiedImageError: If file is corrupted
    
    Postconditions:
        - has_image() returns True
        - get_current_image() returns PIL Image object
        - has_unsaved_changes() returns False
        - get_edit_history() returns empty list
    """
```

**Contract Tests**:
- Valid PNG file loads successfully
- Valid JPG file loads successfully
- Invalid file path raises FileNotFoundError
- Corrupted image file raises appropriate exception
- After load, current and original images are identical

---

### load_from_clipboard

```python
def load_from_clipboard(self) -> None:
    """Load image from system clipboard.
    
    Raises:
        ValueError: If clipboard does not contain image data
    
    Postconditions:
        - has_image() returns True
        - get_current_image() returns PIL Image object
        - get_file_path() returns None (clipboard has no file path)
        - has_unsaved_changes() returns False
```

**Contract Tests**:
- Clipboard with image loads successfully
- Clipboard without image raises ValueError with clear message
- After load from clipboard, file_path is None

---

### crop

```python
def crop(self, x: int, y: int, width: int, height: int) -> None:
    """Crop current image to specified rectangular region.
    
    Args:
        x: Left coordinate (0-based, in pixels)
        y: Top coordinate (0-based, in pixels)
        width: Selection width in pixels
        height: Selection height in pixels
    
    Raises:
        ValueError: If no image loaded
        ValueError: If coordinates out of bounds or dimensions invalid
    
    Preconditions:
        - has_image() must return True
        - x, y, width, height must define region within image bounds
        - width and height must be > 0
    
    Postconditions:
        - get_current_image() returns cropped image
        - Image dimensions match width × height
        - has_unsaved_changes() returns True
        - Operation added to edit history
    """
```

**Contract Tests**:
- Crop with valid coordinates succeeds
- Crop updates image dimensions correctly
- Crop marks image as having unsaved changes
- Crop on empty editor raises ValueError
- Crop with out-of-bounds coordinates raises ValueError
- Original image remains unchanged after crop

---

### resize

```python
def resize(self, width: int | None = None, height: int | None = None, 
           percentage: float | None = None) -> None:
    """Resize current image.
    
    Args:
        width: New width in pixels (maintains aspect ratio if height is None)
        height: New height in pixels (maintains aspect ratio if width is None)
        percentage: Scale factor as percentage (e.g., 50.0 for 50%)
        
    Raises:
        ValueError: If no image loaded
        ValueError: If no resize parameters provided
        ValueError: If both dimensions and percentage provided
        ValueError: If dimensions < 50px or > 10000px (warning thresholds)
    
    Preconditions:
        - has_image() must return True
        - Exactly one of (width, height, percentage) or both (width, height) provided
        - If width or height provided, value must be positive integer
        - If percentage provided, value must be > 0
    
    Postconditions:
        - get_current_image() returns resized image
        - Image dimensions match requested size (or proportional if aspect ratio maintained)
        - has_unsaved_changes() returns True
        - Operation added to edit history
    """
```

**Contract Tests**:
- Resize by width only maintains aspect ratio
- Resize by height only maintains aspect ratio
- Resize by percentage scales proportionally
- Resize by both width and height uses exact dimensions
- Resize marks image as having unsaved changes
- Resize with no parameters raises ValueError
- Resize on empty editor raises ValueError

---

### revert

```python
def revert(self) -> None:
    """Revert current image to original (undo all edits).
    
    Raises:
        ValueError: If no image loaded
    
    Preconditions:
        - has_image() must return True
    
    Postconditions:
        - get_current_image() returns original image (identical to state after load)
        - has_unsaved_changes() returns False
        - Edit history cleared
    """
```

**Contract Tests**:
- Revert after edits restores original image
- Revert clears edit history
- Revert marks image as having no unsaved changes
- Revert on empty editor raises ValueError
- Multiple reverts are idempotent (no-op after first)

---

### save_to_file

```python
def save_to_file(self, file_path: Path, format: str = 'PNG', 
                 quality: int = 90) -> None:
    """Save current image to file system.
    
    Args:
        file_path: Destination file path
        format: Image format ('PNG' or 'JPEG')
        quality: JPEG quality (1-100, default 90), ignored for PNG
        
    Raises:
        ValueError: If no image loaded
        ValueError: If format not supported
        ValueError: If quality out of range (1-100)
        OSError: If insufficient disk space or write permission denied
    
    Preconditions:
        - has_image() must return True
        - format must be 'PNG' or 'JPEG'
        - quality must be 1-100 (if JPEG)
    
    Postconditions:
        - File created at file_path with current image data
        - has_unsaved_changes() returns False
        - If original loaded from file, file_path updated to new location
    """
```

**Contract Tests**:
- Save as PNG succeeds and preserves transparency
- Save as JPEG succeeds with specified quality
- Save updates internal file path
- Save marks image as having no unsaved changes
- Save with invalid format raises ValueError
- Save with invalid quality raises ValueError
- Save on empty editor raises ValueError

---

### Query Methods

```python
def has_image(self) -> bool:
    """Check if image is currently loaded."""

def get_current_image(self) -> PILImage.Image | None:
    """Get current image data (None if no image loaded)."""

def get_original_image(self) -> PILImage.Image | None:
    """Get original unmodified image (None if no image loaded)."""

def has_unsaved_changes(self) -> bool:
    """Check if current image differs from last saved state."""

def get_dimensions(self) -> Tuple[int, int] | None:
    """Get current image dimensions as (width, height), or None if no image."""

def get_file_path(self) -> Path | None:
    """Get original file path (None if loaded from clipboard or never saved)."""

def get_edit_history(self) -> List[str]:
    """Get list of operation descriptions (e.g., ['crop', 'resize'])."""
```

**Contract Tests**:
- Query methods return correct values in all states (empty, loaded, edited)
- get_current_image() never mutates image (returns copy or reference)
- has_unsaved_changes() accurate after load, edit, save, revert

---

## Contract Verification

**Test Suite**: `tests/contract/test_image_editor_contract.py`

**Verification Strategy**:
1. **Interface completeness**: All methods defined and callable
2. **Parameter types**: Type hints match actual parameter types
3. **Precondition enforcement**: Methods raise ValueError when preconditions violated
4. **Postcondition verification**: State changes match documented postconditions
5. **Exception contracts**: Documented exceptions raised for error conditions

**Example Contract Test**:

```python
def test_crop_contract_postconditions():
    editor = ImageEditor()
    editor.load_from_file(Path("test_image.png"))
    
    original_width, original_height = editor.get_dimensions()
    
    # Perform crop
    editor.crop(10, 10, 100, 100)
    
    # Verify postconditions
    assert editor.has_image() == True
    assert editor.get_dimensions() == (100, 100)
    assert editor.has_unsaved_changes() == True
    assert len(editor.get_edit_history()) == 1
    assert editor.get_original_image().size == (original_width, original_height)
```

---

## Implementation Notes

**Error Handling**: All public methods validate inputs and raise descriptive exceptions.

**Thread Safety**: Not required (single-threaded Qt event loop).

**Performance**: Operations should complete in <1 second for 4K images (per performance requirements).

**Logging**: Log errors and operations >500ms (per performance monitoring requirement).
