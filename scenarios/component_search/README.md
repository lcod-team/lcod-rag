# Component search scenario

Run this scenario to exercise `lcod://rag/registry/search_components@0.1.0` end to
end. It expects Qdrant and Ollama to be reachable (the default configuration
matches the `docker-compose.yml` stack in this repository).

Example:

```bash
lcod-run \
  --compose scenarios/component_search/compose.yaml \
  --input '{"query": "Find the merge helper"}'
```

The scenario outputs a small summary containing the number of matches, the first
hit (including metadata) and any warnings returned by the component.
