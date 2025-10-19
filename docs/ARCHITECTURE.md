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
         | Ingestion CLI              |
         v                            |
+--------+---------+         +-------v---------+
|  rag-ingest CLI  |         |   rag-api       |
|  (Typer / Python)|         | (FastAPI)       |
+--------+---------+         | - /query        |
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
|  (nucone.local)  |
+------------------+
```

### Key integration points

- **Ollama** provides both embedding and generative models. We use `nomic-embed-text` for vectors and `llama3.1` for responses.
- **Vector store** is powered by Qdrant (bundled in `docker-compose.yml`). The collection name defaults to `lcod_docs` but can be changed via environment variables.
- **Existing services** such as Open WebUI or Dify can call `rag-api` directly. The API returns the retrieved passages alongside the generated answer so consumers can render citations.

## Components

### 1. Ingestion pipeline (`app/ingest`)

- Discovers documentation files based on `config/sources.yaml`.
- Uses LangChain text splitters to create overlapping chunks (default 1 000 tokens / 200 overlap).
- Requests embeddings from Ollama and stores vectors in Qdrant.
- Stores metadata (repository, file path, heading) to support filtering.

Command example:

```bash
python -m app.ingest.cli run --config config/sources.yaml \
       --collection lcod_docs --recreate
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

1. Operators run `app.ingest.cli` locally or on `nucone.local` (could be cron-triggered).
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

