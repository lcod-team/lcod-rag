# lcod://rag/ingest/upsert_chunks@0.1.0

Takes embedded chunk records and pushes them to Qdrant using the `/points`
endpoint. Payloads include the original chunk metadata together with the raw
text so downstream applications can display excerpts without an additional
lookup. Data is uploaded in configurable batches (default 32 points per
request). Any HTTP failures are captured as warnings so operators can retry or
inspect the problematic batch.
