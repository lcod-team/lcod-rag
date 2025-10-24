.PHONY: install dev run ingest lint format docker-up docker-down

LCOD_RUN ?= lcod-run
LCOD_INGEST_COMPOSE ?= packages/rag/components/ingest.run_pipeline/compose.yaml

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

run:
	uvicorn app.rag_api.main:app --host 0.0.0.0 --port 8088 --reload

ingest:
	$(LCOD_RUN) --compose $(LCOD_INGEST_COMPOSE)

lint:
	python -m compileall app

format:
	autopep8 -r app -i || true

docker-up:
	docker compose up -d

docker-down:
	docker compose down
