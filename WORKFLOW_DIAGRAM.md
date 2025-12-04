# Automated Release Workflow Diagram

## Branching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                      BRANCHING FLOW                          │
└─────────────────────────────────────────────────────────────┘

feature/my-feature
       │
       │ (create from develop)
       │
       ├──> make changes
       │
       └──> PR to develop
              │
              │ (merge after CI passes)
              ▼
           develop
              │
              │ (accumulate features)
              │ (CI runs on every push)
              │
              └──> PR to main (for release)
                     │
                     │ (merge after review)
                     ▼
                   main ──────────> 🚀 AUTOMATIC RELEASE
                     │
                     ├──> Create version tag (v1.2.3)
                     ├──> Update major tag (v1)
                     ├──> Generate changelog
                     └──> Publish GitHub release
```

## Release Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    RELEASE AUTOMATION                        │
└─────────────────────────────────────────────────────────────┘

Commit to main
    │
    ▼
┌──────────────────┐
│  Release.yml     │  ◄── Triggered automatically
│  Workflow Runs   │
└──────────────────┘
    │
    ├──> 1. Analyze commit messages
    │       └──> Determine version bump type
    │           ├─ [major] or "breaking change" → v1.x.x → v2.0.0
    │           ├─ feat: or [minor]             → v1.2.x → v1.3.0
    │           └─ other commits                → v1.2.3 → v1.2.4
    │
    ├──> 2. Create version tags
    │       ├─ Specific: v1.2.3 (immutable)
    │       └─ Major: v1 (updated to latest v1.x.x)
    │
    ├──> 3. Generate changelog
    │       └──> From git commit history
    │
    └──> 4. Create GitHub Release
            └──> Published with changelog


Users can now use:
  uses: gulbinas/semaphore-action@v1      ◄── Latest v1.x.x
  uses: gulbinas/semaphore-action@v1.2.3  ◄── Specific version
```

## Version Tag System

```
┌─────────────────────────────────────────────────────────────┐
│                    VERSION TAGS                              │
└─────────────────────────────────────────────────────────────┘

Repository Tags:
    v1.0.0  ──┐
    v1.1.0  ──┤
    v1.2.0  ──┼──> v1 (major version tag, auto-updated)
    v1.2.1  ──┤
    v1.2.2  ──┤
    v1.2.3  ──┘  (latest v1.x.x)

When new release is created:
    1. Create v1.2.4 (new specific version)
    2. Update v1 → points to v1.2.4
    3. Users using @v1 automatically get v1.2.4

Breaking change release:
    1. Create v2.0.0 (new major version)
    2. Create v2 → points to v2.0.0
    3. v1 still points to v1.2.3 (old major version preserved)
    4. Users on @v1 stay on v1.x.x (no breaking changes)
    5. Users can opt-in to @v2 when ready
```

## Development Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                 CONTRIBUTOR WORKFLOW                         │
└─────────────────────────────────────────────────────────────┘

Developer:
    1. git checkout develop
    2. git checkout -b feature/awesome-feature
    3. Make changes & test locally
    4. git commit -m "feat: Add awesome feature"
    5. git push origin feature/awesome-feature
    6. Create PR to develop
       │
       ▼
    CI runs:
       ├─ Linting
       ├─ Unit tests (Python 3.11, 3.12)
       ├─ Docker build test
       ├─ Integration test
       └─ Security scan
       │
       ▼
    PR merged to develop
       │
       ▼
    Feature is in develop branch
       (ready for next release)


Maintainer (when ready to release):
    Option 1: Use GitHub Actions UI
       1. Go to Actions → "Create Release PR"
       2. Click "Run workflow"
       3. Select version bump type
       4. Review created PR
       5. Merge PR
          │
          ▼
       Automatic release happens!

    Option 2: Manual PR
       1. Create PR: develop → main
       2. Add [major], [minor], or feat: in commit
       3. Merge PR
          │
          ▼
       Automatic release happens!
