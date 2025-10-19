from __future__ import annotations

import logging
from typing import Iterable
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from .config import get_settings, CollectionMetadata

logger = logging.getLogger(__name__)


def _client() -> QdrantClient:
    settings = get_settings()
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)


def ensure_collection(vector_size: int) -> None:
    settings = get_settings()
    client = _client()
    collection = settings.qdrant_collection
    try:
        info = client.get_collection(collection)
        size = info.vector_size or info.config.params.vectors.vector_size  # type: ignore[attr-defined]
        if size != vector_size:
            logger.warning("Collection %s vector size mismatch (%s != %s), recreating.", collection, size, vector_size)
            client.delete_collection(collection)
        else:
            return
    except Exception:  # collection missing
        pass

    client.recreate_collection(
        collection_name=collection,
        vectors_config=qmodels.VectorParams(size=vector_size, distance=qmodels.Distance.COSINE),
    )


def upsert_documents(documents: Iterable[tuple[str, list[float], CollectionMetadata]]) -> None:
    settings = get_settings()
    client = _client()
    payloads = []
    vectors = []
    ids = []
    for text, vector, metadata in documents:
        payload = metadata.model_dump(exclude_none=True)
        payload["text"] = text
        payloads.append(payload)
        vectors.append(vector)
        ids.append(str(uuid4()))

    if not payloads:
        return

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=qmodels.Batch(ids=ids, vectors=vectors, payloads=payloads),
    )


def search(query_vector: list[float], limit: int) -> list[qmodels.ScoredPoint]:
    settings = get_settings()
    client = _client()
    return client.search(
        collection_name=settings.qdrant_collection,
        query_vector=query_vector,
        limit=limit,
        with_payload=True,
    )
