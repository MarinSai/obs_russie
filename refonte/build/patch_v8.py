# ════════════════════════════════════════════════════════════════════
#  HUITIÈME PASSE (retours sur téléphone) : déplacement à un doigt, chronologie par jour défilante, alignements
# ════════════════════════════════════════════════════════════════════

# ── Carte zoomée : un doigt déplace la carte (à l'échelle d'ensemble, il fait défiler la page) ──
sub("border-radius:6px;overflow:hidden;user-select:none;touch-action:pan-y;cursor:'",
    "border-radius:6px;overflow:hidden;user-select:none;touch-action:' + (Z.k > ZMIN + 0.05 ? 'none' : 'pan-y') + ';cursor:'")
sub("const panStart = ev => { if (ev.button !== 0 || ev.target.closest('button,a,input,article')) return;",
    "const panStart = ev => { if (ev.button !== 0 || ev.isPrimary === false || this.pinch || ev.target.closest('button,a,input,article')) return;")
sub("const panMove = ev => { const d = this.drag; if (!d) return;", "const panMove = ev => { const d = this.drag; if (!d || this.pinch || ev.isPrimary === false) return;")

# ── Chronologie : par jour aussi sur téléphone ; la frise défile horizontalement et s'ouvre sur la dernière semaine ──
sub('''      <div id="chrono" data-rv="bars" style="{{slotGrid}}">''',
    '''      <div class="chr-sc" id="chr-sc">
      <div id="chrono" data-rv="bars" style="{{slotGrid}}">''')
sub('''            <span style="{{w.track}}"><span class="wkbar" style="{{w.bar}}"></span></span>
          </button>
        </sc-for>
      </div>
  </div>''', '''            <span style="{{w.track}}"><span class="wkbar" style="{{w.bar}}"></span></span>
          </button>
        </sc-for>
      </div>
      </div>
  </div>''')
sub("    const CW = st.cw || Math.max(280, Math.min(st.vw, 1440) - 2 * Math.min(40, st.vw * .03));",
    "    const CW0 = st.cw || Math.max(280, Math.min(st.vw, 1440) - 2 * Math.min(40, st.vw * .03)), scD = CW0 < 760 && CW0 / (NWC * 7) < 15, CW = scD ? NWC * 7 * 22 : CW0;")
sub("const slotGrid = 'display:grid;grid-template-columns:repeat(' + NCOL + ',minmax(0,1fr));border-bottom:1px solid #3a3a3d';",
    "const slotGrid = 'display:grid;grid-template-columns:repeat(' + NCOL + ',minmax(0,1fr));border-bottom:1px solid #3a3a3d' + (scD ? ';width:' + CW + 'px' : '');")
sub("const weekGrid = 'display:grid;grid-template-columns:repeat(' + NWC + ',minmax(0,1fr))';",
    "const weekGrid = 'display:grid;grid-template-columns:repeat(' + NWC + ',minmax(0,1fr))' + (scD ? ';width:' + CW + 'px' : '');")
sub("    const ch = document.getElementById('chrono');\n    if (ch) {", "    const ch = document.getElementById('chr-sc');\n    if (ch) {")
sub("      sync();\n    }\n    // Méthodologie",
    "      sync();\n      if (ch.scrollWidth > ch.clientWidth + 4 && this.chrEnd !== ch.scrollWidth) { this.chrEnd = ch.scrollWidth; ch.scrollLeft = ch.scrollWidth; }\n    }\n    // Méthodologie")

# ── Glisser en partant d'un hexagone déplace aussi la carte ; un simple toucher l'ouvre toujours
#    (la capture du pointeur n'est prise qu'après 6 px de mouvement, pour ne pas voler le clic) ──
sub("ev.target.closest('button,a,input,article')) return; cancelAnimationFrame(this.zr); clearTimeout(this.ct); const [fx, fy] = rel(ev); this.drag = { fx, fy, z: this.view() }; try { ev.currentTarget.setPointerCapture(ev.pointerId); } catch (err) {} ev.currentTarget.classList.add('drag'); };",
    "ev.target.closest('button:not(.pt),a,input,article,.mini')) return; cancelAnimationFrame(this.zr); clearTimeout(this.ct); const [fx, fy] = rel(ev); this.drag = { fx, fy, x0: ev.clientX, y0: ev.clientY, z: this.view(), id: ev.pointerId, el: ev.currentTarget, cap: false }; };")
sub("const panMove = ev => { const d = this.drag; if (!d || this.pinch || ev.isPrimary === false) return; this.backZ = null;",
    "const panMove = ev => { const d = this.drag; if (!d || this.pinch || ev.isPrimary === false) return; if (!d.cap) { if (Math.hypot(ev.clientX - d.x0, ev.clientY - d.y0) < 6) return; d.cap = true; try { d.el.setPointerCapture(d.id); } catch (err) {} d.el.classList.add('drag'); } this.backZ = null;")
sub("const panEnd = ev => { if (!this.drag) return; this.drag = null;", "const panEnd = ev => { if (!this.drag) return; const moved = this.drag.cap; this.drag = null; if (!moved) return;")

# ── Légende : la pastille « Ukraine » reprend exactement le remplissage et le contour de la carte ──
sub('''<span style="width: 14px; height: 11px; flex: none; background: #242220; border: 1px solid #46423c;"></span>Ukraine : guerre de haute intensité''',
    '''<span style="width: 14px; height: 11px; flex: none; background: #29261f; border: 1px solid #6a604f;"></span>Ukraine : guerre de haute intensité''')

