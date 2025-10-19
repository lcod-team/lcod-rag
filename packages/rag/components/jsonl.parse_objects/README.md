# lcod://rag/jsonl/parse_objects@0.1.0

Parses JSON Lines (JSONL) content and returns the objects that could be decoded.

Inputs:

- `text` — string containing zero or more newline-separated JSON objects.

Outputs:

- `items` — array of decoded objects (non-object entries are ignored).
- `warnings` — array of warning strings describing malformed or skipped lines.
