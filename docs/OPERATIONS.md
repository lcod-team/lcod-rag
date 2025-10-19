# Operations Guide

This document describes how to deploy and operate the LCOD RAG stack on `nucone.local`.

## 1. Clone & sync repositories

```bash
ssh nucone.local
mkdir -p ~/git
cd ~/git
# Clone the LCOD repositories that will feed the RAG index
for repo in lcod-spec lcod-resolver lcod-components lcod-kernel-js lcod-kernel-rs; do
  if [ ! -d "$repo" ]; then
    git clone git@github.com:lcod-team/$repo.git
  else
    (cd $repo && git pull --ff-only)
  fi
done
# Clone the rag stack itself
if [ ! -d lcod-rag ]; then
  git clone git@github.com:lcod-team/lcod-rag.git
fi
```

Keep the repositories up-to-date (daily cron or manual pull) so ingestion reflects the latest documentation.

## 2. Configure the stack

1. Copy sample configuration files:

   ```bash
   cd ~/git/lcod-rag
   cp config/sources.example.yaml config/sources.yaml
   cp config/.env.example config/.env
   ```

2. Edit `config/sources.yaml` and update the `path` entries to match `/home/<user>/git/<repo>`.
3. Review `config/.env` and adjust models/collection names if necessary.

## 3. Deploy services

Use Docker Compose to start the vector store and API:

```bash
cd ~/git/lcod-rag
docker compose up -d
```

The stack creates a dedicated Docker network (`lcod-rag_default`) and persists Qdrant data under `./data/qdrant` (bind-mounted on the host). Port `8088` is exposed for the API.

### Integration with Traefik

If the server already runs Traefik, add the following snippet to `docker-compose.override.yml` to route traffic (example: expose as `rag.nucone.local`):

```yaml
services:
  rag-api:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.lcod-rag.rule=Host(`rag.nucone.local`)"
      - "traefik.http.routers.lcod-rag.entrypoints=websecure"
      - "traefik.http.routers.lcod-rag.tls.certresolver=letsencrypt"
      - "traefik.http.services.lcod-rag.loadbalancer.server.port=8088"
```

Restart the compose stack afterwards.

## 4. Run an ingestion pass

```bash
cd ~/git/lcod-rag
source .venv/bin/activate  # if you created a virtualenv
OLLAMA_BASE_URL=http://127.0.0.1:11434 \
QDRANT_URL=http://127.0.0.1:6333 \
python -m app.ingest.cli --config config/sources.yaml --collection lcod_docs --recreate
```

- `--recreate` drops and re-creates the Qdrant collection (useful when schema changes).
- The example above overrides the Ollama/Qdrant URLs for host execution. When running inside Docker, keep the defaults (`http://host.docker.internal:11434` and `http://qdrant:6333`).

Schedule the ingestion via cron or a systemd timer if you need regular updates.

## 5. Consume the API

`rag-api` exposes the following endpoints:

- `GET /health` → `{ "status": "ok" }`
- `POST /query` → body `{ "query": "…", "top_k": 5 }`
- `POST /ingest` → body `{ "document": "…", "metadata": {"source": "manual"} }`

Example query:

```bash
curl -X POST https://rag.nucone.local/query \
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
2. Add a **REST Tool** with POST method and URL `https://rag.nucone.local/query`.
3. Map the input schema `{ "query": "{{prompt}}" }` so the user prompt is forwarded to RAG.
4. Optionally render contexts in the WebUI response card.

### Dify integration

Create a new **Dataset** in Dify and configure a custom “External Knowledge Base” pointing to `/query`. Use the returned `contexts` array to build message variables or citations.

## 6. Backups & maintenance

- Qdrant data lives in `./data/qdrant`. Include it in the nightly backups of `nucone.local`.
- Monitor container health with `docker ps` or integrate with the existing Prometheus stack.
- When upgrading dependencies, rebuild the API image: `docker compose build rag-api && docker compose up -d`.
