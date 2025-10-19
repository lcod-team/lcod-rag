.PHONY: install dev run ingest lint format docker-up docker-down

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

run:
	uvicorn app.rag_api.main:app --host 0.0.0.0 --port 8088 --reload

ingest:
	python -m app.ingest.cli run --config config/sources.yaml

lint:
	python -m compileall app

format:
	autopep8 -r app -i || true

docker-up:
	docker compose up -d

docker-down:
	docker compose down

