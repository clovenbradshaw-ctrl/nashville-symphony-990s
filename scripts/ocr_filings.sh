#!/bin/sh
# OCR every scanned filing (filings/*/*.pdf) with word positions, N at a time (JOBS=6 by default).
#   scripts/ocr_filings.sh            all of them
#   scripts/ocr_filings.sh file.pdf   one filing
# Skips filings that already have a .ocr.json, and PDFs that already carry a text layer. Needs pdftoppm, tesseract, python3.
cd "$(dirname "$0")/.." || exit 1
case "$1" in
  *.pdf)
    pdf="$1"
    n=$(pdfinfo "$pdf" 2>/dev/null | awk '/^Pages/{print $2}')
    [ "$(pdftotext "$pdf" - 2>/dev/null | wc -c)" -gt $(( 200 * ${n:-1} )) ] && { echo "skip $pdf (has a text layer)"; exit 0; }
    python3 scripts/ocr_filing.py "$pdf" ;;
  *) ls filings/*/*.pdf | xargs -P "${JOBS:-6}" -n1 "$0" ;;
esac
