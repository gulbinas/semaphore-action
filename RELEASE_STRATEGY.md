# Release Strategy and Branching Guide

This document describes the automated release workflow and branching strategy for semaphore-action.

## Branching Strategy

### Main Branches

1. **`main`** - Production-ready code
   - All commits to main trigger an automatic release
   - Protected branch (merges only via pull requests)
   - Always deployable

2. **`develop`** - Integration branch for development
   - Feature branches merge here first
   - Comprehensive CI runs on all commits
   - PRs from develop to main trigger releases

### Feature Branches

- Create from: `develop`
- Merge to: `develop`
- Naming: `feature/description`, `fix/description`, `docs/description`

## Automated Release Process

### How It Works

1. When changes are merged to `main`, the release workflow automatically:
   - Determines the next version number
   - Creates a new version tag (e.g., `v1.2.3`)
   - Updates the major version tag (e.g., `v1`)
   - Generates a changelog from commit messages
   - Creates a GitHub release

### Version Bumping

The version bump type is determined by commit messages:

- **Major version bump** (e.g., v1.x.x → v2.0.0):
  - Commit message contains `[major]` or `breaking change`
  - Example: `[major] Remove deprecated API endpoints`

- **Minor version bump** (e.g., v1.2.x → v1.3.0):
  - Commit message contains `[minor]`, `feat:`, or `feature:`
  - Example: `feat: Add new retry mechanism`

- **Patch version bump** (e.g., v1.2.3 → v1.2.4):
  - All other commits (fixes, docs, etc.)
  - Example: `fix: Resolve timeout issue`

### Version Tags

Two types of tags are maintained:

1. **Specific version tags** (e.g., `v1.2.3`)
   - Immutable reference to a specific release
   - Use for guaranteed reproducibility

2. **Major version tags** (e.g., `v1`)
   - Automatically updated to point to latest v1.x.x release
   - Use for automatic updates within major version

## Usage Examples

### Recommended: Use Major Version Tags

```yaml
- name: Run Semaphore Task
  uses: gulbinas/semaphore-action@v1
  with:
    api_key: ${{ secrets.SEMAPHORE_API_KEY }}
    api_url: ${{ secrets.SEMAPHORE_API_URL }}
    ws_api_url: ${{ secrets.SEMAPHORE_WS_API_URL }}
    project_id: 1
```

**Benefits:**
- Automatically receive bug fixes and minor features
- No breaking changes (within same major version)
- Recommended for most users

### Pin to Specific Version

```yaml
- name: Run Semaphore Task
  uses: gulbinas/semaphore-action@v1.2.3
  with:
    api_key: ${{ secrets.SEMAPHORE_API_KEY }}
    # ... other inputs
```

**Benefits:**
- Guaranteed reproducibility
- No unexpected changes
- Use for critical production workflows

### Development/Testing: Use Main Branch

```yaml
- name: Run Semaphore Task
  uses: gulbinas/semaphore-action@main
  with:
    # ... inputs
```

**Note:** Not recommended for production. Use only for testing latest changes.

## Workflow for Contributors

### Working on a New Feature

```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/my-new-feature

# 2. Make changes and commit
git add .
git commit -m "feat: Add my new feature"

# 3. Push and create PR to develop
git push origin feature/my-new-feature
# Create PR: feature/my-new-feature → develop
```

### Releasing to Production

```bash
# 1. Create PR from develop to main
# Create PR: develop → main

# 2. After PR is merged, release workflow runs automatically
# - New version tag is created
# - GitHub release is published
# - Major version tag is updated
```

### Hotfix Process

For urgent fixes that need to go directly to production:

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. Make the fix
git add .
git commit -m "fix: Resolve critical bug"

# 3. Create PR to main
git push origin hotfix/critical-bug
# Create PR: hotfix/critical-bug → main

# 4. After merge, backport to develop
git checkout develop
git merge main
git push origin develop
```

## Release Workflow Configuration

### Skipping Release

To push to main without triggering a release:

```bash
git commit -m "docs: Update README [skip ci]"
```

### Custom Version Bump

Include keywords in commit messages:

- `[major]` - Force major version bump
- `[minor]` or `feat:` - Force minor version bump
- Default behavior - Patch version bump

### Example Commit Messages

```bash
# Patch release (v1.2.3 → v1.2.4)
git commit -m "fix: Correct API timeout handling"

# Minor release (v1.2.3 → v1.3.0)
git commit -m "feat: Add retry mechanism for failed requests"

# Major release (v1.2.3 → v2.0.0)
git commit -m "[major] Remove deprecated legacy API support"
```

## CI/CD Workflows

### On Develop Branch

- Full test suite
- Code quality checks
- Security scanning
- Docker build validation
- Integration tests

### On Pull Requests to Main

- All develop branch checks
- Additional release validation

### On Push to Main

- All checks above
- Automatic release creation
- Tag generation
- Changelog generation

## Branch Protection Rules (Recommended)

### For `main` branch:
- Require pull request reviews (at least 1)
- Require status checks to pass
- Require branches to be up to date
- Do not allow force pushes
- Do not allow deletions

### For `develop` branch:
- Require status checks to pass
- Allow force pushes (with caution)
- Do not allow deletions

## Migration Guide

### For Existing Users

If you're currently using:
```yaml
uses: gulbinas/semaphore-action@main
```

Update to:
```yaml
uses: gulbinas/semaphore-action@v1  # or latest version tag
```

This ensures stability while receiving updates.

### First Release Setup

The first release will be created as `v1.0.0` when the first commit is pushed to main after the release workflow is added.

## Troubleshooting

### Release Workflow Not Triggering

1. Check that commit doesn't contain `[skip ci]`
2. Verify workflow file is on main branch
3. Check GitHub Actions permissions in repository settings

### Wrong Version Number

- Check commit message for version keywords
- Manual tags can be created if needed:
  ```bash
  git tag -a v1.2.3 -m "Release v1.2.3"
  git push origin v1.2.3
  ```

## Best Practices

1. **Always use tagged versions in production workflows**
2. **Test changes on develop branch first**
3. **Write clear commit messages** for accurate changelog
4. **Review PRs carefully** before merging to main
5. **Use semantic versioning** principles in version bumps

## Support

For issues or questions:
- Open an issue in the repository
- Check existing releases and their changelogs
- Review closed PRs for similar changes
