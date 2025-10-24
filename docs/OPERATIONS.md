# Operations Guide

This document describes how to deploy and operate the LCOD RAG stack on the shared LCOD infrastructure.

## 1. Clone & sync repositories

```bash
ssh <lcod-server>
mkdir -p ~/git
cd ~/git
# Clone the LCOD repositories that will feed the RAG index
for repo in lcod-spec lcod-resolver lcod-components lcod-kernel-js lcod-kernel-rs; do
  if [ ! -d "$repo" ]; then
    git clone git@github.com:lcod-team/$repo.git
  else
    (cd "$repo" && git pull --ff-only)
  fi
done
# Clone the rag stack itself
if [ ! -d lcod-rag ]; then
  git clone git@github.com:lcod-team/lcod-rag.git
fi
```

Keep the repositories up-to-date (daily cron or manual pull) so ingestion reflects the latest documentation.

## 2. Configure the stack

1. Copy the sample environment file:

   ```bash
   cd ~/git/lcod-rag
   cp config/.env.example config/.env
   ```

2. Review `config/.env` and adjust model names, collection identifiers and service URLs if necessary.

## 3. Deploy services

Use Docker Compose to start the vector store and API:

```bash
cd ~/git/lcod-rag
docker compose up -d
```

The stack creates a dedicated Docker network (`lcod-rag_default`) and persists Qdrant data under `./data/qdrant` (bind-mounted on the host). Port `8088` is exposed for the API.

### Integration with Traefik

If the server already runs Traefik, add the following snippet to `docker-compose.override.yml` to route traffic (example: expose as `rag.internal.lcod`):

```yaml
services:
  rag-api:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.lcod-rag.rule=Host(`rag.internal.lcod`)"
      - "traefik.http.routers.lcod-rag.entrypoints=websecure"
      - "traefik.http.routers.lcod-rag.tls.certresolver=letsencrypt"
      - "traefik.http.services.lcod-rag.loadbalancer.server.port=8088"
```

Restart the compose stack afterwards.

## 4. Run an ingestion pass

```bash
cd ~/git/lcod-rag
export OLLAMA_BASE_URL=${OLLAMA_BASE_URL:-http://127.0.0.1:11434}
export QDRANT_URL=${QDRANT_URL:-http://127.0.0.1:6333}
export QDRANT_COLLECTION=${QDRANT_COLLECTION:-lcod_docs}
export RAG_EMBED_MODEL=${RAG_EMBED_MODEL:-nomic-embed-text}

lcod-run --compose packages/rag/components/ingest.run_pipeline/compose.yaml
```

- Make sure the `lcod-run` binary (>= 0.1.12) is available on the server PATH.
- Set `QDRANT_API_KEY`, `QDRANT_DISTANCE`, `OLLAMA_BASE_URL` or any other
  overrides before running the compose.
- The pipeline recreates the collection when the vector size changes. Force a
  clean rebuild by passing `--state '{"recreateCollection": true}'` to
  `lcod-run` if you need to drop the existing data explicitly.

Schedule the ingestion via cron or a systemd timer if you need regular updates.

## 5. Consume the API

`rag-api` exposes the following endpoints:

- `GET /health` → `{ "status": "ok" }`
- `POST /query` → body `{ "query": "…", "top_k": 5 }`
- `POST /ingest` → body `{ "document": "…", "metadata": {"source": "manual"} }`

Example query:

```bash
curl -X POST https://rag.internal.lcod/query \
     -H 'Content-Type: application/json' \
     -d '{"query": "How does the resolver merge catalogue pointers?"}'
```

The response includes:

```json
{
  "answer": "…",
  "contexts": [
    {
      "text": "…",
      "score": 0.87,
      "metadata": {
        "repo": "lcod-spec",
        "path": "docs/resolver/README.md",
        "heading": "Registry scopes"
      }
    }
  ]
}
```

### Open WebUI integration

1. Navigate to *Settings → Tools*.
2. Add a **REST Tool** with POST method and URL `https://rag.internal.lcod/query`.
3. Map the input schema `{ "query": "{{prompt}}" }` so the user prompt is forwarded to RAG.
4. Optionally render contexts in the WebUI response card.

### Dify integration

Create a new **Dataset** in Dify and configure a custom “External Knowledge Base” pointing to `/query`. Use the returned `contexts` array to build message variables or citations.

## 6. Backups & maintenance

- Qdrant data lives in `./data/qdrant`. Include it in the nightly backups of the host.
- Monitor container health with `docker ps` or integrate with the existing Prometheus stack.
- When upgrading dependencies, rebuild the API image: `docker compose build rag-api && docker compose up -d`.
