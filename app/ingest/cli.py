from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

import typer

from app.rag_api.ingest import ingest_documents, load_environment
from app.rag_api.config import get_settings
from .sources import load_sources

app = typer.Typer(help="LCOD RAG ingestion CLI")
logger = logging.getLogger("rag-ingest")
logging.basicConfig(level=logging.INFO)


@app.command()
def run(
    config: Path = typer.Option(Path("config/sources.yaml"), exists=True, readable=True, show_default=True),
    collection: Optional[str] = typer.Option(None, "--collection", "-c", help="Override collection name"),
    recreate: bool = typer.Option(False, "--recreate", help="Drop and recreate the collection", is_flag=True),
) -> None:
    """Run a full ingestion based on the YAML configuration file."""
    load_environment()
    if collection:
        os.environ["QDRANT_COLLECTION"] = collection
        get_settings.cache_clear()  # type: ignore[attr-defined]
    sources = load_sources(config)
    documents: list[tuple[str, str, str]] = []
    for source in sources:
        for repo, path in source.iter_files():
            text = path.read_text(encoding="utf-8")
            documents.append((repo, str(path), text))

    if not documents:
        typer.echo("No documents found – check your config paths")
        raise typer.Exit(code=1)

    target_collection = collection or get_settings().qdrant_collection

    if recreate:
        from qdrant_client import QdrantClient

        client = QdrantClient(url=get_settings().qdrant_url, api_key=get_settings().qdrant_api_key or None)
        try:
            client.delete_collection(target_collection)
        except Exception:
            pass
    ingest_documents(documents)
    typer.echo(f"Ingested {len(documents)} documents into {target_collection}")


if __name__ == "__main__":
    app()