```

## CI/CD Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                     CI/CD PIPELINE                           │
└─────────────────────────────────────────────────────────────┘

Push to develop:
    ├─ develop-ci.yml runs
    ├─ All tests & checks
    └─ Security scanning

PR to develop:
    ├─ develop-ci.yml runs
    ├─ pr-testing.yml runs
    └─ Must pass before merge

Push to main:
    ├─ pr-testing.yml runs
    ├─ release.yml runs
    ├─ integration.yml runs
    ├─ python.yml runs
    └─ 🚀 Release created!

All workflows:
    ✅ Explicit permissions
    ✅ Security hardened
    ✅ Latest action versions
```

## Quick Reference

### For Users (Using the Action)

```yaml
# Recommended: Get automatic updates within major version
uses: gulbinas/semaphore-action@v1

# Stable: Pin to specific version
uses: gulbinas/semaphore-action@v1.2.3

# Development: Use latest (not recommended for production)
uses: gulbinas/semaphore-action@main
```

### For Contributors

```bash
# Feature development
git checkout develop
git checkout -b feature/my-feature
git commit -m "feat: Add feature"
git push origin feature/my-feature
# Create PR to develop

# Bug fix
git checkout develop
git checkout -b fix/bug-name
git commit -m "fix: Resolve bug"
git push origin fix/bug-name
# Create PR to develop

# Hotfix (urgent)
git checkout main
git checkout -b hotfix/critical-issue
git commit -m "fix: Critical issue"
git push origin hotfix/critical-issue
# Create PR to main, then backport to develop
```

### For Maintainers

```bash
# Creating a release
# Option 1: GitHub Actions UI → Create Release PR → Select version type

# Option 2: Manual
git checkout develop
git pull
# Create PR from develop to main
# Merge PR → automatic release
```

## Commit Message Impact

```
Commit Message                    → Version Change → Example
─────────────────────────────────────────────────────────────
"fix: Bug fix"                    → Patch         → v1.2.3 → v1.2.4
"docs: Update README"             → Patch         → v1.2.3 → v1.2.4
"feat: New feature"               → Minor         → v1.2.3 → v1.3.0
"[minor] Add feature"             → Minor         → v1.2.3 → v1.3.0
"[major] Breaking change"         → Major         → v1.2.3 → v2.0.0
"breaking change: Remove API"     → Major         → v1.2.3 → v2.0.0
```

## File Structure

```
semaphore-action/
├── .github/
│   ├── workflows/
│   │   ├── release.yml            ← Automatic releases
│   │   ├── develop-ci.yml         ← CI for develop
│   │   ├── create-release-pr.yml  ← Release PR helper
│   │   ├── pr-testing.yml         ← PR validation
│   │   ├── integration.yml        ← Integration tests
│   │   └── python.yml             ← Linting
│   └── ISSUE_TEMPLATE/
│       └── release.yml            ← Release request template
├── RELEASE_STRATEGY.md            ← Detailed release docs
├── QUICK_START.md                 ← Quick reference
├── CONTRIBUTING.md                ← Contribution guide
├── IMPLEMENTATION_SUMMARY.md      ← Implementation overview
├── WORKFLOW_DIAGRAM.md            ← This file
└── README.md                      ← Main documentation
```

## Benefits Summary

✅ **Automated Releases** - No manual tagging or changelog writing
✅ **Semantic Versioning** - Clear, meaningful version numbers
✅ **Safe Updates** - Major version tags prevent breaking changes
✅ **Professional Process** - Structured workflow for all contributors
✅ **Comprehensive Docs** - Clear guidance for everyone
✅ **Security** - Hardened workflows with explicit permissions
✅ **Flexibility** - Multiple ways to create releases
✅ **User-Friendly** - Easy to use with version tags

---

For more details, see:
- [RELEASE_STRATEGY.md](RELEASE_STRATEGY.md) - Complete guide
- [QUICK_START.md](QUICK_START.md) - Quick reference
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - What was created
