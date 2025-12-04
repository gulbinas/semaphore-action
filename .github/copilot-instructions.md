# GitHub Copilot Instructions for Semaphore Action

## Project Overview

This is a Python-based GitHub Action that invokes Ansible Semaphore tasks via API calls and polls for results using WebSocket connections. The action is containerized using Docker and runs on GitHub Actions workflows.

**Stack:**
- Python 3.11+
- Docker (container-based action)
- WebSockets for real-time monitoring
- Semaphore API client library
- pytest for testing

## Build and Test Commands

### Environment Setup
```bash
make dev-setup    # Set up complete development environment (creates venv and installs all dependencies)
make venv         # Create virtual environment only
make install      # Install production dependencies only
make install-dev  # Install development dependencies
```

### Testing
```bash
make test         # Run main unit tests (12 tests, 84% coverage)
make test-basic   # Run basic tests only
make test-all     # Run all available tests
make test-coverage # Run tests with coverage report
make ci-test      # Run tests in CI format (XML coverage output)
```

### Code Quality
```bash
make lint         # Run flake8 linting
make format       # Format code with Black
make security     # Run security checks (bandit + safety)
make check        # Run all quality checks (test + lint + security)
```

### Docker
```bash
make docker-build # Build Docker image
make docker-test  # Test Docker functionality
```

### Development Workflow
```bash
make start        # Quick start: setup environment and run tests
make clean        # Remove build artifacts
make status       # Show environment status
make info         # Show project information
```

## Project Structure

```
semaphore-action/
├── main.py                           # Main GitHub Action logic (API calls and WebSocket handling)
├── action.yml                        # GitHub Action metadata and inputs/outputs
├── Dockerfile                        # Container definition for the action
├── requirements.txt                  # Production dependencies (semaphore_client, websockets)
├── requirements-dev.txt              # Development dependencies (pytest, flake8, bandit, etc.)
├── Makefile                          # Development automation and commands
├── .github/
│   └── workflows/
│       ├── pr-testing.yml           # Comprehensive PR testing workflow
│       ├── integration.yml          # Basic integration tests
│       └── python.yml               # Legacy linting workflow
├── test_*.py                        # Unit tests (12 tests, 84% coverage)
├── DEVELOPMENT.md                   # Detailed development guide
└── README.md                        # User-facing documentation
```

## Code Style and Conventions

### Python Style
- **Formatting:** Black code formatter (automatic formatting with `make format`)
- **Linting:** Flake8 for code quality checks
- **Line length:** 120 characters (Black default)
- **Imports:** Standard library first, then third-party, then local imports
- **Type hints:** Not strictly required but encouraged for public functions

### Testing Conventions
- Use pytest for all tests
- Mock external API calls and WebSocket connections
- Use real API response data from `test_data.py` for integration testing
- Aim for descriptive test names: `test_<component>_<scenario>_<expected_result>`
- Use pytest fixtures for common setup (see existing tests)
- Tests should be in files named `test_*.py`

### GitHub Action Patterns
- Read inputs from environment variables: `os.environ["INPUT_<NAME>"]`
- Write outputs using `set_github_action_output(name, value)` helper function
- Always write to `GITHUB_OUTPUT` file for action outputs
- Handle exceptions gracefully and provide clear error messages

### API and WebSocket Handling
- Use semaphore_client library for API interactions
- Configure API client with bearer token authentication
- Strip ANSI escape codes from WebSocket log output using `ansi_escape` regex
- Polls WebSocket for task updates until status is 'success' or 'error'
- Handle `ConnectionClosed` exceptions for WebSocket disconnections

## Security Best Practices

### Secrets and Credentials
- **NEVER** commit API keys or credentials
- All sensitive data must come from environment variables or GitHub secrets
- API keys are passed through GitHub Action inputs (`api_key`, `api_url`, etc.)

