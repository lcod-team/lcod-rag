# LCOD RAG Stack

This repository hosts the Retrieval-Augmented Generation (RAG) stack used by the LCOD organisation. It glues together the existing AI services (Ollama, Open WebUI and Dify) with a dedicated ingestion pipeline and a lightweight retrieval API.

## Goals

- **Centralise knowledge** from LCOD repositories (`lcod-spec`, `lcod-resolver`, `lcod-components`, `lcod-kernel-*`, …) in a searchable vector store.
- **Expose a simple API** that other tools (Open WebUI, Dify apps, IDE assistants) can call for semantic search + answer generation.
- **Automate ingestion** so new commits or documentation drops can be synchronised quickly.
- Remain close to the existing infrastructure (Docker, Ollama, Weaviate/Qdrant) to simplify operations.

The stack is meant to run on the shared LCOD infrastructure, but every component is containerised so the same setup can be reproduced elsewhere.

## Repository layout

```
app/
  rag_api/        # FastAPI service (retrieval + generation)
config/
  .env.example          # Example environment file for the API container
docs/
  ARCHITECTURE.md # High-level description of the stack and integration points
  OPERATIONS.md   # Operational playbooks (deployment, ingestion, backups)
Dockerfile        # Builds the rag-api container image
docker-compose.yml
Makefile          # Automation shortcuts (install, run, ingest, lint)
requirements.txt  # Python dependencies for the API service
packages/rag/components/ingest.*  # LCOD ingestion pipeline
```

## Quick start (local workstation)

1. Create and activate a virtualenv, then install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy the sample environment file and edit it to match your setup:

   ```bash
   cp config/.env.example config/.env
   ```

3. Launch the services with Docker Compose:

   ```bash
   docker compose up -d
   ```

4. Run an ingestion pass with `lcod-run` (download the latest LCOD runtime bundle first):

   ```bash
   lcod-run --compose packages/rag/components/ingest.run_pipeline/compose.yaml
   ```

   The pipeline honours the same environment variables as the previous Python
   scripts: set `OLLAMA_BASE_URL`, `QDRANT_URL`, `QDRANT_COLLECTION`,
   `QDRANT_API_KEY` and `RAG_EMBED_MODEL` as needed before running the command.

5. Query the API:

   ```bash
   curl -X POST http://localhost:8088/query \
        -H 'Content-Type: application/json' \
        -d '{"query": "What is the resolver responsible for?"}'
   ```

## Registry snapshot powered by `lcod-run`

The RAG ingestion pipeline ships LCOD components that can be executed directly
with the standalone `lcod-run` binary (Rust). Once the repository is cloned, the
registry snapshot can be refreshed without extra configuration:

```bash
lcod-run --compose packages/rag/components/registry.refresh_snapshot/compose.yaml
```

The compose downloads the official LCOD catalogues, resolves the components, and
updates `data/registry.snapshot.json` only when the content changes. When a
different catalogue pointer or snapshot location is required, provide overrides
through the compose state (see component READMEs for the available fields).
Standard `lcod-run` flags (`--log-level`, `--timeout`, `--global-cache`, …) remain
available for advanced scenarios.

## Deployment

The target server already runs the required dependencies:

- **Ollama** (HTTP API on `http://127.0.0.1:11434`) for both embeddings and generation.
- **Traefik + Docker** for routing and SSL.
- **Existing AI stacks** (Dify, Open WebUI) that will consume this RAG API.

See [`docs/OPERATIONS.md`](docs/OPERATIONS.md) for the detailed procedure (clone repo, configure compose, schedule ingestion, monitoring).

## Status

The repository currently provides the base scaffolding, ingestion utilities and API skeleton. Next iterations will plug the API into Open WebUI (custom retriever) and Dify datasets.
