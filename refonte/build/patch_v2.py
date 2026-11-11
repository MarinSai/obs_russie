# ════════════════════════════════════════════════════════════════════
#  DEUXIÈME PASSE : fond de carte, étiquettes de pays, chronologie, journal
#  (exécuté par patch.py, après la première passe ; utilise sub() et between())
# ════════════════════════════════════════════════════════════════════

# ── Fond de carte : liseré de côte en dégradé, teintes retravaillées, étiquettes de pays ──
sub("""          <path d="{{grat}}" fill="none" stroke="#18181b" stroke-width="1" vector-effect="non-scaling-stroke"></path>""",
    """          <path d="{{grat}}" fill="none" stroke="#1d1d21" stroke-width="1" vector-effect="non-scaling-stroke"></path>""")
sub("""          <path d="{{land}}" fill="#19191c" stroke="#3a3a3f" stroke-width=".8" vector-effect="non-scaling-stroke"></path>
          <path d="{{ukr}}" fill="#242220" stroke="#46423c" stroke-width=".8" vector-effect="non-scaling-stroke"></path>
          <path d="{{east}}" fill="#34121a" stroke="#8f2a35" stroke-width=".8" vector-effect="non-scaling-stroke"></path>""",
    """          <path d="{{land}}" fill="none" stroke="#ffffff" stroke-opacity=".022" stroke-width="16" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{east}}" fill="none" stroke="#ffffff" stroke-opacity=".022" stroke-width="16" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{land}}" fill="none" stroke="#ffffff" stroke-opacity=".03" stroke-width="8" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{east}}" fill="none" stroke="#ffffff" stroke-opacity=".03" stroke-width="8" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{land}}" fill="none" stroke="#ffffff" stroke-opacity=".05" stroke-width="3" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{east}}" fill="none" stroke="#ffffff" stroke-opacity=".05" stroke-width="3" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{land}}" fill="#1d1d21" stroke="#3b3b42" stroke-width=".7" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{ukr}}" fill="#29261f" stroke="#544d41" stroke-width=".8" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
          <path d="{{east}}" fill="#2b0f15" stroke="#7d2733" stroke-width=".8" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>""")
sub("""        <sc-for list="{{points}}" as="p" hint-placeholder-count="0">""",
    """        <sc-for list="{{mapLabels}}" as="lb" hint-placeholder-count="0"><span class="mlab" aria-hidden="true" style="{{lb.style}}">{{lb.name}}</span></sc-for>
        <sc-for list="{{points}}" as="p" hint-placeholder-count="0">""")
sub("aspect-ratio:1000/720;min-height:min(560px, calc(100vw - 32px));background:#0f0f10;border:1px solid #262628;",
    "aspect-ratio:1000/720;min-height:min(560px, calc(100vw - 32px));background:radial-gradient(120% 95% at 42% 42%,#131317 0%,#0c0c0e 70%);border:1px solid #2c2c30;")
