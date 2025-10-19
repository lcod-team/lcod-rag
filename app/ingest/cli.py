from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

from app.rag_api.config import get_settings
from app.rag_api.ingest import ingest_documents, load_environment
from .sources import load_sources

logger = logging.getLogger("rag-ingest")
logging.basicConfig(level=logging.INFO)


def main() -> None:
    parser = argparse.ArgumentParser(description="LCOD RAG ingestion CLI")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/sources.yaml"),
        help="Path to the ingestion configuration file",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default=None,
        help="Override the Qdrant collection name",
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Drop the collection before inserting new documents",
    )
    args = parser.parse_args()

    load_environment()
    if not args.config.exists():
        parser.error(f"Config file {args.config} does not exist")

    if args.collection:
        os.environ["QDRANT_COLLECTION"] = args.collection
        get_settings.cache_clear()  # type: ignore[attr-defined]

    sources = load_sources(args.config)
    documents: list[tuple[str, str, str]] = []
    for source in sources:
        for repo, path in source.iter_files():
            text = path.read_text(encoding="utf-8")
            documents.append((repo, str(path), text))

    if not documents:
        parser.error("No documents found – check your config paths")

    if args.recreate:
        from qdrant_client import QdrantClient

        settings = get_settings()
        client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
        try:
            client.delete_collection(settings.qdrant_collection)
        except Exception:
            pass

    ingest_documents(documents)


if __name__ == "__main__":
    main()
