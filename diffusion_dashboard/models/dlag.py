from __future__ import annotations
import pandas as pd
import numpy as np
import statsmodels.api as sm

def distributed_lag(y: pd.Series, X: pd.DataFrame, lags: int, add_const: bool = True):
    df = pd.concat([y, X], axis=1)
    cols = []
    for col in X.columns:
        for L in range(0, lags + 1):
            df[f"{col}_L{L}"] = df[col].shift(L)
            cols.append(f"{col}_L{L}")
    df = df.dropna()
    Y = df[y.name]
    Xd = df[cols]
    if add_const:
        Xd = sm.add_constant(Xd)
    model = sm.OLS(Y, Xd).fit(cov_type="HAC", cov_kwds={"maxlags": max(1, lags)})
    return model
