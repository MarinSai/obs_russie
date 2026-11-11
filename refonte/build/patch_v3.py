# ════════════════════════════════════════════════════════════════════
#  TROISIÈME PASSE : défilement de la fiche, hexagones, halo, chronologie animée, ouverture, fond de page
#  (exécuté par patch.py après patch_v2.py)
# ════════════════════════════════════════════════════════════════════

# ── Fiche : la molette (ou deux doigts) au-dessus de la fiche fait défiler la fiche, plus la carte ──
sub('''    const onWheel = ev => {
      const [fx, fy, r] = rel(ev);''', '''    const onWheel = ev => {
      if (ev.target && ev.target.closest && ev.target.closest('.fiche')) return;
      const [fx, fy, r] = rel(ev);''')

# ── Hexagones : coins adoucis (polygone à sommets arrondis, sans masque), léger reflet, halo de couleur sous les marqueurs de la carte ──
sub("const HEX = 'clip-path:polygon(25% 3%,75% 3%,100% 50%,75% 97%,25% 97%,0 50%)';",
    "const HEX = 'clip-path:var(--mh)';")
sub("const HEXP = 'clip-path:polygon(50% 0,97% 25%,97% 75%,50% 100%,3% 75%,3% 25%)';",
    "const HEXP = 'clip-path:var(--mhp)';")
sub("const HEXV = HEX.slice(10), HEXPV = HEXP.slice(10);",
    "const HEXV = 'var(--mh)', HEXPV = 'var(--mhp)';\nconst SHEEN = 'linear-gradient(155deg,rgba(255,255,255,.28),rgba(255,255,255,0) 52%,rgba(0,0,0,.18)),';")
sub("hex: 'position:absolute;inset:0;' + (nc ? HEXP : HEX) + ';background:' + (sel ? '#ffffff' : c) + (nc && !sel ? ';opacity:.8' : ''),",
    "hex: 'position:absolute;inset:0;' + (nc ? HEXP : HEX) + ';background:' + (sel ? '#ffffff' : SHEEN + c) + (nc && !sel ? ';opacity:.8' : ''),")
sub("hex: HEX + ';background:' + (selD ? '#ffffff' : COLOR[e.seuil])", "hex: HEX + ';background:' + (selD ? '#ffffff' : SHEEN + COLOR[e.seuil])", n=2)
sub('''    const legend = SEUILS.map(sv =>''', '''    // Halo de couleur sous les marqueurs dont l'attribution est au moins suspectée (calque à part, sous les hexagones) ;
    // plus le seuil est élevé, plus le halo est marqué. Les « non déterminés » restent mats.
    const GLOW = { 'Confirmé': '70', 'Attribué': '5c', 'Suspecté': '4a' };
    const glows = pts.filter(o => GLOW[o.e.seuil]).map(({ e, j, xy }) => {
      const c = COLOR[e.seuil], g = Math.round(size * (e.id === st.sel ? 4.6 : 3.4));
      return { k: e.id + ':' + j, style: 'left:' + xy[0] + '%;top:' + xy[1] + '%;width:' + g + 'px;height:' + g + 'px;margin:' + (-g / 2) + 'px 0 0 ' + (-g / 2) + 'px;background:radial-gradient(closest-side,' + c + GLOW[e.seuil] + ',' + c + '14 58%,' + c + '00)' };
    });
    const legend = SEUILS.map(sv =>''')
sub('''        <sc-for list="{{mapLabels}}" as="lb" hint-placeholder-count="0">''',
    '''        <sc-for list="{{glows}}" as="g" hint-placeholder-count="0"><span class="gl" data-k="{{g.k}}" style="{{g.style}}"></span></sc-for>
        <sc-for list="{{mapLabels}}" as="lb" hint-placeholder-count="0">''')
sub('''      mapLabels,''', '''      mapLabels, glows,''')

# ── Chronologie : les hexagones tombent à leur place (à l'arrivée à l'écran, puis jour après jour pendant la lecture) ──
sub('''<button class="pt wd" sc-camel-on-click="{{dot.pick}}" aria-label="{{dot.label}}" style="{{dot.style}}"><span style="{{dot.hex}}"></span></button>''',
    '''<button class="pt wd" data-id="{{dot.id}}" data-l="{{dot.later}}" sc-camel-on-click="{{dot.pick}}" aria-label="{{dot.label}}" style="{{dot.style}}"><span style="{{dot.hex}}"></span></button>''')
sub('''<span style="font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: #f3f1ec;">{{w.total}}</span>''',
    '''<span data-n="{{w.total}}" data-count aria-hidden="true" style="font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: #f3f1ec;"></span>''')
sub('''<span style="{{w.track}}"><span style="{{w.bar}}"></span></span>''', '''<span style="{{w.track}}"><span class="wkbar" style="{{w.bar}}"></span></span>''')
sub('''    // Pays choisi dans le classement : la carte vient le cadrer''', '''    // Chronologie pendant la lecture : les hexagones du jour atteint tombent à leur place
    const lp = this.laterPrev || new Map(), ln = new Map();
    root.querySelectorAll('#chrono .wd[data-id]').forEach(el => {
      const id = el.getAttribute('data-id'), l = el.getAttribute('data-l') === '1';
      ln.set(id, l);
      if (st.day !== null && lp.get(id) === true && !l) hexFall(el, 0, true);
    });
    this.laterPrev = ln;
    // Pays choisi dans le classement : la carte vient le cadrer''')

