# Variables
PYTHON := python
POETRY := poetry
PROJECT := fastapi_service
VERSION_TAG ?= latest
PORT ?= 8080
HOST ?= 0.0.0.0

# Docker registry settings (update with your own registry)
REGISTRY_URL ?= fastapi-service

# Version info
VERSION ?= latest
GIT_COMMIT = $(shell git rev-parse --short HEAD)
GIT_BRANCH ?= $(shell git rev-parse --abbrev-ref HEAD)
BUILD_DATE = $(shell date -u +'%Y-%m-%dT%H:%M:%SZ')
SERVICE ?= api-local

# Colors for terminal output
BLUE := \033[34m
GREEN := \033[32m
RED := \033[31m
YELLOW := \033[33m
RESET := \033[0m

.PHONY: help install test lint format clean run docker-build docker-run docker-dev docker-stop kill-port version-last version-next docker-base-build docker-base-push docker-push docker-build-push docker-logs docker-logs-dev docker-restart docker-dev-restart db-init db-migrate db-upgrade db-downgrade db-revision db-current db-history info

# Default target
help:
	@echo "$(BLUE)FastAPI Service Boilerplate - Available Commands:$(RESET)"
	@echo ""
	@echo "$(GREEN)Development:$(RESET)"
	@echo "  $(GREEN)make install$(RESET)                - Install project dependencies and setup pre-commit"
	@echo "  $(GREEN)make test$(RESET)                   - Run all tests"
	@echo "  $(GREEN)make test-unit$(RESET)              - Run unit tests only"
	@echo "  $(GREEN)make test-integration$(RESET)       - Run integration tests only"
	@echo "  $(GREEN)make test-infrastructure$(RESET)    - Run infrastructure tests (fast)"
	@echo "  $(GREEN)make test-infrastructure-slow$(RESET) - Run infrastructure tests (all)"
	@echo "  $(GREEN)make test-e2e$(RESET)              - Run E2E tests"
	@echo "  $(GREEN)make test-coverage$(RESET)          - Run tests with coverage report"
	@echo "  $(GREEN)make test-coverage-unit$(RESET)     - Run unit tests with coverage"
	@echo "  $(GREEN)make lint-all$(RESET)              - Run all linting checks (black, isort, flake8)"
	@echo "  $(GREEN)make format$(RESET)                - Auto-format code with black and isort"
	@echo "  $(GREEN)make clean$(RESET)                 - Clean up temporary files and cache"
	@echo "  $(GREEN)make run$(RESET)                   - Run the FastAPI application"
	@echo "  $(GREEN)make dev$(RESET)                   - Run in development mode with auto-reload"
	@echo ""
	@echo "$(GREEN)Database:$(RESET)"
	@echo "  $(GREEN)make db-init$(RESET)       - Initialize database (create tables)"
	@echo "  $(GREEN)make db-migrate$(RESET)    - Create new migration"
	@echo "  $(GREEN)make db-upgrade$(RESET)    - Apply migrations"
	@echo "  $(GREEN)make db-downgrade$(RESET)  - Rollback last migration"
	@echo "  $(GREEN)make db-revision$(RESET)   - Create empty migration"
	@echo ""
	@echo "$(GREEN)Docker:$(RESET)"
	@echo "  $(GREEN)make docker-base-build$(RESET) - Build base Docker image"
	@echo "  $(GREEN)make docker-build$(RESET)      - Build Docker image (default: api-local)"
	@echo "  $(GREEN)make docker-build-push$(RESET) - Build and push Docker image"
	@echo "  $(GREEN)make docker-run$(RESET)        - Run with docker compose (production)"
	@echo "  $(GREEN)make docker-dev$(RESET)        - Run with docker compose (development)"
	@echo "  $(GREEN)make docker-stop$(RESET)       - Stop docker compose"
	@echo "  $(GREEN)make docker-logs$(RESET)       - Show docker compose logs (production)"
	@echo "  $(GREEN)make docker-logs-dev$(RESET)  - Show docker compose logs (development)"
	@echo "  $(GREEN)make docker-restart$(RESET)    - Restart docker compose services"
	@echo "  $(GREEN)make docker-dev-restart$(RESET) - Restart docker compose services (dev)"
	@echo ""
	@echo "$(GREEN)Utilities:$(RESET)"
	@echo "  $(GREEN)make update$(RESET)        - Update dependencies"
	@echo "  $(GREEN)make info$(RESET)          - Show project information"
	@echo "  $(GREEN)make version-last$(RESET)  - Get the latest version"
	@echo "  $(GREEN)make version-next$(RESET)  - Calculate next version number"

# Install dependencies
install:
	@echo "$(BLUE)Installing project dependencies...$(RESET)"
	$(POETRY) install --with dev
	@echo "$(BLUE)Setting up pre-commit hooks...$(RESET)"
	$(POETRY) run pre-commit install
	@echo "$(GREEN)Installation complete! Pre-commit hooks installed.$(RESET)"

# Run tests
test:
	@echo "$(BLUE)Running tests...$(RESET)"
	$(POETRY) run pytest tests/ -v

test-unit:
	@echo "$(BLUE)Running unit tests...$(RESET)"
	$(POETRY) run pytest tests/unit/ -v

test-integration:
	@echo "$(BLUE)Running integration tests...$(RESET)"
	$(POETRY) run pytest tests/integration/ -v

test-infrastructure:
	@echo "$(BLUE)Running infrastructure tests...$(RESET)"
	@echo "$(YELLOW)Note: This requires Docker Compose to be running$(RESET)"
	$(POETRY) run pytest tests/infrastructure/ -v -m "not slow"

test-infrastructure-slow:
	@echo "$(BLUE)Running infrastructure tests (including slow tests)...$(RESET)"
	@echo "$(YELLOW)Note: This requires Docker Compose to be running$(RESET)"
	$(POETRY) run pytest tests/infrastructure/ -v

test-e2e:
	@echo "$(BLUE)Running E2E tests...$(RESET)"
	$(POETRY) run pytest tests/e2e/ -v

# Run tests with coverage
test-coverage:
	@echo "$(BLUE)Running tests with coverage...$(RESET)"
	$(POETRY) run pytest tests/ --cov=$(PROJECT) --cov-report=term-missing --cov-report=html

test-coverage-unit:
	@echo "$(BLUE)Running unit tests with coverage...$(RESET)"
	$(POETRY) run pytest tests/unit/ --cov=$(PROJECT) --cov-report=term-missing --cov-report=html

# Format code
format:
	@echo "$(BLUE)Formatting code with black and isort...$(RESET)"
	$(POETRY) run black src/ tests/
	$(POETRY) run isort src/ tests/
	@echo "$(GREEN)Code formatting complete!$(RESET)"

# Run pre-commit checks
lint-all:
	@echo "$(BLUE)Running pre-commit checks...$(RESET)"
	$(POETRY) run pre-commit run --all-files

# Clean up temporary files
clean:
	@echo "$(BLUE)Cleaning up temporary files...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(RESET)"

# Kill any process using the specified port
kill-port:
	@echo "$(BLUE)Checking for processes on port $(PORT)...$(RESET)"
	@lsof -ti:$(PORT) | xargs kill -9 2>/dev/null || echo "$(GREEN)Port $(PORT) is free$(RESET)"

# Run the application
run: kill-port
	@echo "$(BLUE)Starting FastAPI application...$(RESET)"
	@echo "$(BLUE)Loading environment variables...$(RESET)"
	@if [ -f .env ]; then \
		export $$(grep -v '^#' .env | xargs); \
	else \
		echo "$(YELLOW)Warning: .env file not found, using default values$(RESET)"; \
	fi
	$(POETRY) run python -m fastapi_service.main

# Run in development mode
dev: run

# Docker commands - Base image
docker-base-build:
	@echo "$(BLUE)Building base Docker image version $(VERSION)...$(RESET)"
	GIT_BRANCH=$(GIT_BRANCH) \
	docker compose -f docker/docker-compose.build.yml build \
		--no-cache \
		--pull \
		--build-arg VERSION=$(VERSION) \
		--build-arg GIT_COMMIT=$(GIT_COMMIT) \
		--build-arg BUILD_DATE=$(BUILD_DATE) \
		api-base

docker-base-push:
	@echo "$(BLUE)Pushing base Docker image to Docker Hub...$(RESET)"
	@echo "$(YELLOW)Make sure you're logged in: docker login$(RESET)"
	GIT_BRANCH=$(GIT_BRANCH) \
	docker compose -f docker/docker-compose.build.yml push api-base

# Docker commands - Service images
docker-build:
	@echo "$(BLUE)Building Docker image version $(VERSION) for $(SERVICE)...$(RESET)"
	GIT_BRANCH=$(GIT_BRANCH) \
	docker compose -f docker/docker-compose.build.yml build \
		--no-cache \
		--pull \
		--build-arg VERSION=$(VERSION) \
		--build-arg GIT_COMMIT=$(GIT_COMMIT) \
		--build-arg BUILD_DATE=$(BUILD_DATE) \
		$(SERVICE)

docker-push:
	@echo "$(BLUE)Pushing Docker image to Docker Hub: nunenuh/fastapi-service:$(VERSION)-$(GIT_BRANCH)...$(RESET)"
	@echo "$(YELLOW)Make sure you're logged in: docker login$(RESET)"
	GIT_BRANCH=$(GIT_BRANCH) \
	docker compose -f docker/docker-compose.build.yml push $(SERVICE)

docker-build-push: docker-build docker-push

# Docker run commands
docker-run:
	@echo "$(BLUE)Running services with Docker Compose (production)...$(RESET)"
	@docker compose -f docker/docker-compose.run.yml up -d
	@echo "$(GREEN)Services started! Check logs with: make docker-logs$(RESET)"

docker-dev:
	@echo "$(BLUE)Running services with Docker Compose (development)...$(RESET)"
	@docker compose -f docker/docker-compose.dev.yml up -d
	@echo "$(GREEN)Development services started! Check logs with: make docker-logs-dev$(RESET)"

docker-stop:
	@echo "$(BLUE)Stopping Docker Compose services...$(RESET)"
	@docker compose -f docker/docker-compose.run.yml down 2>/dev/null || true
	@docker compose -f docker/docker-compose.dev.yml down 2>/dev/null || true
	@echo "$(GREEN)All services stopped!$(RESET)"

docker-logs:
	@echo "$(BLUE)Showing Docker Compose logs (production)...$(RESET)"
	@docker compose -f docker/docker-compose.run.yml logs -f

docker-logs-dev:
	@echo "$(BLUE)Showing Docker Compose logs (development)...$(RESET)"
	@docker compose -f docker/docker-compose.dev.yml logs -f

docker-restart: docker-stop docker-run

docker-dev-restart: docker-stop docker-dev

# Update dependencies
update:
	@echo "$(BLUE)Updating dependencies...$(RESET)"
	$(POETRY) update
	@echo "$(GREEN)Dependencies updated!$(RESET)"

# Version management
version-last:
	@CURRENT_VERSION=`git tag -l "v*" --sort=-v:refname | head -n 1 | sed 's/^v//' || echo "0.0.0"`; \
	if [ -z "$$CURRENT_VERSION" ]; then \
		CURRENT_VERSION="0.0.0"; \
	fi; \
	echo -n "$$CURRENT_VERSION"

version-next:
	@CURRENT_VERSION=`make -s version-last`; \
	MAJOR=`echo "$$CURRENT_VERSION" | cut -d. -f1`; \
	MINOR=`echo "$$CURRENT_VERSION" | cut -d. -f2`; \
	PATCH=`echo "$$CURRENT_VERSION" | cut -d. -f3`; \
	VERSION_TYPE=$${VERSION_TYPE:-patch}; \
	case $$VERSION_TYPE in \
		major) \
			NEW_MAJOR=`expr $$MAJOR + 1`; \
			NEW_VERSION="$$NEW_MAJOR.0.0";; \
		minor) \
			NEW_MINOR=`expr $$MINOR + 1`; \
			NEW_VERSION="$$MAJOR.$$NEW_MINOR.0";; \
		patch|*) \
			NEW_PATCH=`expr $$PATCH + 1`; \
			NEW_VERSION="$$MAJOR.$$MINOR.$$NEW_PATCH";; \
	esac; \
	echo "$$NEW_VERSION"

# Database migrations
db-init:
	@echo "$(BLUE)Initializing database...$(RESET)"
	$(POETRY) run alembic upgrade head

db-migrate:
	@echo "$(BLUE)Creating migration...$(RESET)"
	@read -p "Migration message: " msg; \
	$(POETRY) run alembic revision --autogenerate -m "$$msg"

db-upgrade:
	@echo "$(BLUE)Applying migrations...$(RESET)"
	$(POETRY) run alembic upgrade head

db-downgrade:
	@echo "$(BLUE)Rolling back last migration...$(RESET)"
	$(POETRY) run alembic downgrade -1

db-revision:
	@echo "$(BLUE)Creating empty migration...$(RESET)"
	@read -p "Migration message: " msg; \
	$(POETRY) run alembic revision -m "$$msg"

db-current:
	@echo "$(BLUE)Current database revision:$(RESET)"
	$(POETRY) run alembic current

db-history:
	@echo "$(BLUE)Migration history:$(RESET)"
	$(POETRY) run alembic history

# Show project info
info:
	@echo "$(BLUE)Project Information:$(RESET)"
	@echo "$(GREEN)Project:$(RESET) $(PROJECT)"
	@echo "$(GREEN)Version:$(RESET) $(VERSION)"
	@echo "$(GREEN)Port:$(RESET) $(PORT)"
	@echo "$(GREEN)Host:$(RESET) $(HOST)"
	@echo "$(GREEN)Git Branch:$(RESET) $(GIT_BRANCH)"
	@echo "$(GREEN)Git Commit:$(RESET) $(GIT_COMMIT)"
	@echo "$(GREEN)Python:$(RESET) $$($(POETRY) run python --version)"
	@echo "$(GREEN)Poetry:$(RESET) $$($(POETRY) --version)"

