from __future__ import annotations
import yaml
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class DashboardConfig:
    paths: Dict[str, str]
    indicators: Dict[str, Any]
    models: Dict[str, Any]
    alerts: Dict[str, Any]

def load_config(path: str) -> DashboardConfig:
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    return DashboardConfig(**cfg)
