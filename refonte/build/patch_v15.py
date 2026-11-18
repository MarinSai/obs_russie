# Passe 15 : retours des relecteurs (clarté, accessibilité, téléphone), corrections sans texte nouveau.

# 1. Fiche d'événement hors du cadre de la carte : sur ordinateur, superposée comme avant (enveloppe de même taille) ;
#    sur téléphone, sous la carte, en pleine largeur (CSS dans extra.css).
i0 = t.index('        <!-- Fiche -->\n        <sc-if value="{{hasSel}}"')
i1 = t.index('          </article>\n        </sc-if>\n      </div>', i0)
blk = t[i0:i1 + len('          </article>\n        </sc-if>\n')]
t = t[:i0] + t[i1 + len('          </article>\n        </sc-if>\n'):]
end = '        </sc-if>\n      </div>'
j = t.index('      </div>\n', i0)  # fermeture de #carte
t = t[:j] + '      </div>\n' + blk + '      </div>\n' + t[j + len('      </div>\n'):]
sub('      <div id="carte" data-rv="map"', '      <div class="cwrap" style="position: relative;">\n      <div id="carte" data-rv="map"')
sub('<article class="fiche" role="dialog"', '<article class="fiche fev" role="dialog"')
# l'événement ouvert n'a plus à laisser la place de la fiche sur téléphone
sub("  if (ASP < .9) return { ...f, cy: f.cy + 25 / (f.k * ASP) };", "  if (MOBF()) return f;")
sub("const focusOf = (e, kmin) => {", "const MOBF = () => !!(window.matchMedia && matchMedia('(max-width: 760px)').matches);\nconst focusOf = (e, kmin) => {")
# focus : sur téléphone, la page défile juste ce qu'il faut pour montrer le titre de la fiche
sub("const h = document.getElementById('fiche-t'); if (h) h.focus({ preventScroll: true });", "const h = document.getElementById('fiche-t'); if (h) h.focus({ preventScroll: !MOBF() });")

# 2. Un seul arrêt de tabulation par événement (les copies d'un événement multi-pays sont sautées)
sub('<button class="{{p.cls}}" data-k="{{p.k}}"', '<button class="{{p.cls}}" data-k="{{p.k}}" tabindex="{{p.ti}}"')
sub("    const points = pts.map(({ e, j, xy }) => {\n", "    const tabSeen = new Set();\n    const points = pts.map(({ e, j, xy }) => {\n      const ti = tabSeen.has(e.id) ? '-1' : '0'; tabSeen.add(e.id);\n")
sub("        k: e.id + ':' + j, cls:", "        ti, k: e.id + ':' + j, cls:")
sub("label: n + ' événements', k: 'f:'", "ti: '0', label: n + ' événements', k: 'f:'")

# 3. Carrousel : le focus suit la ligne ouverte dans le journal
sub("setTimeout(() => { const el = document.getElementById('j-' + e.id) || document.getElementById('journal'); if (el) scrollToEl(el, 'start'); }, 60);",
    "setTimeout(() => { const el = document.getElementById('j-' + e.id) || document.getElementById('journal'); if (el) { scrollToEl(el, 'start'); const b = el.querySelector('button'); if (b) b.focus({ preventScroll: true }); } }, 60);")

# 6. Compteurs des seuils et des types : ils suivent aussi le pays, la semaine et le jour choisis
sub("count: EV.filter(e => e.cat === label && st.seuils[e.seuil] && (st.passe || !e.passe)).length,",
    "count: EV.filter(e => e.cat === label && st.seuils[e.seuil] && (st.passe || !e.passe) && inWeek(e) && inCountry(e) && inDay(e)).length,")
sub("count: EV.filter(e => e.seuil === s.id && st.cats[CATKEY[e.cat]] && (st.passe || !e.passe)).length,",
    "count: EV.filter(e => e.seuil === s.id && st.cats[CATKEY[e.cat]] && (st.passe || !e.passe) && inWeek(e) && inCountry(e) && inDay(e)).length,")

