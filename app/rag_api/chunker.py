from __future__ import annotations

from pathlib import Path
from typing import Iterable

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)


def iter_markdown_files(base: Path, patterns: Iterable[str]) -> Iterable[Path]:
    for pattern in patterns:
        for path in base.glob(pattern):
            if path.is_file():
                yield path
