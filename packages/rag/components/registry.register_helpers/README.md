# lcod://rag/registry/register_helpers@0.1.0

Registers the rag workspace components (array utilities, snapshot helpers, etc.) so that other compositions can call them by ID.

Inputs:
- `ragRoot` — path to the `lcod-rag` project root.

Outputs:
- `registered` — number of components registered.
- `warnings` — registration warnings (missing files, etc.).
