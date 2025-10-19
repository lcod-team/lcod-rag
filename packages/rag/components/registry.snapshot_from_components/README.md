# lcod://rag/registry/snapshot_from_components@0.1.0

Builds a deterministic snapshot structure from the list produced by
`registry.collect_components`.

Inputs:

- `components` — array of component records.

Outputs:

- `snapshot` — object keyed by `"<componentId>@<version>"` storing metadata for each component.
- `entries` — sorted array mirroring the snapshot contents, convenient for diffing/serialization.
