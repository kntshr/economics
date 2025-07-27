import sys, os
from diffusion_dashboard.cli import run

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python examples/run_pipeline.py <productivity.csv> <AIOE_DataAppendix.xlsx> [outdir]")
        sys.exit(1)
    prod_csv = sys.argv[1]
    aiie_xlsx = sys.argv[2]
    outdir = sys.argv[3] if len(sys.argv) > 3 else "./outputs"
    res = run(prod_csv, aiie_xlsx, outdir)
    print("Pipeline complete:", res)
