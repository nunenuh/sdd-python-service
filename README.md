# FastAPI Service Boilerplate

A production-ready FastAPI boilerplate for building modern Python web services with clean architecture, best practices, and comprehensive tooling.

## 🚀 Features

- **FastAPI Framework**: High-performance, easy-to-use, modern web framework
- **PostgreSQL**: Structured data storage with SQLAlchemy 2.0+
- **Redis**: Caching and session management
- **Poetry**: Dependency management and packaging
- **Docker Support**: Multi-stage builds for development and production
- **Configuration Management**: Environment-based configuration with Pydantic v2
- **Structured Logging**: JSON-formatted logs with environment-aware configuration
- **Comprehensive Health Checks**: Multiple health endpoints (`/ping`, `/status`, `/detailed`)
- **Code Quality Tools**: Pre-commit hooks, Black, isort, flake8, autoflake
- **Comprehensive Testing**: Pytest with unit, integration, and E2E tests
- **Authentication**: API key-based authentication with proper validation
- **Auto Documentation**: OpenAPI/Swagger docs with interactive UI
- **Database Migrations**: Alembic for database schema management
- **Spec-Driven Development**: AI-readable specifications for consistent code generation

## 📁 Project Structure

```
fastapi-service/
├── src/fastapi_service/          # Main application package
│   ├── core/                     # Core functionality
│   │   ├── auth.py               # API key authentication
│   │   ├── config.py             # Pydantic settings management
│   │   ├── dependencies.py       # FastAPI dependencies
│   │   └── logging.py            # Structured logging setup
│   ├── modules/                  # Feature modules
│   │   └── health/               # Health monitoring endpoints
│   │       ├── apiv1/            # API version 1 handlers
│   │       ├── services.py       # Business logic services
│   │       ├── usecase.py        # Use case orchestration
│   │       └── schemas.py        # Pydantic models
│   ├── dbase/                    # Database layer
│   │   └── sql/                  # SQLAlchemy (PostgreSQL)
│   │       ├── models/           # SQLAlchemy models
│   │       ├── core/             # Database core (session, base)
│   │       └── services/         # Database services
│   ├── shared/                   # Shared utilities
│   │   ├── exceptions.py         # Custom exception classes
│   │   ├── services/            # Shared services
│   │   └── utils/               # Utility functions
│   ├── main.py                   # FastAPI application entry point
│   └── router.py                 # Main API router configuration
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── e2e/                      # End-to-end tests
├── docker/                       # Docker configurations
│   ├── docker-compose.build.yml  # Build configurations
│   ├── docker-compose.dev.yml    # Development runtime
│   ├── docker-compose.run.yml    # Production runtime
│   └── images/                   # Dockerfile images
├── docs/                         # Comprehensive documentation
│   ├── architecture/             # Architecture diagrams
│   ├── deployment/               # Deployment guides
│   ├── development/              # Development setup
│   ├── quickstart/               # Quick start guides
│   └── testing/                  # Testing documentation
├── specs/                        # AI-readable specifications
│   ├── conventions/              # Coding conventions
│   ├── features/                 # Feature specifications
│   ├── api/                      # API specifications
│   └── workflows/                # Workflow templates
├── alembic/                      # Database migrations
├── pyproject.toml                # Poetry project configuration
├── Makefile                      # Development & deployment commands
└── README.md                     # This documentation
```

## 🏗️ Architecture

The boilerplate follows a clean layered architecture pattern:

- **Handler Layer**: FastAPI route handlers (`modules/*/apiv1/handler.py`)
- **Use Case Layer**: Business logic orchestration (`modules/*/usecase.py`)
- **Service Layer**: Business logic (`modules/*/services.py`)
- **Repository Layer**: Data access (`modules/*/repositories.py`)
- **Core Layer**: Configuration, logging, authentication

See `specs/conventions/03-module-structure.md` for detailed module structure guidelines.

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- Poetry
- PostgreSQL 15+ (optional, for database features)
- Redis 7+ (optional, for caching)
- Docker and Docker Compose (optional)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd sdd-python-service
   ```

2. **Install dependencies**:
   ```bash
   make install
   ```
   This will:
   - Install all dependencies using Poetry
   - Set up pre-commit hooks
   - Create `.venv` in the project directory

3. **Configure environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run with Docker Compose** (recommended for development):
   ```bash
   make docker-dev
   ```
   
   This will start:
   - FastAPI application (port 8080)
   - PostgreSQL (port 5432)
   - Redis (port 6379)

5. **Or run locally**:
   ```bash
   make run
   # Or for development with auto-reload:
   make dev
   ```

## 📚 Usage

### Running the Service

```bash
# Development mode with auto-reload
make dev

