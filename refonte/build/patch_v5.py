# ════════════════════════════════════════════════════════════════════
#  CINQUIÈME PASSE : fiche pays, légende des pictogrammes et du halo
#  (exécuté par patch.py après patch_v4.py)
#  Aucun texte nouveau : tous les libellés existent déjà dans la page (donc dans i18n.py).
# ════════════════════════════════════════════════════════════════════

_LAB = "font-size: 10.5px; letter-spacing: .18em; text-transform: uppercase; color: #a3a09a;"
_FP_INNER = '''
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
              <span style="''' + _LAB + ''' padding-top: 10px;">Pays les plus visés<span style="font-family: 'IBM Plex Mono', monospace; letter-spacing: .04em;"> — {{cf.rank}}</span></span>
              <button sc-camel-on-click="{{cf.close}}" class="ib" aria-label="Fermer le détail" style="flex: none; border: 1px solid #333336; border-radius: 50%; background: none; width: 34px; height: 34px; display: grid; place-items: center; color: #dedbd6;"><svg width="12" height="12" sc-camel-view-box="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M2 2l10 10M12 2 2 12"></path></svg></button>
            </div>
            <h3 class="fp-t" style="margin: -6px 0 0; font-family: 'GC Sanomat', Georgia, serif; font-weight: 400; font-size: 36px; line-height: 1.02; letter-spacing: -.01em;">{{cf.name}}</h3>
            <div style="display: flex; align-items: flex-end; gap: 14px; border-bottom: 1px solid #262628; padding-bottom: 14px;">
              <span class="fig" style="font-size: 54px; line-height: .86; color: #ea4d62;">{{cf.n}}</span>
              <span style="font-size: 11.5px; letter-spacing: .16em; text-transform: uppercase; color: #a3a09a; padding-bottom: 2px;">Événements affichés</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 9px;">
              <span style="''' + _LAB + '''">Seuil d'attribution</span>
              <div style="display: flex; gap: 2px; height: 8px;"><sc-for list="{{cf.seg}}" as="g" hint-placeholder-count="3"><span style="{{g.style}}"></span></sc-for></div>
              <div style="display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 13px; color: #c9c5bd;">
                <sc-for list="{{cf.seuils}}" as="g" hint-placeholder-count="3"><span style="display: inline-flex; align-items: center; gap: 7px;"><span class="hx" style="{{g.sw}}"></span>{{g.label}} <span style="font-family: 'IBM Plex Mono', monospace; color: #f3f1ec;">{{g.n}}</span></span></sc-for>
              </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 7px;">
              <span style="''' + _LAB + '''">{{tType}}</span>
              <sc-for list="{{cf.cats}}" as="c" hint-placeholder-count="3">
                <div style="display: flex; align-items: center; gap: 10px; font-size: 14px;">
                  <svg width="15" height="15" sc-camel-view-box="0 0 24 24" aria-hidden="true" style="{{c.gs}}"><path d="{{c.g}}" fill-rule="evenodd"></path></svg>
                  <span style="width: 112px; flex: none; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{c.label}}</span>
                  <span style="flex: 1; height: 5px; background: #1c1c1e;"><span style="{{c.bar}}"></span></span>
                  <span style="width: 18px; text-align: right; font-family: 'IBM Plex Mono', monospace; font-size: 13px;">{{c.n}}</span>
                </div>
              </sc-for>
            </div>
            <div style="display: flex; flex-direction: column; gap: 6px;">
              <span style="''' + _LAB + '''">La chronologie</span>
              <div style="display: flex; align-items: stretch; height: 78px; border-bottom: 1px solid #3a3a3d;">
                <sc-for list="{{cf.cols}}" as="w" hint-placeholder-count="8"><span style="{{w.style}}"><sc-for list="{{w.dots}}" as="d" hint-placeholder-count="0"><span class="hx" style="{{d.s}}"></span></sc-for></span></sc-for>
              </div>
              <div style="{{cf.dStyle}}"><span>{{cf.d0}}</span><span>{{cf.d1}}</span></div>
            </div>
            <div style="display: flex; flex-direction: column;">
              <span style="''' + _LAB + ''' margin-bottom: 8px;">Le journal</span>
              <sc-for list="{{cf.last}}" as="j" hint-placeholder-count="3">
                <button class="fj" sc-camel-on-click="{{j.pick}}"><span class="fj-d">{{j.date}}</span><span class="fj-t"><span class="hx" style="{{j.sw}}"></span>{{j.nom}}</span></button>
              </sc-for>
            </div>
'''

