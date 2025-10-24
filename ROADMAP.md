# Roadmap

## Current Focus

- [x] Implement LCOD-based ingestion pipeline ([#3](https://github.com/lcod-team/lcod-rag/issues/3))
- [x] Deliver embeddings and Qdrant upsert via lcdrun pipeline ([#4](https://github.com/lcod-team/lcod-rag/issues/4))

## Next Ideas

- [ ] Automate nightly ingestion runs from nucone.local (cron/systemd)
- [ ] Expose ingestion metrics (vector count, upsert delta) to monitoring
- [ ] Build a component search helper (Ollama embedding + Qdrant query contract)
