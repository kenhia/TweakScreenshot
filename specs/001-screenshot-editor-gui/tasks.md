# Tasks: Screenshot Editor GUI

**Branch**: `001-screenshot-editor-gui` | **Date**: 2026-01-10  
**Input**: Design documents from `specs/001-screenshot-editor-gui/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Task Format

Each task follows: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Parallelizable (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label (US1, US2, etc.) - used for user story phases only
- **File paths**: Exact paths included in descriptions

## Implementation Strategy

**MVP Focus**: User Stories 1 and 5 (Load/Display + Save) deliver immediate value  
**Incremental Delivery**: Each user story can be completed independently  
**TDD Discipline**: Tests written first (RED), then implementation (GREEN), then refactor  
**Pre-commit Gates**: format → lint → tests before each stage commit

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, tooling, and basic structure

- [X] T001 Create project structure per plan.md (src/ui/, src/core/, src/models/, src/utils/, tests/)
- [X] T002 Initialize Python project with uv in pyproject.toml (dependencies: PySide6, Pillow, pytest, pytest-qt)
- [X] T003 [P] Configure ruff for formatting and linting in pyproject.toml
- [X] T004 [P] Create Invoke-Build tasks file .tasks.build.ps1 (format, lint, test commands)
- [X] T005 [P] Setup pytest configuration in pyproject.toml (test paths, markers)
- [X] T006 [P] Create pre-commit validation script .specify/scripts/powershell/pre-commit-check.ps1
- [X] T007 Create README.md with quick-start guide (install, run, test)
- [X] T008 **Stage Commit**: "chore(setup): initialize Python project with PySide6, Pillow, pytest"

**Constitution Compliance**: Establishes Code Quality Standards (Principle III) infrastructure per constitution.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure REQUIRED before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Create base Image model in src/models/image_model.py (original_data, current_data, validation)
- [ ] T010 [P] Create EditHistory model in src/models/edit_history.py (operations stack, add_operation, clear methods)
- [ ] T011 [P] Create utility validators in src/utils/validators.py (image dimensions, file paths, format validation)
- [ ] T012 [P] Create logger configuration in src/utils/logger.py (file logging per Constitution V)
- [ ] T013 [P] Setup error handling utilities in src/utils/error_handlers.py (QMessageBox wrappers per Constitution IV)
- [ ] T014 Create main window skeleton in src/ui/main_window.py (QMainWindow, menu bar, status bar)
- [ ] T015 Run format → lint → unit tests for foundation code
- [ ] T016 **Stage Commit**: "chore(foundation): add base models, utilities, main window skeleton"

**Constitution Compliance**: Foundation includes UX error patterns (Principle IV) and performance logging (Principle V).

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Load and Display Screenshot (Priority: P1) 🎯 MVP

**Goal**: Users can load screenshots from file or clipboard (Ctrl-V) and see them displayed in the application

**Independent Test**: Copy image to clipboard, press Ctrl-V in app, verify image appears. Or use File > Open to load image file.

### Tests for US1 (MANDATORY per Constitution II: TDD) ✅

> **TDD Workflow**: Write test → Verify test FAILS (RED) → Implement → Test PASSES (GREEN) → Refactor

- [ ] T017 [P] [US1] Write contract test for ImageEditor.load_from_file() in tests/contract/test_image_editor_contract.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T018 [P] [US1] Write contract test for ImageEditor.load_from_clipboard() in tests/contract/test_image_editor_contract.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T019 [P] [US1] Write unit test for file_ops.load_image_from_file() in tests/unit/test_file_ops.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T020 [P] [US1] Write unit test for clipboard.load_image_from_clipboard() in tests/unit/test_clipboard.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T021 [P] [US1] Write integration test for "Load from file workflow" in tests/integration/test_ui_workflows.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T022 [P] [US1] Write integration test for "Paste from clipboard workflow" in tests/integration/test_ui_workflows.py
  - **TDD Gate**: Test MUST fail before implementation

**Checkpoint - RED**: All US1 tests written and FAILING. Ready for implementation.

### Implementation for US1

- [ ] T023 [P] [US1] Implement load_image_from_file() in src/core/file_ops.py (uses Pillow, validates format, handles errors)
- [ ] T024 [P] [US1] Implement load_image_from_clipboard() in src/core/clipboard.py (QClipboard to PIL, format conversion)
- [ ] T025 [US1] Implement ImageEditor.load_from_file() in src/core/image_editor.py (calls file_ops, updates Image model)
- [ ] T026 [US1] Implement ImageEditor.load_from_clipboard() in src/core/image_editor.py (calls clipboard, updates Image model)
- [ ] T027 [P] [US1] Create ImageViewer widget in src/ui/widgets/image_viewer.py (QLabel with QScrollArea, DPI-aware display)
- [ ] T028 [US1] Integrate File > Open menu action in src/ui/main_window.py (QFileDialog, call ImageEditor.load_from_file)
- [ ] T029 [US1] Integrate Ctrl-V paste action in src/ui/main_window.py (keyPressEvent, call ImageEditor.load_from_clipboard)
- [ ] T030 [US1] Add error dialogs for invalid files and empty clipboard (Constitution IV: clear error messages)
- [ ] T031 [US1] Add status bar updates showing image dimensions (Constitution IV: help mechanisms)
- [ ] T032 [US1] Add logging for load operations >500ms (Constitution V: performance monitoring)

**Checkpoint - GREEN**: All US1 tests now PASSING. Implementation complete.

### Code Quality & Refactor for US1

- [ ] T033 [US1] Run pre-commit checks: ruff format → ruff check → pytest (Constitution III)
- [ ] T034 [US1] Refactor for clarity if needed (DRY principle, extract common patterns)
- [ ] T035 [US1] Add docstrings to all public methods (Constitution IV: documentation)
- [ ] T036 [US1] **Stage Commit**: "feat(US1): implement load and display screenshot from file/clipboard"

**Final Checkpoint**: US1 fully functional, tested, documented, and committed. Ready for next story.

---

## Phase 4: User Story 5 - Save Edited Screenshot (Priority: P1) 🎯 MVP

**Goal**: Users can save their edited (or unedited) screenshot to disk in PNG or JPG format

**Independent Test**: Load an image, click File > Save As, choose location and format, verify file created and valid.

**Phase Transition Gate**: US1 must be complete (all tests pass, code committed) before starting US5.

### Tests for US5 (MANDATORY per Constitution II: TDD) ✅

- [ ] T037 [P] [US5] Write contract test for ImageEditor.save_to_file() in tests/contract/test_image_editor_contract.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T038 [P] [US5] Write unit test for file_ops.save_image_to_file() in tests/unit/test_file_ops.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T039 [P] [US5] Write unit test for file_ops.check_disk_space() in tests/unit/test_file_ops.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T040 [P] [US5] Write integration test for "Save workflow with PNG format" in tests/integration/test_ui_workflows.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T041 [P] [US5] Write integration test for "Save workflow with JPG format" in tests/integration/test_ui_workflows.py
  - **TDD Gate**: Test MUST fail before implementation

**Checkpoint - RED**: All US5 tests written and FAILING.

### Implementation for US5

- [ ] T042 [P] [US5] Implement save_image_to_file() in src/core/file_ops.py (PIL save, format selection, quality for JPG)
- [ ] T043 [P] [US5] Implement check_disk_space() in src/core/file_ops.py (estimate file size, validate space)
- [ ] T044 [P] [US5] Implement estimate_file_size() in src/core/file_ops.py (approximate based on dimensions/format)
- [ ] T045 [US5] Implement ImageEditor.save_to_file() in src/core/image_editor.py (calls file_ops, clears unsaved flag)
- [ ] T046 [US5] Integrate File > Save As menu action in src/ui/main_window.py (QFileDialog with format filter)
- [ ] T047 [US5] Add overwrite confirmation dialog (Constitution IV: UX consistency)
- [ ] T048 [US5] Add disk space check before save with error dialog (edge case handling)
- [ ] T049 [US5] Add JPG quality selection dialog (default 90%)
- [ ] T050 [US5] Add logging for save operations (Constitution V: monitoring)

**Checkpoint - GREEN**: All US5 tests PASSING. US1 + US5 = functional MVP.

### Code Quality & Refactor for US5

- [ ] T051 [US5] Run pre-commit checks: ruff format → ruff check → pytest
- [ ] T052 [US5] Refactor file_ops module if needed (common error handling patterns)
- [ ] T053 [US5] Add docstrings and update README with save examples
- [ ] T054 [US5] **Stage Commit**: "feat(US5): implement save screenshot to PNG/JPG with disk space check"

**MVP Milestone**: Application can now load, display, and save screenshots - delivers immediate value!

---

## Phase 5: User Story 2 - Crop Screenshot (Priority: P2)

**Goal**: Users can select a rectangular region with mouse drag and crop image to that selection

**Independent Test**: Load image, drag selection rectangle, click Crop button, verify only selected area remains.

**Dependencies**: US1 complete (need image loaded and displayed)

### Tests for US2 (MANDATORY per Constitution II: TDD) ✅

- [ ] T055 [P] [US2] Write contract test for ImageEditor.crop() in tests/contract/test_image_editor_contract.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T056 [P] [US2] Write unit test for Selection model validation in tests/unit/test_selection.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T057 [P] [US2] Write integration test for "Crop workflow" in tests/integration/test_ui_workflows.py
  - **TDD Gate**: Test MUST fail before implementation

**Checkpoint - RED**: All US2 tests written and FAILING.

### Implementation for US2

- [ ] T058 [US2] Create Selection model in src/models/selection.py (x, y, width, height, validation, bounds checking)
- [ ] T059 [US2] Implement ImageEditor.crop() in src/core/image_editor.py (PIL crop, update current_data, add to history)
- [ ] T060 [US2] Create CropSelector widget in src/ui/widgets/crop_selector.py (mouse drag selection overlay)
- [ ] T061 [US2] Integrate CropSelector into ImageViewer in src/ui/widgets/image_viewer.py
- [ ] T062 [US2] Add Edit > Crop menu action and toolbar button in src/ui/main_window.py
- [ ] T063 [US2] Add selection cancellation (Escape key, click outside)
- [ ] T064 [US2] Add selection bounds snapping to image edges
- [ ] T065 [US2] Update EditHistory when crop applied
- [ ] T066 [US2] Add logging for crop operations (Constitution V)

**Checkpoint - GREEN**: All US2 tests PASSING. Crop functionality complete.

### Code Quality & Refactor for US2

- [ ] T067 [US2] Run pre-commit checks: ruff format → ruff check → pytest
- [ ] T068 [US2] Refactor CropSelector if needed (simplify mouse event handling)
- [ ] T069 [US2] Add docstrings and update README with crop examples
- [ ] T070 [US2] **Stage Commit**: "feat(US2): implement crop screenshot with mouse selection"

---

## Phase 6: User Story 4 - Revert Edits (Priority: P2)

**Goal**: Users can restore the original unedited image with a single action

**Independent Test**: Load image, perform any edit (crop/resize), click Edit > Revert, verify original restored.

**Dependencies**: US2 complete (need edits to revert from)

### Tests for US4 (MANDATORY per Constitution II: TDD) ✅

- [ ] T071 [P] [US4] Write contract test for ImageEditor.revert() in tests/contract/test_image_editor_contract.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T072 [P] [US4] Write integration test for "Revert after crop" in tests/integration/test_ui_workflows.py
  - **TDD Gate**: Test MUST fail before implementation

**Checkpoint - RED**: All US4 tests written and FAILING.

### Implementation for US4

- [ ] T073 [US4] Implement ImageEditor.revert() in src/core/image_editor.py (copy original_data to current_data, clear history)
- [ ] T074 [US4] Add Edit > Revert menu action in src/ui/main_window.py (enable only when has_unsaved_changes)
- [ ] T075 [US4] Add Ctrl-R keyboard shortcut for revert
- [ ] T076 [US4] Update status bar after revert
- [ ] T077 [US4] Add logging for revert operations

**Checkpoint - GREEN**: All US4 tests PASSING. Revert complete.

### Code Quality & Refactor for US4

- [ ] T078 [US4] Run pre-commit checks: ruff format → ruff check → pytest
- [ ] T079 [US4] Add docstrings and update README
- [ ] T080 [US4] **Stage Commit**: "feat(US4): implement revert to original image"

---

## Phase 7: User Story 3 - Resize Screenshot (Priority: P3)

**Goal**: Users can resize image by specifying dimensions (width/height) or percentage scale

**Independent Test**: Load image, open Edit > Resize dialog, enter "800" for width, apply, verify dimensions changed.

**Dependencies**: US1 complete

### Tests for US3 (MANDATORY per Constitution II: TDD) ✅

- [ ] T081 [P] [US3] Write contract test for ImageEditor.resize() in tests/contract/test_image_editor_contract.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T082 [P] [US3] Write unit test for resize input validation in tests/unit/test_validators.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T083 [P] [US3] Write integration test for "Resize with proportional width" in tests/integration/test_ui_workflows.py
  - **TDD Gate**: Test MUST fail before implementation
- [ ] T084 [P] [US3] Write integration test for "Resize with percentage" in tests/integration/test_ui_workflows.py
  - **TDD Gate**: Test MUST fail before implementation

**Checkpoint - RED**: All US3 tests written and FAILING.

### Implementation for US3

- [ ] T085 [US3] Implement ImageEditor.resize() in src/core/image_editor.py (PIL resize with LANCZOS filter, update current_data, add to history)
- [ ] T086 [US3] Create ResizeDialog in src/ui/dialogs/resize_dialog.py (width/height inputs, aspect ratio lock, percentage mode)
- [ ] T087 [US3] Add resize input validation (positive integers, extreme dimension warnings per edge cases)
- [ ] T088 [US3] Add Edit > Resize menu action in src/ui/main_window.py (open dialog, call ImageEditor.resize)
- [ ] T089 [US3] Add warning dialog for extreme dimensions (<50px or >10000px) with override option
- [ ] T090 [US3] Update status bar with new dimensions after resize
- [ ] T091 [US3] Add logging for resize operations (Constitution V)

**Checkpoint - GREEN**: All US3 tests PASSING. Resize complete.

### Code Quality & Refactor for US3

- [ ] T092 [US3] Run pre-commit checks: ruff format → ruff check → pytest
- [ ] T093 [US3] Refactor ResizeDialog if needed (simplify aspect ratio logic)
- [ ] T094 [US3] Add docstrings and update README with resize examples
- [ ] T095 [US3] **Stage Commit**: "feat(US3): implement resize with dimensions/percentage and extreme size warnings"

---

## Phase 8: User Story 6 - Image Markup (Priority: P4 - Stretch Goal)

**Goal**: Users can add text, boxes, and arrows to screenshots for instructional documentation

**Independent Test**: Load image, click "Add Text", type text, verify appears. Click "Add Arrow", drag between points, verify arrow appears.

**Dependencies**: US1 complete. Note: This is a STRETCH GOAL - only implement if time permits.

### Tests for US6 (OPTIONAL - Stretch Goal)

- [ ] T096 [P] [US6] Write unit test for MarkupElement model in tests/unit/test_markup_element.py
- [ ] T097 [P] [US6] Write integration test for "Add text markup" in tests/integration/test_ui_workflows.py
- [ ] T098 [P] [US6] Write integration test for "Add arrow markup" in tests/integration/test_ui_workflows.py

### Implementation for US6

- [ ] T099 [US6] Create MarkupElement model in src/models/markup_element.py (type, position, content, style)
- [ ] T100 [P] [US6] Create TextTool widget in src/ui/widgets/text_tool.py (click to place, editable text box)
- [ ] T101 [P] [US6] Create ArrowTool widget in src/ui/widgets/arrow_tool.py (drag from point A to B)
- [ ] T102 [P] [US6] Create BoxTool widget in src/ui/widgets/box_tool.py (drag rectangle outline)
- [ ] T103 [US6] Integrate markup tools into main_window toolbar
- [ ] T104 [US6] Implement markup rendering on ImageViewer
- [ ] T105 [US6] Implement markup selection/move/delete functionality
- [ ] T106 [US6] Flatten markup into image on save (PIL draw operations)
- [ ] T107 [US6] Add logging for markup operations

### Code Quality & Refactor for US6

- [ ] T108 [US6] Run pre-commit checks: ruff format → ruff check → pytest
- [ ] T109 [US6] Refactor markup tools for consistency
- [ ] T110 [US6] Add docstrings and update README with markup examples
- [ ] T111 [US6] **Stage Commit**: "feat(US6): implement image markup with text, arrows, boxes (stretch goal)"

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [ ] T112 [P] Add large image warning dialog (>10MB, >10000px) per edge cases in spec.md
- [ ] T113 [P] Add paste-over confirmation dialog (unsaved changes warning) per edge cases
- [ ] T114 [P] Implement DPI awareness for Windows per edge cases (Qt::AA_EnableHighDpiScaling)
- [ ] T115 [P] Add application icon and window title
- [ ] T116 [P] Create Help > About dialog with version info
- [ ] T117 [P] Add Help > User Guide menu item (opens README in browser)
- [ ] T118 [P] Add tooltips to all toolbar buttons (Constitution IV: help mechanisms)
- [ ] T119 [P] Create screenshots for README in docs/screenshots/
- [ ] T120 Performance optimization: Profile crop/resize for 4K images, ensure <1s (Constitution V)
- [ ] T121 Memory profiling: Verify <300MB usage for 4K images (Constitution V)
- [ ] T122 Cold start optimization: Ensure <2s startup time (Constitution V)
- [ ] T123 Run full quickstart.md validation (install, run, test all user stories)
- [ ] T124 Run format → lint → full test suite as final gate
- [ ] T125 **Stage Commit**: "polish: add edge case handling, help system, performance optimization"

---

## Dependencies & Execution Order

### Phase Dependencies (Critical Path)

```text
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← BLOCKS all user stories
    ↓
    ├─→ Phase 3 (US1) ──→ Phase 4 (US5) ← MVP milestone
    │       ↓
    │   Phase 5 (US2) ──→ Phase 6 (US4)
    │       ↓
    │   Phase 7 (US3)
    │       ↓
    │   Phase 8 (US6 - Stretch)
    ↓
