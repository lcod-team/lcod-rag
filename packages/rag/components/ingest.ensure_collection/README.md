# lcod://rag/ingest/ensure_collection@0.1.0

Creates or updates the target Qdrant collection before ingesting new vectors.
The component inspects the current collection configuration and recreates it
when the stored vector size differs from the expected dimensionality or when the
`recreate` flag is set. Authentication is handled through the optional
`apiKey` input (forwarded as the `api-key` header).

A status string is returned to help pipelines log whether the collection was
created, reused, or recreated.
