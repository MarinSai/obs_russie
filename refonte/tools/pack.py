#!/usr/bin/env python3
"""Réinsère build/template.html dans le bundle d'origine -> site/observatoire_test.html (même format, mêmes polices et ressources)."""
import json, re, os, sys
ROOT = '/home/claude/work'
src = open(os.path.join(ROOT, 'src/observatoire.html'), encoding='utf-8').read()
tpl = open(os.path.join(ROOT, 'build/template.html'), encoding='utf-8').read()
m = re.search(r'(<script type="__bundler/template">)(.*?)(</script>)', src, re.S)
assert json.loads(m.group(2)) == open(os.path.join(ROOT, 'unpacked/template.html'), encoding='utf-8').read()
enc = json.dumps(tpl, ensure_ascii=False).replace('</', '<\\u002F')
out = src[:m.start(2)] + enc + src[m.end(2):]
dst = os.path.join(ROOT, 'site', sys.argv[1] if len(sys.argv) > 1 else 'observatoire_test.html')
open(dst, 'w', encoding='utf-8').write(out)
# contrôle : relecture
m2 = re.search(r'<script type="__bundler/template">(.*?)</script>', out, re.S)
assert json.loads(m2.group(1)) == tpl
print('écrit', dst, len(out), 'octets (origine :', len(src), ')')
