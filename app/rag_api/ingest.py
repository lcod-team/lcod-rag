from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv

from .config import CollectionMetadata, get_settings
from .chunker import chunk_text
from .llm import embed_texts
from .vector_store import ensure_collection, upsert_documents

logger = logging.getLogger(__name__)


def load_environment() -> None:
    """Load config/.env if present (no-op during API runtime where pydantic already reads it)."""
    load_dotenv("config/.env", override=False)


def ingest_documents(documents: Iterable[tuple[str, str, str]]) -> None:
    """
    Ingest an iterable of (repo, path, content) tuples.
    """
    load_environment()
    settings = get_settings()

    chunks: list[tuple[str, CollectionMetadata]] = []
    for repo, path, content in documents:
        splitted = chunk_text(content)
        for idx, chunk in enumerate(splitted):
            metadata = CollectionMetadata(repo=repo, path=path, chunk_index=idx)
            chunks.append((chunk, metadata))

    if not chunks:
        logger.info("No documents to ingest")
        return

    texts = [chunk for chunk, _ in chunks]
    vectors = embed_texts(texts)
    ensure_collection(len(vectors[0]))
    upsert_documents(((chunk, vector, metadata) for (chunk, metadata), vector in zip(chunks, vectors)))
    logger.info("Ingested %s chunks into collection %s", len(chunks), settings.qdrant_collection)


def ingest_file(path: Path, repo: str) -> None:
    content = path.read_text(encoding="utf-8")
    ingest_documents([(repo, str(path), content)])
