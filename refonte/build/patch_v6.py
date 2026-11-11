# ════════════════════════════════════════════════════════════════════
#  SIXIÈME PASSE (après relecture critique) : seuil par le remplissage, constat en ouverture,
#  corrections d'accessibilité, chronologie par semaine sur ordinateur
#  Aucun texte nouveau : les libellés repris existent déjà dans la page.
# ════════════════════════════════════════════════════════════════════

# ── Seuil d'attribution : le remplissage de l'hexagone double la couleur (plein, trois quarts, un tiers, contour) ──
sub("(sel ? ';background:#ffffff' : ';--c:' + c) + (nc && !sel ? ';opacity:.8' : ''),",
    "(sel ? ';background:#ffffff' : ';--c:' + c + ';--f:' + FILL[e.seuil]) + (nc && !sel ? ';opacity:.8' : ''),")
sub("(selD ? ';background:#ffffff' : ';--c:' + COLOR[e.seuil])", "(selD ? ';background:#ffffff' : ';--c:' + COLOR[e.seuil] + ';--f:' + FILL[e.seuil])", n=2)
sub("glyphStyle(CATKEY[e.cat], sz >= 18 && !sel && !e.passe)", "glyphStyle(CATKEY[e.cat], sz >= 18 && !sel && !e.passe, e.seuil)")
sub("glyphStyle(CATKEY[e.cat], !selD && HXC >= 17)", "glyphStyle(CATKEY[e.cat], !selD && HXC >= 17, e.seuil)", n=2)
# légendes et fiche pays : mêmes pastilles
sub("sw: 'width:12px;height:12px;flex:none;' + HEX + ';background:' + sv.color }));",
    "sw: 'position:relative;width:12px;height:13px;flex:none;' + HEX + ';--c:' + sv.color + ';--f:' + FILL[sv.id] }));")
sub('''<span style="{{l.sw}}"></span>''', '''<span class="hx" style="{{l.sw}}"></span>''', n=2)
sub("dot: 'width:13px;height:13px;flex:none;' + HEX + ';background:' + s.color + ';opacity:' + (on ? 1 : .3),",
    "dot: 'position:relative;width:13px;height:14px;flex:none;' + HEX + ';--c:' + s.color + ';--f:' + FILL[s.id] + ';opacity:' + (on ? 1 : .3),")
sub('''<span style="{{s.dot}}"></span>''', '''<span class="hx" style="{{s.dot}}"></span>''')
sub("HEX + ';--c:' + c;\n    const cfRank", "HEX + ';--c:' + COLOR[c] + ';--f:' + FILL[c];\n    const cfRank")
sub("sw: cfSw(x.color, 10)", "sw: cfSw(x.id, 10)")
sub("cfSw(COLOR[e.seuil], cfHs)", "cfSw(e.seuil, cfHs)")
sub("cfSw(COLOR[e.seuil], 9)", "cfSw(e.seuil, 9)")

# ── Nom accessible et infobulle des hexagones : type et seuil en toutes lettres ──
sub("label: fShort(e.date) + ' — ' + e.nom,", "label: fShort(e.date) + ' — ' + e.nom + ' — ' + L(e.cat) + ', ' + L(e.seuil),", n=4)

# ── Constat en ouverture : la dernière semaine complète, sur toute la base (sans les filtres) ──
sub('''        <div style="display: flex; align-items: center; gap: 16px; color: #dd203c;">
          <svg class="cue"''',
    '''        <div class="hlead" style="{{heroLead.style}}">
          <span class="fig" style="font-size: clamp(44px, 5vw, 72px); line-height: .86; color: #f3f1ec;">{{heroLead.n}}</span>
          <span style="display: flex; flex-direction: column; gap: 5px;"><span style="font-size: 11.5px; letter-spacing: .18em; text-transform: uppercase; color: #ea4d62;">{{heroLead.label}}</span><span style="font-size: 15px; line-height: 1.35; color: #d6d3ce; max-width: 48ch;">{{heroLead.note}}</span></span>
        </div>
        <div style="display: flex; align-items: center; gap: 16px; color: #dd203c;">
          <svg class="cue"''')
sub('''<span style="font-size: 16px; line-height: 1.35;">Faites défiler pour explorer la carte.</span>''',
    '''<span style="font-size: 16px; line-height: 1.35; color: #ea4d62;">Faites défiler pour explorer la carte.</span>''')
