# rag workspace package

Utility components used by the LCOD RAG ingestion pipeline.

Components:

- `lcod://rag/jsonl/parse_objects@0.1.0` — parse JSON Lines into objects and capture malformed entries.
- `lcod://rag/array/compact@0.1.0` — remove `null`/`undefined` entries from an array.
- `lcod://rag/array/flatten@0.1.0` — flatten a shallow array of arrays.
- `lcod://rag/array/pluck@0.1.0` — pluck a field from each object in a list.
- `lcod://rag/registry/normalize_component@0.1.0` — normalise registry catalogue records into ingestion-friendly entries.
- `lcod://rag/registry/load_manifest_records@0.1.0` — fetch catalogue manifests from disk or HTTP and return raw records.
- `lcod://rag/registry/collect_components@0.1.0` — main flow turning `catalogues.json` into component metadata plus warnings.
- `lcod://rag/registry/fetch_component_docs@0.1.0` — download README snippets for each component based on its source metadata.
- `lcod://rag/registry/search_components@0.1.0` — embed a natural language query and run a Qdrant vector search to retrieve relevant component documentation.
- `lcod://rag/registry/register_helpers@0.1.0` — register the rag workspace helper components for the current run.
- `lcod://rag/registry/snapshot_from_components@0.1.0` — build a deterministic snapshot map from the collected components.
- `lcod://rag/registry/diff_snapshots@0.1.0` — compare previous and current snapshots to detect additions, removals and changes.
- `lcod://rag/registry/snapshot_read@0.1.0` — load an on-disk snapshot (if present) with warnings for missing/invalid files.
- `lcod://rag/registry/snapshot_write@0.1.0` — persist the snapshot JSON only when the content changes.
- `lcod://rag/registry/prepare_ingestion@0.1.0` — drive the snapshot read → collect → diff orchestration before embedding updates.
- `lcod://rag/registry/refresh_snapshot@0.1.0` — run the ingestion flow and update the snapshot on disk in a single command.