sub("""    const UL = D && D.ukrLabel ? D.ukrLabel : null;""",
    """    // Étiquettes de pays : masquées quand la carte est trop petite pour les porter (mobile, vue d'ensemble)
    const mapLabels = [];
    if (D && wPx * Z.k >= 600) {
      // Placement recalculé seulement quand les hexagones ou le zoom changent (pas à chaque déplacement de la carte)
      const lkey = key + '|' + ASP.toFixed(3);
      if (this.labKey !== lkey) {
        this.labKey = lkey;
        const R = size / 2 + 4, pp = raw.map((o, i) => [this.spreadVal[i][0] * wPx / 100, this.spreadVal[i][1] * hPx / 100]), placed = [];
        this.labVal = paysLabels(D).map(l => {
          const x = l.x * Z.k * wPx / 100, y = l.y * Z.k * ASP * hPx / 100, w2 = l.name.length * 4.4 + 8;
          // l'étiquette cherche, autour du repère du pays et sans sortir de ses frontières, une place libre de tout hexagone et de toute autre étiquette
          for (const o of LAB_OFF) {
            const px = x + o[0], py = y + o[1];
            if (pp.some(q => Math.abs(q[0] - px) < w2 + R && Math.abs(q[1] - py) < 8 + R)) continue;
            if (placed.some(q => Math.abs(q[0] - px) < w2 + q[2] + 6 && Math.abs(q[1] - py) < 15)) continue;
            // test de frontière en dernier : c'est le plus coûteux
            if (o[0] || o[1]) { const bx = px / wPx * 1000 / Z.k, by = py / hPx * 720 / (Z.k * ASP); if (!l.rings.some(q => bx >= q.x0 && bx <= q.x1 && by >= q.y0 && by <= q.y1 && inRing(bx, by, q.r))) continue; }
            placed.push([px, py, w2]);
            return { name: l.name, x: px / wPx * 100, y: py / hPx * 100 };
          }
          return null; // aucune place libre : l'étiquette attend le zoom plutôt que d'être à moitié cachée
        }).filter(Boolean);
      }
      this.labVal.forEach(l => { const x = l.x - Z.cx * Z.k + 50, y = l.y - Z.cy * Z.k * ASP + 50; const hw = (l.name.length * 4.4 + 10) / wPx * 100; if (x - hw > 0 && x + hw < 100 && y > 2 && y < (x - hw < 52 ? 94.5 : 98)) mapLabels.push({ name: l.name, style: 'left:' + x.toFixed(2) + '%;top:' + y.toFixed(2) + '%' }); });
    }
    // Cadrage d'un pays : ses épingles (événements propres à ce pays) et son repère
    const fitCountry = name => {
      const ps = [];
      EV.forEach(e => { if (paysOf(e).length === 1 && e.pays === name && (st.passe || !e.passe)) allPos(e).forEach(q => ps.push(q.raw || q.eu)); });
      if (D) paysLabels(D).forEach(l => { if (l.name === name) ps.push([l.x, l.y]); });
      if (!ps.length) return null;
      const xs = ps.map(q => q[0]), ys = ps.map(q => q[1]);
      const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
      return { k: Math.min(4, Math.max(1.4, Math.min(58 / Math.max(1, x1 - x0), 58 / Math.max(1, (y1 - y0) * ASP)))), cx: (x0 + x1) / 2, cy: (y0 + y1) / 2 };
    };
    this.fitCountry = fitCountry;
    const UL = D && D.ukrLabel ? D.ukrLabel : null;""")
sub("""    const panMove = ev => { const d = this.drag; if (!d) return; this.backZ = null; const""", """    const panMove = ev => { const d = this.drag; if (!d) return; this.backZ = null; this.cBack = null; const""")
sub("""    const zoomAt = (f, fx, fy) => { this.backZ = null; const z""", """    const zoomAt = (f, fx, fy) => { this.backZ = null; this.cBack = null; const z""")
sub("""ev.preventDefault(); this.backZ = null; const d =""", """ev.preventDefault(); this.backZ = null; this.cBack = null; const d =""")
sub("""    this.closeSel = closeSel;""", """    this.closeSel = closeSel; this.animTo = animTo;""")
sub("""    // Méthodologie
    if (st.methodOpen && !prevState.methodOpen)""", """    // Pays choisi dans le classement : la carte vient le cadrer ; à la désélection, retour à la vue d'avant
    if ((prevState.country || null) !== (st.country || null) && this.animTo) {
      if (st.country) { if (!prevState.country) this.cBack = this.view(); const z = this.fitCountry && this.fitCountry(st.country); if (z) this.animTo(z, true); }
      else if (this.cBack) { const b = this.cBack; this.cBack = null; if (!st.sel) this.animTo(b, true); }
    }
    // Largeur réelle de la chronologie : décide du pas (jour ou semaine)
    const ch = document.getElementById('chrono');
    if (ch) {
      const sync = () => { const w = ch.clientWidth; if (w && Math.abs(w - (this.state.cw || 0)) > 1) this.setState({ cw: w }); };
      if (this.chEl !== ch) { this.chEl = ch; if (this.cro) this.cro.disconnect(); if (typeof ResizeObserver !== 'undefined') { this.cro = new ResizeObserver(sync); this.cro.observe(ch); } }
      sync();
    }
    // Méthodologie
    if (st.methodOpen && !prevState.methodOpen)""")
