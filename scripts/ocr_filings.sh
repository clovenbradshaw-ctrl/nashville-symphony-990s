#!/bin/sh
# OCR scanned filings to sidecars: filings/<ein>/<year>-form-990.ocr.txt (one form feed after each page, so the page count equals the PDF's).
#   scripts/ocr_filings.sh            all filings/*/*.pdf, 4 at a time (set JOBS=n)
#   scripts/ocr_filings.sh file.pdf   one filing
# Skips filings that already have a sidecar or already have a text layer. Needs pdftoppm and tesseract.
cd "$(dirname "$0")/.." || exit 1
case "$1" in
  *.pdf)
    pdf="$1"; out="${pdf%.pdf}.ocr.txt"
    [ -s "$out" ] && { echo "skip $pdf"; exit 0; }
    [ "$(pdftotext "$pdf" - 2>/dev/null | wc -c)" -gt $(( 200 * $(pdfinfo "$pdf" | awk '/^Pages/{print $2}') )) ] && { echo "skip $pdf (has a text layer)"; exit 0; }
    tmp=$(mktemp -d); pdftoppm -r 200 -gray -png "$pdf" "$tmp/p"
    : > "$out.part"
    for p in "$tmp"/p*.png; do tesseract "$p" - --psm 6 2>/dev/null >> "$out.part"; printf '\f' >> "$out.part"; done
    mv "$out.part" "$out"; rm -rf "$tmp"; echo "done $pdf $(wc -c < "$out") chars" ;;
  *) ls filings/*/*.pdf | xargs -P "${JOBS:-4}" -n1 "$0" ;;
esac
