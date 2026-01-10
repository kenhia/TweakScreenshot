<!--
===============================================================================
SYNC IMPACT REPORT - Constitution Update
===============================================================================
Version Change: INITIAL → 1.0.0
Date: 2026-01-10

NEW PRINCIPLES:
  I.   Personal Project Confirmation - Prevents accidental use on work projects
  II.  Test-Driven Development (TDD) - Mandatory red-green-refactor cycle
  III. Code Quality Standards - Automated formatting and linting requirements
  IV.  User Experience Consistency - Interface, accessibility, and documentation
  V.   Performance Requirements - Defined targets, monitoring, and optimization

NEW SECTIONS:
  - Development Workflow: Stage/phase commits, pre-commit checks, phase transitions
  - Language-Specific Tooling: Python (uv, ruff), PowerShell (Invoke-Build, pester, VS Code)
  - Governance: Versioning policy, compliance validation, amendment procedures

TEMPLATE UPDATES:
  ✅ plan-template.md - Constitution Check section updated with 5 principles
  ✅ spec-template.md - Performance requirements and UX standards added
  ✅ tasks-template.md - Pre-commit and testing task types updated

FOLLOW-UP ACTIONS:
  - For new languages: Prompt user to define tooling and update this constitution
  - All projects must confirm "Ken's Personal Constitution" before planning phase

===============================================================================
-->

# Ken's Personal Constitution

## Core Principles

### I. Personal Project Confirmation (NON-NEGOTIABLE)

**Prior to starting the planning phase, the agent MUST explicitly confirm with the user**:
*"This project will use Ken's Personal Constitution. Is this a personal project (not a work/client project)?"*

**Rationale**: This prevents accidental application of personal workflows, tooling choices, and quality standards to professional/client work that may have different requirements or constraints.

### II. Test-Driven Development (TDD) (NON-NEGOTIABLE)

**All code MUST follow strict TDD discipline**:
- Tests written FIRST → User reviews and approves test scenarios → Tests MUST fail initially → Then implement → Tests pass
- Red-Green-Refactor cycle strictly enforced: Write failing test (Red) → Make it pass (Green) → Improve code quality (Refactor)
- No implementation code written before corresponding tests exist
- Contract tests for all public interfaces and integration points
- Unit tests for all business logic and data transformations

**Rationale**: TDD ensures requirements are testable, catches regressions early, enables confident refactoring, and serves as living documentation of system behavior.

### III. Code Quality Standards (NON-NEGOTIABLE)

**All code MUST meet automated quality gates before commit**:
- Formatting: Code automatically formatted to project standards (language-specific, see Tooling section)
- Linting: Zero linting errors allowed; warnings must be justified or fixed
- Type safety: Leverage type systems where available (Python type hints, TypeScript, etc.)
- Complexity: Functions/methods kept simple; complex logic requires justification and documentation
- Documentation: Public interfaces documented with purpose, parameters, return values, and examples

**Rationale**: Automated quality standards eliminate bike-shedding, maintain consistency across the codebase, reduce cognitive load during code review, and prevent quality erosion over time.

### IV. User Experience Consistency

**All user-facing functionality MUST provide consistent, intuitive experiences**:
- Interface patterns: Consistent command structures, argument naming, output formats
- Error messages: Clear, actionable, with suggested remediation steps
- Documentation: Every feature has quick-start guide, examples, and API reference
- Accessibility: Consider keyboard navigation, screen readers, color contrast where applicable
- Help text: `--help` for CLIs, tooltips for UIs, inline guidance for complex workflows

**Rationale**: Consistent UX reduces learning curve, minimizes support burden, increases adoption, and demonstrates respect for users' time and cognitive capacity.

### V. Performance Requirements

**All implementations MUST define and meet measurable performance targets**:
- Response time: Define acceptable latency (e.g., <200ms for UI interactions, <1s for API calls)
- Throughput: Define capacity targets where applicable (e.g., requests/second, records/minute)
- Resource usage: Define memory and CPU constraints (especially for background processes)
- Scalability: Identify bottlenecks and document scaling strategy for growth
- Monitoring: Instrument performance-critical paths with logging and metrics

**Rationale**: Defining performance expectations upfront prevents "works on my machine" surprises, guides architectural decisions, and ensures the system remains responsive as it grows.

## Development Workflow

### Stage and Phase Commits

**All projects MUST commit at each stage/phase boundary**:
- After specification (spec.md)
- After implementation plan (plan.md, research.md, data-model.md)
- After task breakdown (tasks.md)
- After each user story implementation
- After each major refactoring or architectural change

