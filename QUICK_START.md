# Quick Start: Using Semaphore Action with Version Tags

This guide will help you quickly integrate semaphore-action into your workflows using the new versioning system.

## For Action Users

### Basic Usage (Recommended)

Use the major version tag to automatically receive bug fixes and new features:

```yaml
- name: Run Semaphore Task
  uses: gulbinas/semaphore-action@v1
  with:
    api_key: ${{ secrets.SEMAPHORE_API_KEY }}
    api_url: ${{ secrets.SEMAPHORE_API_URL }}
    ws_api_url: ${{ secrets.SEMAPHORE_WS_API_URL }}
    project_id: 1
    myInput: world
```

### Production Usage (Stable)

Pin to a specific version for guaranteed reproducibility:

```yaml
- name: Run Semaphore Task
  uses: gulbinas/semaphore-action@v1.2.3
  with:
    api_key: ${{ secrets.SEMAPHORE_API_KEY }}
    api_url: ${{ secrets.SEMAPHORE_API_URL }}
    ws_api_url: ${{ secrets.SEMAPHORE_WS_API_URL }}
    project_id: 1
    myInput: world
```

## For Contributors

### Quick Development Workflow

```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# 2. Make changes and test
make test

# 3. Commit with descriptive message
git commit -m "feat: Add new feature"

# 4. Push and create PR to develop
git push origin feature/my-feature
# Create PR: feature/my-feature → develop
```

### Creating a Release

#### Option 1: Using GitHub UI (Recommended)

1. Go to Actions tab in GitHub
2. Select "Create Release PR" workflow
3. Click "Run workflow"
4. Choose version bump type (patch/minor/major)
5. Review and merge the created PR

#### Option 2: Manual PR

1. Create PR from `develop` to `main`
2. Add commit message prefix in PR description:
   - `[major]` for breaking changes
   - `feat:` for new features
   - Default for bug fixes
3. Merge PR - release happens automatically!

## Version Bump Guide

| Change Type | Example | Version Change | Tag to Use |
|-------------|---------|----------------|------------|
| Bug fix | `fix: Resolve timeout` | v1.2.3 → v1.2.4 | Default |
| New feature | `feat: Add retry logic` | v1.2.3 → v1.3.0 | `feat:` or `[minor]` |
| Breaking change | `[major] Remove old API` | v1.2.3 → v2.0.0 | `[major]` |

## Common Questions

**Q: Which version should I use in my workflow?**  
A: Use `@v1` for most cases. It gives you updates automatically while preventing breaking changes.

**Q: How do I know which version is current?**  
A: Check the [Releases page](https://github.com/gulbinas/semaphore-action/releases) on GitHub.

**Q: When should I pin to a specific version?**  
A: Pin to specific versions (e.g., `@v1.2.3`) for critical production workflows where you need guaranteed behavior.

**Q: Can I still use `@main`?**  
A: Yes, but it's not recommended for production. Use it only for testing unreleased features.

## Need More Help?

- See [RELEASE_STRATEGY.md](RELEASE_STRATEGY.md) for detailed documentation
- Check [README.md](README.md) for complete action documentation
- Open an issue for questions or problems
