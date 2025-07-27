# diffusion-dashboard (v0.1)

A Python toolkit to implement the **Diffusion Dashboard**: indicators (Layers A–D), econometric spine (stacked diffusion curves, distributed lags), and outcome panels (DiD/event-studies), with alert rules.

## Install (editable)
```bash
pip install -e ./diffusion_dashboard_v01
```

## Quick start
Prepare two inputs:
1) `productivity.csv` with columns: `sector,year,value` (e.g., labour productivity index by 2-digit NAICS).  
2) `AIOE_DataAppendix.xlsx` (Felten–Raj–Seamans) to derive exposure per sector.

Then run:
```bash
python diffusion_dashboard_v01/examples/run_pipeline.py /path/to/productivity.csv /path/to/AIOE_DataAppendix.xlsx ./outputs
```

Outputs:
- DiD regression summary (sector & year FE, clustered SEs)
- Event-study coefficients CSV + plot
- Group means plot (high vs low exposure, 95% bands)

See `docs/` for the architecture and API.
