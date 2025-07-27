from __future__ import annotations
import pandas as pd
import numpy as np

def rebase_to_base_year(df: pd.DataFrame, value_col: str, id_col: str, time_col: str, base_year: int, out_col: str = "rebased") -> pd.DataFrame:
    df = df.copy()
    def _reb(g: pd.DataFrame) -> pd.DataFrame:
        if (g[time_col] == base_year).any():
            base = float(g.loc[g[time_col] == base_year, value_col].iloc[0])
            g[out_col] = g[value_col] / base * 100.0
        else:
            g[out_col] = np.nan
        return g
    return df.groupby(id_col, group_keys=False).apply(_reb)

def weighted_mean(x: pd.Series, w: pd.Series) -> float:
    w = w.astype(float).fillna(0.0)
    x = x.astype(float).fillna(0.0)
    s = w.sum()
    return float((x * w).sum() / s) if s else float("nan")
