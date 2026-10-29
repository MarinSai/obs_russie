# Construit midterms/index.html (et senat.html, ancien lien) à partir de la maquette du canevas (src/senat.dc.html)
import pathlib
d = pathlib.Path(__file__).parent
s = (d / 'senat.dc.html').read_text()
comp = s[s.index('class Component'):s.rindex('</script>')]
page = (d / 'shell.html').read_text().replace('/*__COMPONENT__*/', comp)
for name in ('index.html', 'senat.html'):
    (d.parent / name).write_text(page)
print('ok')
