"""Write data/summary.md: per-year prose lines from the processed CSVs, for text readers like Holodeck."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
out = ["# Nashville Symphony: Form 990 financial summary\n",
       "Source: IRS Form 990 data via ProPublica Nonprofit Explorer. Dollars, as filed.\n"]
for p in sorted((ROOT / "data/processed").glob("*.csv")):
    rows = list(csv.DictReader(open(p)))
    out.append(f"\n## {rows[0]['org']} (EIN {rows[0]['ein']})\n")
    for r in rows:
        n = lambda k: f"${int(float(r[k])):,}" if r[k] not in ("", None) else "n/a"
        out.append(f"- Fiscal year {r['tax_prd_yr']} (period {r['tax_prd']}): total revenue {n('totrevenue')}, "
                   f"total expenses {n('totfuncexpns')}, contributions {n('totcntrbgfts')}, "
                   f"total assets {n('totassetsend')}, total liabilities {n('totliabend')}, "
                   f"net assets {n('totnetassetend')}.")
(ROOT / "data/summary.md").write_text("\n".join(out) + "\n")