sub("""zoomReset: () => { this.backZ = null; animTo(defZ(), true); },""", """zoomReset: () => { this.backZ = null; this.cBack = null; animTo(defZ(), true); },
      mapLabels,""")

# ── Chronologie : chaque événement sur son jour, semaines en repères ; pas hebdomadaire quand la place manque ──
between('''  <div style="overflow-x: auto;">
    <div style="min-width: 560px; display: flex; flex-direction: column; gap: 0;">''', '''  <!-- 3. Les images (onglet Médias de la feuille) -->''', """  <div class="chr">
      <div class="chr-h">
        <span style="display: inline-flex; align-items: center; gap: 8px; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; color: #a3a09a;"><span style="width: 10px; height: 11px; background: #dd203c; clip-path: polygon(25% 0, 75% 0, 100% 50%, 75% 100%, 25% 100%, 0 50%);"></span>Événements par semaine</span>
        <span class="chr-lg">
          <sc-for list="{{legend}}" as="l" hint-placeholder-count="4">
            <span style="display: inline-flex; align-items: center; gap: 7px;"><span style="{{l.sw}}"></span>{{l.label}}</span>
          </sc-for>
        </span>
        <span style="font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #a3a09a;">{{cumLabel}}</span>
      </div>
      <div id="chrono" data-rv="bars" style="{{slotGrid}}">
        <sc-for list="{{slots}}" as="sl" hint-placeholder-count="7">
          <div style="{{sl.style}}">
            <span style="{{sl.topStyle}}">{{sl.top}}</span>
            <div style="{{sl.stack}}">
              <sc-for list="{{sl.dots}}" as="dot" hint-placeholder-count="1">
                <button class="pt wd" sc-camel-on-click="{{dot.pick}}" aria-label="{{dot.label}}" style="{{dot.style}}"><span style="{{dot.hex}}"></span></button>
              </sc-for>
            </div>
            <span aria-hidden="true" style="{{sl.footStyle}}">{{sl.foot}}</span>
          </div>
        </sc-for>
      </div>
      <div style="{{weekGrid}}">
        <sc-for list="{{weeksDone}}" as="w" hint-placeholder-count="5">
          <button class="wk" sc-camel-on-click="{{w.pick}}" aria-pressed="{{w.on}}" aria-label="{{w.aria}}" style="{{w.style}}">
            <span style="{{w.rowStyle}}"><span style="{{w.labStyle}}">{{w.label}}</span><span style="{{w.totStyle}}"><span style="font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: #f3f1ec;">{{w.total}}</span><span style="{{w.deltaStyle}}">{{w.delta}}</span></span></span>
            <span style="{{w.track}}"><span style="{{w.bar}}"></span></span>
          </button>
        </sc-for>
      </div>
  </div>

""")
sub('''    const wCounts = Array.from({ length: NW }, (_, i) => timeline.filter(e => weekOf(e.date) === i).length);''',
    '''    const wCounts = Array.from({ length: NW }, (_, i) => timeline.filter(e => weekOf(e.date) === i).length);
    // Géométrie de la chronologie. Pas d'un jour tant qu'un hexagone tient dans sa colonne ; sinon pas d'une semaine (mobile, longue période)
    const CW = st.cw || Math.max(280, Math.min(st.vw, 1440) - 2 * Math.min(40, st.vw * .03));
    const NSL = NWC * 7, byDay = CW / NSL >= 15, NCOL = byDay ? NSL : NWC, slotW = CW / NCOL, wCell = CW / NWC;
    const HXC = byDay ? Math.max(9, Math.min(20, Math.floor(slotW) - 6)) : Math.max(8, Math.min(16, Math.floor(slotW) - 8));
    const perRow = byDay ? 1 : Math.max(1, Math.min(4, Math.floor((slotW - 6) / (HXC + 4))));
    const wTop = Math.max(1, ...wCounts.slice(0, NWC)), wTight = wCell < 96, wStep = Math.max(1, Math.ceil(34 / wCell));''')
