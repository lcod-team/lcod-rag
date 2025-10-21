# lcod://rag/registry/collect_components@0.1.0

End-to-end flow that reads an LCOD registry pointer (`catalogues.json`), resolves
the catalogues using helpers from `lcod-spec`, registers the local RAG helpers,
and returns normalised component entries ready for ingestion.

Inputs (all optional):

- `projectPath` — base directory for resolving catalogue paths (defaults to the compose directory).
- `cataloguesUrl` — HTTP(S) URL for the registry pointer (defaults to the official `lcod-registry` catalogue URL).
- `cataloguesPath` — local override for the pointer file.
- `sourceId` — identifier for the synthetic registry source (defaults to `catalogues`).
- `cacheDir` — cache directory for downloaded catalogues.
- `cwd` — working directory forwarded to helper calls (defaults to `projectPath`).
- `specRoot` — optional path to a local `lcod-spec` checkout (only used when dereferencing relative manifest paths).
- `ragRoot` — path to the `lcod-rag` checkout (used to register helper components).

Outputs:

- `components` — array of normalised entries `{ componentId, version, registryId, priority, sha256, manifest, manifestPath, manifestUrl }`.
- `warnings` — array of warning strings raised while registering helper components, resolving catalogues, or normalising entries.
- `componentCount` — number of components extracted across all catalogues.
- `cataloguesCount` — number of catalogue manifests successfully processed.