Phase 9 (Polish)
```

### User Story Independence

- **US1 (Load/Display)**: No dependencies - can start after Foundation
- **US5 (Save)**: Depends on US1 (need image loaded)
- **US2 (Crop)**: Depends on US1 (need image displayed)
- **US4 (Revert)**: Depends on US2 or US3 (need edits to revert)
- **US3 (Resize)**: Depends on US1 (need image loaded)
- **US6 (Markup)**: Depends on US1 (need image loaded), stretch goal

### Parallel Execution Opportunities

**Within Setup (Phase 1)**:
- T003 (ruff config) ∥ T004 (Invoke-Build) ∥ T005 (pytest config) ∥ T006 (pre-commit script) ∥ T007 (README)

**Within Foundation (Phase 2)**:
- T010 (EditHistory) ∥ T011 (validators) ∥ T012 (logger) ∥ T013 (error handlers)

**Within US1 Tests**:
- T017-T022 (all 6 test files) can be written in parallel

**Within US1 Implementation**:
- T023 (file_ops) ∥ T024 (clipboard) ∥ T027 (ImageViewer widget)

**Within US5 Tests**:
- T037-T041 (all 5 test files) can be written in parallel

**Within US5 Implementation**:
- T042 (save) ∥ T043 (check_disk_space) ∥ T044 (estimate_file_size)

**Within US2-US6**: Similar parallelization for tests and independent implementation tasks

**Within Polish (Phase 9)**:
- T112-T119 (all UI polish tasks) can run in parallel

### Recommended MVP Scope

**Minimum Viable Product** (delivers immediate value):
- Phase 1: Setup
- Phase 2: Foundational
- Phase 3: US1 (Load and Display) ← Essential
- Phase 4: US5 (Save) ← Essential

**Total MVP tasks**: ~54 tasks (T001-T054)  
**Estimated MVP effort**: 2-3 days with TDD discipline

**Post-MVP increments**:
- Increment 1: Add US2 (Crop) + US4 (Revert) for basic editing
- Increment 2: Add US3 (Resize) for dimension control
- Increment 3: Add US6 (Markup) if time permits (stretch goal)
- Increment 4: Phase 9 (Polish) for production quality

---

## Task Summary

**Total Tasks**: 125  
**Setup Tasks**: 8  
**Foundational Tasks**: 8  
**US1 (Load/Display) Tasks**: 20 (6 tests + 10 implementation + 4 quality)  
**US5 (Save) Tasks**: 18 (5 tests + 9 implementation + 4 quality)  
**US2 (Crop) Tasks**: 16 (3 tests + 9 implementation + 4 quality)  
**US4 (Revert) Tasks**: 10 (2 tests + 5 implementation + 3 quality)  
**US3 (Resize) Tasks**: 15 (4 tests + 7 implementation + 4 quality)  
**US6 (Markup - Stretch) Tasks**: 16 (3 tests + 8 implementation + 5 quality)  
**Polish Tasks**: 14

**Parallelization Potential**: ~45 tasks marked [P] can run concurrently (36% of all tasks)

**Constitution Compliance Verified**:
- ✅ TDD enforced: 23 test tasks written FIRST (RED phase explicit)
- ✅ Pre-commit gates: 8 quality checkpoints with format → lint → test
- ✅ Stage commits: 9 commit points after each phase completion
- ✅ UX consistency: Error dialogs, help text, tooltips per Principle IV
- ✅ Performance monitoring: Logging tasks for operations >500ms per Principle V

**Format Validation**: All 125 tasks follow `- [ ] [ID] [P?] [Story?] Description` format with exact file paths.
