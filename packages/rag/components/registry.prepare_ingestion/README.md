# lcod://rag/registry/prepare_ingestion@0.1.0

Orchestrates the registry pre-ingestion flow: load previous snapshot, collect
current components, compute the new snapshot and the diff.

Inputs:

- `projectPath`, `cataloguesPath`, `sourceId`, `cacheDir`, `cwd` — forwarded to `registry.collect_components`.
- `specRoot` — path to `lcod-spec`.
- `ragRoot` — path to `lcod-rag` (used to register local helpers).
- `snapshotPath` — path to the snapshot JSON on disk.
- `missingSnapshotWarning` (optional) — warning emitted when the snapshot is absent.

Outputs:

- `components` — normalized component list from the registry.
- `snapshot` / `snapshotEntries` — structures produced by `registry.snapshot_from_components`.
- `diff` — `{ added, removed, updated, unchanged }` from `registry.diff_snapshots`.
- `previousExists` — boolean indicating whether a snapshot was previously stored.
- `warnings` — combined warnings from reading the snapshot and collecting components.
