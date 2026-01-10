# Research: Screenshot Editor GUI

**Date**: 2026-01-10  
**Purpose**: Document technology decisions, best practices, and resolved clarifications for implementation

## Technology Stack Decisions

### Decision: PySide6 vs PyQt6 for GUI Framework

**Chosen**: PySide6

**Rationale**:
- **Licensing**: PySide6 is LGPL (more permissive), PyQt6 is GPL/commercial license
- **Official Qt bindings**: PySide6 is maintained by Qt Company, ensuring long-term support
- **API parity**: Both expose same Qt6 API, functionally equivalent
- **Community**: Both have strong communities, PySide6 slightly more active in Python ecosystem
- **Personal project**: LGPL license is acceptable, avoids GPL copyleft concerns

**Alternatives considered**:
- PyQt6: Rejected due to GPL licensing for open-source projects
- Tkinter: Rejected due to limited widget set, poor DPI support, dated appearance
- Kivy: Rejected as overkill for desktop-only application, better for mobile
- wxPython: Rejected due to smaller community, less modern API

### Decision: Pillow for Image Manipulation

**Chosen**: Pillow (PIL Fork)

**Rationale**:
- **Industry standard**: Most widely used Python imaging library
- **Comprehensive format support**: PNG, JPG, BMP, plus transparency handling
- **Performance**: C-optimized operations, handles 4K images efficiently
- **Simple API**: Intuitive resize, crop, paste operations
- **Well-documented**: Extensive docs and Stack Overflow coverage
- **Qt integration**: Easy conversion between PIL Images and QPixmap/QImage

**Alternatives considered**:
- OpenCV (cv2): Rejected as overkill (computer vision library), heavier dependency
- imageio: Rejected as too low-level, missing high-level editing operations
- Wand (ImageMagick): Rejected due to external dependency (ImageMagick binary), more complex setup

### Decision: pytest + pytest-qt for Testing

**Chosen**: pytest with pytest-qt plugin

**Rationale**:
- **TDD alignment**: pytest's simple assertion syntax supports fast test writing
- **GUI testing**: pytest-qt provides qtbot fixture for simulating Qt events
- **Fixtures**: Powerful fixture system for test setup (mock images, temp files)
- **Coverage**: pytest-cov integration for code coverage tracking
- **Constitutional requirement**: Aligns with Python testing standards in constitution

**Alternatives considered**:
- unittest: Rejected due to more verbose syntax, less idiomatic in modern Python
- nose2: Rejected as pytest has better plugin ecosystem and active development

## Best Practices: PySide6 GUI Development

### Application Architecture

**Pattern**: Model-View-Controller (MVC) variant
- **Model** (`models/`): Image data, edit history, selection state
- **View** (`ui/`): Qt widgets, windows, dialogs
- **Controller** (`core/`): Business logic, image operations

**Rationale**: Separates presentation from logic, enables unit testing of core operations without GUI

### Qt Main Window Pattern

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.connect_signals()
        
    def init_ui(self):
        # Create menu bar, toolbar, status bar, central widget
        # Layout widgets
        
    def connect_signals(self):
        # Connect Qt signals to slots (event handlers)
```

**Best practices**:
- Use `QMainWindow` as top-level window (provides menu bar, status bar, toolbar areas)
- Separate UI initialization from signal connections for clarity
- Use Qt Designer (`.ui` files) for complex layouts (optional, not required for this project)
- Store references to widgets that need runtime updates (status bar, image display)

### Image Display with QLabel and QScrollArea

**Pattern**: `QScrollArea` containing `QLabel` with `QPixmap`

```python
self.image_label = QLabel()
self.image_label.setAlignment(Qt.AlignCenter)
self.scroll_area = QScrollArea()
self.scroll_area.setWidget(self.image_label)
self.setCentralWidget(self.scroll_area)

