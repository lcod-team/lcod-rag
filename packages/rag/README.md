# rag workspace package

Utility components used by the LCOD RAG ingestion pipeline.

Components:

- `lcod://rag/jsonl/parse_objects@0.1.0` — parse JSON Lines into objects and capture malformed entries.
- `lcod://rag/array/compact@0.1.0` — remove `null`/`undefined` entries from an array.
- `lcod://rag/array/flatten@0.1.0` — flatten a shallow array of arrays.
- `lcod://rag/array/pluck@0.1.0` — pluck a field from each object in a list.
- `lcod://rag/registry/normalize_component@0.1.0` — normalise registry catalogue records into ingestion-friendly entries.
- `lcod://rag/registry/collect_components@0.1.0` — main flow turning `catalogues.json` into component metadata plus warnings.
- `lcod://rag/registry/snapshot_from_components@0.1.0` — build a deterministic snapshot map from the collected components.
- `lcod://rag/registry/diff_snapshots@0.1.0` — compare previous and current snapshots to detect additions, removals and changes.
- `lcod://rag/registry/snapshot_read@0.1.0` — load an on-disk snapshot (if present) with warnings for missing/invalid files.
- `lcod://rag/registry/snapshot_write@0.1.0` — persist the snapshot JSON only when the content changes.
- `lcod://rag/registry/prepare_ingestion@0.1.0` — drive the snapshot read → collect → diff orchestration before embedding updates.
