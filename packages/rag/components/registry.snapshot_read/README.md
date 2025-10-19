# lcod://rag/registry/snapshot_read@0.1.0

Reads a snapshot JSON file if it exists and returns a normalized object along
with warnings.

Inputs:

- `path` — filesystem path to the snapshot JSON.
- `warningMessage` (optional) — message to include when the file is missing.

Outputs:

- `snapshot` — object loaded from disk (empty object when missing/invalid).
- `exists` — boolean indicating if the file was found.
- `warnings` — array of warning strings (missing file, parse errors, etc.).
