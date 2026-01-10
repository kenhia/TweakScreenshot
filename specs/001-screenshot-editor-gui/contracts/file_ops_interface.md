# Contract: File Operations Interface

**Purpose**: Define the public API for file I/O operations (load, save, clipboard)  
**Module**: `src/core/file_ops.py`  
**Contract Type**: Module Functions

## load_image_from_file

```python
def load_image_from_file(file_path: Path) -> Tuple[PILImage.Image, str]:
    """Load image from file system and detect format.
    
    Args:
        file_path: Path to image file
        
    Returns:
        Tuple of (PIL Image object, format string)
        Format will be 'PNG', 'JPEG', or 'BMP'
        
    Raises:
        FileNotFoundError: If file_path does not exist
        PIL.UnidentifiedImageError: If file is corrupted or not a valid image
        ValueError: If image format not supported (not PNG/JPG/BMP)
    
    Postconditions:
        - Returned image is in RGB or RGBA mode
        - Format string is uppercase ('PNG', 'JPEG', 'BMP')
    """
```

**Contract Tests**:
- Load PNG returns image and 'PNG'
- Load JPEG returns image and 'JPEG'
- Load BMP returns image and 'BMP'
- Load non-existent file raises FileNotFoundError
- Load corrupted file raises PIL.UnidentifiedImageError
- Load unsupported format (GIF, TIFF, WebP) raises ValueError
- Returned image mode is RGB or RGBA

---

## save_image_to_file

```python
def save_image_to_file(image: PILImage.Image, file_path: Path, 
                       format: str = 'PNG', quality: int = 90) -> None:
    """Save PIL Image to file system.
    
    Args:
        image: PIL Image object to save
        file_path: Destination path (will be created/overwritten)
        format: 'PNG' or 'JPEG'
        quality: JPEG quality (1-100), ignored for PNG
        
    Raises:
        ValueError: If format not 'PNG' or 'JPEG'
        ValueError: If quality not in range 1-100
        OSError: If write fails (permissions, disk space, etc.)
    
    Side Effects:
        - Creates or overwrites file at file_path
        - Converts RGBA to RGB if saving as JPEG
    
    Postconditions:
        - File exists at file_path
        - File can be re-loaded with load_image_from_file
    """
```

**Contract Tests**:
- Save PNG preserves transparency
- Save JPEG converts RGBA to RGB
- Save JPEG applies quality parameter
- Save with invalid format raises ValueError
- Save with quality < 1 or > 100 raises ValueError
- Saved file can be reloaded successfully

---

## check_disk_space

```python
def check_disk_space(file_path: Path, estimated_size_mb: float) -> bool:
    """Check if sufficient disk space available for save operation.
    
    Args:
        file_path: Destination path (directory must exist)
        estimated_size_mb: Estimated file size in MB
        
    Returns:
        True if sufficient space, False otherwise
        
    Raises:
        FileNotFoundError: If destination directory does not exist
    
    Implementation Note:
        Uses os.statvfs (Linux/Mac) or shutil.disk_usage (Windows)
        Adds 10% buffer to estimated_size for safety
    """
```

**Contract Tests**:
- Returns True when sufficient space available
- Returns False when insufficient space
- Raises FileNotFoundError for non-existent directory

---

## estimate_file_size

```python
def estimate_file_size(image: PILImage.Image, format: str) -> float:
    """Estimate file size in MB for given image and format.
    
    Args:
        image: PIL Image object
        format: 'PNG' or 'JPEG'
        
    Returns:
        Estimated file size in megabytes
        
    Implementation Note:
        PNG: Roughly width × height × channels × 0.7 (compression factor)
        JPEG: Roughly width × height × 0.05 (high compression)
    """
```

**Contract Tests**:
- PNG estimate within 50% of actual size
- JPEG estimate within 50% of actual size
- Larger images produce larger estimates

---

## load_image_from_clipboard

```python
def load_image_from_clipboard() -> PILImage.Image:
    """Load image from system clipboard.
    
    Returns:
        PIL Image object from clipboard
        
    Raises:
        ValueError: If clipboard does not contain image data
        
    Implementation Note:
        Uses QApplication.clipboard() to access Qt clipboard
        Converts QImage to PIL Image
    """
```

**Contract Tests**:
- Clipboard with image returns PIL Image
- Clipboard without image raises ValueError
- Clipboard with text raises ValueError
- Returned image mode is RGB or RGBA

---

## qimage_to_pil

```python
def qimage_to_pil(qimage: QImage) -> PILImage.Image:
    """Convert Qt QImage to PIL Image.
    
    Args:
        qimage: Qt QImage object
        
    Returns:
        PIL Image object
        
    Implementation Note:
        Handles RGB32, ARGB32, and RGB888 QImage formats
        Converts to RGB or RGBA PIL mode
    """
```

**Contract Tests**:
- QImage RGB32 converts to PIL RGB
- QImage ARGB32 converts to PIL RGBA
- Conversion preserves image dimensions
- Conversion preserves pixel data (spot check)

---

## pil_to_qimage

```python
def pil_to_qimage(pil_image: PILImage.Image) -> QImage:
    """Convert PIL Image to Qt QImage.
    
    Args:
        pil_image: PIL Image object
        
    Returns:
        Qt QImage object
        
    Implementation Note:
        Converts PIL RGB to QImage RGB888
        Converts PIL RGBA to QImage ARGB32
    """
```

**Contract Tests**:
- PIL RGB converts to QImage RGB888
- PIL RGBA converts to QImage ARGB32
- Conversion preserves image dimensions
- Conversion preserves pixel data (spot check)

---

## Contract Verification

**Test Suite**: `tests/contract/test_file_ops_contract.py`

**Test Resources**:
- `tests/fixtures/test_images/` directory with valid PNG, JPEG, BMP files
- Corrupted image files for error testing
- Temporary directory for save operations

**Verification Strategy**:
1. **Happy paths**: All functions succeed with valid inputs
2. **Error paths**: Functions raise documented exceptions for invalid inputs
3. **Conversion round-trips**: PIL ↔ QImage conversions preserve data
4. **File system**: Save/load round-trips preserve image data

**Example Contract Test**:

```python
def test_save_load_roundtrip():
    # Create test image
    original = PILImage.new('RGB', (100, 100), color='red')
    
    # Save to temp file
    temp_file = Path(tmp_dir) / 'test.png'
    save_image_to_file(original, temp_file, format='PNG')
    
    # Load back
    loaded, format = load_image_from_file(temp_file)
    
    # Verify
    assert format == 'PNG'
    assert loaded.size == original.size
    assert loaded.mode == original.mode
    # Pixel-level comparison
    assert list(loaded.getdata()) == list(original.getdata())
```

---

## Implementation Notes

**Platform Differences**:
- Disk space check uses platform-specific APIs (os.statvfs vs shutil.disk_usage)
- Clipboard access via Qt is cross-platform

**Performance**:
- Image conversions (PIL ↔ QImage) should be <100ms for 4K images
- File I/O limited by disk speed; SSD expected for target platform

**Error Messages**:
- All exceptions include descriptive messages (per UX requirement)
- ValueError messages suggest corrective actions
