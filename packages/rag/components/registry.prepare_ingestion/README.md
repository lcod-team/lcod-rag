# lcod://rag/registry/prepare_ingestion@0.1.0

Orchestrates the registry pre-ingestion flow: load previous snapshot, collect
current components, compute the new snapshot and the diff.

Inputs (all optional unless noted):

- `ragRoot` — base directory of the `lcod-rag` checkout (defaults to the compose directory).
- `projectPath` / `cwd` — forwarded to `registry.collect_components` (default to `ragRoot`).
- `cataloguesUrl` — catalogue pointer URL (defaults to the official `lcod-registry` JSON).
- `cataloguesPath` — local override for the catalogue pointer.
- `cacheDir` — cache directory for downloaded assets (defaults to `<ragRoot>/.lcod/cache`).
- `sourceId` — forwarded to `registry.collect_components`.
- `specRoot` — optional path to a local `lcod-spec` checkout (only used when reading manifests from disk).
- `snapshotPath` — file used to persist the registry snapshot (defaults to `<ragRoot>/data/registry.snapshot.json`).
- `missingSnapshotWarning` — warning emitted when the snapshot is absent.

Outputs:

- `components` — normalized component list from the registry.
- `snapshot` / `snapshotEntries` — structures produced by `registry.snapshot_from_components`.
- `diff` — `{ added, removed, updated, unchanged }` from `registry.diff_snapshots`.
- `previousExists` — boolean indicating whether a snapshot was previously stored.
- `warnings` — combined warnings from reading the snapshot and collecting components.
- `componentCount` — number of components returned by the ingestion flow.
- `cataloguesCount` — number of catalogue entries processed.
- `snapshotPath` — resolved path used for reading/writing the snapshot file.
