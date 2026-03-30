# Pharmacy Management System

Odoo 18 Training Project

# Commit & Branch Convention

## Format
```
<dev>/<prefix>(<scope>): <description>
```
```
john/feat(pos): add dynamic button grid
sara/fix(auth): resolve token expiry
```

---

## Developer Nicknames
| Developer     | Prefix  |
|---------------|---------|
| John Smith    | `john`  |
| Sara Ali      | `sara`  |
| Mohamed Khaled| `mk`    |
> Add your entry here when onboarding.

---

## Allowed Prefixes
| Prefix     | Use For                        |
|------------|--------------------------------|
| `feat`     | New feature                    |
| `fix`      | Bug fix                        |
| `hotfix`   | Critical production patch      |
| `refactor` | Code restructure, no logic change |
| `chore`    | CI, deps, config               |
| `docs`     | Documentation only             |
| `test`     | Tests only                     |

---

## Branch Naming
```
<dev>/<prefix>/<TICKET-ID>-<description>
john/feat/POS-142-button-grid
sara/fix/AUTH-89-token-expiry
```

---

## CI — `.github/workflows/lint-commits.yml`
```yaml
name: Lint Commits
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: npm i -D @commitlint/cli
      - run: npx commitlint --from=HEAD~1 --to=HEAD
```

---

## ✅ Valid &nbsp;&nbsp; ❌ Invalid
```bash
✅ git commit -m "john/feat(pos): add button grid"
✅ git commit -m "sara/fix(api): null check on product fetch"
❌ git commit -m "fixed stuff"
❌ git commit -m "feat(pos): missing dev prefix"
```
