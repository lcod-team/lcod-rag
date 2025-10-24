# lcod://rag/ingest/extract_documents@0.1.0

Transforms the registry snapshot produced by `lcod://rag/registry/prepare_ingestion@0.1.0`
into flat documentation records. Each record keeps the originating component
identifier, doc label (for example `readme`), optional source URL and commit, and
the raw markdown text. The component ignores documentation entries that do not
carry textual content unless `includeEmpty` is set to `true`.

Returned objects follow the shape:

```json
{
  "componentId": "lcod://namespace/name@1.2.3",
  "version": "1.2.3",
  "docKey": "readme",
  "text": "...markdown...",
  "repo": "https://github.com/org/repo",
  "commit": "abcdef0",
  "docUrl": "https://raw.githubusercontent.com/org/repo/abcdef0/path/README.md",
  "manifest": "packages/foo/lcp.toml",
  "composePath": "packages/foo/compose.yaml",
  "source": {
    "registryId": "catalogues",
    "priority": 10
  }
}
```

The component also aggregates warnings for entries that are missing a
`documentation` block so hosts can surface incomplete catalogue records.
