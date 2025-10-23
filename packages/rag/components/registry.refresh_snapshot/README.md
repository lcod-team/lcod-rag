# lcod://rag/registry/refresh_snapshot@0.1.0

Convenience wrapper that collects the registry catalogues and immediately
persists the resulting snapshot to disk. It delegates to
`registry.prepare_ingestion@0.1.0` for the heavy lifting and reuses
`registry.snapshot_write@0.1.0` to update the JSON file only when the content
changes.

Inputs (all optional unless noted):

- `ragRoot`, `projectPath`, `cwd` — forwarded to `registry.prepare_ingestion`.
- `cataloguesUrl`, `cataloguesPath` — source of the LCOD catalogues pointer.
- `sourceId`, `repoRoots`, `specRoot`, `cacheDir` — advanced overrides kept for
  parity with the underlying compose.
- `snapshotPath` — target file for the snapshot (defaults to
  `<ragRoot>/data/registry.snapshot.json`).
- `missingSnapshotWarning` — custom warning message when the snapshot file does
  not exist yet.

Outputs:

- `components` — component list returned by `registry.prepare_ingestion`.
- `snapshot` / `snapshotEntries` — values returned by
  `registry.prepare_ingestion`.
- `diff` — `{ added, removed, updated, unchanged }` entries relative to the
  previous snapshot.
- `previousExists` — boolean indicating whether a snapshot file was previously present.
- `componentCount`, `cataloguesCount` — summary counts for quick reporting.
- `snapshotPath` — resolved path passed to `snapshot_write`.
- `snapshotWritten` — boolean indicating whether the file changed on disk.
- `warnings` — aggregated warnings from the ingestion flow.
