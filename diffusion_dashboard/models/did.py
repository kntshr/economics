from __future__ import annotations
import pandas as pd
import statsmodels.formula.api as smf

def did_continuous(df: pd.DataFrame, y: str, exposure: str, post: str, id_col: str, time_col: str, cluster: str = None):
    df = df.copy()
    term = f"{exposure}:{post}"
    formula = f"{y} ~ {term} + C({id_col}) + C({time_col})"
    if cluster is None:
        res = smf.ols(formula, data=df).fit()
    else:
        res = smf.ols(formula, data=df).fit(cov_type="cluster", cov_kwds={"groups": df[cluster]})
    return res

def event_study(df: pd.DataFrame, y: str, exposure: str, year_col: str, base_year: int, id_col: str, cluster: str = None):
    df = df.copy()
    years = sorted(df[year_col].unique())
    terms = []
    for yr in years:
        if yr == base_year:
            continue
        nm = f"exp_y_{yr}"
        df[nm] = (df[year_col] == yr).astype(int) * df[exposure]
        terms.append(nm)
    formula = f"{y} ~ {' + '.join(terms)} + C({id_col}) + C({year_col})"
    if cluster is None:
        res = smf.ols(formula, data=df).fit()
    else:
        res = smf.ols(formula, data=df).fit(cov_type="cluster", cov_kwds={"groups": df[cluster]})
    import pandas as pd
    coefs = res.params[[t for t in terms if t in res.params]]
    ses = res.bse[[t for t in terms if t in res.bse]]
    out = pd.DataFrame({ "year": [int(t.split('_')[-1]) for t in coefs.index], "beta": coefs.values, "se": ses.values }).sort_values("year")
    return res, out
