from __future__ import annotations

import logging
from fastapi import FastAPI, HTTPException

from .config import get_settings, CollectionMetadata
from .llm import embed_texts, generate_answer
from .models import QueryRequest, QueryResponse, ContextChunk, IngestRequest, HealthResponse
from .vector_store import search, ensure_collection, upsert_documents

logger = logging.getLogger("rag-api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="LCOD RAG API", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse()


@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest) -> QueryResponse:
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")
    settings = get_settings()
    top_k = request.top_k or settings.top_k

    embeddings = embed_texts([request.query])
    ensure_collection(len(embeddings[0]))
    points = search(embeddings[0], limit=top_k)

    contexts = []
    ordered_texts = []
    for point in points:
        payload = point.payload or {}
        text = payload.get("text", "")
        metadata = {
            "repo": payload.get("repo"),
            "path": payload.get("path"),
            "heading": payload.get("heading"),
            "chunk_index": payload.get("chunk_index"),
        }
        contexts.append(ContextChunk(text=text, score=point.score or 0.0, metadata={k: v for k, v in metadata.items() if v is not None}))
        ordered_texts.append(text)

    if not contexts:
        return QueryResponse(answer="I do not have enough information yet.", contexts=[])

    answer = generate_answer(request.query, ordered_texts)
    return QueryResponse(answer=answer, contexts=contexts)


@app.post("/ingest")
def ingest_snippet(request: IngestRequest) -> dict[str, str]:
    if not request.document.strip():
        raise HTTPException(status_code=400, detail="Document must not be empty")

    settings = get_settings()
    collection = request.collection or settings.qdrant_collection

    vector = embed_texts([request.document])[0]
    ensure_collection(len(vector))
    metadata = CollectionMetadata(**request.metadata)
    upsert_documents([(request.document, vector, metadata)])
    return {"status": "ok", "collection": collection}
