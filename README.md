# Python Container Action Template

[![Action Template](https://img.shields.io/badge/Action%20Template-Python%20Container%20Action-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAM6wAADOsB5dZE0gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAERSURBVCiRhZG/SsMxFEZPfsVJ61jbxaF0cRQRcRJ9hlYn30IHN/+9iquDCOIsblIrOjqKgy5aKoJQj4O3EEtbPwhJbr6Te28CmdSKeqzeqr0YbfVIrTBKakvtOl5dtTkK+v4HfA9PEyBFCY9AGVgCBLaBp1jPAyfAJ/AAdIEG0dNAiyP7+K1qIfMdonZic6+WJoBJvQlvuwDqcXadUuqPA1NKAlexbRTAIMvMOCjTbMwl1LtI/6KWJ5Q6rT6Ht1MA58AX8Apcqqt5r2qhrgAXQC3CZ6i1+KMd9TRu3MvA3aH/fFPnBodb6oe6HM8+lYHrGdRXW8M9bMZtPXUji69lmf5Cmamq7quNLFZXD9Rq7v0Bpc1o/tp0fisAAAAASUVORK5CYII=)](https://github.com/jacobtomlinson/python-container-action)
[![Actions Status](https://github.com/jacobtomlinson/python-container-action/workflows/Lint/badge.svg)](https://github.com/jacobtomlinson/python-container-action/actions)
[![Actions Status](https://github.com/jacobtomlinson/python-container-action/workflows/Integration%20Test/badge.svg)](https://github.com/jacobtomlinson/python-container-action/actions)

This is a template for creating GitHub actions and contains a small Python application which will be built into a minimal [Container Action](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-a-docker-container-action). Our final container from this template is ~50MB, yours may be a little bigger once you add some code. If you want something smaller check out my [go-container-action template](https://github.com/jacobtomlinson/go-container-action/actions).

In `main.py` you will find a small example of accessing Action inputs and returning Action outputs. For more information on communicating with the workflow see the [development tools for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/development-tools-for-github-actions).

> 🏁 To get started, click the `Use this template` button on this repository [which will create a new repository based on this template](https://github.blog/2019-06-06-generate-new-repositories-with-repository-templates/).

## Usage

Semaphore Action allows you to invoke Ansible Semaphore tasks from your GitHub Actions workflows.

### Versioning

This action uses semantic versioning with automated releases. You can reference it in several ways:

- **Recommended**: Use major version tag (e.g., `@v1`) for automatic updates within the same major version
- **Stable**: Use specific version tag (e.g., `@v1.2.3`) for guaranteed reproducibility
- **Development**: Use `@main` for the latest changes (not recommended for production)

See [RELEASE_STRATEGY.md](RELEASE_STRATEGY.md) for detailed information about the release process.

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run Semaphore Task
      uses: gulbinas/semaphore-action@v1  # Use latest v1.x.x version
      with:
        myInput: world
        api_key: ${{ secrets.SEMAPHORE_API_KEY }}
        api_url: ${{ secrets.SEMAPHORE_API_URL }}
        ws_api_url: ${{ secrets.SEMAPHORE_WS_API_URL }}
        project_id: 1
```

### Using Specific Version

For critical workflows, pin to a specific version:

```yaml
    - name: Run Semaphore Task
      uses: gulbinas/semaphore-action@v1.2.3  # Pin to specific version
      with:
        myInput: world
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myInput`  | An example mandatory input    |
| `anotherInput` _(optional)_  | An example optional input    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myOutput`  | An example output (returns 'Hello world')    |

## Examples

### Using Major Version Tag (Recommended)

Get automatic updates for bug fixes and new features within the same major version:

```yaml
- name: Run Semaphore Task
  uses: gulbinas/semaphore-action@v1
  with:
    myInput: world
    api_key: ${{ secrets.SEMAPHORE_API_KEY }}
    api_url: ${{ secrets.SEMAPHORE_API_URL }}
    ws_api_url: ${{ secrets.SEMAPHORE_WS_API_URL }}
    project_id: 1
```

### Using Specific Version Tag

Pin to a specific version for guaranteed reproducibility:

```yaml
- name: Run Semaphore Task  
  uses: gulbinas/semaphore-action@v1.2.3
  with:
    myInput: world
    api_key: ${{ secrets.SEMAPHORE_API_KEY }}
    api_url: ${{ secrets.SEMAPHORE_API_URL }}
    ws_api_url: ${{ secrets.SEMAPHORE_WS_API_URL }}
    project_id: 1
```

### Using the optional input

This is how to use the optional input.

```yaml
with:
  myInput: world
  anotherInput: optional
```

### Using outputs

```yaml
steps:
- uses: actions/checkout@v4
- name: Run Semaphore Task
  id: semaphore
  uses: gulbinas/semaphore-action@v1
  with:
    myInput: world
    api_key: ${{ secrets.SEMAPHORE_API_KEY }}
    api_url: ${{ secrets.SEMAPHORE_API_URL }}
    ws_api_url: ${{ secrets.SEMAPHORE_WS_API_URL }}
    project_id: 1

- name: Check outputs
  run: |
    echo "Outputs - ${{ steps.semaphore.outputs.myOutput }}"
```

## Release Information

This action uses automated releases with semantic versioning:

- **Tags**: Each release is tagged with a version number (e.g., `v1.2.3`)
- **Major version tags**: Automatically updated to point to the latest release in that major version (e.g., `v1` → `v1.2.3`)
- **Changelog**: Automatically generated for each release

For detailed information about the release process, branching strategy, and contribution guidelines, see [RELEASE_STRATEGY.md](RELEASE_STRATEGY.md).

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Development workflow
- Branching strategy
- Commit message format
- Pull request process
- Testing guidelines

### Quick Links

- [Quick Start Guide](QUICK_START.md) - Fast reference for common tasks
- [Release Strategy](RELEASE_STRATEGY.md) - Detailed release and branching documentation
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to this project

## License

See [LICENSE](LICENSE) file for details.

```