# Display image
pixmap = QPixmap.fromImage(QImage(...))
self.image_label.setPixmap(pixmap)
```

**Rationale**: 
- `QLabel` can display QPixmap directly
- `QScrollArea` provides automatic scrollbars for large images
- Simpler than custom QGraphicsView for basic image display

### Clipboard Operations

```python
from PySide6.QtGui import QClipboard, QImage

clipboard = QApplication.clipboard()
mime_data = clipboard.mimeData()

if mime_data.hasImage():
    qimage = clipboard.image()  # Returns QImage
    # Convert to PIL Image for manipulation
    pil_image = qimage_to_pil(qimage)
```

**Best practices**:
- Check `mime_data.hasImage()` before accessing clipboard image
- Handle cases where clipboard has text, files, or other non-image data
- QImage ↔ PIL Image conversion needed for Pillow operations

### Dialog Best Practices

**Error dialogs**:
```python
QMessageBox.critical(self, "Error Title", "Error message with suggestion.")
```

**Confirmation dialogs**:
```python
reply = QMessageBox.question(
    self, "Confirm", "Replace image? Unsaved changes will be lost.",
    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
)
```

**Input dialogs** (for resize):
```python
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout
# Custom dialog with form layout for width/height inputs
```

### Keyboard Shortcuts

```python
# In main window
shortcut_paste = QShortcut(QKeySequence("Ctrl+V"), self)
shortcut_paste.activated.connect(self.paste_image)

shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
shortcut_save.activated.connect(self.save_image)
```

**Constitutional alignment**: Meets UX consistency requirement for standard shortcuts

### DPI Awareness (High-DPI Displays)

```python
# In main.py before creating QApplication
from PySide6.QtCore import Qt
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
app = QApplication(sys.argv)
```

**Rationale**: Ensures crisp UI on 4K monitors and mixed-DPI multi-monitor setups (edge case #6)

## Best Practices: Pillow Image Manipulation

### Image Loading

```python
from PIL import Image

# Load from file
image = Image.open(filepath)

# Handle format variations
image = image.convert('RGB')  # Ensure RGB mode for JPG
# or image.convert('RGBA') for PNG with transparency
```

**Error handling**: Wrap in try/except to catch corrupt files, unsupported formats

### Crop Operation

```python
# box = (left, top, right, bottom)
box = (selection.x, selection.y, 
       selection.x + selection.width, 
       selection.y + selection.height)
cropped = image.crop(box)
```

**Note**: Pillow crop uses (left, top, right, bottom), not (x, y, width, height)

### Resize Operation

```python
# Proportional resize (maintain aspect ratio)
width_ratio = new_width / image.width
new_height = int(image.height * width_ratio)
resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Percentage resize
scale_factor = percentage / 100.0
new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
resized = image.resize(new_size, Image.Resampling.LANCZOS)
```

**Best practices**:
- Use `Image.Resampling.LANCZOS` for high-quality downscaling (best quality, slower)
- Use `Image.Resampling.BICUBIC` for upscaling
- For performance-critical paths, `Image.Resampling.BILINEAR` is faster with acceptable quality

### Save Operation

```python
# PNG (lossless, transparency support)
image.save(filepath, format='PNG')

# JPG (lossy, no transparency, smaller file)
if image.mode == 'RGBA':
    # Convert to RGB (JPG doesn't support transparency)
    rgb_image = image.convert('RGB')
    rgb_image.save(filepath, format='JPEG', quality=90)
else:
    image.save(filepath, format='JPEG', quality=90)
```

**Quality parameter**: 90 is good balance for documentation screenshots (spec requirement)

## Best Practices: Testing Qt Applications

### Unit Testing Core Logic (No GUI)

```python
def test_crop_image():
    # Create test image
    image = Image.new('RGB', (100, 100), color='red')
    
    # Perform operation
    cropped = crop_operation(image, x=10, y=10, width=50, height=50)
    
    # Assert
    assert cropped.size == (50, 50)
