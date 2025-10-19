from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., description="User natural-language query")
    top_k: int | None = Field(default=None, ge=1, le=20, description="Override default number of contexts")


class ContextChunk(BaseModel):
    text: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    answer: str
    contexts: list[ContextChunk]


class IngestRequest(BaseModel):
    document: str = Field(..., description="Raw text to ingest")
    metadata: dict[str, Any] = Field(default_factory=dict)
    collection: str | None = None


class HealthResponse(BaseModel):
    status: str = "ok"
