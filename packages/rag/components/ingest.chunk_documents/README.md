# lcod://rag/ingest/chunk_documents@0.1.0

Splits documentation records into fixed-size text chunks suitable for embedding.
The component expects the objects emitted by
`lcod://rag/ingest/extract_documents@0.1.0`. Chunks are generated with a simple
sliding window measured in characters; by default each chunk spans up to 1000
characters with a 200-character overlap to preserve context across boundaries.

Metadata from the original document is preserved on each chunk together with the
chunk index and total chunk count so downstream systems can reconstruct the
original source. Empty or whitespace-only documents are skipped with a warning.
