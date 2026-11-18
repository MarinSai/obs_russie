# Passe 16 : textes nouveaux validés par Marin (traductions dans i18n_production) et retours des relecteurs.

# a. Lien d'évitement « Passer la carte » (bouton : l'ancre de l'adresse sert au lien direct #EVEN…)
sub('      <div class="cwrap" style="position: relative;">',
    '      <button class="skip" sc-camel-on-click="{{skipMap}}">Passer la carte</button>\n      <div class="cwrap" style="position: relative;">')
sub('      <div class="player" data-play="{{playState}}"', '      <div class="player" id="sk-play" tabindex="-1" data-play="{{playState}}"')
sub("      hasSel: !!s, closeSel,", "      hasSel: !!s, closeSel, skipMap: () => { const el = document.getElementById('sk-play'); if (el) el.focus(); }, liveMsg: st.playing ? '' : fbarCount, mapAria: 'Carte des ' + nShown + ' événements', dayText: (dd => fLong(dd.getFullYear() + '-' + String(dd.getMonth() + 1).padStart(2, '0') + '-' + String(dd.getDate()).padStart(2, '0')))(dateOfDay(curDay)),")

# b. Annonce des filtres pour les lecteurs d'écran
sub('      <div id="carte" data-rv="map"', '      <p class="sr-only" role="status" aria-live="polite">{{liveMsg}}</p>\n      <div id="carte" role="group" aria-label="{{mapAria}}" data-rv="map"')

# c. Curseur de la chronologie : date en toutes lettres
sub('<input id="day-range" type="range" min="0" max="{{dayMax}}" step="1" value="{{dayVal}}"', '<input id="day-range" type="range" min="0" max="{{dayMax}}" step="1" value="{{dayVal}}" aria-valuetext="{{dayText}}"')

# d. Foyers sur téléphone : nom accessible avec les pays
sub("ti: '0', label: n + ' événements', k: 'f:'",
    "ti: '0', label: (() => { const c = new Map(); g.m.forEach(o => { const ps = paysOf(o.e); ps.forEach(p => c.set(p, (c.get(p) || 0) + (ps.length > 1 ? .1 : 1))); }); return [...c.entries()].sort((a, b) => b[1] - a[1]).slice(0, 2).map(x => x[0]).join(' / '); })() + ' — ' + n + ' événements', k: 'f:'")

# f. Constat d'ouverture : la semaine retenue est la dernière semaine complète
sub("label: 'Dernière semaine', note: 'semaine du '", "label: 'Dernière semaine complète', note: 'semaine du '")

# g. Un seul bouton de réinitialisation (« Tout réinitialiser », au-dessus de la carte)
i0 = t.index('        <div class="side-reset"'); i1 = t.index('</div>\n', i0) + len('</div>\n')
assert 'Réinitialiser la sélection' in t[i0:i1]; t = t[:i0] + t[i1:]

# h. Légende : « Fait antérieur » rejoint la ligne Carte, « Action non classifiable » la ligne Type
fa = '''        <span style="display: inline-flex; align-items: center; gap: 8px;"><span style="{{legendPasse}}"><span style="{{legendPasseCore}}"></span></span>Fait antérieur au 23 sept.</span>\n'''
nc = '''        <span style="display: inline-flex; align-items: center; gap: 8px;"><span style="{{legendNc}}"></span>Action non classifiable</span>\n'''
sub('''        <span class="lg-sep" aria-hidden="true" style="width: 1px; height: 14px; background: #333336;"></span>\n''' + fa + nc, '')
sub('''          <span style="display: inline-flex; align-items: center; gap: 7px;"><span style="position: relative; display: inline-block; flex: none; width: 17px; height: 19px;"><span class="hx" style="position: absolute; inset: 0; clip-path: var(--mh); --c: #a9a59d;"></span><svg class="gly" sc-camel-view-box="0 0 24 24" aria-hidden="true" style="{{l.gs}}"><path d="{{l.g}}" fill-rule="evenodd"></path></svg></span>{{l.label}}</span>
        </sc-for>\n''', '''          <span style="display: inline-flex; align-items: center; gap: 7px;"><span style="position: relative; display: inline-block; flex: none; width: 17px; height: 19px;"><span class="hx" style="position: absolute; inset: 0; clip-path: var(--mh); --c: #a9a59d;"></span><svg class="gly" sc-camel-view-box="0 0 24 24" aria-hidden="true" style="{{l.gs}}"><path d="{{l.g}}" fill-rule="evenodd"></path></svg></span>{{l.label}}</span>
        </sc-for>\n''' + nc)
sub('''        <span class="lg-h" style="font-size: 10.5px; letter-spacing: .18em; text-transform: uppercase; color: #a3a09a;">Carte</span>\n''',
    '''        <span class="lg-h" style="font-size: 10.5px; letter-spacing: .18em; text-transform: uppercase; color: #a3a09a;">Carte</span>\n''' + fa)