# Production mode
make run
```

### Database Migrations

```bash
# Create a new migration
make db-migrate

# Apply migrations
make db-upgrade

# Rollback last migration
make db-downgrade
```

### Testing

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests
make test-integration

# Run with coverage
make test-coverage
```

### Code Quality

```bash
# Format code
make format

# Run all linting checks
make lint-all
```

## 🔧 Configuration

Configuration is managed via environment variables. See `env.example` for all available options.

Key configuration areas:
- **Application**: `APP_NAME`, `APP_VERSION`, `APP_ENVIRONMENT`, `APP_DEBUG`
- **Database**: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- **Redis**: `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`
- **Authentication**: `APP_X_API_KEY`
- **CORS**: `ALLOWED_ORIGINS_STR`

## 📖 Documentation

- **API Documentation**: Available at `/docs` when server is running (Swagger UI)
- **Specifications**: See `specs/` directory for AI-readable specifications
- **Architecture**: See `docs/architecture/` for architecture documentation
- **Development**: See `docs/development/` for development guides
- **Deployment**: See `docs/deployment/` for deployment guides

## 🧩 Adding New Features

Follow the module structure conventions:

1. Create a new module in `src/fastapi_service/modules/your-module/`
2. Follow the structure: `apiv1/handler.py`, `schemas.py`, `usecase.py`, `services.py`, `repositories.py` (if needed)
3. Add your routes to `src/fastapi_service/router.py`
4. Create specifications in `specs/features/your-module/`

See `specs/conventions/03-module-structure.md` for detailed guidelines.

## 🐳 Docker

### Building Images

```bash
# Build base image
make docker-base-build

# Build service image
make docker-build
```

### Running Services

```bash
# Development environment
make docker-dev

# Production environment
make docker-run

# View logs
make docker-logs-dev
```

## 🧪 Testing

The boilerplate includes comprehensive testing setup:

- **Unit Tests**: Test individual components
- **Integration Tests**: Test API endpoints
- **E2E Tests**: Test complete workflows
- **Infrastructure Tests**: Test external dependencies (PostgreSQL, Redis)

## 📝 Code Style

- Follow PEP 8
- Use Black for formatting (line length: 88)
- Use isort for import sorting
- Type hints required for all functions
- See `specs/conventions/01-python-conventions.md` for details

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `make test`
4. Format code: `make format`
5. Commit following conventional commits
6. Push and create a pull request

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

This boilerplate is based on best practices from modern Python web development and clean architecture principles.


## 🚀 Features

- **FastAPI Framework**: High-performance, easy-to-use, modern web framework
- **PostgreSQL**: Structured data storage with SQLAlchemy 2.0+
- **Redis**: Caching and session management
- **Poetry**: Dependency management and packaging
- **Docker Support**: Multi-stage builds for development and production
- **Configuration Management**: Environment-based configuration with Pydantic v2
- **Structured Logging**: JSON-formatted logs with environment-aware configuration
- **Comprehensive Health Checks**: Multiple health endpoints (`/ping`, `/status`, `/detailed`)
- **Code Quality Tools**: Pre-commit hooks, Black, isort, flake8, autoflake
- **Comprehensive Testing**: Pytest with unit, integration, and E2E tests
- **Authentication**: API key-based authentication with proper validation
- **Auto Documentation**: OpenAPI/Swagger docs with interactive UI
- **Database Migrations**: Alembic for database schema management
- **Spec-Driven Development**: AI-readable specifications for consistent code generation

## 📁 Project Structure

```
fastapi-service/
├── src/fastapi_service/          # Main application package
│   ├── core/                     # Core functionality
│   │   ├── auth.py               # API key authentication
│   │   ├── config.py             # Pydantic settings management
│   │   ├── dependencies.py       # FastAPI dependencies
│   │   └── logging.py            # Structured logging setup
│   ├── modules/                  # Feature modules
│   │   └── health/               # Health monitoring endpoints
│   │       ├── apiv1/            # API version 1 handlers
│   │       ├── services.py       # Business logic services
│   │       ├── usecase.py        # Use case orchestration
│   │       └── schemas.py        # Pydantic models
│   ├── dbase/                    # Database layer
│   │   └── sql/                  # SQLAlchemy (PostgreSQL)
│   │       ├── models/           # SQLAlchemy models
│   │       ├── core/             # Database core (session, base)
│   │       └── services/         # Database services
│   ├── shared/                   # Shared utilities
│   │   ├── exceptions.py         # Custom exception classes
│   │   ├── services/            # Shared services
│   │   └── utils/               # Utility functions
│   ├── main.py                   # FastAPI application entry point
│   └── router.py                 # Main API router configuration
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── e2e/                      # End-to-end tests
├── docker/                       # Docker configurations
│   ├── docker-compose.build.yml  # Build configurations
│   ├── docker-compose.dev.yml    # Development runtime
│   ├── docker-compose.run.yml    # Production runtime
│   └── images/                   # Dockerfile images
├── docs/                         # Comprehensive documentation
│   ├── architecture/             # Architecture diagrams
│   ├── deployment/               # Deployment guides
│   ├── development/              # Development setup
│   ├── quickstart/               # Quick start guides
│   └── testing/                  # Testing documentation
├── specs/                        # AI-readable specifications
│   ├── conventions/              # Coding conventions
│   ├── features/                 # Feature specifications
│   ├── api/                      # API specifications
│   └── workflows/                # Workflow templates
├── alembic/                      # Database migrations
├── pyproject.toml                # Poetry project configuration
├── Makefile                      # Development & deployment commands
└── README.md                     # This documentation
```

