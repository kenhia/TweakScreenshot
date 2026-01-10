# Invoke-Build tasks for TweakScreenshot
# Usage: Invoke-Build <TaskName>

# Default task runs format, lint, and test
task . Format, Lint, Test

# Format all Python code with ruff
task Format {
    exec { uv run ruff format src/ tests/ }
}

# Lint all Python code with ruff
task Lint {
    exec { uv run ruff check src/ tests/ }
}

# Run all tests with pytest
task Test {
    exec { uv run pytest }
}

# Run tests with coverage report
task Coverage {
    exec { uv run pytest --cov=src --cov-report=html --cov-report=term }
}

# Pre-commit validation: format -> lint -> test
task PreCommit Format, Lint, Test

# Clean build artifacts
task Clean {
    Remove-Item -Path "build", "dist", "*.egg-info", ".pytest_cache", "htmlcov", ".coverage" -Recurse -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Include "__pycache__", "*.pyc" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue
}
