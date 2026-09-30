"""Fetch IRS Form 990 data for Nashville Symphony orgs from ProPublica Nonprofit Explorer."""
import csv, json, pathlib, urllib.request

ORGS = {
    620550979: "nashville-symphony-association",
    626222276: "nashville-symphony-endowment-fund",
}
ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://projects.propublica.org/nonprofits/api/v2/organizations/{}.json"
FIELDS = ["tax_prd_yr", "tax_prd", "formtype", "totrevenue", "totfuncexpns", "totassetsend",
          "totliabend", "totnetassetend", "totcntrbgfts", "totprgmrevnue", "invstmntinc",
          "compnsatncurrofcr", "pdf_url"]

def main():
    summary = []
    for ein, slug in ORGS.items():
        raw = json.load(urllib.request.urlopen(API.format(ein)))
        (ROOT / "data/raw" / f"{slug}.json").write_text(json.dumps(raw, indent=1))
        rows = sorted(raw["filings_with_data"], key=lambda f: f["tax_prd_yr"])
        with open(ROOT / "data/processed" / f"{slug}.csv", "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["ein", "org"] + FIELDS)
            for f in rows:
                w.writerow([ein, raw["organization"]["name"]] + [f.get(k) for k in FIELDS])
                summary.append((slug, f["tax_prd_yr"]))
    print(len(summary), "filings")

if __name__ == "__main__":
    main()
