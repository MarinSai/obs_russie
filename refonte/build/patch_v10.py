# ════════════════════════════════════════════════════════════════════
#  DIXIÈME PASSE : les faits antérieurs au 23 septembre sont inclus par défaut (compteurs, carte),
#  sans case à cocher ; leur statut est signalé sur la carte, dans la fiche et dans le journal.
#  Textes nouveaux (à ajouter à i18n.py au passage en production, voir refonte/i18n_ajouts.py) :
#   - « documentées par l’Observatoire, dont {{nPasse}} antérieures au 23 septembre 2026. »
#   - 'dont ' et ' faits antérieurs au 23 sept.' (résumé du panneau)
#  Textes retirés : la case « Faits antérieurs au 23 sept. ({{nPasse}}) », la pastille « Avec les faits antérieurs au 23 sept. »,
#  (« depuis le 23 sept. 2026 » reste utilisé.)
# ════════════════════════════════════════════════════════════════════

# état initial et remise à zéro : faits antérieurs inclus
sub("passe: false, week: null, country: null, sel: null, showAll: false,", "passe: true, week: null, country: null, sel: null, showAll: false,")
sub("set({ seuils: ALL_SEUILS(), cats: ALL_CATS(), passe: false, week: null, country: null, day: null, playing: false, fresh: false }); },",
    "set({ seuils: ALL_SEUILS(), cats: ALL_CATS(), passe: true, week: null, country: null, day: null, playing: false, fresh: false }); },")

# plus de case à cocher ni de pastille de filtre
sub('''        <label style="display: flex; align-items: center; gap: 10px; padding: 12px 8px 0; font-size: 13.5px; color: #b9b6b0; cursor: pointer;">
          <input id="passe" type="checkbox" checked="{{passe}}" sc-camel-on-change="{{togglePasse}}" style="flex: none; accent-color: #dd203c; width: 16px; height: 16px; margin: 0;">
          <span>Faits antérieurs au 23 sept. ({{nPasse}})</span>
        </label>
''', '')
sub("    if (st.passe) chips.push({ t: 'Avec les faits antérieurs au 23 sept.', x: () => set({ passe: false }) });\n", '')
sub("|| Object.values(st.cats).some(v => !v) || st.passe || st.week !== null", "|| Object.values(st.cats).some(v => !v) || st.week !== null")

# « Rejouer » : les faits antérieurs sont présents dès le premier jour
sub("const inDay = e => st.day === null || (!e.passe && dayIdx(e.date) <= st.day);", "const inDay = e => st.day === null || e.passe || dayIdx(e.date) <= st.day;")

# chiffres clés : toute la base
sub("const EVN = EV.filter(e => !e.passe), nAll = EVN.length;", "const EVN = EV, nAll = EVN.length;")
sub('''<span class="kdesc">de sabotage, d’espionnage et de déstabilisation, documentées depuis le 23 septembre 2026.</span>''',
    '''<span class="kdesc">de sabotage, d’espionnage et de déstabilisation, documentées par l’Observatoire, dont {{nPasse}} antérieures au 23 septembre 2026.</span>''')

# résumé du panneau : « 22 pays — dont 21 faits antérieurs au 23 sept. » ; « depuis le 23 sept. 2026 » quand la sélection n'en contient aucun
sub("    let scope = 'depuis le 23 sept. 2026';", "    const nPS = filtered.filter(e => e.passe).length;\n    let scope = nPS ? 'dont ' + nPS + ' faits antérieurs au 23 sept.' : 'depuis le 23 sept. 2026';")

# journal : mention sous le titre, avec le type et le seuil
sub('''<span style="{{e.seuilStyle}}">{{e.seuil}}</span></span></span>''',
    '''<span style="{{e.seuilStyle}}">{{e.seuil}}</span><sc-if value="{{e.passe}}" hint-placeholder-val="{{false}}"><span aria-hidden="true">—</span><span style="color: #c9c5bd;">Fait antérieur au 23 sept.</span></sc-if></span></span>''')
sub("        dot: 'position:relative;width:12px;height:12px;flex:none;align-self:center;' + HEX + ';background:' + c + ';opacity:' + (e.passe ? .45 : 1),",
    "        passe: !!e.passe,\n        dot: 'position:relative;width:12px;height:12px;flex:none;align-self:center;' + HEX + ';background:' + c + ';opacity:' + (e.passe ? .45 : 1),")
