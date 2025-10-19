# lcod://rag/registry/collect_components@0.1.0

End-to-end flow that reads an LCOD registry pointer (`catalogues.json`), resolves
the catalogues using helpers from `lcod-spec`, registers the local RAG helpers,
and returns normalised component entries ready for ingestion.

Inputs:

- `projectPath` — base directory for resolving catalogue paths (defaults to `.`).
- `cataloguesPath` — path to the `catalogues.json` pointer (defaults to `catalogues.json`).
- `sourceId` — identifier for the synthetic registry source (defaults to `catalogues`).
- `cacheDir` — optional cache directory for downloaded catalogues.
- `cwd` — optional working directory.
- `specRoot` — path to the `lcod-spec` checkout.
- `ragRoot` — path to the `lcod-rag` checkout (for registering local components).

Outputs:

- `components` — array of normalised entries `{ componentId, version, registryId, priority, sha256, manifest, manifestPath, manifestUrl }`.
- `warnings` — array of warning strings raised while registering helper components, resolving catalogues, or normalising entries.
