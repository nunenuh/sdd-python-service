{
  description = "Sain Crawler News - FastAPI Python Microservice for News Scraping";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Python 3.11 as specified in pyproject.toml
            python311
            python311Packages.pip
            
            # Poetry for dependency management (built with Python 3.11)
            python311Packages.poetry-core
            poetry
            
            # System libraries for Python packages with C extensions
            postgresql_15      # PostgreSQL client library
            zlib               # Compression library
            openssl            # SSL/TLS library
            libffi             # Foreign function interface
            libxml2            # XML parsing library (for lxml)
            libxslt            # XSLT library (for lxml)
            
            # Development tools
            git
            gcc                # C compiler for building extensions
            pkg-config         # Helper tool for compiling
            curl               # For health checks
            docker             # Docker for containerization
            docker-compose     # Docker Compose for orchestration
          ];

          shellHook = ''
            # Set up environment for building Python packages with C extensions
            export POSTGRES_INCLUDE_DIR="${pkgs.postgresql_15}/include"
            export POSTGRES_LIB_DIR="${pkgs.postgresql_15}/lib"
            
            # Set up library paths
            export LD_LIBRARY_PATH="${pkgs.postgresql_15}/lib:${pkgs.zlib}/lib:${pkgs.openssl}/lib:${pkgs.libffi}/lib:${pkgs.libxml2}/lib:${pkgs.libxslt}/lib:$LD_LIBRARY_PATH"
            
            echo "🚀 Sain Crawler News Development Environment"
            echo "Python: $(python --version)"
            echo "Poetry: $(poetry --version)"
            echo "PostgreSQL: Available (${pkgs.postgresql_15}/bin/psql)"
            echo ""
            echo "Quick commands:"
            echo "  poetry install    - Install dependencies"
            echo "  poetry shell      - Activate virtual environment"
            echo "  poetry run dev    - Run development server"
            echo "  make docker-run   - Start services with Docker Compose"
            echo ""
          '';
        };
      }
    );
}

