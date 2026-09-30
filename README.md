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

## Filings (the sources)
`filings/` holds the IRS Form 990 returns themselves; `filings/manifest.csv` lists each with its IRS source.

| Who | Years | Source |
|---|---|---|
| Nashville Symphony Association (62-0550979) | 2016, 2017, 2018, 2019, 2022, 2024 | scanned PDF from the IRS, plus an `.ocr.txt` sidecar (tesseract) |
| | 2020, 2021, 2023, 2025 | ProPublica's "Public Visual Render" of the IRS e-file, saved as PDF (the IRS published no scan); the IRS XML is kept beside it |
| Nashville Symphony Endowment Trust (62-6222276) | 2016, 2017, 2018 | scanned PDF, plus `.ocr.txt` |

Years are the year the fiscal period ends (the Association's runs Aug 1 to Jul 31). Not here: everything before 2016 (ProPublica has scans back to 2000 behind a bot check); the Endowment Trust after 2018; Form 990-T returns. OCR text can misread a figure, so check it against the PDF; the structured CSVs in `data/processed/` agree with the e-file XML to the dollar for 2020, 2021 and 2023.

Rebuild: `scripts/ocr_filings.sh` (scanned PDF to `.ocr.txt`; skips PDFs that already have text), `scripts/xml_to_text.py` (XML to `.readable.txt`).

## Explore it
Live explorer (GitHub Pages): https://clovenbradshaw-ctrl.github.io/nashville-symphony-990s/
It is a vendored copy of [Holodeck](https://github.com/clovenbradshaw-ctrl/holodeck) under `vendor/holodeck/` (see its `VENDORING.md` for provenance and local patches) that loads the filings on open. `?repo=owner/name` loads any repo's text files; add `&path=filings/` to load PDF filings and their sidecars the way this repo is set up.
