import argparse
from backend.pipeline import run_pipeline, export_reports

def main():
    parser = argparse.ArgumentParser(description="Run SaaS Spend Optimizer pipeline and export CSV reports.")
    parser.add_argument("--transactions", required=True, help="Path to transactions.csv")
    parser.add_argument("--inventory", default=None, help="Path to inventory.csv (optional)")
    parser.add_argument("--outdir", default="outputs", help="Output directory for exported reports")
    args = parser.parse_args()

    results = run_pipeline(args.transactions, args.inventory)

    print("\n=== SUMMARY ===")
    print(results["summary"].to_string(index=False))

    paths = export_reports(results, args.outdir)
    print("\nExported reports:")
    for p in paths:
        print(" -", p)

if __name__ == "__main__":
    main()
