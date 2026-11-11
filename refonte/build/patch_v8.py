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
