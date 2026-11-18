# Passe 19 : chronologie par type d'action, villes repères sur la carte zoomée, bouton des nouveautés sur 7 jours.
CIT = open(os.path.join(ROOT, 'build/cities.js'), encoding='utf-8').read()
sub("const DOT = s =>", CIT + "const DOT = s =>")

# ---- C. Bouton : événements ajoutés au cours des 7 derniers jours
sub("    const FRESH = new Set(EV.filter(e => e.entree === lastEntry).map(e => e.id));",
    "    const isoD = d => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');\n    const freshFrom = isoD(dateOfDay(dayIdx(lastEntry) - 6));\n    const FRESH = new Set(EV.filter(e => e.entree >= freshFrom).map(e => e.id));")
sub("label: nFresh + (nFresh > 1 ? ' derniers événements' : ' dernier événement'), date: fDot(lastEntry),",
    "label: nFresh + (nFresh > 1 ? ' derniers événements' : ' dernier événement'), date: fDot(freshFrom),")
sub("<span>Mise à jour</span> · {{freshT.date}}", "<span>Ajoutés depuis le</span> {{freshT.date}}")

# ---- B. Villes repères (au-delà d'un certain zoom, sans chevaucher hexagones ni étiquettes)
sub('''        <sc-for list="{{mapLabels}}" as="lb" hint-placeholder-count="0"><span class="mlab" aria-hidden="true" style="{{lb.style}}">{{lb.name}}</span></sc-for>''',
    '''        <sc-for list="{{mapLabels}}" as="lb" hint-placeholder-count="0"><span class="mlab" aria-hidden="true" style="{{lb.style}}">{{lb.name}}</span></sc-for>
        <sc-for list="{{mapCities}}" as="ct" hint-placeholder-count="0"><span class="{{ct.cls}}" aria-hidden="true" style="{{ct.style}}"><i></i>{{ct.name}}</span></sc-for>''')
sub("            placed.push([px, py, w2]);\n            return { name: l.name, x: px / wPx * 100, y: py / hPx * 100 };",
    "            placed.push([px, py, w2]); this.labBoxes.push([px - w2, py - 8, px + w2, py + 8]);\n            return { name: l.name, x: px / wPx * 100, y: py / hPx * 100 };")
sub("        const R = size / 2 + 4, pp = raw.map(", "        this.labBoxes = [];\n        const R = size / 2 + 4, pp = raw.map(")
sub("        }).filter(Boolean);\n      }\n      this.labVal.forEach(",
    """        }).filter(Boolean);
        // villes : point exact, nom à droite, à gauche, au-dessus ou au-dessous ; écartée si le point ou le nom touche un hexagone ou une étiquette
        this.cityVal = [];
        if (wPx * Z.k >= (wPx < 520 ? 1000 : 2100)) {
          const RH = size / 2 + 3, boxes = this.labBoxes.slice();
          const hit = (x0, y0, x1, y1) => pp.some(q => q[0] + RH > x0 && q[0] - RH < x1 && q[1] + RH > y0 && q[1] - RH < y1) || boxes.some(b => b[0] < x1 && b[2] > x0 && b[1] < y1 && b[3] > y0);
          CITIES.forEach(c => {
            const x = c[0] * Z.k * wPx / 100, y = c[1] * Z.k * ASP * hPx / 100, w = c[2].length * (c[3] ? 7.2 : 6.4) + 4, h = c[3] ? 15 : 14;
            // point recouvert par un hexagone : le nom seul, un peu plus loin (pour les capitales et les villes les plus proches)
            const covered = hit(x - 5, y - 5, x + 5, y + 5), gaps = covered ? [16, 26] : [7];
            for (const g of gaps) {
              const opts = [['r', x + g, y - h / 2], ['l', x - g - w, y - h / 2], ['t', x - w / 2, y - g - h], ['b', x - w / 2, y + g]];
              for (const [s, x0, y0] of opts) {
                if (hit(x0, y0, x0 + w, y0 + h)) continue;
                boxes.push([x0, y0, x0 + w, y0 + h]); if (!covered) boxes.push([x - 5, y - 5, x + 5, y + 5]);
                this.cityVal.push({ name: c[2], cap: c[3], s: s + (covered ? ' nod g' + g : ''), x: x / wPx * 100, y: y / hPx * 100 });
                return;
              }
            }
          });
        }
      }
      (this.cityVal || []).forEach(c => { const x = c.x - Z.cx * Z.k + 50, y = c.y - Z.cy * Z.k * ASP + 50; if (x > 1 && x < 99 && y > 2 && y < 97) mapCities.push({ name: c.name, cls: 'mcity ' + c.s + (c.cap ? ' cap' : ''), style: 'left:' + x.toFixed(2) + '%;top:' + y.toFixed(2) + '%' }); });
      this.labVal.forEach(""")
sub("    const mapLabels = [];\n", "    const mapLabels = [], mapCities = [];\n")
sub("      vb,\n      lastUpdate:", "      vb, mapCities,\n      lastUpdate:")

# ---- A. Chronologie par type d'action
sub("this.state = { data: null, seuils: ALL_SEUILS(), cats: ALL_CATS(), passe: true, week: null,", "this.state = { data: null, seuils: ALL_SEUILS(), cats: ALL_CATS(), passe: true, chrT: false, week: null,")
sub('''  <div class="chr">\n      <div class="chr-h">''', '''  <div class="chr">
      <div class="ctog" role="group"><button sc-camel-on-click="{{chrDay}}" aria-pressed="{{chrDayOn}}">Par jour</button><button sc-camel-on-click="{{chrType}}" aria-pressed="{{chrTypeOn}}">Par type</button></div>
      <div class="chr-h">''')
