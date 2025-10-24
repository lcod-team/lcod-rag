# LCOD RAG Architecture

## Overview

The LCOD RAG stack provides a retrieval layer that indexes documentation, specs and code snippets from the LCOD repositories. It exposes a lightweight API that other tools (Open WebUI, Dify, IDE assistants) can call to perform semantic search and answer generation.

```
+-----------------+         +------------------+
| LCOD Repositories|        |   External Tools |
| (spec, resolver, |        | - Open WebUI     |
|  components, …) |        | - Dify agents    |
+--------+--------+        | - IDE copilots   |
         |                 +---------+--------+
         | Ingestion Compose          |
         v                            |
+--------------------+       | - /ingest      |
| LCOD ingest flow   |       +-------+--------+
| (lcod-run compose) |               |
+--------------------+               |
         | Upserts            | - /ingest      |
         v                    +-------+--------+
+--------+---------+                 |
|  Qdrant Vector DB|<---------------+
|  (Docker service)|    Vector search results
+------------------+
         |
         | Embeddings (Ollama / nomic-embed-text)
         v
+------------------+
|   Ollama Server  |
| (LCOD infra)     |
+------------------+
```

### Key integration points

- **Ollama** provides both embedding and generative models. We use `nomic-embed-text` for vectors and `llama3.1` for responses.
- **Vector store** is powered by Qdrant (bundled in `docker-compose.yml`). The collection name defaults to `lcod_docs` but can be changed via environment variables.
- **Existing services** such as Open WebUI or Dify can call `rag-api` directly. The API returns the retrieved passages alongside the generated answer so consumers can render citations.

## Components

### 1. Ingestion pipeline (`lcod://rag/ingest/run_pipeline`)

- Resolves components and documentation directly from the LCOD registry.
- Uses the LCOD chunking helper to build overlapping text windows (default
  1 000 characters / 200 overlap).
- Calls the Ollama embeddings endpoint and stores vectors in Qdrant through
  dedicated LCOD components.
- Preserves metadata (component URI, doc key, registry source) for filtering
  and provenance.

Command example:

```bash
lcod-run --compose packages/rag/components/ingest.run_pipeline/compose.yaml
```

### 2. Retrieval API (`app/rag_api`)

- FastAPI application exposing:
  - `POST /query` – Retrieve top-K chunks and ask Ollama to generate an answer.
  - `POST /ingest` – Optional endpoint to ingest ad-hoc snippets (used by automations).
  - `GET /health` – Readiness probe for Traefik / monitoring.
- The service relies on the same ingestion utilities, so metadata schema stays consistent.

### 3. Docker Compose (`docker-compose.yml`)

- `qdrant` service (ports `6333/6334`). Persistence stored under `./data/qdrant` by default.
- `rag-api` service built from `Dockerfile`. The container exposes port `8088` and connects to Ollama through `host.docker.internal:11434`.
- `.env.example` documents the tunables (collection name, models, hostnames).

## Data flow

1. Operators run the LCOD ingestion compose (`lcod-run --compose packages/rag/components/ingest.run_pipeline/compose.yaml`) locally or via cron on the target host.
2. Each ingestion pass creates/updates the Qdrant collection and upserts chunks.
3. Clients query `rag-api` with a natural language prompt. The service:
   - Queries Qdrant for similar chunks (`top_k` configurable).
   - Crafts a prompt combining the user question and retrieved context.
   - Sends the prompt to Ollama for generation.
   - Returns `{ answer, contexts }` to the caller.
4. Open WebUI can register a “custom tool” pointing to `/query`; Dify can wrap it as a dataset retriever.

## Future extensions

- **Watchers**: Add Git hooks or scheduled ingestion to detect new commits.
- **Source connectors**: Extend ingestion to Confluence/Notion or API specs.
- **Multi-tenant indices**: Use Qdrant payload filters per product/scope.
- **Tracing**: Emit events to OpenTelemetry / Jaeger for observability.
