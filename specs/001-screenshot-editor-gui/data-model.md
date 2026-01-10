# Data Model: Screenshot Editor GUI

**Date**: 2026-01-10  
**Purpose**: Define entities, their attributes, relationships, and state management

## Core Entities

### Image

**Purpose**: Represents the screenshot being edited, including original and current state

**Attributes**:
- `original_data: PIL.Image.Image` - The unmodified image loaded from file/clipboard (immutable after load)
- `current_data: PIL.Image.Image` - The current edited version of the image
- `width: int` - Current image width in pixels (derived from `current_data.width`)
- `height: int` - Current image height in pixels (derived from `current_data.height`)
- `format: str | None` - Original file format ('PNG', 'JPEG', 'BMP', None if from clipboard)
- `file_path: Path | None` - Original file path if loaded from file, None if pasted from clipboard
- `has_unsaved_changes: bool` - Flag indicating if current_data differs from last saved state

**Validation Rules**:
- Width and height must be > 0
- Image data must be in RGB or RGBA mode
- Format must be one of: PNG, JPEG, BMP, or None

**State Transitions**:
```
EMPTY → LOADED (load_image or paste_image)
LOADED → EDITED (crop or resize applied)
EDITED → SAVED (save_image)
EDITED → LOADED (revert to original)
LOADED → EMPTY (user pastes new image and confirms replace)
```

**Lifecycle**:
1. Created empty on application start
2. Populated when user loads file or pastes from clipboard
3. Modified by crop/resize operations (creates new current_data, preserves original_data)
4. Reverted by copying original_data to current_data
5. Saved by writing current_data to file
6. Replaced when new image loaded

---

### EditHistory

**Purpose**: Track editing operations to support revert functionality and operation metadata

**Attributes**:
- `operations: List[EditOperation]` - Stack of operations applied to the image
- `original_image: PIL.Image.Image` - Reference to the unmodified original (same as Image.original_data)

**Operations** (EditOperation dataclass):
```python
@dataclass
class EditOperation:
    type: str  # 'crop', 'resize'
    timestamp: datetime
    parameters: Dict[str, Any]  # e.g., {'x': 10, 'y': 20, 'width': 100, 'height': 100}
```

**Methods**:
- `add_operation(op: EditOperation) -> None` - Add operation to history
- `clear() -> None` - Clear all operations (called after revert or new image load)
- `get_operation_summary() -> str` - Human-readable summary (e.g., "2 operations: crop, resize")

**Validation Rules**:
- Operations list cannot exceed reasonable size (e.g., 100 operations to prevent memory issues)
- Each operation must have valid type and parameters

**State Transitions**:
```
EMPTY → HAS_OPERATIONS (first edit applied)
HAS_OPERATIONS → HAS_OPERATIONS (additional edits)
HAS_OPERATIONS → EMPTY (revert called, or new image loaded)
```

**Usage**:
- Primarily for display/debugging (operation count in status bar)
- Revert functionality doesn't replay operations; it copies original_data to current_data
- Future enhancement: Could enable undo/redo if individual operations stored

---

### Selection

**Purpose**: Represents the rectangular region selected by user for cropping

**Attributes**:
- `x: int` - Left coordinate of selection in pixels (0-based)
- `y: int` - Top coordinate of selection in pixels (0-based)
- `width: int` - Selection width in pixels
- `height: int` - Selection height in pixels
- `is_active: bool` - Whether selection is currently being drawn or confirmed
- `image_bounds: Tuple[int, int]` - Reference to parent image dimensions for validation

**Validation Rules**:
- x, y, width, height must all be >= 0
- x + width must be <= image width
- y + height must be <= image height
- width and height must be > 0 (no zero-size selections)
- Selection automatically clamps to image boundaries if user drags outside

**State Transitions**:
```
INACTIVE → DRAWING (user begins click-drag)
DRAWING → ACTIVE (user releases mouse, selection confirmed)
ACTIVE → INACTIVE (user presses Escape, clicks outside, or crops)
INACTIVE → INACTIVE (no selection exists)
```

**Methods**:
- `to_box() -> Tuple[int, int, int, int]` - Convert to Pillow crop box format: (left, top, right, bottom)
- `clamp_to_bounds(image_width: int, image_height: int) -> None` - Ensure selection within image
- `clear() -> None` - Deactivate and reset selection

**Lifecycle**:
1. Created when user begins click-drag on image
2. Updated continuously during drag (real-time visual feedback)
3. Finalized when user releases mouse
4. Used by crop operation to determine crop region
5. Cleared after crop or when user cancels (Escape, click outside)

---

### MarkupElement (Stretch Goal - Phase 2)

**Purpose**: Represents an annotation (text, box, arrow) added to the image