sub('''      <button class="skip" sc-camel-on-click="{{skipChr}}">Passer la chronologie</button>\n      <div class="chr-sc" id="chr-sc">''',
    '''      <button class="skip" sc-camel-on-click="{{skipChr}}">Passer la chronologie</button>
      <sc-if value="{{chrTOn}}" hint-placeholder-val="{{false}}">
      <div class="ct-sc"><div class="ct" style="{{ctGrid}}">
        <span class="ct-h"></span>
        <sc-for list="{{ctHead}}" as="h" hint-placeholder-count="8"><span class="ct-h">{{h}}</span></sc-for>
        <span class="ct-h"></span>
        <sc-for list="{{ctRows}}" as="r" hint-placeholder-count="7">
          <span class="ct-l">{{r.label}}</span>
          <sc-for list="{{r.cells}}" as="c" hint-placeholder-count="8"><span class="ct-c" style="{{c.style}}">
            <sc-for list="{{c.dots}}" as="dot" hint-placeholder-count="1"><button class="pt wd ctd" data-id="{{dot.id}}" sc-camel-on-click="{{dot.pick}}" aria-label="{{dot.label}}" style="{{dot.style}}"><span class="{{dot.hxc}}" style="{{dot.hex}}"></span></button></sc-for>
          </span></sc-for>
          <span class="ct-n">{{r.n}}</span>
        </sc-for>
      </div></div>
      </sc-if>
      <div class="chr-sc" id="chr-sc" style="{{chrDayStyle}}">''')
sub("    return {\n      loading: !D,", """    const ctW = Array.from({ length: NWC }, (_, i) => i);
    const ctCats = [...new Set(timeline.map(e => e.cat))].map(c => [c, timeline.filter(e => e.cat === c).length]).sort((a, b) => b[1] - a[1]);
    const ctRows = ctCats.map(([c, n]) => ({ label: L(c), n: String(n), cells: ctW.map(i => {
      const evs = timeline.filter(e => e.cat === c && weekOf(e.date) === i).sort((a, b) => rank(a) - rank(b) || (a.date < b.date ? -1 : 1));
      return { style: st.week !== null && st.week !== i ? 'opacity:.25' : '', dots: evs.map(e => { const selD = e.id === st.sel; return {
        id: e.id, label: fShort(e.date) + ' — ' + e.nom + ' — ' + L(e.cat) + ', ' + L(e.seuil),
        pick: () => { if (selD) { closeSel(); return; } set(filtered.includes(e) ? { sel: e.id } : { sel: e.id, day: null, week: null }); openSel(e); const el = document.getElementById('carte'); if (el) scrollToEl(el, 'center'); },
        style: 'position:relative;transform:none;flex:none;width:13px;height:13px;padding:0;border:0;background:transparent',
        hxc: selD ? '' : 'hx', hex: HEX + (selD ? ';background:#ffffff' : ';--c:' + COLOR[e.seuil] + ';--f:' + FILL[e.seuil] + DOT(e.seuil)) }; }) };
    }) }));
    return {
      chrTOn: !!st.chrT, chrDayOn: st.chrT ? 'false' : 'true', chrTypeOn: st.chrT ? 'true' : 'false',
      chrDay: () => set({ chrT: false }), chrType: () => { set({ chrT: true }); setTimeout(() => { const s = document.querySelector('.ct-sc'); if (s) s.scrollLeft = s.scrollWidth; }, 60); }, chrDayStyle: st.chrT ? 'display:none' : '',
      ctHead: ctW.map(wLab), ctRows, ctGrid: 'grid-template-columns:minmax(100px,170px) repeat(' + NWC + ',minmax(54px,1fr)) 34px',
      loading: !D,""")
# en mode « par type » : intitulé et cumul propres à la vue par jour masqués ; semaine en cours incluse
sub('''      <div class="chr-h">\n        <span style="display: inline-flex; align-items: center; gap: 8px; font-size: 11px;''', '''      <div class="chr-h">\n        <span class="chr-dl" style="display: inline-flex; align-items: center; gap: 8px; font-size: 11px;''')
sub('''        <span style="font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #a3a09a;">{{cumLabel}}</span>''', '''        <span class="chr-dl" style="font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #a3a09a;">{{cumLabel}}</span>''')
sub('''  <div class="chr">\n      <div class="ctog"''', '''  <div class="chr" data-t="{{chrTypeOn}}">\n      <div class="ctog"''')
sub("    const ctW = Array.from({ length: NWC }, (_, i) => i);", "    const ctW = Array.from({ length: NW }, (_, i) => i);")
sub("repeat(' + NWC + ',minmax(54px,1fr)) 34px'", "repeat(' + NW + ',minmax(64px,1fr)) 34px'")
# « Passer la chronologie » valable aussi en vue par type : le focus va juste après le tableau
sub("      </div></div>\n      </sc-if>\n      <div class=\"chr-sc\"", "      </div></div>\n      <span id=\"sk-ct\" tabindex=\"-1\"></span>\n      </sc-if>\n      <div class=\"chr-sc\"")
sub("skipChr: () => { const el = document.getElementById('sk-wk'); if (el) el.focus(); },", "skipChr: () => { const el = document.getElementById(st.chrT ? 'sk-ct' : 'sk-wk'); if (el) el.focus(); },")
