# Docker Images

This directory contains Dockerfile definitions for building Docker images.

## Purpose

Multi-stage Docker builds for different environments:
- **Dockerfile.base**: Base image with dependencies
- **Dockerfile.stg**: Staging environment image
- **Dockerfile.prd**: Production environment image

## Usage

\`\`\`bash
# Build base image
make docker-base-build

# Build service image
make docker-build
\`\`\`
