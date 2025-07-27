from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_group_means(stats: pd.DataFrame, time_col: str, mean_col: str="mean", se_col: str="se",
                     group_col: str="group", title: str="", ylabel: str="Index (base=100)"):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for grp, g in stats.groupby(group_col):
        x = g[time_col].values.astype(float)
        m = g[mean_col].values.astype(float)
        se = g[se_col].values.astype(float)
        ax.plot(x, m, marker='o', linewidth=2, label=str(grp))
        ax.fill_between(x, m - 1.96*se, m + 1.96*se, alpha=0.15)
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel(ylabel)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.25)
    return fig, ax

def plot_event_study(df: pd.DataFrame, year_col: str="year", beta_col: str="beta", se_col: str="se",
                     title: str = "Event-study: exposure × year (baseline omitted)"):
    z = 1.96
    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = df[year_col].values.astype(float)
    b = df[beta_col].values.astype(float)
    se = df[se_col].values.astype(float)
    ax.axhline(0, color='black', linewidth=1)
    ax.errorbar(x, b, yerr=z*se, fmt='o-', color='black', capsize=3, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Effect (index points)")
    ax.grid(alpha=0.25)
    return fig, ax
