from __future__ import annotations

import logging
from typing import Iterable
import requests

from .config import get_settings

logger = logging.getLogger(__name__)


def embed_texts(chunks: Iterable[str]) -> list[list[float]]:
    settings = get_settings()
    base_url = settings.ollama_base_url.rstrip("/")
    url = f"{base_url}/api/embeddings"
    vectors: list[list[float]] = []
    for chunk in chunks:
        payload = {"model": settings.embedding_model, "prompt": chunk}
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        vector = data.get("embedding") or data.get("data", [{}])[0].get("embedding")
        if not isinstance(vector, list):
            raise ValueError("Ollama embedding response malformed")
        vectors.append(vector)
    return vectors


def generate_answer(question: str, contexts: list[str]) -> str:
    settings = get_settings()
    base_url = settings.ollama_base_url.rstrip("/")
    url = f"{base_url}/api/generate"
    context_prompt = "\n\n".join(contexts)
    prompt = (
        "You are an assistant for LCOD developers. Use the documentation snippets to answer the question. "
        "If the answer is not present, say you don't know.\n\n"
        f"Context:\n{context_prompt}\n\nQuestion: {question}\nAnswer:"
    )
    response = requests.post(url, json={"model": settings.generative_model, "prompt": prompt, "stream": False}, timeout=120)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, dict) and "response" in data:
        return data["response"].strip()
    if isinstance(data, dict) and "data" in data:
        # Streaming responses aggregated by Ollama >=0.1.44
        return "".join(chunk.get("response", "") for chunk in data["data"]).strip()
    raise ValueError("Unexpected response from Ollama generate API")
