# Development Guide - Semaphore GitHub Action

## 🚀 Quick Start

```bash
# Setup development environment and run tests
make start

# Or step by step:
make dev-setup    # Set up environment and install dependencies
make test         # Run comprehensive tests
make help         # See all available commands
```

## 📋 Available Make Targets

### Environment Setup
```bash
make venv         # Create virtual environment
make install      # Install production dependencies
make install-dev  # Install development dependencies  
make dev-setup    # Complete development environment setup
```

### Testing
```bash
make test         # Run main unit tests
make test-basic   # Run basic tests only
make test-all     # Run all available tests
make test-coverage # Run tests with coverage report
make test-live    # Run live API demonstration (safe)
make ci-test      # Run tests in CI format
```

### Code Quality
```bash
make lint         # Run code linting with flake8
make format       # Format code with black
make security     # Run security checks (bandit, safety)
make check        # Run all quality checks (test + lint + security)
```

### Docker
```bash
make docker-build # Build Docker image
make docker-test  # Test Docker functionality
```

### Development
```bash
make clean        # Remove build artifacts
make clean-venv   # Remove virtual environment  
make clean-all    # Complete cleanup
make info         # Show project information
make status       # Show environment status
```

## 🔄 GitHub Actions Workflow

The project includes a comprehensive PR testing workflow (`.github/workflows/pr-testing.yml`) with:

### Validation Jobs
- **Code Validation**: Basic tests, linting, environment setup
- **Comprehensive Testing**: Multi-Python version testing (3.11, 3.12) with coverage
- **Docker Testing**: Build and functionality tests
- **Integration Testing**: Test the action itself with real inputs
- **Security Scanning**: Bandit and Safety security checks

### Workflow Triggers
```yaml
on:
  pull_request:
    branches: [ main, master, develop ]
  push:
    branches: [ main, master, develop ]
```

### Status Checks
All PRs must pass:
- ✅ Unit tests (12 tests with 84% coverage)
- ✅ Multi-Python compatibility (3.11, 3.12)
- ✅ Docker build and functionality
- ✅ Integration tests
- ✅ Security scanning
- ✅ Code linting

## 🛠️ Development Workflow

### 1. Initial Setup
```bash
git clone <repository>
cd semaphore-action
make start  # Sets up everything and runs tests
```

### 2. Making Changes
```bash
# Activate virtual environment
source .venv/bin/activate

# Make your changes to main.py or tests

# Run tests frequently
make test

# Check code quality
make check
```

### 3. Before Committing
```bash
# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install

# Run full validation
make check

# Format code
make format
```

### 4. Creating Pull Requests
When you create a PR, GitHub Actions will automatically:
1. Validate your code across multiple Python versions
2. Run comprehensive tests with coverage
3. Test Docker build and functionality  
4. Run integration tests
5. Perform security scanning
6. Provide detailed feedback on any failures

## 📁 Project Structure

```
semaphore-action/
├── main.py                           # Main GitHub Action code
├── requirements.txt                  # Production dependencies
├── requirements-dev.txt              # Development dependencies
├── Makefile                          # Development automation
├── Dockerfile                        # Container definition
├── action.yml                        # GitHub Action metadata
│
├── .github/workflows/
│   ├── pr-testing.yml               # Comprehensive PR testing
│   ├── integration.yml              # Basic integration test
│   └── python.yml                   # Legacy linting workflow
│
├── tests/
│   ├── test_basic.py                # Basic functionality tests
│   ├── test_semaphore_action_fixed.py # Comprehensive unit tests
│   ├── test_data.py                 # Real API response data
│   └── test_live_api.py             # Live API demonstration
│
├── .pre-commit-config.yaml          # Pre-commit hooks
└── .venv/                           # Virtual environment (created)
```

## 🧪 Testing Strategy

### Unit Tests (84% Coverage)
- **GitHub Action output writing** - File I/O operations
- **API task creation** - Semaphore API interaction
- **WebSocket monitoring** - Async real-time log streaming
- **Error handling** - Exception scenarios and edge cases
- **Configuration** - Environment variable processing
- **Integration** - End-to-end workflow testing

### Real Data Integration
Tests use **actual API responses** from live Semaphore system:
- Template endpoints (`/api/project/1/templates`)
- Task creation (`POST /api/project/1/tasks`)
- Task monitoring (`GET /api/project/1/tasks/{id}`)
- WebSocket messages (real Ansible execution logs)

### CI/CD Testing Matrix
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]
    os: [ubuntu-latest]
```

## 🔧 Troubleshooting

### Common Issues

**Virtual environment not found:**
```bash
make clean-venv && make venv
```

**Dependencies not installing:**
```bash
make clean-all && make dev-setup
```

**Tests failing:**
```bash
make test-verbose  # Get detailed test output
make status       # Check environment status
```

**Docker issues:**
```bash
make docker-build  # Rebuild Docker image
make docker-test   # Test Docker functionality
```

### Environment Validation
```bash
make status       # Check virtual environment and dependencies
make info         # Show project configuration
python --version  # Verify Python version
```

## 🚀 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Setup** development environment: `make start`
4. **Make** your changes and add tests
5. **Validate** your changes: `make check`
6. **Commit** your changes: `git commit -m 'Add amazing feature'`
7. **Push** to the branch: `git push origin feature/amazing-feature`
8. **Create** a Pull Request

The automated PR workflow will validate your changes across multiple environments and provide detailed feedback.

## 📊 Quality Metrics

- **Test Coverage**: 84% (12/12 tests passing)
- **Python Compatibility**: 3.11, 3.12
- **Security**: Bandit + Safety scanning
- **Code Quality**: Flake8 linting + Black formatting
- **Integration**: Docker + GitHub Actions testing

---

**Happy coding! 🎉**
