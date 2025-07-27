from __future__ import annotations
import pandas as pd

def load_aiie_appendix_b(path: str) -> pd.DataFrame:
    """Load Felten–Raj–Seamans AIIE Appendix B (industry exposure, 4-digit NAICS)."""
    df = pd.read_excel(path, sheet_name="Appendix B")
    df["naics4"] = df["NAICS"].astype(str).str.zfill(4)
    df["naics2"] = df["naics4"].str[:2]
    return df.rename(columns={"AIIE": "exposure"})
