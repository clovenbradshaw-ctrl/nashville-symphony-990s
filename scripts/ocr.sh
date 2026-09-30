#!/bin/sh
# OCR every PDF in data/raw/pdfs into data/raw/text/<name>.txt (pdftotext first, tesseract if no text layer).
cd "$(dirname "$0")/.." && mkdir -p data/raw/text
for f in data/raw/pdfs/*.pdf; do
  [ -e "$f" ] || continue
  b=$(basename "$f" .pdf); o=data/raw/text/$b.txt
  pdftotext -layout "$f" "$o"
  if [ "$(wc -c < "$o")" -lt 500 ]; then
    tmp=$(mktemp -d); pdftoppm -r 300 -png "$f" "$tmp/p"
    : > "$o"; for p in "$tmp"/p*.png; do tesseract "$p" - 2>/dev/null >> "$o"; done; rm -rf "$tmp"
  fi
  echo "$b: $(wc -c < "$o") chars"
done
