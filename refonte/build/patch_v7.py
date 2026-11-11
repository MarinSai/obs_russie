# ════════════════════════════════════════════════════════════════════
#  SEPTIÈME PASSE : chiffres clés sur le périmètre « depuis le 23 septembre », foyers regroupés sur téléphone
# ════════════════════════════════════════════════════════════════════

# ── Chiffres clés : même périmètre que la carte (hors faits antérieurs au 23 septembre) ──
sub("const nAll = EV.length;", "const EVN = EV.filter(e => !e.passe), nAll = EVN.length;")
sub("const nPaysAll = new Set(EV.flatMap(paysOf)).size;", "const nPaysAll = new Set(EVN.flatMap(paysOf)).size;")
sub("const nAttr = EV.filter(e => e.seuil === 'Attribué' || e.seuil === 'Confirmé').length;", "const nAttr = EVN.filter(e => e.seuil === 'Attribué' || e.seuil === 'Confirmé').length;")

# ── Téléphone : les événements trop serrés forment un foyer, grand hexagone rempli selon les seuils de ses événements ;
#    un toucher zoome sur le foyer, qui se défait à mesure qu'on approche ──
sub("    const key = Z.k + '|' + wPx + '|' + hPx + '|' + size + '|' + raw.map(o => o.e.id + ':' + o.j).join(',');",
    """    const clus = [];
    if (wPx < 520 && raw.length) {
      const G = [], DG = 24;
      raw.forEach(o => {
        const x = o.p[0] * wPx / 100, y = o.p[1] * hPx / 100;
        let g = o.e.id === st.sel ? null : G.find(q => !q.solo && Math.hypot(q.x - x, q.y - y) < DG);
        if (!g) { g = { x, y, m: [], solo: o.e.id === st.sel }; G.push(g); }
        g.m.push(o); g.x += (x - g.x) / g.m.length; g.y += (y - g.y) / g.m.length;
      });
      raw.length = 0;
      G.forEach(g => { if (g.m.length < 5) g.m.forEach(o => raw.push(o)); else clus.push(g); });
    }
    const key = Z.k + '|' + wPx + '|' + hPx + '|' + size + '|' + raw.map(o => o.e.id + ':' + o.j).join(',');""")
sub("    // Halo de couleur sous les marqueurs dont l'attribution est au moins suspectée",
    """    clus.forEach(g => {
      const n = g.m.length, sz = Math.round(20 + 4.4 * Math.sqrt(n)), xs = g.m.map(o => o.p[0]), ys = g.m.map(o => o.p[1]);
      const mx = xs.reduce((a, b) => a + b, 0) / n, my = ys.reduce((a, b) => a + b, 0) / n;
      let acc = 0; const bands = [];
      SEUILS.forEach(sv => { const k = g.m.filter(o => o.e.seuil === sv.id).length; if (!k) return; const a = acc, b = acc + k / n * 100; acc = b; bands.push((sv.id === 'Non déterminé' ? '#17171a' : sv.color) + ' ' + a.toFixed(1) + '% ' + b.toFixed(1) + '%'); });
      points.push({
        label: n + ' événements', k: 'f:' + g.m[0].e.id + ':' + n, cls: 'pt clu',
        pick: () => animTo({ k: Math.min(8, Z.k * 2.3), cx: mx / Z.k, cy: my / (Z.k * ASP) }, true),
        style: 'left:' + (mx - Z.cx * Z.k + 50) + '%;top:' + (my - Z.cy * Z.k * ASP + 50) + '%;width:' + sz + 'px;height:' + sz + 'px;border:0;background:transparent;z-index:2;filter:drop-shadow(2.5px -2.5px 0 #6f6c66) drop-shadow(0 0 5px rgba(0,0,0,.55))',
        hxc: '', g: '', gs: 'display:none',
        hex: 'position:absolute;inset:0;' + HEX + ';background:#cfcbc3',
        core: 'position:absolute;inset:7%;' + HEX + ';background:linear-gradient(to top,' + bands.join(',') + ')'
      });
    });
    // Halo de couleur sous les marqueurs dont l'attribution est au moins suspectée""")

# ── Téléphone : les foyers se défont dès que la carte est assez zoomée (plus aucun regroupement au-delà de ×2,6) ;
#    un toucher sur un foyer zoome au moins jusqu'à ce seuil ──
sub("    if (wPx < 520 && raw.length) {", "    if (wPx < 520 && raw.length && Z.k < CLZ) {")
sub("pick: () => animTo({ k: Math.min(8, Z.k * 2.3),", "pick: () => animTo({ k: Math.min(ZMAX, Math.max(CLZ + .05, Z.k * 2.3)),")
sub("const ZMAX = 6, ZMIN = 0.74;", "const ZMAX = 6, ZMIN = 0.74, CLZ = 2.6;")

# ── Constat en ouverture : « 11 événements », puis la semaine (chaînes existantes) ──
sub('''          <span class="fig" style="font-size: clamp(44px, 5vw, 72px); line-height: .86; color: #f3f1ec;">{{heroLead.n}}</span>
          <span style="display: flex; flex-direction: column; gap: 5px;"><span style="font-size: 11.5px; letter-spacing: .18em; text-transform: uppercase; color: #ea4d62;">{{heroLead.label}}</span>''',
    '''          <span style="font-size: 11.5px; letter-spacing: .18em; text-transform: uppercase; color: #ea4d62;">{{heroLead.label}}</span>
          <span style="display: flex; flex-direction: column; gap: 6px;"><span style="display: flex; align-items: baseline; gap: 10px;"><span class="fig" style="font-size: clamp(44px, 5vw, 72px); line-height: .86; color: #f3f1ec;">{{heroLead.n}}</span><span style="font-family: 'GC Sanomat', Georgia, serif; font-size: clamp(22px, 2.2vw, 30px); line-height: 1; color: #f3f1ec;">{{heroLead.unit}}</span></span>''')
sub("const heroLead = { n: String(hN), label: 'Dernière semaine',", "const heroLead = { n: String(hN), unit: (' événements').trim(), label: 'Dernière semaine',")
sub("style: EV.length && lw > 0 ? 'display:flex;align-items:center;gap:18px' : 'display:none' };",
    "style: EV.length && lw > 0 ? 'display:flex;flex-direction:column;gap:10px' : 'display:none' };")
sub('''  <!-- Chiffres clés -->
  <section style="''', '''  <!-- Chiffres clés -->
  <section class="kfsec" style="''')
