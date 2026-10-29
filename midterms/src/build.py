# Construit midterms/senat.html à partir de la maquette du canevas (src/senat.dc.html)
import pathlib
d = pathlib.Path(__file__).parent
s = (d / 'senat.dc.html').read_text()
comp = s[s.index('class Component'):s.rindex('</script>')]
shell = (d / 'shell.html').read_text()
(d.parent / 'senat.html').write_text(shell.replace('/*__COMPONENT__*/', comp))
print('ok')
