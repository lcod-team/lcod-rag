# lcod://rag/registry/normalize_component@0.1.0

Normalises a registry catalogue record (plus its source metadata) into a component
entry ready for ingestion.

Inputs:

- `record` — raw registry record (typically from catalogues JSONL).
- `source` — metadata for the registry source (contains defaults, priority, etc.).

Outputs:

- `component` — normalised entry (`null` when id/version are missing).
- `warnings` — array of warning strings (missing required fields, malformed entries).
