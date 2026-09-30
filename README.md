# Nashville Symphony 990s

IRS Form 990 financials for the Nashville Symphony Association (EIN 62-0550979) and the Nashville Symphony Endowment Fund (EIN 62-6222276).

- `data/raw/` original ProPublica API JSON
- `data/processed/` one CSV per organization
- `data/summary.md` per-year prose lines (what Holodeck reads)
- `scripts/` `fetch.py` then `summarize.py` rebuild everything

## Coverage (not 40 years)
Association: tax years 2011-2023. Endowment Fund: 2011-2017. ProPublica's structured data starts at 2011. Earlier years (mid-1990s on) exist only in the IRS SOI extracts and scanned returns; not yet included. No separate foundation entity was found; the Players Assembly (union) has no financial data.

## Use in Holodeck
Add panel -> enter `<owner>/nashville-symphony-990s` once pushed to GitHub.

## Audit-derived supplement
`data/raw/archive-org/` holds OCR text of the Nashville Symphony audited financial statements for FY2011/2010 (Internet Archive mirror of a DocumentCloud upload). `data/processed/audit-derived.csv` records the balance-sheet totals that parse cleanly: FY2010 is new; FY2011 matches the 990. Revenue and expense lines are not extracted (OCR column layout is scrambled).

## Explore it
Live explorer (GitHub Pages): https://clovenbradshaw-ctrl.github.io/nashville-symphony-990s/
It is a vendored copy of [Holodeck](https://github.com/clovenbradshaw-ctrl/holodeck) under `vendor/holodeck/` (see its `VENDORING.md` for provenance and the one local patch) that loads this repo's files on open. To point it at any repo: `vendor/holodeck/index.html?repo=owner/name`.
