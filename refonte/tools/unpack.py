import sys, json, re, base64, gzip, os
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
html = open(src, encoding='utf-8').read()
def island(t):
    m = re.search(r'<script type="__bundler/%s">\s*(.*?)\s*</script>' % t, html, re.S)
    return m.group(1)
man = json.loads(island('manifest'))
tpl = json.loads(island('template'))
open(os.path.join(out, 'template.html'), 'w', encoding='utf-8').write(tpl)
for u, e in man.items():
    b = base64.b64decode(e['data'])
    if e.get('compressed'): b = gzip.decompress(b)
    print(u, e['mime'], e.get('compressed'), len(b))
    ext = {'text/javascript':'js'}.get(e['mime'], e['mime'].split('/')[-1])
    open(os.path.join(out, u + '.' + ext), 'wb').write(b)
print('template chars', len(tpl), 'lines', tpl.count('\n'))
