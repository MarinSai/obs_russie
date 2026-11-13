# ════════════════════════════════════════════════════════════════════
#  NEUVIÈME PASSE : voir sur la carte les événements ajoutés lors de la dernière mise à jour
#  Libellés repris de la page (' derniers événements', 'Mise à jour') : rien de nouveau à traduire.
# ════════════════════════════════════════════════════════════════════

# ── Bouton dans le panneau de la carte, sous le nombre d'événements ──
sub('''        <span style="font-size: 14px; color: #ea4d62; line-height: 1.45;">{{nPays}} pays — {{scope}}</span>
        <div class="side-reset"''', '''        <span style="font-size: 14px; color: #ea4d62; line-height: 1.45;">{{nPays}} pays — {{scope}}</span>
        <button class="nwb" sc-camel-on-click="{{freshT.pick}}" aria-pressed="{{freshT.on}}" style="{{freshT.style}}"><span class="nwd" aria-hidden="true"></span><span style="display: flex; flex-direction: column; gap: 3px; text-align: left;"><span style="font-size: 14px; line-height: 1.2;">{{freshT.label}}</span><span style="font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: .1em; text-transform: uppercase; color: #a3a09a; white-space: nowrap;"><span>Mise à jour</span> · {{freshT.date}}</span></span></button>
        <div class="side-reset"''')

# ── Les événements de la dernière mise à jour : même date d'entrée dans la base que la plus récente ──
sub("    const NW = weekOf(lastEntry) + 1;", "    const NW = weekOf(lastEntry) + 1;\n    const FRESH = new Set(EV.filter(e => e.entree === lastEntry).map(e => e.id));")

# hexagones : les nouveaux cerclés de blanc, les autres estompés ; pas de foyers sur téléphone dans ce mode
sub("k: e.id + ':' + j, cls: sel ? 'pt is-sel' : 'pt',", "k: e.id + ':' + j, cls: (sel ? 'pt is-sel' : 'pt') + (st.fresh ? (FRESH.has(e.id) ? ' is-new' : sel ? '' : ' is-dim') : ''),")
sub("if (wPx < 520 && raw.length && Z.k < CLZ) {", "if (wPx < 520 && raw.length && Z.k < CLZ && !st.fresh) {")
sub("const glows = pts.filter(o => GLOW[o.e.seuil])", "const glows = pts.filter(o => GLOW[o.e.seuil] && (!st.fresh || FRESH.has(o.e.id)))")

# bouton : bascule, et la carte cadre les nouveaux événements (puis revient à la vue précédente)
sub("    const legendTypes = Object.keys(CATKEY)", '''    const fDot = d => { const p = parse(d); return String(p.j).padStart(2, '0') + '.' + String(p.m).padStart(2, '0') + '.' + p.y; };
    const fitFresh = () => {
      const ps = []; EV.forEach(e => { if (FRESH.has(e.id) && (st.passe || !e.passe)) allPos(e).forEach(q => ps.push(q.raw || q.eu)); });
      if (!ps.length) return null;
      const xs = ps.map(q => q[0]), ys = ps.map(q => q[1]), x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
      return clampZ({ k: Math.min(3.2, Math.max(ZMIN, Math.min(62 / Math.max(1, x1 - x0), 62 / Math.max(1, (y1 - y0) * ASP)))), cx: (x0 + x1) / 2, cy: (y0 + y1) / 2 });
    };
    const nFresh = EV.filter(e => FRESH.has(e.id) && (st.passe || !e.passe)).length;
    const freshT = {
      on: st.fresh ? 'true' : 'false', label: nFresh + ' derniers événements', date: fDot(lastEntry),
      style: nFresh && lastEntry > '2026-09-23' ? 'display:flex;align-items:center;gap:11px;align-self:flex-start;margin-top:12px;padding:9px 14px 9px 12px;border:1px solid ' + (st.fresh ? '#f3f1ec' : '#3a3a3d') + ';background:' + (st.fresh ? '#f3f1ec' : 'transparent') + ';color:' + (st.fresh ? '#0b0b0c' : '#f3f1ec') + ';cursor:pointer;min-height:44px;box-sizing:border-box' : 'display:none',
      pick: () => {
        if (st.fresh) { set({ fresh: false }); if (this.freshBack) { this.animTo(this.freshBack, true); this.freshBack = null; } return; }
        if (st.sel) closeSel();
        this.freshBack = this.view(); set({ fresh: true, sel: null });
        const z = fitFresh(); if (z) this.animTo(z, true);
      }
    };
    const legendTypes = Object.keys(CATKEY)''')
sub("legend, legendPasse, legendPasseCore, legendNc, heroLead, cf,", "legend, legendPasse, legendPasseCore, legendNc, heroLead, freshT, cf,")
sub("reset: () => { stop(); set({ seuils: ALL_SEUILS(), cats: ALL_CATS(), passe: false, week: null, country: null, day: null, playing: false }); },",
    "reset: () => { stop(); this.freshBack = null; set({ seuils: ALL_SEUILS(), cats: ALL_CATS(), passe: false, week: null, country: null, day: null, playing: false, fresh: false }); },")