## 🏗️ Architecture

The boilerplate follows a clean layered architecture pattern:

- **Handler Layer**: FastAPI route handlers (`modules/*/apiv1/handler.py`)
- **Use Case Layer**: Business logic orchestration (`modules/*/usecase.py`)
- **Service Layer**: Business logic (`modules/*/services.py`)
- **Repository Layer**: Data access (`modules/*/repositories.py`)
- **Core Layer**: Configuration, logging, authentication

See `specs/conventions/03-module-structure.md` for detailed module structure guidelines.

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- Poetry
- PostgreSQL 15+ (optional, for database features)
- Redis 7+ (optional, for caching)
- Docker and Docker Compose (optional)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd sdd-python-service
   ```

2. **Install dependencies**:
   ```bash
   make install
   ```
   This will:
   - Install all dependencies using Poetry
   - Set up pre-commit hooks
   - Create `.venv` in the project directory

3. **Configure environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run with Docker Compose** (recommended for development):
   ```bash
   make docker-dev
   ```
   
   This will start:
   - FastAPI application (port 8080)
   - PostgreSQL (port 5432)
   - Redis (port 6379)

5. **Or run locally**:
   ```bash
   make run
   # Or for development with auto-reload:
   make dev
   ```

## 📚 Usage

### Running the Service

```bash
# Development mode with auto-reload
make dev

# Production mode
make run
```

### Database Migrations

```bash
# Create a new migration
make db-migrate

# Apply migrations
make db-upgrade

# Rollback last migration
make db-downgrade
```

### Testing

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests
make test-integration

# Run with coverage
make test-coverage
```

### Code Quality

```bash
# Format code
make format

# Run all linting checks
make lint-all
```

## 🔧 Configuration

Configuration is managed via environment variables. See `env.example` for all available options.

Key configuration areas:
- **Application**: `APP_NAME`, `APP_VERSION`, `APP_ENVIRONMENT`, `APP_DEBUG`
- **Database**: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- **Redis**: `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`
- **Authentication**: `APP_X_API_KEY`
- **CORS**: `ALLOWED_ORIGINS_STR`

## 📖 Documentation

- **API Documentation**: Available at `/docs` when server is running (Swagger UI)
- **Specifications**: See `specs/` directory for AI-readable specifications
- **Architecture**: See `docs/architecture/` for architecture documentation
- **Development**: See `docs/development/` for development guides
- **Deployment**: See `docs/deployment/` for deployment guides

## 🧩 Adding New Features

Follow the module structure conventions:

1. Create a new module in `src/fastapi_service/modules/your-module/`
2. Follow the structure: `apiv1/handler.py`, `schemas.py`, `usecase.py`, `services.py`, `repositories.py` (if needed)
3. Add your routes to `src/fastapi_service/router.py`
4. Create specifications in `specs/features/your-module/`

See `specs/conventions/03-module-structure.md` for detailed guidelines.

## 🐳 Docker

### Building Images

```bash
# Build base image
make docker-base-build

# Build service image
make docker-build
```

### Running Services

```bash
# Development environment
make docker-dev

# Production environment
make docker-run

# View logs
make docker-logs-dev
```

## 🧪 Testing

The boilerplate includes comprehensive testing setup:

- **Unit Tests**: Test individual components
- **Integration Tests**: Test API endpoints
- **E2E Tests**: Test complete workflows
- **Infrastructure Tests**: Test external dependencies (PostgreSQL, Redis)

## 📝 Code Style

- Follow PEP 8
- Use Black for formatting (line length: 88)
- Use isort for import sorting
- Type hints required for all functions
- See `specs/conventions/01-python-conventions.md` for details

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `make test`
4. Format code: `make format`
5. Commit following conventional commits
6. Push and create a pull request

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

This boilerplate is based on best practices from modern Python web development and clean architecture principles.
