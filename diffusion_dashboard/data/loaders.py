from __future__ import annotations
import pandas as pd

def load_csv(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, **kwargs)

def load_excel(path: str, sheet_name: str = 0, **kwargs) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet_name, **kwargs)
