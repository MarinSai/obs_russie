# ════════════════════════════════════════════════════════════════════
#  QUATRIÈME PASSE : densité, carte de situation, lien de l'événement, surface des hexagones, marge à l'ouest
#  (exécuté par patch.py après patch_v3.py)
# ════════════════════════════════════════════════════════════════════

# ── Vue d'ensemble décalée vers l'ouest : le Portugal n'est plus collé au bord ──
sub("const DEFZ = { k: ZMIN, cx: 47.3, cy: 57.6 };", "const DEFZ = { k: ZMIN, cx: 44.2, cy: 57.6 };")

# ── Hexagones : liseré clair et dégradé intérieur ; pictogramme du type quand l'hexagone est assez grand ──
sub('''<span style="{{p.hex}}"></span><span style="{{p.core}}"></span></button>''',
    '''<span class="{{p.hxc}}" style="{{p.hex}}"></span><span style="{{p.core}}"></span><svg class="gly" sc-camel-view-box="0 0 24 24" aria-hidden="true" style="{{p.gs}}"><path d="{{p.g}}" fill-rule="evenodd"></path></svg></button>''')
sub("hex: 'position:absolute;inset:0;' + (nc ? HEXP : HEX) + ';background:' + (sel ? '#ffffff' : SHEEN + c) + (nc && !sel ? ';opacity:.8' : ''),",
    "hxc: sel ? '' : 'hx', g: GLYPH[CATKEY[e.cat]][0], gs: glyphStyle(CATKEY[e.cat], sz >= 18 && !sel && !e.passe),\n        hex: 'position:absolute;inset:0;' + (nc ? HEXP : HEX) + (sel ? ';background:#ffffff' : ';--c:' + c) + (nc && !sel ? ';opacity:.8' : ''),")
sub('''<span style="{{dot.hex}}"></span></button>''',
    '''<span class="{{dot.hxc}}" style="{{dot.hex}}"></span><svg class="gly" sc-camel-view-box="0 0 24 24" aria-hidden="true" style="{{dot.gs}}"><path d="{{dot.g}}" fill-rule="evenodd"></path></svg></button>''')
sub("hex: HEX + ';background:' + (selD ? '#ffffff' : SHEEN + COLOR[e.seuil])",
    "hxc: selD ? '' : 'hx', g: GLYPH[CATKEY[e.cat]][0], gs: glyphStyle(CATKEY[e.cat], !selD && HXC >= 17),\n            hex: HEX + (selD ? ';background:#ffffff' : ';--c:' + COLOR[e.seuil])", n=2)

# ── Densité : nappe très discrète sous les hexagones, dessinée sur un canevas ──
sub('''        <sc-if value="{{loading}}" hint-placeholder-val="{{false}}">''',
    '''        <canvas id="heat" aria-hidden="true"></canvas>
        <sc-if value="{{loading}}" hint-placeholder-val="{{false}}">''')
sub("this.mapNow = { k: Z.k, cx: Z.cx, cy: Z.cy, asp: ASP, w: wPx, h: hPx, sel: st.sel, items };",
    "this.mapNow = { k: Z.k, cx: Z.cx, cy: Z.cy, asp: ASP, w: wPx, h: hPx, sel: st.sel, items, sig: key };")
sub('''    this.mapMotion();
    // Fiche : changement d'événement sans fermeture''', '''    this.mapMotion();
    this.drawHeat();
    // Fiche : changement d'événement sans fermeture''')