### Dependencies
- Run `make security` before committing to check for vulnerabilities
- Use Safety and Bandit for security scanning
- Keep dependencies updated but test thoroughly

### Code Security
- Validate all external inputs
- Handle API exceptions properly to avoid information leakage
- Use secure WebSocket connections when possible

## GitHub Actions Workflow

### PR Testing Pipeline
All PRs must pass the comprehensive testing workflow (`.github/workflows/pr-testing.yml`):

1. **Code Validation** - Basic tests, linting, environment setup
2. **Comprehensive Testing** - Multi-Python version testing (3.11, 3.12) with coverage
3. **Docker Testing** - Build and functionality tests
4. **Integration Testing** - Test the action itself with real inputs
5. **Security Scanning** - Bandit and Safety security checks

### Required Checks
- ✅ All 12 unit tests passing (84% coverage)
- ✅ Python 3.11 and 3.12 compatibility
- ✅ Docker build successful
- ✅ Integration tests passing
- ✅ No security vulnerabilities
- ✅ Code linting passing

## Development Guidelines

### Making Changes
1. Create feature branch from `main`
2. Run `make start` to ensure environment is set up
3. Make changes to code
4. Run `make test` frequently to catch issues early
5. Run `make check` before committing to validate all quality checks
6. Optional: Run `make format` to auto-format code

### Before Creating PR
```bash
make check        # Validates tests, linting, and security
make format       # Auto-formats code with Black
git status        # Verify changes
```

### Adding New Features
- Add corresponding tests in `test_*.py` files
- Update `DEVELOPMENT.md` if adding new commands or workflows
- Update `README.md` if changing user-facing functionality
- Ensure Docker build still works if modifying dependencies

### Modifying Dependencies
- Add to `requirements.txt` for production dependencies
- Add to `requirements-dev.txt` for development/testing tools
- Run `make install-dev` to update environment
- Test thoroughly, especially Docker build

## Boundaries and Restrictions

### What NOT to Change
- Do not modify `.github/workflows/` files unless specifically addressing CI/CD issues
- Do not remove or significantly alter existing tests without good reason
- Do not change the Docker base image without testing thoroughly
- Do not modify the `action.yml` interface without coordinating with users

### Files to Avoid
- Do not commit to `.venv/` directory (virtual environment)
- Do not commit `__pycache__/` or `.pytest_cache/` directories
- Do not commit coverage reports or test artifacts
- Do not commit IDE-specific files (these are in `.gitignore`)

### Dependencies
- Prefer using existing libraries over adding new ones
- The `semaphore_client` library is from a custom repository and should not be replaced
- Only update Python version requirements if absolutely necessary

## Common Tasks

### Adding a New Test
```python
# In test_semaphore_action_fixed.py or new test file
def test_my_new_feature(mocker):
    # Setup mocks if needed
    mock_api = mocker.patch('semaphore_client.ApiClient')
    
    # Test the functionality
    result = my_function()
    
    # Assert expectations
    assert result == expected_value
```

### Debugging WebSocket Issues
- Check `test_data.py` for real WebSocket message examples
- Use `test_live_api.py` for live API testing (safe, read-only)
- Verify ANSI escape code removal with `ansi_escape` regex

### Testing the Docker Action Locally
```bash
make docker-build              # Build the Docker image
make docker-test              # Test Docker functionality
# Or test manually:
docker build -t semaphore-action .
docker run --rm -e INPUT_MYINPUT=world semaphore-action
```

## Additional Resources

- **DEVELOPMENT.md** - Comprehensive development guide
- **Makefile** - All available commands and targets
- **test_data.py** - Real API response data for testing
- **action.yml** - Action inputs, outputs, and configuration

## Questions and Support

If you need clarification on any part of the codebase:
1. Check `DEVELOPMENT.md` for detailed development information
2. Review existing tests to understand expected behavior
3. Run `make help` to see all available Makefile targets
4. Look at `test_data.py` for examples of real API responses
