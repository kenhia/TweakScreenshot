# Quick Start Guide: Screenshot Editor GUI

**Project**: TweakScreenshot  
**Date**: 2026-01-10  
**Target Audience**: Developers setting up and working on this project

## Prerequisites

**Required**:
- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **uv** - Fast Python package manager - [Install uv](https://github.com/astral-sh/uv)
- **Git** - Version control
- **Windows 10+** - Primary target platform (cross-platform compatible)

**Recommended**:
- **VS Code** with Python extension
- **PowerShell 5.1+** (for Invoke-Build tasks)

---

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/kenhia/TweakScreenshot.git
cd TweakScreenshot
```

### 2. Install Dependencies

```bash
# Initialize uv environment and install all dependencies
uv sync

# This installs:
# - PySide6 (Qt6 GUI framework)
# - Pillow (image manipulation)
# - pytest, pytest-qt, pytest-cov (testing)
# - ruff (formatting and linting)
```

### 3. Verify Setup

```bash
# Check Python version
uv run python --version
# Should show Python 3.11 or higher

# Run tests (should show 0 tests initially)
uv run pytest

# Check ruff
uv run ruff --version
```

---

## Development Workflow

### Running the Application

```bash
# Run from source
uv run python src/main.py
```

**Expected behavior**:
- Application window opens in <2 seconds
- Empty workspace with menu bar and status bar
- "No image loaded" message or empty display area

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_image_editor.py

# Run with coverage report
uv run pytest --cov=src --cov-report=html

# Run only unit tests (fast)
uv run pytest tests/unit/

# Run integration tests (includes GUI, slower)
uv run pytest tests/integration/
```

### Code Quality Checks

```bash
# Format all Python code
uv run ruff format src/ tests/

# Check for linting errors
uv run ruff check src/ tests/

# Fix auto-fixable linting issues
uv run ruff check src/ tests/ --fix
```

### Pre-Commit Workflow (Constitutional Requirement)

**Before every commit**:

```powershell
# Using Invoke-Build (once set up)
Invoke-Build PreCommit

# Or manually:
uv run ruff format src/ tests/
uv run ruff check src/ tests/
uv run pytest
```

**`.tasks.build.ps1`** will automate this:

```powershell
# Install Invoke-Build (one-time)
Install-Module -Name InvokeBuild -Scope CurrentUser

# Run pre-commit checks
Invoke-Build PreCommit

# Output:
# ✓ Formatting complete
# ✓ Linting passed (0 errors)
# ✓ All tests passed (X tests)
```

---

## Project Structure

```
TweakScreenshot/
├── src/
│   ├── main.py              # Application entry point
│   ├── ui/                  # GUI components (PySide6 widgets)
│   │   ├── main_window.py
│   │   ├── widgets/
│   │   └── dialogs/
│   ├── core/                # Business logic (image operations)
│   │   ├── image_editor.py
│   │   ├── clipboard.py
│   │   └── file_ops.py
│   ├── models/              # Data models (Image, EditHistory, Selection)
│   │   ├── image_model.py
│   │   └── selection.py
│   └── utils/               # Utilities (validators, logger)
│       ├── validators.py
│       └── logger.py
├── tests/
│   ├── unit/                # Unit tests (no GUI dependencies)
│   ├── integration/         # Integration tests (with GUI)
│   ├── contract/            # Contract tests (API verification)
│   └── fixtures/            # Test data (sample images)
├── docs/
│   └── screenshots/         # Example screenshots for README
├── specs/                   # Design documents (this folder)
│   └── 001-screenshot-editor-gui/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── contracts/
│       └── quickstart.md    # This file
├── pyproject.toml           # Project config, dependencies
├── README.md                # User-facing quick-start
├── .tasks.build.ps1         # Invoke-Build automation
└── .gitignore
```

---

## TDD Workflow (Constitutional Requirement)

**Test-Driven Development is mandatory**. Follow this cycle:

### 1. Write Failing Test (RED)

```python
# tests/unit/test_image_editor.py
def test_crop_image():
    editor = ImageEditor()
    editor.load_from_file(Path("tests/fixtures/test.png"))
    
    editor.crop(10, 10, 100, 100)
    
    assert editor.get_dimensions() == (100, 100)
    assert editor.has_unsaved_changes() == True
```

Run test: `uv run pytest tests/unit/test_image_editor.py::test_crop_image`

**Expected**: Test fails (RED) - `crop()` method doesn't exist yet

### 2. Implement Minimum Code to Pass (GREEN)

```python
# src/core/image_editor.py
def crop(self, x: int, y: int, width: int, height: int) -> None:
    if not self.has_image():
        raise ValueError("No image loaded")
    
    box = (x, y, x + width, y + height)
    self._current_image = self._current_image.crop(box)
    self._has_unsaved_changes = True
```

Run test again: **Expected**: Test passes (GREEN)

### 3. Refactor (REFACTOR)

- Add type hints
- Extract validation logic
- Add docstring
- Run tests to ensure they still pass

### 4. Commit

```bash
git add src/core/image_editor.py tests/unit/test_image_editor.py
git commit -m "feat: implement crop operation with tests"
```

---

## Common Development Tasks

### Adding a New Feature

1. **Write specification** in `specs/` (if not already done)
2. **Write tests first** (TDD requirement)
3. **Implement feature** to pass tests
4. **Run pre-commit checks** (format, lint, test)
5. **Commit** with descriptive message

### Debugging GUI Issues

```python
# Add to src/main.py for debugging
import sys
from PySide6.QtCore import QLoggingCategory

# Enable Qt debug output
QLoggingCategory.setFilterRules("*.debug=true")

app = QApplication(sys.argv)
```

**pytest-qt debugging**:
```bash
# Run GUI tests with visible windows (not hidden)
uv run pytest tests/integration/ --no-start-xvfb

# Show Qt warning messages
uv run pytest tests/integration/ -s
```

### Creating Test Fixtures

```python
# tests/conftest.py
import pytest
from PIL import Image
from pathlib import Path

@pytest.fixture
def sample_image(tmp_path):
    """Create a temporary test image."""
    image = Image.new('RGB', (200, 200), color='blue')
    file_path = tmp_path / "test_image.png"
    image.save(file_path)
    return file_path

# Usage in tests:
def test_load_image(sample_image):
    editor = ImageEditor()
    editor.load_from_file(sample_image)
    assert editor.has_image() == True
```

---

## Troubleshooting

### Issue: "uv: command not found"

**Solution**: Install uv:
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify
uv --version
```

### Issue: "ModuleNotFoundError: No module named 'PySide6'"

**Solution**: Sync dependencies:
```bash
uv sync
```

### Issue: Tests fail with Qt platform plugin error

**Solution**: Set environment variable:
```bash
# Windows
set QT_QPA_PLATFORM=windows

# Linux
export QT_QPA_PLATFORM=offscreen
```

### Issue: ruff not found

**Solution**: Ensure using `uv run`:
```bash
# Wrong
ruff check src/

# Correct
uv run ruff check src/
```

---

## IDE Setup (VS Code)

### Recommended Extensions

- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **Ruff** (charliermarsh.ruff)
- **Test Explorer UI** (hbenl.vscode-test-explorer)

### Settings (`.vscode/settings.json`)

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "ruff.lint.args": ["--config=pyproject.toml"],
  "ruff.format.args": ["--config=pyproject.toml"]
}
```

### Tasks (`.vscode/tasks.json`)

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Application",
      "type": "shell",
      "command": "uv run python src/main.py",
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "label": "Run Tests",
      "type": "shell",
      "command": "uv run pytest",
      "group": "test"
    }
  ]
}
```

---

## Next Steps

1. **Explore the codebase**: Start with `src/main.py`, follow imports
2. **Run existing tests**: `uv run pytest -v` to see test structure
3. **Pick a user story**: Refer to `specs/001-screenshot-editor-gui/spec.md`
4. **Follow TDD**: Write test → Implement → Refactor → Commit
5. **Check constitution**: Ensure all requirements met in `specs/001-screenshot-editor-gui/plan.md`

---

## Resources

- **PySide6 Documentation**: https://doc.qt.io/qtforpython-6/
- **Pillow Documentation**: https://pillow.readthedocs.io/
- **pytest Documentation**: https://docs.pytest.org/
- **pytest-qt Plugin**: https://pytest-qt.readthedocs.io/
- **Ruff Documentation**: https://docs.astral.sh/ruff/

---

## Getting Help

- **Specification Questions**: See `specs/001-screenshot-editor-gui/spec.md`
- **Architecture Questions**: See `specs/001-screenshot-editor-gui/data-model.md` and `contracts/`
- **Technical Decisions**: See `specs/001-screenshot-editor-gui/research.md`
- **Constitution/Workflow**: See `.specify/memory/constitution.md`

**Project Repository**: https://github.com/kenhia/TweakScreenshot