sub('''        style: 'display:flex;justify-content:space-between;align-items:center;gap:6px;padding:10px;border:0;border-left:1px solid #2c2c30;border-top:2px solid ' + (on ? RED : '#2c2c30') + ';background:' + (on ? 'rgba(221,32,60,.1)' : 'transparent') + ';color:' + (on ? RED_TXT : '#a3a09a')''',
    '''        style: 'display:flex;flex-direction:column;gap:7px;min-width:0;padding:' + (wTight ? '8px 2px 10px' : '10px 10px 12px') + ';border:0;border-left:1px solid #2c2c30;border-top:2px solid ' + (on ? RED : 'transparent') + ';background:' + (on ? 'rgba(221,32,60,.1)' : 'transparent') + ';color:' + (on ? '#ffffff' : '#a3a09a'),
        rowStyle: 'display:flex;justify-content:' + (wTight ? 'center' : 'space-between') + ';align-items:baseline;gap:6px;min-width:0',
        labStyle: 'text-transform:uppercase;' + (wTight ? 'font-size:9.5px;letter-spacing:.04em;line-height:1.25;text-align:center;visibility:' + (i % wStep === 0 ? 'visible' : 'hidden') : 'font-size:12px;letter-spacing:.1em;white-space:nowrap'),
        totStyle: wTight ? 'display:none' : 'display:inline-flex;gap:8px;align-items:baseline',
        // barre de la semaine, proportionnelle au nombre d'événements (au pas d'une semaine, la colonne fait déjà barre)
        track: byDay ? 'display:block;height:3px;background:#222225' : 'display:none',
        bar: 'display:block;height:100%;width:' + (n / wTop * 100).toFixed(1) + '%;background:' + (on ? RED : '#6f6d68') + ';transition:width .5s cubic-bezier(.2,.7,.2,1),background-color .2s\'''')
sub('''        deltaStyle: 'font-family:\\'IBM Plex Mono\\',monospace;font-size:11px;color:' + (diff > 0 ? RED : '#75736e'),''',
    '''        deltaStyle: 'font-family:\\'IBM Plex Mono\\',monospace;font-size:11px;color:' + (diff > 0 ? RED_TXT : '#8f8c86'),''')
sub('''    const dayGrid = 'display:grid;grid-template-columns:repeat(' + NDAYS + ',minmax(0,1fr));align-items:end;padding-top:8px';''',
    '''    const rank = e => SEUILS.findIndex(x => x.id === e.seuil);
    const slotEv = Array.from({ length: NCOL }, (_, c) => timeline.filter(e => (byDay ? dayIdx(e.date) === c - WOFF : weekOf(e.date) === c)).sort((a, b) => rank(a) - rank(b) || (a.date < b.date ? -1 : 1)));
    const stackH = Math.max(4, ...slotEv.map(v => Math.ceil(v.length / perRow))) * (HXC + 4);
    const MONO = 'font-family:\\'IBM Plex Mono\\',monospace;';
    // jour le plus chargé : annoté au-dessus de sa colonne
    const peakC = byDay ? slotEv.reduce((b, v, i) => (v.length > slotEv[b].length ? i : b), 0) : -1;
    const slots = slotEv.map((evs, c) => {
      const wk = byDay ? Math.floor(c / 7) : c, di = c - WOFF, dt = byDay ? dateOfDay(di) : null;
      const pre = byDay && di < 0;                                  // jours d'avant le début de la veille
      const m1 = byDay && di > 0 && dt.getDate() === 1;             // premier du mois
      const cur = byDay && st.day !== null && di === st.day;        // jour atteint par la lecture
      const dimW = st.week !== null && st.week !== wk;
      const pk = c === peakC && evs.length > 1 && !m1;
      return {
        top: byDay ? (m1 ? MOIS[dt.getMonth()] : pk ? 'Jour le plus chargé' : '') : (evs.length ? String(evs.length) : ''),
        topStyle: MONO + 'height:16px;line-height:16px;white-space:nowrap;' + (pk ? 'align-self:center;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:' + RED_TXT : byDay ? 'align-self:flex-start;padding-left:6px;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#a3a09a' : 'font-size:12.5px;color:' + (st.week === c ? RED_TXT : '#dedbd6')),
        foot: byDay && slotW >= 21 && !pre ? String(dt.getDate()) : '',
        footStyle: MONO + 'height:14px;line-height:14px;font-size:9.5px;color:' + (cur ? '#ffffff' : c % 7 === 0 ? '#a3a09a' : '#6f6d68') + (byDay && slotW >= 21 ? '' : ';display:none'),
        style: 'position:relative;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:5px;min-width:0;padding:8px 0 5px;box-sizing:border-box;opacity:' + (dimW ? .22 : 1) + ';transition:opacity .3s;background:' + (m1 ? 'linear-gradient(#4a4950,#4a4950) 0 0/1px 100% no-repeat' : !byDay || c % 7 === 0 ? 'linear-gradient(#2c2c30,#2c2c30) 0 26px/1px 100% no-repeat' : 'none') + (cur ? ',rgba(221,32,60,.16)' : pre ? ',repeating-linear-gradient(135deg,#19191c 0 2px,transparent 2px 7px)' : ''),
        stack: 'display:flex;flex-wrap:wrap-reverse;justify-content:center;align-content:flex-start;gap:4px;width:' + (perRow * HXC + (perRow - 1) * 4) + 'px;height:' + stackH + 'px',
        dots: evs.map(e => {
          const selD = e.id === st.sel, later = st.day !== null && dayIdx(e.date) > st.day;
          return {
            id: e.id, later: later ? '1' : '0',
            label: fShort(e.date) + ' — ' + e.nom,
            pick: () => {
              if (selD) { closeSel(); return; }
              set(filtered.includes(e) ? { sel: e.id } : { sel: e.id, day: null, week: null });
              openSel(e);
              const el = document.getElementById('carte');
              if (el) scrollToEl(el, 'center');
            },
            style: 'position:relative;transform:none;flex:none;width:' + HXC + 'px;height:' + HXC + 'px;padding:0;border:0;background:transparent;opacity:' + (later ? .15 : 1) + ';transition:opacity .3s',
            hex: HEX + ';background:' + (selD ? '#ffffff' : COLOR[e.seuil])
          };
        })
      };
    });
    const slotGrid = 'display:grid;grid-template-columns:repeat(' + NCOL + ',minmax(0,1fr));border-bottom:1px solid #3a3a3d';
    const dayGrid = 'display:grid;grid-template-columns:repeat(' + NDAYS + ',minmax(0,1fr));align-items:end;padding-top:8px';''')
