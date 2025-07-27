from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, Any

@dataclass
class DataSource:
    code: str
    name: str
    loader: Callable[..., Any]
    description: str = ""

class Registry:
    def __init__(self) -> None:
        self._sources: Dict[str, DataSource] = {}

    def register(self, src: DataSource) -> None:
        self._sources[src.code] = src

    def get(self, code: str) -> DataSource:
        return self._sources[code]

    def list(self) -> Dict[str, DataSource]:
        return dict(self._sources)

registry = Registry()
