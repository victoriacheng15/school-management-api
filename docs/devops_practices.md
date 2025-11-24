# DevOps Practices

## Table of Contents

- [Overview](#overview)
- [Workflow Architecture](#workflow-architecture)
      - [Path-Based Triggering](#path-based-triggering)
- [Active Workflows](#active-workflows)
      - [Format, Test & Coverage (ciyml)](#1-format-test--coverage-ciyml)
      - [Build and Push Docker Image to GHCR (ghcryml)](#2-build-and-push-docker-image-to-ghcr-ghcryml)
      - [Markdownlint (markdownlintyml)](#3-markdownlint-markdownlintyml)

This document outlines all DevOps workflows, CI/CD pipelines, and automation practices used in the school-management-api project.

## Overview

The project uses GitHub Actions for continuous integration, deployment, and code quality checks. All workflows follow a snake_case naming convention and use path filters to optimize CI/CD execution.

## Workflow Architecture

### Path-Based Triggering

All workflows use path filters to ensure they only run when relevant files change:

- **API workflows**: Trigger on `run.py`, `db/**`, `app/**`, or `tests/**` changes
- **Documentation workflows**: Trigger on `**/*.md` changes

This approach:

- Reduces unnecessary workflow runs
- Saves CI/CD minutes
- Provides faster feedback
- Keeps concerns separated

## Active Workflows

### 1. Format, Test & Coverage (`ci.yml`)

**Purpose**: Ensures consistent code formatting, validates that all tests pass, and reports code coverage for pull requests.

**Trigger**:

- Pull requests to `main` branch that modify files in `run.py`, `db/**`, `app/**`, or `tests/**`
- Manual dispatch (`workflow_dispatch`)

**Environment Variables**:

- `PYTHON_VERSION`: `3.10`

**Jobs**:

1. **Format Job**:
   - Checkout code
   - Setup Python 3.10
   - Install dependencies (`make install`)
   - Check formatting with Ruff (`ruff format --check .`)

2. **Test Job** (runs after format):
   - Checkout code
   - Setup Python 3.10
   - Install dependencies (`make install`)
   - Run tests with coverage (`make coverage`)
   - Upload coverage artifact

3. **Coverage Report Job** (runs after test):
   - Checkout code
   - Download coverage artifact
   - Post PR comment with coverage summary table

**Key Features**:

- Fails PR if formatting issues are detected
- Prevents broken code from reaching main branch
- Coverage threshold: 80%
- Automated PR comment with coverage metrics (Pass/Fail status)
- Required check before merge

**Required Secrets**:

- `LOCAL_DB_HOST`: Database host for testing
- `LOCAL_DB_NAME`: Database name for testing
- `LOCAL_DB_USER`: Database user for testing
- `LOCAL_DB_PASSWORD`: Database password for testing

---

### 2. Build and Push Docker Image to GHCR (`ghcr.yml`)

**Purpose**: Builds the Docker image using the multi-stage Dockerfile and pushes it to GitHub Container Registry (GHCR).

**Trigger**:

- Push to `main` branch
- Manual dispatch (`workflow_dispatch`)

**Steps**:

1. Checkout code
2. Log in to GitHub Container Registry using `GITHUB_TOKEN`
3. Build Docker image from `Dockerfile.multi-stage` and tag as `ghcr.io/victoriacheng15/school-api:latest`
4. Push image to GHCR

**Key Features**:

- Automated build and publish on merge to main
- Uses multi-stage Dockerfile for optimized image size
- Image available for deployments from GHCR

**Note**: Originally intended to push to Azure Container Registry (ACR), but switched to GitHub Container Registry due to challenges with the `azure/login` workflow authentication at the time of implementation.

---

### 3. Markdownlint (`markdownlint.yml`)

**Purpose**: Ensures consistent markdown formatting across all documentation files.

**Trigger**:

- Pull requests that modify `**/*.md` files
- Manual dispatch (`workflow_dispatch`)

**Steps**:

1. Checkout code
2. Install markdownlint-cli globally via npm
3. Run markdown linter on all `.md` files

**Key Features**:

- Maintains documentation quality
- Enforces markdown best practices
- Validates all markdown files in the repository