sub('''  // Onde discrète autour d'un hexagone''', '''  // Nappe de densité : une tache floue par événement affiché ; les taches se cumulent là où les événements se serrent
  drawHeat() {
    const cv = document.getElementById('heat'), m = this.mapNow;
    if (!cv || !m || !cv.getContext) return;
    const hk = [m.k, m.cx, m.cy, m.w, m.h, m.sig].join('|');
    if (this.heatKey === hk) return;
    this.heatKey = hk;
    const q = .5, W = Math.max(1, Math.round(m.w * q)), H = Math.max(1, Math.round(m.h * q)); // demi-résolution : la nappe est floue
    if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; }
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, W, H);
    // en zoomant, la tache s'élargit moins vite que la carte et s'éclaircit : la nappe reste un fond
    const zf = Math.max(1, m.k / ZMIN), R = Math.max(24, m.w * .052 * ZMIN * Math.pow(zf, .62)) * q, al = 1 / Math.pow(zf, .55);
    m.items.forEach(b => {
      const x = (b.sx - m.cx * m.k + 50) / 100 * W, y = (b.sy - m.cy * m.k * m.asp + 50) / 100 * H;
      if (x < -R || x > W + R || y < -R || y > H + R) return;
      const g = ctx.createRadialGradient(x, y, 0, x, y, R);
      g.addColorStop(0, 'rgba(255,226,194,' + (.11 * al).toFixed(3) + ')'); g.addColorStop(.5, 'rgba(255,226,194,' + (.045 * al).toFixed(3) + ')'); g.addColorStop(1, 'rgba(255,226,194,0)');
      ctx.fillStyle = g; ctx.fillRect(x - R, y - R, 2 * R, 2 * R);
    });
  }
  // Carte de situation : le cadre rouge suit la vue, y compris pendant un geste
  miniRect() {
    const r = document.getElementById('mini-r');
    if (!r) return;
    const z = this.live || this.renderZ || this.state.z, w = 1000 / z.k, h = 720 / (z.k * ASP);
    r.setAttribute('x', (z.cx * 10 - w / 2).toFixed(1)); r.setAttribute('y', (z.cy * 7.2 - h / 2).toFixed(1));
    r.setAttribute('width', w.toFixed(1)); r.setAttribute('height', h.toFixed(1));
  }
  // Onde discrète autour d'un hexagone''')

# ── Carte de situation : miniature de la vue d'ensemble, visible dès qu'on a zoomé ; un clic recentre ──
sub('''  paint() {
    const L = document.getElementById('mapLayer'); if (!L) return;''', '''  paint() {
    const L = document.getElementById('mapLayer'); if (!L) return;
    this.miniRect();''')
sub('''pointer-events: none;">{{zoomHint}}</span>''', '''pointer-events: none;">{{zoomHint}}</span>
        <button class="mini" tabindex="-1" aria-hidden="true" sc-camel-on-click="{{miniPick}}" style="{{miniStyle}}"><svg sc-camel-view-box="{{miniVb}}" sc-camel-preserve-aspect-ratio="xMidYMid slice" style="display: block; width: 100%; height: 100%;"><path d="{{land}}" fill="#33333a"></path><path d="{{ukr}}" fill="#4b4536"></path><path d="{{east}}" fill="#4d1a23"></path><rect id="mini-r" x="0" y="0" width="10" height="10" fill="rgba(221,32,60,.16)" stroke="#dd203c" stroke-width="1.5" vector-effect="non-scaling-stroke"></rect></svg></button>''')
sub('''    const points = pts.map(({ e, j, xy }) => {''', '''    // Carte de situation
    const mz = clampZ(defZ()), mvW = 1000 / mz.k, mvH = 720 / (mz.k * ASP), mvX = mz.cx * 10 - mvW / 2, mvY = mz.cy * 7.2 - mvH / 2;
    const miniOn = Z.k > mz.k * 1.3, miniW = wPx < 560 ? 92 : 150;
    const miniStyle = 'position:absolute;z-index:6;left:14px;bottom:' + (wPx < 560 ? 30 : 36) + 'px;width:' + miniW + 'px;height:' + Math.round(miniW * hPx / wPx) + 'px;padding:0;border:1px solid #3a3a3d;border-radius:4px;overflow:hidden;background:rgba(12,12,13,.92);box-shadow:0 8px 24px rgba(0,0,0,.45);cursor:pointer;transition:opacity .3s,transform .3s cubic-bezier(.2,.7,.2,1);opacity:' + (miniOn ? 1 : 0) + ';transform:translateY(' + (miniOn ? 0 : 8) + 'px);pointer-events:' + (miniOn ? 'auto' : 'none');
    const miniPick = ev => {
      const r = ev.currentTarget.getBoundingClientRect(), z = this.view();
      this.backZ = null; this.cBack = null;
      animTo({ k: z.k, cx: (mvX + (ev.clientX - r.left) / r.width * mvW) / 10, cy: (mvY + (ev.clientY - r.top) / r.height * mvH) / 7.2 }, true);
    };
    const points = pts.map(({ e, j, xy }) => {''')
