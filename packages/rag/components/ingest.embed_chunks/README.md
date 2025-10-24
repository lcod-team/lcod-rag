# lcod://rag/ingest/embed_chunks@0.1.0

Takes the chunked documentation records and resolves embeddings by calling the
Ollama HTTP API (`/api/embeddings`). The component operates sequentially, which
keeps request rates manageable for the default single-instance deployment. Base
URL and model are derived from the inputs, or fall back to the environment
variables `OLLAMA_BASE_URL` / `RAG_EMBED_MODEL`, or finally to sensible defaults
(`http://localhost:11434` and `nomic-embed-text`).

On success each chunk is returned with a `vector` field that contains the
floating-point embedding. Errors are recorded as warnings so hosts can retry or
surface partial results. A `dimension` output indicates the vector size
reported by the first successful response.