# ── Fiche pays sur la carte (ordinateur) : même cadre que la fiche d'un événement ──
sub('''        <!-- Fiche -->''',
    '''        <!-- Fiche pays -->
        <sc-if value="{{cf.map}}" hint-placeholder-val="{{false}}">
          <article class="fiche fpays" style="position: absolute; z-index: 10; top: 14px; right: 14px; bottom: 14px; width: min(390px, calc(100% - 28px)); overflow-y: auto; box-sizing: border-box; background: #0d0d0e; border: 1px solid #333336; border-top: 2px solid #dd203c; border-radius: 6px; padding: 16px 24px 22px; display: flex; flex-direction: column; gap: 16px; box-shadow: 0 20px 60px rgba(0,0,0,.5);">''' + _FP_INNER + '''          </article>
        </sc-if>

        <!-- Fiche -->''')

# ── Sur mobile, le classement est sous la carte : la fiche pays s'ouvre sur place, sous le classement ──
sub('''        </sc-for>
      </div>
    </aside>''',
    '''        </sc-for>
        <sc-if value="{{cf.inline}}" hint-placeholder-val="{{false}}">
          <article class="fpays fpays-in" style="margin-top: 12px; box-sizing: border-box; background: #0d0d0e; border: 1px solid #333336; border-top: 2px solid #dd203c; border-radius: 6px; padding: 12px 16px 16px; display: flex; flex-direction: column; gap: 15px;">''' + _FP_INNER + '''          </article>
        </sc-if>
      </div>
    </aside>''')

# ── Données de la fiche pays : les événements affichés sur la carte pour ce pays ──
sub("const rk = [...m].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 8);",
    "const rkAll = [...m].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])), rk = rkAll.slice(0, 8);")
sub("pick: () => set({ country: on ? null : name, sel: null }),",
    "pick: () => set({ country: on ? null : name, sel: null, cfOff: false }),")
sub('''    // Adresse de l'événement : celle de la page qui intègre l'Observatoire''',
    '''    // Fiche pays : ouverte quand un pays est choisi dans le classement, tant qu'aucun événement n'est ouvert
    const cfShow = !!st.country && !s && !st.cfOff, cfN = st.country ? m.get(st.country) : 0;
    const cfL = cfShow ? filtered.slice().sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0)) : [];
    const cfSw = (c, z) => 'position:relative;display:inline-block;flex:none;width:' + z + 'px;height:' + (z * 1.1).toFixed(1) + 'px;' + HEX + ';--c:' + c;
    const cfRank = e => SEUILS.findIndex(x => x.id === e.seuil);
    const cfSe = SEUILS.map(sv => ({ id: sv.id, color: sv.color, n: cfL.filter(e => e.seuil === sv.id).length })).filter(x => x.n);
    const cfCa = Object.keys(CATKEY).map(c => ({ c, n: cfL.filter(e => e.cat === c).length })).filter(x => x.n).sort((a, b) => b.n - a.n);
    const cfMax = Math.max(1, ...cfCa.map(x => x.n));
    const cfAnt = e => e.passe || dayIdx(e.date) < 0, cfOld = cfL.filter(cfAnt), cfW = Array.from({ length: NW }, (_, i) => cfL.filter(e => !cfAnt(e) && Math.min(NW - 1, weekOf(e.date)) === i).sort((a, b) => cfRank(a) - cfRank(b)));
    const cfTop = Math.max(1, cfOld.length, ...cfW.map(x => x.length)), cfHs = Math.max(5, Math.min(11, Math.floor(74 / cfTop / 1.1) - 1));
    const cfCol = (list, old, i) => ({ style: 'flex:1 1 0;min-width:0;display:flex;flex-direction:column-reverse;align-items:center;gap:1px;padding-bottom:2px;' + (old ? 'border-right:1px dashed #4a4950;opacity:.6' : i ? 'border-left:1px solid #1c1c1e' : ''), dots: list.map(e => ({ s: cfSw(COLOR[e.seuil], cfHs) })) });
    const cfD = i => { const d = dateOfDay(weekStartDay(i)); return d.getDate() + ' ' + MOIS[d.getMonth()]; };
    const cf = {
      map: cfShow && st.vw >= 760, inline: cfShow && st.vw < 760,
      name: st.country || '', n: String(cfL.length), rank: !cfN ? '–' : (rkAll.filter(r => r[1] > cfN).length + 1) + ' / ' + rkAll.length,
      close: () => set({ cfOff: true }),
      seg: cfSe.map(x => ({ style: 'flex:' + x.n + ' 1 0;background:' + x.color })),
      seuils: cfSe.map(x => ({ label: L(x.id), n: String(x.n), sw: cfSw(x.color, 10) })),
      cats: cfCa.map(x => ({ label: L(x.c), n: String(x.n), g: GLYPH[CATKEY[x.c]][0], gs: 'flex:none;' + (GLYPH[CATKEY[x.c]][1] ? 'fill:none;stroke:#b9b6b0;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round' : 'fill:#b9b6b0;stroke:none'), bar: 'display:block;height:100%;width:' + (x.n / cfMax * 100).toFixed(1) + '%;background:#dedbd6' })),
      cols: (cfOld.length ? [cfCol(cfOld, true, 0)] : []).concat(cfW.map((x, i) => cfCol(x, false, i))),
      d0: cfD(0), d1: cfD(NW - 1), dStyle: 'display:flex;justify-content:space-between;font-family:IBM Plex Mono,monospace;font-size:10px;letter-spacing:.04em;color:#8f8c86;padding-left:' + (cfOld.length ? (100 / (NW + 1)).toFixed(2) + '%' : '0'),
      last: cfL.slice(0, 3).map(e => { const p = parse(e.date); return {
        date: cfAnt(e) ? fShort(e.date) : p.j + ' ' + MOIS[p.m - 1], nom: e.nom, sw: cfSw(COLOR[e.seuil], 9) + ';margin-right:8px',
        pick: () => { set({ sel: e.id }); openSel(e); if (st.vw < 760) { const el = document.getElementById('carte'); if (el) scrollToEl(el, 'center'); } }
      }; })
    };
    // Légende des pictogrammes : les types d'action, avec le même dessin que dans les hexagones
    const legendTypes = Object.keys(CATKEY).filter(c => CATKEY[c] !== 'nc').map(c => ({ label: L(c), g: GLYPH[CATKEY[c]][0], gs: glyphStyle(CATKEY[c], true) }));

    // Adresse de l'événement : celle de la page qui intègre l'Observatoire''')