# ── Ouverture : carte plus présente, lueur à l'est, événements qui s'allument dans l'ordre chronologique ──
sub('''    <div aria-hidden="true" style="position: absolute; inset: -4% -6% 0 22%; -webkit-mask-image: radial-gradient(ellipse 70% 75% at 62% 45%, #000 30%, transparent 78%); mask-image: radial-gradient(ellipse 70% 75% at 62% 45%, #000 30%, transparent 78%);">''',
    '''    <div aria-hidden="true" style="position: absolute; inset: 0; background: radial-gradient(60% 85% at 100% 34%, rgba(221,32,60,.22), rgba(221,32,60,.06) 45%, rgba(221,32,60,0) 72%);"></div>
    <div class="hmap" aria-hidden="true" style="position: absolute; inset: -10% -9% -6% 12%; -webkit-mask-image: radial-gradient(ellipse 78% 84% at 60% 46%, #000 34%, transparent 80%); mask-image: radial-gradient(ellipse 78% 84% at 60% 46%, #000 34%, transparent 80%);">''')
sub('''          <path d="{{grat}}" fill="none" stroke="#18181a" stroke-width="1" vector-effect="non-scaling-stroke"></path>''',
    '''          <path d="{{grat}}" fill="none" stroke="#232327" stroke-width="1" vector-effect="non-scaling-stroke"></path>''')
sub('''          <path d="{{land}}" fill="#151517" stroke="#2c2c30" stroke-width=".8" vector-effect="non-scaling-stroke"></path>
          <path d="{{ukr}}" fill="#1c1b1a" stroke="#34312d" stroke-width=".8" vector-effect="non-scaling-stroke"></path>
          <path d="{{east}}" fill="#220e13" stroke="#5e2029" stroke-width=".8" vector-effect="non-scaling-stroke"></path>''',
    '''          <path d="{{land}}" fill="none" stroke="#ffffff" stroke-opacity=".025" stroke-width="16" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{east}}" fill="none" stroke="#ffffff" stroke-opacity=".025" stroke-width="16" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{land}}" fill="none" stroke="#ffffff" stroke-opacity=".045" stroke-width="5" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{east}}" fill="none" stroke="#ffffff" stroke-opacity=".045" stroke-width="5" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{land}}" fill="#1b1b1f" stroke="#3a3a41" stroke-width=".8" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{ukr}}" fill="#262319" stroke="#4d4636" stroke-width=".8" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{east}}" fill="#2e1016" stroke="#7d2733" stroke-width=".8" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>''')
sub('''<span class="hdot" style="{{h.style}}"></span>''', '''<span class="hdot" style="{{h.style}}"><span style="{{h.hex}}"></span></span>''')
sub('''      return { style: 'left:' + xy[0] + '%;top:' + xy[1] + '%;width:9px;height:9px;' + HEX + ';background:' + c + ';animation-delay:' + ((i * 0.53) % 3.6).toFixed(2) + 's' };''',
    '''      // halo + hexagone ; allumage dans l'ordre des dates, une seule fois (plus de pulsation sans fin)
      return { style: 'left:' + xy[0] + '%;top:' + xy[1] + '%;background:radial-gradient(closest-side,' + c + '70,' + c + '1c 55%,' + c + '00);animation-delay:' + (0.5 + Math.max(0, dayIdx(e.date)) / Math.max(1, LAST_DAY) * 3.2).toFixed(2) + 's', hex: HEX + ';background:' + SHEEN + c };''')
sub('''@keyframes heroPulse{0%{opacity:.2;transform:translate(-50%,-50%) scale(.7)}35%{opacity:.9;transform:translate(-50%,-50%) scale(1.1)}100%{opacity:.2;transform:translate(-50%,-50%) scale(.7)}}
''', '')
sub('''.hdot{position:absolute;animation:heroPulse 3.6s ease-in-out infinite}
''', '')

# ── Page : grain très léger sur le fond, filets en dégradé, intertitres plus grands ──
sub('''<div style="position: relative; background: #0b0b0c; color: #f3f1ec; font-family: 'GC National', system-ui, sans-serif; font-size: 15px;" data-canvas-width="1440"''',
    '''<div class="pg" style="position: relative; background: #0b0b0c; color: #f3f1ec; font-family: 'GC National', system-ui, sans-serif; font-size: 15px;" data-canvas-width="1440"''')
sub('''font-weight: 400; font-size: clamp(22px, 2.2vw, 30px); line-height: 1.1;">''', '''font-weight: 400; font-size: clamp(26px, 3vw, 42px); line-height: 1.05; letter-spacing: -.012em;">''', n=4)

# le grain du fond de page se prolonge sur l'ouverture (pas de marche visible à la jonction)
sub('''    <div id="glbars" aria-hidden="true"''', '''    <div class="hgrain" aria-hidden="true"></div>
    <div id="glbars" aria-hidden="true"''')
