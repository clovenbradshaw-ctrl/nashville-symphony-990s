"""Render IRS e-file 990 XML (filings/*/*.xml) as readable text sidecars (<name>.readable.txt): one line per value,
'Group > Field: value', dollar amounts shown with $ so a reader can tell a figure from a count. No values are changed."""
import re, sys, glob, xml.etree.ElementTree as ET

def words(tag):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', tag).replace(' Amt', '').replace(' Txt', '').replace(' Cnt', ' count').replace(' Ind', '').replace(' Dt', ' date').strip()

def render(path):
    root = ET.parse(path).getroot(); lines = []
    def walk(el, trail):
        tag = el.tag.split('}')[-1]; kids = list(el)
        if not kids:
            v = (el.text or '').strip()
            if not v: return
            if tag.endswith('Amt') and re.fullmatch(r'-?\d+', v): v = ('-' if v.startswith('-') else '') + '${:,}'.format(abs(int(v)))
            lines.append(' > '.join(trail[-3:] + [words(tag)]) + ': ' + v)
        else:
            for k in kids: walk(k, trail + [words(tag)] if tag not in ('Return', 'ReturnData') else trail)
    walk(root, []); return '\n'.join(lines) + '\n'

for f in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else 'filings/*/*.xml')):
    out = f[:-4] + '.readable.txt'; open(out, 'w').write(render(f)); print(out, sum(1 for _ in open(out)), 'lines')
