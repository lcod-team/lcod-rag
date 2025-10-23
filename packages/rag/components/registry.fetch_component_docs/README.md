# lcod://rag/registry/fetch_component_docs@0.1.0

Fetches documentation snippets for a registry component using the metadata
available during ingestion. The component currently supports repositories hosted
on GitHub and downloads the README that sits next to the component definition.

Inputs:

- `component` — normalized registry entry (`componentId`, `composePath`,
  `sourceRepo`, `sourceMetadata.commit`, ...).

Outputs:

- `component` — same structure, enriched with `documentation.readme` (when
  available).
- `warnings` — list of non-fatal issues (missing repo/commit, README not found,
  unsupported host, ...).

When the repository or commit cannot be resolved, documentation is omitted and a
warning is returned so that callers can surface the issue or retry later.
