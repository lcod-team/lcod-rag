# lcod://rag/registry/snapshot_write@0.1.0

Writes the snapshot object to disk (JSON) only when the contents change.

Inputs:

- `path` — destination file path.
- `snapshot` — object to serialize.

Outputs:

- `changed` — boolean indicating whether the file was rewritten.
