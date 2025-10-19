from __future__ import annotations

import yaml
from pathlib import Path
from typing import Iterable

from app.rag_api.chunker import iter_markdown_files


class SourceEntry:
    def __init__(self, name: str, base_path: Path, patterns: list[str]):
        self.name = name
        self.base_path = base_path
        self.patterns = patterns

    def iter_files(self) -> Iterable[tuple[str, Path]]:
        for path in iter_markdown_files(self.base_path, self.patterns):
            yield self.name, path


def load_sources(path: Path) -> list[SourceEntry]:
    data = yaml.safe_load(path.read_text())
    entries: list[SourceEntry] = []
    for repo in data.get("repositories", []):
        name = repo.get("name")
        base = Path(repo.get("path", ""))
        include = repo.get("include", ["**/*.md"])
        if not name or not base.exists():
            continue
        entries.append(SourceEntry(name=name, base_path=base, patterns=include))
    return entries
