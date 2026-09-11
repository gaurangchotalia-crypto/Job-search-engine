.PHONY: help install run-web run-cli test clean docker-build docker-run docker-stop setup lint format

help:
	@echo "Job Scraper - Available Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup           - Create virtual environment and install dependencies"
	@echo "  make install         - Install dependencies"
	@echo ""
	@echo "Running the Scraper:"
	@echo "  make run-web         - Start web server (http://localhost:5000)"
	@echo "  make run-cli         - Run CLI scraper"
	@echo "  make run-cli-help    - Show CLI help options"
	@echo ""
	@echo "Development:"
	@echo "  make lint            - Run linters (flake8, pylint)"
	@echo "  make format          - Format code (autopep8)"
	@echo "  make test            - Run tests (if available)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run Docker container"
	@echo "  make docker-stop     - Stop Docker container"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           - Remove cache, logs, and temporary files"
	@echo ""

setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Setup complete! Run 'source venv/bin/activate' to activate the environment."

install:
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

run-web:
	python app.py

run-cli:
	python cli.py

run-cli-help:
	python cli.py --help

run-cli-custom:
	@read -p "Enter job role (default: investor relations): " role; \
	read -p "Enter location (default: Mumbai): " location; \
	python cli.py --role "$$role" --location "$$location"

test:
	@echo "Running tests..."
	python -m pytest tests/ -v || echo "No tests found"

lint:
	@echo "Running linters..."
	flake8 *.py --max-line-length=120 || true
	pylint *.py || true

format:
	@echo "Formatting code..."
	autopep8 --in-place --aggressive --aggressive *.py

docker-build:
	docker build -t job-scraper:latest .
	@echo "✅ Docker image built!"

docker-run:
	docker-compose up -d
	@echo "✅ Docker container started! Access at http://localhost:5000"

docker-stop:
	docker-compose down
	@echo "✅ Docker container stopped!"

docker-logs:
	docker-compose logs -f

clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	rm -rf *.egg-info
	rm -rf .eggs
	rm -rf build dist
	rm -f *.json
	rm -f *.log
	@echo "✅ Cleanup complete!"

freeze:
	pip freeze > requirements-dev.txt
	@echo "✅ Frozen dependencies to requirements-dev.txt"

.DEFAULT_GOAL := help
