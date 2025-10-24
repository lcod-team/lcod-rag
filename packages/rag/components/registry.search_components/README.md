<!-- AUTO-GENERATED: edit lcp.toml and run scripts/build-component-artifacts.mjs -->
<p><img src="https://api.iconify.design/mdi:text-search.svg?height=48&width=48" alt="Search LCOD registry documentation chunks using a natural language query." width="48" height="48" /></p>

# lcod://rag/registry/search_components@0.1.0

Search LCOD registry documentation chunks using a natural language query.

## Inputs

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | string | Yes | Natural language query used to search component documentation. |
| `topK` | integer \| null | No | Maximum number of matches to return. |
| `scoreThreshold` | number \| null | No | Optional minimum similarity score; lower matches are filtered out. |
| `qdrantUrl` | string \| null | No | Base URL for the Qdrant HTTP API (defaults to $QDRANT_URL or http://localhost:6333). |
| `collection` | string \| null | No | Target Qdrant collection (defaults to $QDRANT_COLLECTION or lcod_docs). |
| `apiKey` | string \| null | No | Optional Qdrant API key forwarded as the `api-key` header. |
| `ollamaBaseUrl` | string \| null | No | Base URL for the Ollama server used to embed the query (defaults to $OLLAMA_BASE_URL or http://localhost:11434). |
| `embeddingModel` | string \| null | No | Name of the Ollama embedding model (defaults to $RAG_EMBED_MODEL, $OLLAMA_EMBED_MODEL or nomic-embed-text). |
| `embeddingTimeoutMs` | integer \| null | No | HTTP timeout in milliseconds for the embedding request. |
| `embeddingMaxRetries` | integer \| null | No | Number of retry attempts for the embedding request. |
| `searchTimeoutMs` | integer \| null | No | HTTP timeout in milliseconds for the Qdrant search request. |
| `filter` | object \| null | No | Optional Qdrant filter object to restrict the search scope. |

## Outputs

| Name | Type | Description |
| --- | --- | --- |
| `matches` | array<object> | Ordered search matches returned by Qdrant (best score first). |
| `matchCount` | integer | Number of matches returned after optional score filtering. |
| `queryVector` | array \| null | Embedding vector produced for the natural language query. |
| `dimension` | integer | Vector dimensionality reported for the query embedding. |
| `warnings` | array | Warnings produced while embedding the query or querying Qdrant. |
| `queryText` | string \| null | Normalised query text forwarded to the embedding request. |

## Notes

Search LCOD registry documentation chunks stored in Qdrant from a natural
language query. The component embeds the query with the same Ollama model used
by the ingestion pipeline, executes a vector search against Qdrant and returns
the scored matches together with their metadata.

### Flow

1. Normalise the incoming query and reject empty payloads.
2. Reuse `lcod://rag/ingest/embed_chunks@0.1.0` to obtain the embedding vector
   from Ollama.
3. Post a `/collections/{collection}/points/search` request to Qdrant
   (defaults to the `QDRANT_URL`/`QDRANT_COLLECTION` environment variables).
4. Filter and return the matches ordered by relevance together with the stored
   payload (component identifiers, documentation metadata, raw chunk text).

### Example

```yaml
compose:
  - call: lcod://rag/registry/search_components@0.1.0
    in:
      query: "How do I merge two objects in LCOD?"
      topK: 8
      scoreThreshold: 0.4
```

The component returns scored matches that IDE helpers can surface to developers
alongside the component identifiers and documentation excerpts.
