# Secret scanning (gitleaks)

This repo runs **gitleaks** in GitHub Actions and fails CI when potential secrets are detected.

## Workflow
- GitHub Actions: `.github/workflows/gitleaks.yml`
- Config: `.gitleaks.toml`
- Ignore file: `.gitleaksignore`

## Handling false positives / accepted findings
Prefer the narrowest approach:

### 1) Remove/rotate the secret (best)
If it is a real credential, remove it and **rotate** it.

### 2) Ignore a specific finding via `.gitleaksignore` (recommended)
1. Run locally:
   ```bash
   gitleaks detect --source . --report-format json --report-path gitleaks.json
   ```
2. Copy the `Fingerprint` value for the accepted finding into `.gitleaksignore` (one per line).

### 3) Add a targeted allowlist rule in `.gitleaks.toml`
Use this only when a whole class of files/strings is known-safe (e.g., certain binary formats).
Keep allowlists as narrow as possible.
