.PHONY: help build up down logs shell-backend shell-frontend migrate test clean

help:
	@echo "Available commands:"
	@echo "  make build         - Build Docker images"
	@echo "  make up            - Start all services"
	@echo "  make down          - Stop all services"
	@echo "  make logs          - View logs"
	@echo "  make shell-backend - Access backend shell"
	@echo "  make shell-frontend - Access frontend shell"
	@echo "  make migrate       - Run database migrations"
	@echo "  make test          - Run tests"
	@echo "  make clean         - Clean up containers and volumes"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell-backend:
	docker-compose exec backend bash

shell-frontend:
	docker-compose exec frontend sh

migrate:
	docker-compose exec backend alembic upgrade head

test:
	docker-compose exec backend pytest

clean:
	docker-compose down -v
	docker system prune -f
