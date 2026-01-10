# TweakScreenshot

GUI application for editing screenshots for markdown documentation. Load images via file or clipboard, perform basic edits (crop, resize, revert), and save in PNG/JPG formats.

## Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```powershell
# Clone the repository
git clone https://github.com/kenhia/TweakScreenshot.git
cd TweakScreenshot

# Install dependencies with uv
uv sync --extra dev
```

### Running the Application

```powershell
# Run the application
uv run python src/main.py
```

### Development Workflow

```powershell
# Format code
uv run ruff format src/ tests/

# Lint code
uv run ruff check src/ tests/

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Run all pre-commit checks (format → lint → test)
.\.specify\scripts\powershell\pre-commit-check.ps1
```

### Using Invoke-Build (Alternative)

```powershell
# Run all checks (default task)
Invoke-Build

# Individual tasks
Invoke-Build Format      # Format code
Invoke-Build Lint        # Lint code
Invoke-Build Test        # Run tests
Invoke-Build PreCommit   # Run pre-commit checks
Invoke-Build Clean       # Clean build artifacts
```

## Features

- **Load & Display**: Load screenshots from file or clipboard (Ctrl-V)
- **Crop**: Select and crop rectangular regions
- **Resize**: Resize by dimensions or percentage
- **Revert**: Restore original image
- **Save**: Save as PNG or JPG with format options
- **Markup** (Stretch Goal): Add text, boxes, and arrows

## Keyboard Shortcuts

- `Ctrl-V`: Paste image from clipboard
- `Ctrl-S`: Save image
- `Ctrl-R`: Revert to original
- `Ctrl-Z`: Undo last operation
- `Escape`: Cancel selection

## Testing

This project follows Test-Driven Development (TDD):

```powershell
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest -m unit           # Unit tests only
uv run pytest -m integration    # Integration tests only
uv run pytest -m contract       # Contract tests only

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing
```

## Project Structure

```
src/
├── main.py              # Application entry point
├── ui/
│   ├── main_window.py   # Main window and layout
│   ├── widgets/         # Custom widgets (image viewer, crop selector)
│   └── dialogs/         # Resize dialog, error dialogs
├── core/
│   ├── image_editor.py  # Core editing logic
│   ├── clipboard.py     # Clipboard operations
│   └── file_ops.py      # File load/save operations
├── models/
│   ├── image_model.py   # Image entity and edit history
│   └── selection.py     # Selection/crop region model
└── utils/
    ├── validators.py    # Input validation
    └── logger.py        # Logging configuration

tests/
├── unit/                # Unit tests
├── integration/         # Integration tests
└── contract/            # Contract tests
```

## License

Personal project by Ken.

## Contributing

This is a personal project following [Ken's Personal Constitution](.specify/memory/constitution.md). All contributions must adhere to TDD discipline and quality standards defined in the constitution.
