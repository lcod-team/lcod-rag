# lcod://rag/ingest/run_pipeline@0.1.0

Runs the full RAG ingestion flow without relying on the legacy Python
scripts. The compose performs the following steps:

1. `registry.prepare_ingestion` — fetch catalogue entries, resolve manifests,
   and attach documentation.
2. `ingest.extract_documents` — flatten documentation blocks into raw text
   records.
3. `ingest.chunk_documents` — split the text into overlapping chunks.
4. `ingest.embed_chunks` — request embeddings from Ollama.
5. `ingest.ensure_collection` — create or recreate the Qdrant collection.
6. `ingest.upsert_chunks` — push the vectors to Qdrant.

All environment variables that were previously used by the Python CLI are still
honoured (`OLLAMA_BASE_URL`, `QDRANT_URL`, `QDRANT_COLLECTION`, `QDRANT_API_KEY`,
`RAG_EMBED_MODEL`, …) and can be overridden via component inputs. The output
exposes high-level metrics (`componentCount`, `documentCount`, `chunkCount`,
`vectorCount`, `upserted`, `collectionStatus`) together with aggregated
warnings.
