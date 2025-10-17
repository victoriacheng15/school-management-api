# DevOps Practices

This repository implements automated code quality and documentation checks using GitHub Actions workflows. The system enforces consistent formatting and style across the codebase.

## Workflows

### CI Workflow: Format, Test, and Coverage

The CI workflow automatically formats code, runs tests, and posts coverage results for pull requests targeting the `main` branch.

**Trigger Conditions:**

- On pull requests targeting the `main` branch.
- When changes are made to files in: `run.py`, `db/`, `app/`, or `tests/`.

**Workflow Steps:**

1. **Check Formatting:** Reports any Python code formatting issues found using Ruff.
2. **Run Tests:** Executes the test suite with `pytest` and calculates code coverage.
3. **Post Coverage Report:** Uploads the coverage results and posts a summary comment on the pull request.

### Docker Image Build & Publish to GHCR

This workflow builds the Docker image using the multi-stage Dockerfile and pushes it to GitHub Container Registry (GHCR) on every push to `main` or when manually triggered.

**Trigger Conditions:**

- On push to the `main` branch.
- Manual trigger via GitHub Actions UI (`workflow_dispatch`).

**Workflow Steps:**

1. **Checkout code:** Checks out the code.
2. **Authenticate to GHCR:** Logs in to GitHub Container Registry using the built-in `GITHUB_TOKEN`.
3. **Build Docker image:** Builds the image from `Dockerfile.multi-stage` and tags it as `ghcr.io/victoriacheng15/school-api:latest`.
4. **Push image:** Pushes the tagged image to GHCR for use in deployments.

### Documentation Linting with Markdownlint

The **Markdownlint Workflow** ensures consistent documentation formatting using [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) for all files in the `docs/` directory.

**Trigger Conditions:**

- On pull requests modifying `docs/*.md` files.
- On direct pushes to `docs/*.md` files.
- Can be manually triggered via GitHub Actions UI (`workflow_dispatch`).

**Workflow Steps:**

1. **Checkout code:** Checks out the code.
2. **Install linter:** Globally installs `markdownlint-cli` via npm.
3. **Run linting:** Reports any markdown style issues found in `docs/`.

## Development Practices

### Contribution Flow

1. Create feature branches from `main`.
2. Open pull requests for all changes.
3. Automated checks will:
    - Check Python code formatting.
    - Run tests and calculate code coverage.
    - Lint Markdown documentation in `docs/`.
4. Address any unresolved linting issues or test failures before merging.

### Quality Enforcement

- Python files maintain consistent style via Ruff.
- All code is automatically tested, and coverage is reported.
- Documentation adheres to Markdown best practices.