sub("""      chronoStats, cumLine, cumArea, cumVb, cumLabel, cumPoints,""", """      chronoStats, slots, slotGrid, cumLine, cumArea, cumVb, cumLabel, cumPoints,""")
sub("""    if (kind === 'bars') Array.prototype.forEach.call(el.children, (col, i) => col.querySelectorAll('.wd').forEach((d, j) => d.animate([{ opacity: 0, transform: 'translateY(8px) scale(.4)' }, { opacity: 1, transform: 'none' }], { duration: 380, delay: i * 70 + j * 22, easing: EASE, fill: 'backwards' })));""",
    """    if (kind === 'bars') { const n = Math.max(1, el.children.length); Array.prototype.forEach.call(el.children, (col, i) => col.querySelectorAll('.wd').forEach((d, j) => hexFall(d, i / n * 1500 + j * 70 + Math.random() * 140, false))); }""")

# ── Journal : date une seule fois par jour, ligne « type — seuil » sous le titre, volet ouvert marqué par un filet, image de l'événement ──
sub('''          <span class="jd" style="width: 92px; flex: none; font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; color: #a3a09a;">{{e.dateShort}}</span>''',
    '''          <span class="jd" style="{{e.dateStyle}}">{{e.dateShort}}</span>''')
sub('''          <span class="jtitle" style="flex: 1 1 240px; min-width: 0; text-align: left;">{{e.nom}}</span>''',
    '''          <span class="jmain"><span class="jtitle">{{e.nom}}</span><span class="jmeta"><span>{{e.cat}}</span><span aria-hidden="true">—</span><span style="{{e.seuilStyle}}">{{e.seuil}}</span></span></span>''')