# ── Glisser avec élan : à la fin du geste, la carte continue sur sa lancée puis ralentit (comme une carte native) ──
sub("d.el.classList.add('drag'); } this.backZ = null; this.cBack = null; const [fx, fy] = rel(ev);",
    "d.el.classList.add('drag'); } const tn = performance.now(); (d.sm = d.sm || []).push([tn, ev.clientX, ev.clientY]); while (d.sm.length > 2 && tn - d.sm[0][0] > 90) d.sm.shift(); this.backZ = null; this.cBack = null; const [fx, fy] = rel(ev);")
sub("const panEnd = ev => { if (!this.drag) return; const moved = this.drag.cap; this.drag = null; if (!moved) return; const m = document.getElementById('carte'); if (m) m.classList.remove('drag'); this.commit(); };",
    """const panEnd = ev => {
      if (!this.drag) return; const d = this.drag, moved = d.cap; this.drag = null; if (!moved) return;
      const m = document.getElementById('carte'); if (m) m.classList.remove('drag');
      // vitesse des 90 dernières millisecondes du geste ; pas d'élan si le doigt s'est arrêté avant de se lever
      const S = d.sm || [], a = S[0], b = S[S.length - 1], dt = a && b ? b[0] - a[0] : 0, idle = b ? performance.now() - b[0] : 1e9;
      let vx = dt > 8 ? (b[1] - a[1]) / dt : 0, vy = dt > 8 ? (b[2] - a[2]) / dt : 0; const sp = Math.hypot(vx, vy);
      if (REDUCE() || idle > 60 || sp < 0.3 || !m) { this.commit(); return; }
      if (sp > 2.5) { vx *= 2.5 / sp; vy *= 2.5 / sp; }
      const r = m.getBoundingClientRect(), z0 = this.view(), TAU = 240, t0 = performance.now();
      const step = () => {
        const t = performance.now() - t0, f = TAU * (1 - Math.exp(-t / TAU)), dx = vx * f, dy = vy * f;
        const want = { k: z0.k, cx: z0.cx - dx / r.width * 100 / z0.k, cy: z0.cy - dy / r.height * 100 / (z0.k * ASP) }, got = clampZ(want);
        this.setLive(got);
        const left = Math.hypot(vx, vy) * Math.exp(-t / TAU);
        if (left < 0.02 || Math.abs(got.cx - want.cx) + Math.abs(got.cy - want.cy) > 1e-6) { this.zr = null; this.commit(); return; }
        this.zr = requestAnimationFrame(step);
      };
      this.zr = requestAnimationFrame(step);
    };""")

# ── Journal : dates et titres alignés sur l'intertitre ; le filet rouge de l'événement ouvert passe dans la marge, à 12 px du texte ──
sub("wrap: 'display:flex;flex-direction:column;scroll-margin-top:90px;", "wrap: 'display:flex;flex-direction:column;margin-left:-14px;padding-left:14px;scroll-margin-top:90px;")

# ── Décodage du titre : les lettres russes s'affichent dans un calque posé sur le titre définitif, coupé à ses bords,
#    avec les mêmes retours à la ligne ; plus de saut de mise en page ni de débordement à droite, et plus de rendu complet de la page à chaque image ──
sub('''<span aria-hidden="true">{{t1}} <span class="hl">{{t2}}</span></span></h1>''',
    '''<span class="treal" aria-hidden="true">{{t1}} <span class="hl">{{t2}}</span></span><span class="tscr" aria-hidden="true"></span></h1>''')
sub('''    let f = REDUCE() ? 46 : 0;
    this.decode = setInterval(() => {
      f++;
      const k = Math.min(1, f / 46);
      const scr = s => s.split('').map((ch, i) => (ch === ' ' || i / s.length < k ? ch : GLYPHS[(i * 7 + f * 13) % GLYPHS.length])).join('');
      if (k >= 1) { clearInterval(this.decode); this.setState({ t1: null, t2: null }); }
      else this.setState({ t1: scr(T1), t2: scr(T2) });
    }, 45);''', '''    const startDecode = () => {
      const h = document.querySelector('h1.glitch'), real = h && h.querySelector('.treal'), ov = h && h.querySelector('.tscr');
      if (!h || !real || !ov || REDUCE()) return;
      // lignes du titre définitif, mot par mot
      const lines = []; let top = null, cur = null, n; const tw = document.createTreeWalker(real, NodeFilter.SHOW_TEXT);
      while ((n = tw.nextNode())) {
        const hl = !!(n.parentElement && n.parentElement.closest('.hl')), re = /\\S+/g; let m;
        while ((m = re.exec(n.textContent))) {
          const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
          const t = r.getBoundingClientRect().top;
          if (!cur || Math.abs(t - top) > 6 || cur.hl !== hl) { cur = { w: [], hl }; lines.push(cur); top = t; }
          cur.w.push(m[0]);
        }
      }
      const txt = lines.map(l => l.w.join(' ')), total = txt.reduce((a, s) => a + s.length, 0);
      if (!total) return;
      let f = 0; h.classList.add('dec');
      const draw = () => {
        f++; const k = Math.min(1, f / 46);
        if (k >= 1) { clearInterval(this.decode); h.classList.remove('dec'); ov.textContent = ''; return; }
        let j = 0; ov.textContent = '';
        txt.forEach((s, li) => {
          const out = s.split('').map(ch => { const i = j++; return ch === ' ' || i / total < k ? ch : GLYPHS[(i * 7 + f * 13) % GLYPHS.length]; }).join('');
          if (li) ov.appendChild(document.createTextNode('\\n'));
          if (lines[li].hl) { const sp = document.createElement('span'); sp.className = 'hl'; sp.textContent = out; ov.appendChild(sp); } else ov.appendChild(document.createTextNode(out));
        });
      };
      draw(); this.decode = setInterval(draw, 45);
    };
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => requestAnimationFrame(startDecode)); else requestAnimationFrame(startDecode);''')
