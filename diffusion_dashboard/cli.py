from __future__ import annotations
import argparse, os
import pandas as pd
from .utils import rebase_to_base_year
from .data.exposure import load_aiie_appendix_b
from .data.transforms import aggregate_exposure_to_naics2
from .models.did import did_continuous, event_study
from .metrics.indicators import compute_group_stats
from .viz.plots import plot_group_means, plot_event_study

def run(prod_csv: str, aiie_xlsx: str, outdir: str = "./outputs", sector_col: str="sector"):
    os.makedirs(outdir, exist_ok=True)

    # 1) Load productivity panel and rebase
    prod = pd.read_csv(prod_csv)
    prod = rebase_to_base_year(prod, value_col="value", id_col=sector_col, time_col="year", base_year=2019, out_col="rebased")

    # 2) Exposure (unweighted to 2-digit sector; replace with weights if available)
    exp4 = load_aiie_appendix_b(aiie_xlsx)
    exp2 = exp4.groupby("naics2")["exposure"].mean().reset_index().rename(columns={"naics2": sector_col})

    panel = prod.merge(exp2, on=sector_col, how="left").dropna(subset=["rebased","exposure"])
    panel["post"] = (panel["year"] >= 2022).astype(int)

    # 3) DiD and event study
    res = did_continuous(panel, y="rebased", exposure="exposure", post="post", id_col=sector_col, time_col="year", cluster=sector_col)
    with open(os.path.join(outdir, "did_summary.txt"), "w") as f:
        f.write(str(res.summary()))

    ev_res, ev_df = event_study(panel, y="rebased", exposure="exposure", year_col="year", base_year=2019, id_col=sector_col, cluster=sector_col)
    ev_df.to_csv(os.path.join(outdir, "event_study_coefs.csv"), index=False)

    # 4) Figures
    median = panel["exposure"].median()
    panel["group"] = (panel["exposure"] >= median).map({True:"High exposure", False:"Low exposure"})
    stats = compute_group_stats(panel, value_col="rebased", group_col="group", time_col="year")
    fig1, _ = plot_group_means(stats, time_col="year", title="Labour productivity by AI-exposure group", ylabel="Index (2019=100)")
    fig1.savefig(os.path.join(outdir, "group_means.png"), dpi=300, bbox_inches="tight")
    fig2, _ = plot_event_study(ev_df, title="Event-study: exposure × year (baseline 2019 omitted)")
    fig2.savefig(os.path.join(outdir, "event_study.png"), dpi=300, bbox_inches="tight")

    return {"n_panel": len(panel), "outdir": outdir}

def main():
    p = argparse.ArgumentParser(description="Diffusion Dashboard v0.1 pipeline")
    p.add_argument("productivity_csv")
    p.add_argument("aiie_xlsx")
    p.add_argument("--outdir", default="./outputs")
    p.add_argument("--sector-col", default="sector")
    args = p.parse_args()
    run(args.productivity_csv, args.aiie_xlsx, args.outdir, sector_col=args.sector_col)

if __name__ == "__main__":
    main()