**Purpose**: Provides historical perspective, enables rollback to known-good states, supports incremental review, and creates natural checkpoints for feedback.

### Pre-Commit Checks (GATE)

**Before ANY commit that includes code changes, the following MUST pass**:
1. **Format code**: Apply language-specific formatter (see Tooling section)
2. **Lint code**: Run language-specific linter, address all errors and unjustified warnings
3. **Run all unit tests**: Full test suite must pass; no skipped tests without documented reason
4. **Validate build**: Project builds/compiles successfully if applicable

**Automated enforcement**: Set up pre-commit hooks where possible; agent must validate manually otherwise.

### Phase Transition Checks (GATE)

**Before transitioning from one phase to the next (e.g., planning → implementation, US1 → US2), perform consistency scan**:
- Verify all tasks in current phase marked complete
- Ensure documentation updated (spec, plan, data-model, contracts)
- Check cross-references (e.g., task IDs mentioned in commits, spec requirements covered in plan)
- Confirm no TODO comments or NEEDS CLARIFICATION markers remain unresolved
- Run full test suite and quality checks

## Language-Specific Tooling

### Python Projects

**Dependency Management**: Use `uv` for all package management and virtual environment operations.

**Formatting**: Use `ruff format` for code formatting.
- Configuration: Define in `pyproject.toml` or `ruff.toml`
- Scope: Apply to all `.py` files including tests

**Linting**: Use `ruff check` for linting.
- Configuration: Define rules in `pyproject.toml` or `ruff.toml`
- Target: Zero errors; warnings require justification or fix

**Testing**: Use `pytest` (or equivalent approved by user).
- Structure: `tests/` directory with `unit/`, `integration/`, `contract/` subdirectories
- Coverage: Track with pytest-cov; aim for >80% on business logic

**Type Checking**: Use `mypy` or Pyright for static type checking (if types used).

### PowerShell Projects

**Build System**: Use `Invoke-Build` for build automation, task running, and CI/CD workflows.

**Formatting**: Use VS Code's PowerShell extension formatter.
- Settings: Configure via `.vscode/settings.json` to ensure consistent team/agent formatting
- Scope: Apply to all `.ps1`, `.psm1`, `.psd1` files

**Linting**: Use PSScriptAnalyzer via PowerShell extension.
- Configuration: Define rules in `PSScriptAnalyzerSettings.psd1`
- Target: Zero errors; warnings require justification or fix

**Testing**: Use `Pester` (v5+) for unit and integration testing.
- Structure: `tests/` directory, files named `*.Tests.ps1`
- Coverage: Use Pester code coverage reports; aim for >80% on functions

### New Languages

**When introducing a language not yet specified in this constitution**:
1. Agent MUST pause and prompt user: *"This project uses [LANGUAGE]. What tooling should we use for formatting, linting, and testing?"*
2. User provides tooling choices
3. Agent MUST update this constitution document with new Language-Specific Tooling section
4. Increment constitution version (MINOR bump for new language addition)
5. Proceed with project using newly defined tooling

## Governance

### Constitution Authority

This constitution is **NON-NEGOTIABLE** and supersedes all other practices, preferences, or defaults.

**Compliance verification**:
- Every plan MUST include Constitution Check section mapping principles to implementation approach
- Every code review validates adherence to Code Quality Standards and TDD principles
- Every phase transition check validates workflow compliance

**Justified exceptions**:
- Exceptions to principles require explicit documentation in plan's "Complexity Tracking" section
- Justification must include: which principle, why exception needed, mitigation strategy, approval status

### Amendment Procedure

**To update this constitution**:
1. Identify principle or section requiring change
2. Draft amendment with rationale and impact analysis
3. Use `/speckit.constitution` command to update constitution and propagate changes to templates
4. Version bump follows semantic versioning (MAJOR/MINOR/PATCH based on change scope)
5. Document change in Sync Impact Report (auto-generated by constitution command)

### Versioning Policy

**MAJOR** (X.0.0): Backward incompatible change - principle removed, redefined, or workflow fundamentally altered.
**MINOR** (X.Y.0): New principle added, new tooling section, or materially expanded guidance.
**PATCH** (X.Y.Z): Clarifications, typo fixes, wording improvements, non-semantic refinements.

**Version**: 1.0.0 | **Ratified**: 2026-01-10 | **Last Amended**: 2026-01-10