**Attributes**:
- `id: UUID` - Unique identifier for the element
- `type: str` - 'text', 'box', or 'arrow'
- `position: Tuple[int, int]` - (x, y) coordinates on image
- `size: Tuple[int, int]` - (width, height) for box, or bounding box for text/arrow
- `content: str | None` - Text content for 'text' type, None for box/arrow
- `color: Tuple[int, int, int]` - RGB color (e.g., (255, 0, 0) for red)
- `thickness: int` - Line thickness for box borders and arrow lines (default 2px)
- `font_size: int | None` - Font size for text elements (default 16)
- `is_selected: bool` - Whether element is currently selected for editing

**Validation Rules**:
- Type must be one of: 'text', 'box', 'arrow'
- Position must be within image bounds
- Color values must be 0-255
- Thickness must be 1-10
- Font size must be 8-72 (if text type)
- Content required for 'text' type, None for others

**State Transitions**:
```
CREATED → PLACED (user finishes drawing element)
PLACED → SELECTED (user clicks element)
SELECTED → PLACED (user clicks elsewhere)
PLACED → RENDERED (save operation flattens markup into image)
```

**Methods**:
- `render(draw: ImageDraw.Draw) -> None` - Draw element onto image using Pillow's ImageDraw
- `contains_point(x: int, y: int) -> bool` - Check if point is inside element (for selection)
- `move(dx: int, dy: int) -> None` - Move element by offset

**Usage** (Stretch Goal):
- Created when user activates markup tool and interacts with image
- Stored in a collection (List[MarkupElement]) in the application state
- Rendered as overlay in UI (non-destructive preview)
- Flattened into image pixels on save (destructive, cannot be edited after save/reload)

---

## Entity Relationships

```
Application (Main Window)
    ↓
    has-one: Image (current loaded image)
    ↓
    has-one: EditHistory (operations applied to Image)
    ↓
    has-one-or-none: Selection (active crop selection)
    ↓
    has-many: List[MarkupElement] (stretch goal, Phase 2)
```

**Relationship Rules**:
- Application always has exactly one Image instance (may be empty/unloaded)
- Image has one EditHistory that tracks its modifications
- Selection is optional; exists only when user is cropping
- MarkupElements (stretch goal) are owned by Application, reference Image for bounds checking

---

## Data Persistence

**No Database**: This is a single-session tool; no persistence of editing state across app launches.

**File I/O Only**:
- **Load**: Read image from file system into Image.original_data and Image.current_data
- **Save**: Write Image.current_data to file system
- **Clipboard**: Read image from OS clipboard into Image.original_data and Image.current_data

**No Session State**: When user closes app, all unsaved changes are lost (warn user if `has_unsaved_changes` is True).

---

## State Management

**Single Source of Truth**: The `Image` entity holds the current state. All UI components reflect this state.

**State Flow**:
```
User Action → Event Handler → Core Operation → Update Image State → Update UI
```

**Example: Crop Operation**:
1. User drags selection → Creates Selection entity
2. User clicks Crop button → Triggers `image_editor.crop(selection)`
3. Core operation: `image.current_data = image.current_data.crop(selection.to_box())`
4. EditHistory: `history.add_operation(EditOperation('crop', ...))`
5. UI updates: Display new cropped image, update status bar dimensions

**Concurrency**: Single-threaded application, no thread safety required (Qt event loop handles events sequentially).

---

## Type Hints and Validation

**Type Annotations**: All entity classes use Python type hints for attributes and methods.

**Validation**: 
- Use Pydantic or dataclasses with custom `__post_init__` for attribute validation
- Raise `ValueError` with descriptive messages for invalid states
- Validation checked at entity creation and before state transitions

**Example**:
```python
from dataclasses import dataclass
from PIL import Image as PILImage
from pathlib import Path

@dataclass
class Image:
    original_data: PILImage.Image
    current_data: PILImage.Image
    format: str | None
    file_path: Path | None
    
    def __post_init__(self):
        if self.original_data.width <= 0 or self.original_data.height <= 0:
            raise ValueError("Image dimensions must be positive")
        if self.format and self.format not in ('PNG', 'JPEG', 'BMP'):
            raise ValueError(f"Unsupported format: {self.format}")
```

---

## Testing Considerations

**Unit Tests**:
- Create Image with mock PIL.Image.Image objects
- Test validation rules (invalid dimensions, formats)
- Test state transitions (LOADED → EDITED → SAVED)

**Integration Tests**:
- Load real image files and verify Image entity populated correctly
- Apply crop/resize and verify current_data updated, original_data unchanged
- Test revert restores original_data

**Contract Tests**:
- Verify Image exposes required attributes
- Verify EditHistory provides add_operation and clear methods
- Verify Selection provides to_box() method with correct format

---

## Future Enhancements (Out of Current Scope)

- **Undo/Redo**: EditHistory could store actual image data or reversible operations
- **Non-destructive editing**: Store operations as a pipeline, only render on save
- **Multi-image support**: Extend Application to manage List[Image] with tabbed interface
- **Persistent markup**: Save markup elements as metadata in PNG (requires custom chunks)

**Current Scope**: Simple, destructive editing with single revert-to-original capability.