sub('''      mapLabels, glows,''', '''      mapLabels, glows, miniStyle, miniPick, miniVb: mvX.toFixed(1) + ' ' + mvY.toFixed(1) + ' ' + mvW.toFixed(1) + ' ' + mvH.toFixed(1),''')

# ── Lien de l'événement : bouton qui copie l'adresse (identifiant de la base, sans texte à traduire) ──
sub('''                <a href="{{src.url}}" target="_blank" rel="noopener" style="font-size: 14px;">↗ {{src.host}}</a>
              </sc-for>
            </div>
          </article>''', '''                <a href="{{src.url}}" target="_blank" rel="noopener" style="font-size: 14px;">↗ {{src.host}}</a>
              </sc-for>
            </div>
            <button class="cpl" sc-camel-on-click="{{copyLink}}" aria-label="{{sel.id}}" style="{{sel.cplStyle}}">
              <sc-if value="{{sel.notCopied}}" hint-placeholder-val="{{true}}"><svg width="13" height="13" sc-camel-view-box="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1.2 1.2"></path><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1.2-1.2"></path></svg></sc-if>
              <sc-if value="{{sel.copied}}" hint-placeholder-val="{{false}}"><svg width="13" height="13" sc-camel-view-box="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 12.5l5 5 10-11"></path></svg></sc-if>
              <span>{{sel.id}}</span>
            </button>
          </article>''')
sub('''      nom: s.nom, cat: L(s.cat), seuil: L(s.seuil), desc: s.desc, passe: s.passe,''',
    '''      nom: s.nom, cat: L(s.cat), seuil: L(s.seuil), desc: s.desc, passe: s.passe,
      id: s.id, copied: st.copied === s.id, notCopied: st.copied !== s.id,
      cplStyle: 'align-self:flex-start;display:inline-flex;align-items:center;gap:8px;margin-top:2px;padding:7px 10px;border:1px solid ' + (st.copied === s.id ? '#dd203c' : '#333336') + ';background:none;font-family:\\'IBM Plex Mono\\',monospace;font-size:11.5px;letter-spacing:.04em;color:' + (st.copied === s.id ? '#f3f1ec' : '#a3a09a'),''')
sub('''    } : { nom: '', cat: '', seuil: '', desc: '', passe: false, dateLong: '', entree: '', lieu: '', seuilStyle: '', sources: [] };''',
    '''    } : { nom: '', cat: '', seuil: '', desc: '', passe: false, dateLong: '', entree: '', lieu: '', seuilStyle: '', sources: [], id: '', copied: false, notCopied: true, cplStyle: 'display:none' };
    // Adresse de l'événement : celle de la page qui intègre l'Observatoire quand elle est lisible (même domaine), sinon celle de cette page
    const copyLink = () => {
      if (!s) return;
      let base = window.location.href.split('#')[0];
      try { if (window.self !== window.top && window.top.location.href) base = window.top.location.href.split('#')[0]; } catch (err) {}
      const url = base + '#' + s.id, id = s.id;
      const ok = () => { this.setState({ copied: id }); clearTimeout(this.cpt); this.cpt = setTimeout(() => this.setState({ copied: null }), 1800); };
      const old = () => { try { const ta = document.createElement('textarea'); ta.value = url; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:absolute;left:-9999px;top:' + (window.scrollY || 0) + 'px'; document.body.appendChild(ta); ta.select(); const done = document.execCommand('copy'); ta.remove(); if (done) ok(); } catch (err) {} };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(ok, old); else old();
    };''')
sub('''      mapBoxStyle, zoomHint, panStart,''', '''      copyLink, mapBoxStyle, zoomHint, panStart,''')
# le lien peut arriver par l'adresse de la page qui intègre l'Observatoire (même domaine)
sub('''    const id = decodeURIComponent((window.location.hash || '').slice(1));''',
    '''    let hsh = window.location.hash || '';
    if (!hsh && window.self !== window.top) { try { hsh = window.top.location.hash || ''; } catch (err) {} }
    const id = decodeURIComponent(hsh.slice(1));''')
