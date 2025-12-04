# Next Steps After Merging This PR

## Immediate Actions

### 1. Merge This PR
This PR should be merged to create the foundation for the new release workflow.

### 2. Create the `develop` Branch
If it doesn't already exist, create a `develop` branch:

```bash
# If main branch exists
git checkout main
git pull
git checkout -b develop
git push origin develop
```

### 3. Set Up Branch Protection (Recommended)

#### For `main` branch:
Go to Repository Settings → Branches → Add rule

- **Branch name pattern**: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging
  - Select: `PR Ready for Merge`, `Code Validation`, `Comprehensive Testing`
- ✅ Require branches to be up to date before merging
- ❌ Do not allow force pushes
- ❌ Do not allow deletions

#### For `develop` branch:
Go to Repository Settings → Branches → Add rule

- **Branch name pattern**: `develop`
- ✅ Require status checks to pass before merging
  - Select: `Develop Branch Ready`, `Code Validation`
- ✅ Require branches to be up to date before merging
- ❌ Do not allow deletions

### 4. Update Repository Settings

#### Enable GitHub Actions
- Go to Settings → Actions → General
- ✅ Allow all actions and reusable workflows
- Set Workflow permissions to: **Read and write permissions**
- ✅ Allow GitHub Actions to create and approve pull requests

### 5. Test the Release Workflow

Create a test release to verify everything works:

```bash
# Make a small change on develop
git checkout develop
echo "# Test" >> TEST.md
git add TEST.md
git commit -m "test: Verify release workflow"
git push origin develop

# Create PR from develop to main via GitHub UI
# Title: "test: First release test"
# Merge the PR

# Watch the release workflow run in Actions tab
# Verify v1.0.0 tag and release are created
```

### 6. Verify the Release

After the test release:

1. Check the **Releases** page for `v1.0.0`
2. Verify both tags exist:
   ```bash
   git fetch --tags
   git tag -l "v*"
   # Should show: v1, v1.0.0
   ```
3. Test using the action:
   ```yaml
   uses: gulbinas/semaphore-action@v1
   ```

## Ongoing Workflow

### For Contributors

**Regular Development**:
1. Always create feature branches from `develop`
2. Submit PRs to `develop` (not `main`)
3. Wait for CI to pass
4. Merge after review

**Working on a Feature**:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "feat: Add my feature"
git push origin feature/my-feature

# Create PR: feature/my-feature → develop
```

### For Maintainers

**Creating a Release**:

**Option 1: Using GitHub Actions UI** (Recommended)
1. Go to **Actions** tab
2. Select **"Create Release PR"** workflow
3. Click **"Run workflow"**
4. Select version bump type:
   - `patch` for bug fixes
   - `minor` for new features
   - `major` for breaking changes
5. Review the created PR
6. Merge when ready → Release happens automatically!

**Option 2: Manual PR**
1. Create PR from `develop` to `main`
2. Add appropriate prefix to merge commit:
   - `fix:` → patch release
   - `feat:` → minor release
   - `[major]` → major release
3. Merge PR → Release happens automatically!

**For Hotfixes** (urgent production fixes):
```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue

# Fix the issue
git add .
git commit -m "fix: Critical security issue"
git push origin hotfix/critical-issue

# Create PR: hotfix/critical-issue → main
# Merge PR (triggers release)

# Backport to develop
git checkout develop
git merge main
git push origin develop
```

## Monitoring Releases

### Watch the Release Workflow
- Go to **Actions** tab after merging to `main`
- Watch **"Release and Tag"** workflow run
- Check for successful completion

### Verify Release Published
- Go to **Releases** page
- Verify new release with changelog
- Check version tags

### Update Documentation
After first release, you may want to:
- Update README badges with release version
- Announce the new versioning system
- Update any external documentation

## Troubleshooting

### Release Workflow Doesn't Trigger
- Check that `release.yml` is on `main` branch
- Verify GitHub Actions is enabled
- Check workflow permissions in Settings
- Ensure commit doesn't contain `[skip ci]`

### Wrong Version Number
- Check commit message format
- Manually create/update tag if needed:
  ```bash
  git tag -a v1.0.1 -m "Release v1.0.1"
  git push origin v1.0.1
  ```

### PR from Develop to Main Fails CI
- Fix issues on develop branch first
- Ensure all tests pass on develop
- Rebase develop on main if needed

## Migration for Existing Users

If users are currently using `@main`:

1. **Announce the change** in release notes
2. **Recommend migration** to `@v1`
3. **Update examples** in documentation
4. **Provide migration guide**:
   ```yaml
   # Before
   uses: gulbinas/semaphore-action@main
   
   # After (recommended)
   uses: gulbinas/semaphore-action@v1
   
   # Or (stable)
   uses: gulbinas/semaphore-action@v1.0.0
   ```

## Best Practices

### Commit Messages
Use semantic commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `[major]` for breaking changes

### Testing Before Release
- Always test on `develop` first
- Run full test suite
- Verify Docker build
- Test integration

### Communication
- Use PR descriptions to explain changes
- Update documentation with new features
- Add breaking changes to release notes
- Announce major releases

## Support

If you encounter issues:
1. Check the workflow logs in Actions tab
2. Review documentation in repository
3. Open an issue with details
4. Tag maintainers if urgent

## Summary

✅ **Merge this PR**
✅ **Create develop branch**
✅ **Set up branch protection**
✅ **Configure GitHub Actions settings**
✅ **Test with a release**
✅ **Follow the new workflow**

The automated release system is now ready! 🚀

---

**Quick Links**:
- [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md) - Visual diagrams
- [QUICK_START.md](QUICK_START.md) - Quick reference
- [RELEASE_STRATEGY.md](RELEASE_STRATEGY.md) - Complete guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
