# Contributing to Semaphore Action

Thank you for considering contributing to semaphore-action! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branching Strategy](#branching-strategy)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)
- [Testing](#testing)

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive environment.

## Getting Started

### Prerequisites

- Python 3.11 or 3.12
- Docker (for local testing)
- Git

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/gulbinas/semaphore-action.git
cd semaphore-action

# Set up development environment
make dev-setup

# Or manually:
make venv
make install-dev
```

### Running Tests

```bash
# Run basic tests
make test-basic

# Run all tests
make test-all

# Run tests with coverage
make test-coverage

# Run linting
make lint

# Run all checks
make check
```

## Development Workflow

We use a **Git Flow** inspired branching model:

1. **main** - Production-ready code, triggers releases
2. **develop** - Integration branch for features
3. **feature/** - New features and enhancements
4. **fix/** - Bug fixes
5. **hotfix/** - Urgent fixes for production

### Creating a New Feature

```bash
# Start from develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/my-awesome-feature

# Make changes
# ... edit files ...

# Run tests
make test

# Commit changes
git add .
git commit -m "feat: Add awesome feature"

# Push and create PR
git push origin feature/my-awesome-feature
```

Then create a Pull Request targeting the `develop` branch.

## Branching Strategy

### Branch Types

- **feature/*** - New features (from develop, merge to develop)
- **fix/*** - Bug fixes (from develop, merge to develop)
- **docs/*** - Documentation updates (from develop, merge to develop)
- **hotfix/*** - Critical fixes (from main, merge to main then develop)

### Branch Lifetime

- **main** - Permanent
- **develop** - Permanent
- **feature/fix/docs** - Delete after merge
- **hotfix** - Delete after merge to both main and develop

## Commit Messages

We follow a semantic commit message format:

### Format

```
<type>: <subject>

[optional body]

[optional footer]
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting, etc.)
- **refactor:** Code refactoring
- **test:** Adding or updating tests
- **chore:** Maintenance tasks

### Examples

```bash
# Feature
git commit -m "feat: Add retry mechanism for failed API calls"

# Bug fix
git commit -m "fix: Resolve timeout issue in websocket connection"

# Documentation
git commit -m "docs: Update README with new usage examples"

# Breaking change (triggers major version)
git commit -m "[major] Remove deprecated legacy authentication method"
```

### Version Impact

Commit messages affect automatic versioning:

- `[major]` or `breaking change` → Major version bump (v1.x.x → v2.0.0)
- `feat:` or `[minor]` → Minor version bump (v1.2.x → v1.3.0)
- Other commits → Patch version bump (v1.2.3 → v1.2.4)

## Pull Request Process

### Creating a Pull Request

1. **Target branch**: PRs should target `develop` (not `main`)
2. **Title**: Use semantic format (e.g., "feat: Add new feature")
3. **Description**: Explain what and why
4. **Tests**: Ensure all tests pass
5. **Review**: Wait for review from maintainers

### PR Checklist

- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts

### Review Process

1. Automated CI checks run on your PR
2. Maintainer reviews code
3. Address any feedback
4. Once approved, PR is merged to develop

## Release Process

### For Contributors

You don't need to worry about releases! They happen automatically when:

1. Your feature is merged to `develop`
2. A maintainer creates a release PR from `develop` to `main`
3. The release PR is merged

### For Maintainers

#### Option 1: Using GitHub Actions (Recommended)

1. Go to **Actions** → **Create Release PR**
2. Click **Run workflow**
3. Select version bump type (patch/minor/major)
4. Review the created PR
5. Merge to trigger automatic release

#### Option 2: Manual Release PR

1. Create PR from `develop` to `main`
2. Ensure title indicates version bump type
3. Merge PR to trigger release workflow

### What Happens on Release

When a PR is merged to `main`:

1. Release workflow runs automatically
2. New version tag is created (e.g., `v1.2.3`)
3. Major version tag is updated (e.g., `v1`)
4. GitHub Release is created with changelog
5. Users can now reference the new version

## Testing

### Test Types

1. **Unit Tests** - Test individual components
2. **Integration Tests** - Test action in GitHub Actions environment
3. **Docker Tests** - Test containerized action

### Running Tests Locally

```bash
# Basic unit tests
make test-basic

# All unit tests
make test

# Integration test (via Docker)
make docker-test

# All checks (tests + lint + security)
make check
```

### Writing Tests

- Place tests in files matching `test_*.py`
- Use pytest fixtures and assertions
- Mock external dependencies
- Test both success and failure cases

Example:

```python
def test_my_feature():
    """Test that my feature works correctly."""
    result = my_feature()
    assert result == expected_value
```

## Code Style

### Python Style

- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 120 characters
- Use descriptive variable names

### Formatting

```bash
# Auto-format code
make format

# Check linting
make lint
```

## Documentation

Update documentation when:

- Adding new features
- Changing existing behavior
- Fixing significant bugs
- Updating dependencies

### Documentation Files

- **README.md** - User-facing documentation
- **RELEASE_STRATEGY.md** - Release process details
- **QUICK_START.md** - Quick reference guide
- **CONTRIBUTING.md** - This file

## Getting Help

- Check existing [Issues](https://github.com/gulbinas/semaphore-action/issues)
- Review [Discussions](https://github.com/gulbinas/semaphore-action/discussions)
- Read [RELEASE_STRATEGY.md](RELEASE_STRATEGY.md) for release details
- Ask questions in a new issue

## Recognition

Contributors are recognized in:

- GitHub contributors list
- Release notes (for significant contributions)
- Special thanks section (for major contributions)

Thank you for contributing! 🎉
