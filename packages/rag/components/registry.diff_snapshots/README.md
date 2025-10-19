# lcod://rag/registry/diff_snapshots@0.1.0

Compares two registry snapshots (objects keyed by `<componentId>@<version>`) and
returns added, removed, updated, and unchanged entries.

Inputs:

- `previous` — snapshot object from the previous ingestion run.
- `current` — snapshot object generated from the latest catalogue.

Outputs:

- `added` — array of entries present only in `current`.
- `removed` — array of entries present only in `previous`.
- `updated` — array of objects `{ previous, current }` where metadata changed.
- `unchanged` — array of entries identical across snapshots.