sub("legend, legendPasse, legendPasseCore, legendNc,", "legend, legendPasse, legendPasseCore, legendNc, cf, legendTypes, tType: 'Type',")

# Échap ferme aussi la fiche pays ; la carte cadre le pays dans la partie laissée libre par la fiche
sub("this.onKey = ev => { if (ev.key === 'Escape' && this.state.sel && this.closeSel) this.closeSel(); };",
    "this.onKey = ev => { if (ev.key !== 'Escape') return; if (this.state.sel && this.closeSel) this.closeSel(); else if (this.state.country && !this.state.cfOff) this.setState({ cfOff: true }); };")
sub("const z = this.fitCountry && this.fitCountry(st.country); if (z) this.animTo(z, true); }",
    "let z = this.fitCountry && this.fitCountry(st.country); if (z && MAPW > 700 && ASP >= .9) z = { ...z, cx: z.cx + 202 / MAPW * 100 / z.k }; if (z) this.animTo(z, true); }")

# ── Légende : le halo est montré sur les pastilles des seuils qui le portent (carte et panneau latéral) ──
sub('''<span style="display: inline-flex; align-items: center; gap: 8px;"><span style="{{l.sw}}"></span>{{l.label}}</span>
        </sc-for>
        <span class="lg-sep"''',
    '''<span style="display: inline-flex; align-items: center; gap: 8px;"><span style="{{l.gw}}"><span style="{{l.sw}}"></span></span>{{l.label}}</span>
        </sc-for>
        <span class="lg-sep"''')
sub("const legend = SEUILS.map(sv => ({ label: L(sv.id), sw: ", "const legend = SEUILS.map(sv => ({ label: L(sv.id), gw: haloStyle(sv.id, sv.color, true), sw: ")
sub('''<span style="{{s.dot}}"></span>''', '''<span style="{{s.gw}}"><span style="{{s.dot}}"></span></span>''')
sub("        dot: 'width:13px;height:13px;flex:none;' + HEX + ';background:' + s.color + ';opacity:' + (on ? 1 : .3),",
    "        gw: haloStyle(s.id, s.color, on),\n        dot: 'width:13px;height:13px;flex:none;' + HEX + ';background:' + s.color + ';opacity:' + (on ? 1 : .3),")

# ── Légende : une ligne « Type » sous celle des seuils, avec les pictogrammes ──
_CARTE = '''      <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 20px; margin-top: 8px; font-size: 12.5px; color: #dedbd6;">
        <span class="lg-h" style="font-size: 10.5px; letter-spacing: .18em; text-transform: uppercase; color: #a3a09a;">Carte</span>'''
sub(_CARTE, '''      <div class="lg-types" style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 18px; margin-top: 8px; font-size: 12.5px; color: #dedbd6;">
        <span class="lg-h" style="font-size: 10.5px; letter-spacing: .18em; text-transform: uppercase; color: #a3a09a;">{{tType}}</span>
        <sc-for list="{{legendTypes}}" as="l" hint-placeholder-count="6">
          <span style="display: inline-flex; align-items: center; gap: 7px;"><span style="position: relative; display: inline-block; flex: none; width: 17px; height: 19px;"><span class="hx" style="position: absolute; inset: 0; clip-path: var(--mh); --c: #a9a59d;"></span><svg class="gly" sc-camel-view-box="0 0 24 24" aria-hidden="true" style="{{l.gs}}"><path d="{{l.g}}" fill-rule="evenodd"></path></svg></span>{{l.label}}</span>
        </sc-for>
      </div>
''' + _CARTE)
