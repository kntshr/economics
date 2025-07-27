from __future__ import annotations
import pandas as pd

def compute_group_stats(panel: pd.DataFrame, value_col: str, group_col: str, time_col: str) -> pd.DataFrame:
    g = panel.groupby([group_col, time_col])[value_col].agg(['mean','count','std']).reset_index()
    g['se'] = g['std'] / g['count']**0.5
    return g