sub("    const lw = NWC - 1, lwN = wCounts[lw] || 0, pwN = wCounts[lw - 1] || 0;",
    '''    const lw = NWC - 1, lwN = wCounts[lw] || 0, pwN = wCounts[lw - 1] || 0;
    const hwN = i => EV.filter(e => !e.passe && weekOf(e.date) === i).length, hN = hwN(lw), hP = hwN(lw - 1);
    const heroLead = { n: String(hN), label: 'Dernière semaine', note: 'semaine du ' + (d => d.getDate() + ' ' + MOIS[d.getMonth()])(dateOfDay(weekStartDay(lw))) + ' (' + (hN - hP >= 0 ? '+' : '−') + Math.abs(hN - hP) + ' par rapport à la précédente)', style: EV.length && lw > 0 ? 'display:flex;align-items:center;gap:18px' : 'display:none' };''')
sub("legend, legendPasse, legendPasseCore, legendNc, cf,", "legend, legendPasse, legendPasseCore, legendNc, heroLead, cf,")

# ── Chronologie : colonnes par semaine aussi sur ordinateur (essai) ──
# (essai de colonnes par semaine sur ordinateur écarté par Marin : la chronologie reste par jour quand la place le permet)
sub(": Math.max(8, Math.min(16, Math.floor(slotW) - 8));", ": Math.max(8, Math.min(slotW >= 120 ? 20 : 16, Math.floor(slotW) - 8));")
sub(": '#6f6d68') + (byDay && slotW >= 21", ": '#8f8c86') + (byDay && slotW >= 21")

# ── Fiche d'événement : nommée, et le focus y entre à l'ouverture puis revient à son point de départ ──
sub('''<article class="fiche" style="''', '''<article class="fiche" role="dialog" aria-labelledby="fiche-t" style="''')
sub('''<h3 class="fiche-t" style="''', '''<h3 class="fiche-t" id="fiche-t" tabindex="-1" style="''')
sub('''    // Pays choisi dans le classement : la carte vient le cadrer''',
    '''    if (st.sel && prevState.sel !== st.sel) {
      if (!prevState.sel) { const a = document.activeElement; this.opener = a && a !== document.body ? a : null; }
      const h = document.getElementById('fiche-t'); if (h) h.focus({ preventScroll: true });
    } else if (!st.sel && prevState.sel) {
      const a = document.activeElement, o = this.opener; this.opener = null;
      if (!a || a === document.body) { const b = o && o.isConnected ? o : document.querySelector('#carte .pt[data-k^="' + prevState.sel + ':"]'); if (b) b.focus({ preventScroll: true }); }
    }
    // Carte : jamais de défilement interne ; un hexagone qui reçoit le focus hors du cadre est ramené au centre
    if (!this.fcw) {
      const c = document.getElementById('carte');
      if (c) {
        this.fcw = 1;
        c.addEventListener('scroll', () => { if (c.scrollLeft || c.scrollTop) { c.scrollLeft = 0; c.scrollTop = 0; } });
        c.addEventListener('focusin', ev => {
          const t = ev.target && ev.target.closest ? ev.target.closest('.pt') : null, m = this.mapNow;
          if (!t || !m || !this.animTo) return;
          const r = t.getBoundingClientRect(), b = c.getBoundingClientRect(), px = r.left + r.width / 2 - b.left, py = r.top + r.height / 2 - b.top;
          if (px > 28 && px < b.width - 28 && py > 28 && py < b.height - 28) return;
          this.animTo({ k: m.k, cx: m.cx + (px - b.width / 2) / (m.w * m.k) * 100, cy: m.cy + (py - b.height / 2) / (m.h * m.k * m.asp) * 100 }, false);
        });
      }
    }
    // Pays choisi dans le classement : la carte vient le cadrer''')

# ── Effet du titre : deux salves au chargement (moins de cinq secondes), puis une à chaque retour de l'ouverture à l'écran ──
sub("else { applyGl(null); this.gt = setTimeout(burst, R(1600, 5200)); }",
    "else { applyGl(null); this.gt = (this.glN = (this.glN || 0) + 1) >= 2 ? null : setTimeout(burst, R(1100, 1900)); }")
sub("this.heroOn = en.isIntersecting; h.classList.toggle('off', !en.isIntersecting);",
    "this.heroOn = en.isIntersecting; h.classList.toggle('off', !en.isIntersecting); if (en.isIntersecting && this.glN >= 2 && !this.gt) { this.glN = 1; this.gt = setTimeout(() => burst(), 500); }")
# mouvement réduit : pas de décodage du titre
sub("    let f = 0;\n    this.decode = setInterval(() => {", "    let f = REDUCE() ? 46 : 0;\n    this.decode = setInterval(() => {")