sub('''            <div style="flex: 1 1 320px; min-width: 0; display: flex; flex-direction: column; gap: 14px;">
              <p style="margin: 0; font-size: 15px; line-height: 1.6; color: #dedbd6;">{{e.desc}}</p>''',
    '''            <div style="flex: 1 1 320px; min-width: 0; display: flex; flex-direction: column; gap: 14px;">
              <sc-if value="{{e.hasImg}}" hint-placeholder-val="{{false}}"><span class="jimg" role="img" aria-label="{{e.imgAlt}}" style="{{e.imgStyle}}"><span style="{{e.imgBadge}}">{{e.imgKind}}</span><sc-if value="{{e.hasCredit}}" hint-placeholder-val="{{false}}"><span style="position: absolute; left: 0; right: 0; bottom: 0; padding: 18px 10px 7px; background: linear-gradient(transparent, rgba(0,0,0,.7)); font-size: 11px; color: #dedbd6; text-align: right;">{{e.credit}}</span></sc-if></span></sc-if>
              <p style="margin: 0; font-size: 15px; line-height: 1.6; color: #dedbd6;">{{e.desc}}</p>''')
sub('''    const sorted = [...filtered].sort((a, b) => b.date.localeCompare(a.date));
    const listed = (st.showAll ? sorted : sorted.slice(0, 10)).map(e => {''',
    '''    const sorted = [...filtered].sort((a, b) => b.date.localeCompare(a.date));
    const JMED = (D && D.media) || {};
    const listed = (st.showAll ? sorted : sorted.slice(0, 10)).map((e, idx, arr) => {
      // image de l'événement dans le volet : photo, ou vignette Mux pour une vidéo
      const jm = JMED[e.id], jmx = jm ? /stream\\.mux\\.com\\/([^/?#.]+)/.exec(jm.src || '') : null;
      const jsrc = !jm ? '' : jmx ? 'https://image.mux.com/' + jmx[1] + '/thumbnail.webp?width=720&time=1' : /\\.(mp4|webm|mov|m4v)(\\?|#|$)/i.test(jm.src || '') ? '' : jm.src;
      const sameDay = idx > 0 && arr[idx - 1].date === e.date;''')
sub('''        wrap: 'display:flex;flex-direction:column;scroll-margin-top:90px;' + (open ? 'background:rgba(255,255,255,.02);' : ''),''',
    '''        wrap: 'display:flex;flex-direction:column;scroll-margin-top:90px;transition:background-color .25s,box-shadow .25s;box-shadow:inset 2px 0 0 ' + (open ? RED : 'transparent') + ';' + (open ? 'background:#111113;' : ''),
        // la date n'est écrite qu'une fois par jour (elle reste lue par les lecteurs d'écran)
        dateStyle: 'width:92px;flex:none;font-family:\\'IBM Plex Mono\\',monospace;font-size:12.5px;color:#a3a09a;opacity:' + (sameDay ? 0 : 1),
        cat: L(e.cat), seuil: L(e.seuil), seuilStyle: 'color:' + (e.seuil === 'Non déterminé' ? '#b9b6b0' : c),
        hasImg: !!jsrc, imgAlt: jm ? jm.alt || e.nom : '', imgKind: jm ? JKIND[jm.type] || JKIND.photo : '',
        imgStyle: jsrc ? 'background-image:url(' + encodeURI(jsrc) + ')' : '',
        imgBadge: 'position:absolute;left:10px;top:10px;padding:4px 8px;border-radius:999px;background:rgba(11,11,12,.75);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#f3f1ec',
        hasCredit: !!(jm && jm.credit), credit: jm && jm.credit ? (jm.credit.startsWith('©') ? jm.credit : '© ' + jm.credit) : '',''')
sub('''padding:15px 8px;border:0;border-bottom:1px solid #1f1f21;color:#f3f1ec;background:' + (on ? 'rgba(221,32,60,.1)' : 'transparent')''',
    '''padding:15px 8px 15px 12px;border:0;border-bottom:1px solid ' + (open ? 'transparent' : '#1f1f21') + ';color:#f3f1ec;background:transparent\'''')
# libellés des médias : définis une fois, avant le journal (le carrousel reprend la même table)
sub('''    const KIND = { photo: 'Photo', 'vidéo': 'Vidéo', satellite: 'Image satellite' };
''', '''    const KIND = JKIND;
''')
sub('''    const JMED = (D && D.media) || {};
''', '''    const JMED = (D && D.media) || {};
    const JKIND = { photo: 'Photo', 'vidéo': 'Vidéo', satellite: 'Image satellite' };
''')
