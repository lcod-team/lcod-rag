# lcod://rag/registry/register_helpers@0.1.0

Registers the RAG workspace components (array utilities, snapshot helpers, documentation fetcher, …) so that ingestion flows can call them via their canonical IDs.

Inputs:
- `ragRoot` — path to the `lcod-rag` project root.

Outputs:
- `helperRegistered` — number of helper components registered in the resolver.
- `helperWarnings` — registration warnings (missing files, invalid manifests, …).
