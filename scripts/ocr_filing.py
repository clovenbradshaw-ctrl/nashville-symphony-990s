"""OCR one scanned filing with word positions.
   scripts/ocr_filing.py filings/<ein>/<year>-form-990.pdf
Writes <name>.ocr.json  {"pages":[{"w":px,"h":px,"words":[[text,x,y,w,h,eol],...]}]}  (x,y,w,h as fractions of the page, eol=1 on a line's last word)
and     <name>.ocr.txt  the same words as plain text, one form feed after each page (so the page count equals the PDF's).
Holodeck draws the words as an invisible layer over the page image, which is what makes names, figures and dates clickable on a scan.
Needs pdftoppm and tesseract."""
import csv, io, json, os, subprocess, sys, tempfile, glob

def ocr_pdf(pdf, dpi=200):
    tmp = tempfile.mkdtemp(); subprocess.run(['pdftoppm', '-r', str(dpi), '-gray', '-png', pdf, tmp + '/p'], check=True)
    pages = []
    for png in sorted(glob.glob(tmp + '/p*.png')):
        tsv = subprocess.run(['tesseract', png, 'stdout', '--psm', '6', 'tsv'], capture_output=True, text=True).stdout
        rows = list(csv.DictReader(io.StringIO(tsv), delimiter='\t', quoting=csv.QUOTE_NONE))
        pg = next((r for r in rows if r['level'] == '1'), None); W = int(pg['width']) if pg else 1; H = int(pg['height']) if pg else 1
        lines = {}
        for r in rows:
            if r['level'] != '5' or not (r.get('text') or '').strip() or float(r['conf']) < 0: continue
            if not any(c.isalnum() for c in r['text']): continue  # dot leaders, rules and stray marks are not words
            lines.setdefault((r['block_num'], r['par_num'], r['line_num']), []).append(r)
        words = []
        for k in sorted(lines, key=lambda k: (int(lines[k][0]['top']), int(lines[k][0]['left']))):
            ws = sorted(lines[k], key=lambda r: int(r['left']))
            for i, r in enumerate(ws):
                words.append([r['text'].strip(), round(int(r['left']) / W, 4), round(int(r['top']) / H, 4), round(int(r['width']) / W, 4), round(int(r['height']) / H, 4), 1 if i == len(ws) - 1 else 0])
        pages.append({'w': W, 'h': H, 'words': words}); os.remove(png)
    os.rmdir(tmp); return pages

if __name__ == '__main__':
    pdf = sys.argv[1]; base = pdf[:-4]
    if os.path.exists(base + '.ocr.json') and os.path.getsize(base + '.ocr.json') > 0: print('skip', pdf); sys.exit(0)
    pages = ocr_pdf(pdf)
    json.dump({'pages': pages}, open(base + '.ocr.json.part', 'w'), separators=(',', ':')); os.replace(base + '.ocr.json.part', base + '.ocr.json')
    txt = ''.join(''.join(w[0] + ('\n' if w[5] else ' ') for w in p['words']) + '\f' for p in pages)
    open(base + '.ocr.txt', 'w').write(txt)
    print('done', pdf, len(pages), 'pages', sum(len(p['words']) for p in pages), 'words')
