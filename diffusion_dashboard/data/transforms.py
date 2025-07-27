from __future__ import annotations
import pandas as pd
import numpy as np
from ..utils import weighted_mean

def aggregate_exposure_to_naics2(exposure_df: pd.DataFrame, weights_df: pd.DataFrame | None = None,
                                 exp_code_col: str = "naics4", exp_val_col: str = "exposure",
                                 w_naics_col: str = "naics4", w_emp_col: str = "employment") -> pd.DataFrame:
    """Aggregate 4-digit NAICS exposure to 2-digit. If weights_df is provided, use employment weights."""
    df = exposure_df.copy()
    df["naics2"] = df["naics4"].astype(str).str[:2]
    if weights_df is None:
        g = df.groupby("naics2")[exp_val_col].mean().reset_index().rename(columns={exp_val_col: "exposure"})
        return g
    w = weights_df.copy()
    w["naics4"] = w[w_naics_col].astype(str).str.zfill(4)
    m = df.merge(w[["naics4", w_emp_col]], on="naics4", how="left")
    m["naics2"] = m["naics4"].str[:2]
    out = m.groupby("naics2").apply(lambda g: weighted_mean(g[exp_val_col], g[w_emp_col])).reset_index(name="exposure")
    return out

def form_cohorts(panel_df: pd.DataFrame, exposure_df: pd.DataFrame, sector_col: str, time_col: str, value_col: str, split: str = "median") -> pd.DataFrame:
    m = panel_df.merge(exposure_df.rename(columns={"naics2": sector_col}), on=sector_col, how="left")
    if split == "median":
        thr = m["exposure"].median()
    else:
        thr = float(split)
    m["group"] = np.where(m["exposure"] >= thr, "High exposure", "Low exposure")
    stats = m.groupby(["group", time_col])[value_col].agg(["mean", "count", "std"]).reset_index()
    stats["se"] = stats["std"] / np.sqrt(stats["count"])
    return stats