```

**Pattern**: Test `core/` modules without Qt dependencies

### Integration Testing GUI with pytest-qt

```python
def test_paste_image(qtbot, tmp_path):
    # Create main window
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Simulate Ctrl+V with image in clipboard
    clipboard = QApplication.clipboard()
    test_image = QImage(100, 100, QImage.Format_RGB32)
    clipboard.setImage(test_image)
    
    # Trigger paste
    qtbot.keyClick(window, Qt.Key_V, Qt.ControlModifier)
    
    # Verify image loaded
    assert window.image_label.pixmap() is not None
```

**pytest-qt features**:
- `qtbot.addWidget()`: Manages widget lifecycle
- `qtbot.keyClick()`: Simulates keyboard input
- `qtbot.mouseClick()`: Simulates mouse events
- `qtbot.waitSignal()`: Waits for Qt signal emission

### Contract Testing

```python
def test_image_editor_contract():
    """Verify ImageEditor class provides required interface."""
    editor = ImageEditor()
    
    # Contract: Must have these methods
    assert hasattr(editor, 'load_image')
    assert hasattr(editor, 'crop')
    assert hasattr(editor, 'resize')
    assert hasattr(editor, 'revert')
    assert hasattr(editor, 'save_image')
    
    # Contract: Methods must accept expected parameters
    import inspect
    sig = inspect.signature(editor.crop)
    assert 'x' in sig.parameters
    assert 'y' in sig.parameters
    assert 'width' in sig.parameters
    assert 'height' in sig.parameters
```

**Purpose**: Ensures public API stability, catches breaking changes

## Dependency Management with uv

### Project Initialization

```bash
# Create new project
uv init

# Add dependencies
uv add PySide6 Pillow
uv add --dev pytest pytest-qt pytest-cov ruff
```

### Development Workflow

```bash
# Sync environment (like pip install -r requirements.txt)
uv sync

# Run tests
uv run pytest

# Run application
uv run python src/main.py
```

**Benefits**: Faster than pip, better dependency resolution, lock file for reproducibility

## Code Quality with ruff

### Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "DTZ", "T10", "EM", "ISC", "ICN", "PIE", "PT", "Q", "RET", "SIM", "TID", "TCH", "ARG", "PTH", "PD", "PL", "TRY", "NPY", "RUF"]
ignore = ["E501"]  # Line too long (handled by formatter)

[tool.ruff.format]
quote-style = "double"
```

### Pre-commit Workflow

```powershell
# Format all Python files
ruff format src/ tests/

# Check for linting errors
ruff check src/ tests/ --fix

# Run tests
pytest
```

**Integration**: Invoke-Build task will automate this sequence

## Performance Considerations

### Memory Management for Large Images

**Challenge**: 4K images (3840×2160 RGB) = ~25MB uncompressed in memory

**Strategy**:
- Keep only 2 copies in memory: original + current edited version
- Edit history stores operation metadata, not full images (e.g., "crop(10,10,100,100)")
- For revert, reapply operations from original instead of storing intermediate images

### Image Display Optimization

**Challenge**: QLabel with QPixmap loads full image into video memory

**Strategy**:
- For images larger than viewport, consider displaying scaled-down version
- Use Qt's `Qt.SmoothTransformation` for display scaling (doesn't modify underlying image)
- Full-resolution image used only for save operation

### Startup Time Optimization

**Target**: <2 seconds cold start

**Strategy**:
- Defer heavy imports (Pillow) until first use if possible
- Compile UI logic (no Qt Designer .ui files, pure Python)
- Use PyInstaller with `--onefile` option for single executable (removes import overhead)

## Resolved Clarifications

All technical details specified in Technical Context section. No NEEDS CLARIFICATION items remain.

**Key decisions locked in**:
- Language: Python 3.11+
- GUI: PySide6 (Qt6)
- Images: Pillow
- Testing: pytest + pytest-qt
- Tooling: uv, ruff, Invoke-Build
- Platform: Windows 10+ desktop (cross-platform capable)
- Architecture: MVC-variant with separated UI/core/models layers

**Ready for Phase 1**: Data model definition and contract specification.
