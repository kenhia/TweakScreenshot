# Implementation Plan: Screenshot Editor GUI

**Branch**: `001-screenshot-editor-gui` | **Date**: 2026-01-10 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-screenshot-editor-gui/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a desktop GUI application for editing screenshots used in markdown documentation. Users can load images via file or clipboard paste (Ctrl-V), perform basic edits (crop, resize), revert to original, and save in PNG/JPG formats. Stretch goal includes markup tools (text, boxes, arrows). Technical approach: Python 3.11+ with PySide6 for native Windows GUI, Pillow for image manipulation, pytest for TDD workflow.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: PySide6 (Qt6 GUI framework), Pillow (image manipulation), pytest + pytest-qt (testing)  
**Storage**: File system only (load from/save to user-selected files), no database  
**Testing**: pytest for unit tests, pytest-qt for GUI integration tests  
**Target Platform**: Windows 10+ desktop (primary), cross-platform compatible (Windows/Mac/Linux via Qt)
**Project Type**: Single desktop application  
**Performance Goals**: UI interactions <100ms, image operations (crop/resize) <1 second for 4K images  
**Constraints**: <300MB memory usage, <10% CPU when idle, <2 second cold start  
**Scale/Scope**: Single-user desktop tool, one image at a time, images up to 4K (3840x2160), 5 core features + 1 stretch goal

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Personal Project Confirmation**: ✅ Confirmed as personal project (user confirmed using Ken's Personal Constitution)

**II. Test-Driven Development (TDD)**: 
- [x] Tests written first for all functionality (pytest + pytest-qt test suites per user story)
- [x] Red-Green-Refactor cycle enforced (tests fail first, then implementation, then refactor)
- [x] Contract tests planned for public interfaces (ImageEditor class, file I/O operations)
- [x] Unit tests planned for business logic (crop, resize, revert operations)

**III. Code Quality Standards**:
- [x] Language-specific formatter configured (ruff format for Python)
- [x] Linter configured with zero-error policy (ruff check)
- [x] Type system leveraged (Python type hints for all function signatures)
- [x] Documentation requirements defined (docstrings for all classes/public methods, README with examples)
- [x] Pre-commit hooks planned (format → lint → test pipeline via Invoke-Build task)

**IV. User Experience Consistency**:
- [x] Interface patterns defined (Qt standard patterns: menu bar, toolbar, keyboard shortcuts Ctrl-V/S/Z, status bar)
- [x] Error message strategy defined (QMessageBox dialogs with clear explanations and suggested actions)
- [x] Documentation plan includes quick-start, examples, API reference (quickstart.md, README, inline help)
- [x] Help/guidance mechanisms specified (tooltips on toolbar, Help menu, status bar dimension display)
- [x] Accessibility considerations addressed (full keyboard navigation, Tab order, focus indicators, Qt accessibility API)

**V. Performance Requirements**:
- [x] Response time targets defined (<100ms UI interactions, <1s crop/resize for 4K images)
- [x] Throughput targets defined (N/A for single-user desktop application)
- [x] Resource constraints specified (<300MB memory, <10% CPU idle, <2s cold start)
- [x] Scalability approach documented (single-threaded sufficient, one image at a time)
- [x] Performance monitoring/instrumentation planned (log file for errors/warnings, track operations >500ms)

**Development Workflow Compliance**:
- [x] Stage/phase commit strategy defined (commit after plan, after each user story, after refactorings)
- [x] Pre-commit checks automated (Invoke-Build task: format → lint → test)
- [x] Phase transition checklist understood and agreed (scan for consistency, run full tests)
- [x] Language-specific tooling confirmed (Python: uv for deps, ruff format/check, pytest)

**Complexity Justification**: None - all constitutional requirements can be met without exceptions.

---

**Post-Phase 1 Re-evaluation** (2026-01-10):

All constitutional requirements remain satisfied after design phase:
- ✅ TDD workflow detailed in quickstart.md with contract tests specified
- ✅ Code quality tooling (ruff format/check) configured in research.md
- ✅ UX patterns (Qt standard widgets, keyboard shortcuts) defined in data model and contracts
- ✅ Performance targets achievable with PySide6 + Pillow (validated in research.md)
- ✅ All contracts specify clear preconditions, postconditions, and error handling

**No design changes required**. Ready for Phase 2 (task breakdown via `/speckit.tasks`).

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # Application entry point
├── ui/
│   ├── main_window.py   # Main window and layout
│   ├── widgets/         # Custom widgets (image viewer, crop selector)
│   └── dialogs/         # Resize dialog, error dialogs
├── core/
│   ├── image_editor.py  # Core editing logic (crop, resize, revert)
│   ├── clipboard.py     # Clipboard operations
│   └── file_ops.py      # File load/save operations
├── models/
│   ├── image_model.py   # Image entity and edit history
│   └── selection.py     # Selection/crop region model
└── utils/
    ├── validators.py    # Input validation
    └── logger.py        # Logging configuration

tests/
├── unit/
│   ├── test_image_editor.py
│   ├── test_file_ops.py
│   └── test_validators.py
├── integration/
│   ├── test_clipboard.py
│   └── test_ui_workflows.py
└── contract/
    └── test_image_editor_contract.py

docs/
└── screenshots/         # Example screenshots for README

pyproject.toml          # uv project config, dependencies
README.md               # Quick-start guide
.tasks.build.ps1        # Invoke-Build tasks (format, lint, test)
```

**Structure Decision**: Single desktop application using standard Python src/ layout. UI layer (PySide6 widgets) separated from core logic (image operations) for testability. Models hold state, core/ handles operations, ui/ handles presentation. Tests organized by type (unit/integration/contract) per TDD requirements.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
