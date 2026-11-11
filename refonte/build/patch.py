#!/usr/bin/env python3
"""Applique la refonte au gabarit d'origine (unpacked/template.html) -> build/template.html.
Chaque remplacement vérifie le nombre d'occurrences attendu : si la page d'origine change, le script s'arrête."""
import re, sys, os
ROOT = '/home/claude/work'
t = open(os.path.join(ROOT, 'unpacked/template.html'), encoding='utf-8').read()
CSS = open(os.path.join(ROOT, 'build/extra.css'), encoding='utf-8').read() + open(os.path.join(ROOT, 'build/assets.css'), encoding='utf-8').read()
MOTION = open(os.path.join(ROOT, 'build/motion.js'), encoding='utf-8').read()

def sub(old, new, n=1, only=None):
    """Remplace `old` par `new`. n = occurrences attendues ; only = n° (0-based) de la seule occurrence à remplacer."""
    global t
    c = t.count(old)
    if c != n:
        sys.exit('ATTENDU %d, TROUVÉ %d : %r' % (n, c, old[:110]))
    if only is None:
        t = t.replace(old, new)
    else:
        i = -1
        for _ in range(only + 1):
            i = t.find(old, i + 1)
        t = t[:i] + new + t[i + len(old):]

def between(a, b, new):
    """Remplace tout le bloc compris entre les repères a (inclus) et b (exclu)."""
    global t
    if t.count(a) != 1 or t.count(b) != 1:
        sys.exit('REPÈRES : %r (%d) / %r (%d)' % (a[:60], t.count(a), b[:60], t.count(b)))
    i, j = t.find(a), t.find(b)
    assert i < j
    t = t[:i] + new + t[j:]

# ══════════════ CSS ══════════════
sub('</style>\n</helmet>', CSS + '</style>\n</helmet>')
sub('.pt:hover{filter:brightness(1.25)}', '.wd:hover{filter:brightness(1.2)}')
sub('.cumpt:hover{transform:translate(-50%,-50%) scale(1.25)}\n', '')

# ══════════════ Gabarit ══════════════
# Ouverture : barres du glitch pilotées directement (plus de rerendu de toute la page à chaque image)
sub('<section style="position: relative; height: clamp(560px, 60vw, 800px); overflow: hidden;">',
    '<section id="hero" style="position: relative; height: clamp(560px, 60vw, 800px); overflow: hidden;">')
sub('''<div aria-hidden="true" style="position: absolute; inset: 0; z-index: 3; pointer-events: none;">
      <sc-for list="{{glBars}}" as="b" hint-placeholder-count="0"><span style="{{b.style}}"></span></sc-for>
    </div>''', '<div id="glbars" aria-hidden="true" style="position: absolute; inset: 0; z-index: 3; pointer-events: none;"></div>')

# Chiffres clés : hiérarchie (chiffre clair, intitulé rouge, précision grise), compteurs
def kf(val, lab, desc):
    return ('''      <div class="kfc">
        <span class="knum fig"><span data-n="{{%s}}" data-count aria-hidden="true"></span><span class="sr-only">{{%s}}</span></span>
        <span class="klab">%s</span>
        <span class="kdesc">%s</span>
      </div>
''' % (val, val, lab, desc))
between('  <!-- Chiffres clés -->', '  <!-- Signalement -->', '''  <!-- Chiffres clés -->
  <section style="max-width: 1440px; margin: 0 auto; padding: 40px clamp(16px, 3vw, 40px) 48px; box-sizing: border-box;">
    <div class="kfg" data-rv="kf">
''' + kf('nAll', 'Opérations russes', 'de sabotage, d’espionnage et de déstabilisation, documentées depuis le 23 septembre 2026.')
    + kf('nPaysAll', 'Pays visés', 'sur les 30 suivis : les 27 États membres, la Moldavie, le Royaume-Uni et la Norvège.')
    + kf('nAttr', 'Attribuées ou confirmées', "les deux niveaux les plus élevés de notre seuil d'attribution.")
    + kf('nWeeks', 'Semaines de veille', 'à partir de la presse et des autorités de chaque pays, dans leur langue.')
    + '''    </div>
  </section>

''')
sub('.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}@media (max-width:760px){.kf{border-left:0!important}}',
    '.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}')
sub('.outnum{color:transparent;-webkit-text-stroke:1px #dd203c}\n@supports not (-webkit-text-stroke:1px #fff){.outnum{color:#dd203c}}\n', '')

# Signalement
sub('<a href="mailto:contact@legrandcontinent.eu" target="_blank" rel="noopener" style=',
    '<a class="cta" href="mailto:contact@legrandcontinent.eu" target="_blank" rel="noopener" style=')

# En-têtes de section : apparition à l'entrée dans l'écran
sub('<header style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 20px 40px; padding:',
    '<header data-rv="up" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 20px 40px; padding:', n=4)

# Types d'action
sub('''<nav aria-label="Types d'action" style=''', '''<nav class="tnav" data-all="{{catsAll}}" aria-label="Types d'action" style=''')
sub('''<span style="font-family: 'IBM Plex Mono', monospace; letter-spacing: 0; color: #75736e;">''',
    '''<span style="font-family: 'IBM Plex Mono', monospace; letter-spacing: 0; color: #8f8c86;">''', n=7)

# Panneau latéral
sub('''<span style="font-family: 'GC Sanomat', Georgia, serif; font-size: 64px; line-height: .95;">{{total}}</span>''',
    '''<span class="fig" style="font-size: 64px; line-height: .95;"><span data-n="{{total}}" aria-hidden="true"></span><span class="sr-only">{{total}}</span></span>''')
sub('<span style="font-size: 14px; color: #dd203c; line-height: 1.45;">{{nPays}} pays — {{scope}}</span>',
    '<span style="font-size: 14px; color: #ea4d62; line-height: 1.45;">{{nPays}} pays — {{scope}}</span>')
sub('<button sc-camel-on-click="{{reset}}" style="border: 1px solid #dd203c; background: #dd203c; padding: 9px 14px; color: #fff;',
    '<button class="ib" sc-camel-on-click="{{reset}}" style="border: 1px solid #dd203c; background: #dd203c; padding: 9px 14px; color: #fff;')
sub('<button sc-camel-on-click="{{clearCountry}}" style="border: 0; background: none; padding: 0; color: #dd203c;',
    '<button class="lnk" sc-camel-on-click="{{clearCountry}}" style="border: 0; background: none; padding: 0; color: #ea4d62;')
sub('<button sc-camel-on-click="{{clearWeek}}" style="border: 0; background: none; padding: 0; color: #dd203c;',
    '<button class="lnk" sc-camel-on-click="{{clearWeek}}" style="border: 0; background: none; padding: 0; color: #ea4d62;')

# Barre des filtres actifs
FB = '<div class="fbar" style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 10px; padding: 10px 12px; margin-bottom: 12px; border: 1px solid #333336; background: #111113;">'
sub(FB, FB.replace('class="fbar"', 'class="fbar fbar-map"'), n=2, only=0)
sub('<button sc-camel-on-click="{{c.x}}" style="border: 1px solid #3a3a3d;', '<button class="chip" sc-camel-on-click="{{c.x}}" style="border: 1px solid #3a3a3d;', n=2)
sub('<button sc-camel-on-click="{{reset}}" style="border: 1px solid #dd203c; background: none; padding: 7px 12px; color: #dd203c;',
    '<button class="cta" sc-camel-on-click="{{reset}}" style="border: 1px solid #dd203c; background: none; padding: 7px 12px; color: #ea4d62;', n=2)
sub('<button sc-camel-on-click="{{toMap}}" style="border: 1px solid #3a3a3d; background: none; padding: 7px 12px;',
    '<button class="chip" sc-camel-on-click="{{toMap}}" style="border: 1px solid #3a3a3d; background: none; padding: 7px 12px;')

# Carte : marqueurs repérés par événement, calque d'effets
sub('<div id="carte" sc-camel-on-pointer-down=', '<div id="carte" data-rv="map" sc-camel-on-pointer-down=')
sub('<button class="pt" sc-camel-on-click="{{p.pick}}" aria-label="{{p.label}}" style="{{p.style}}">',
    '<button class="{{p.cls}}" data-k="{{p.k}}" sc-camel-on-click="{{p.pick}}" aria-label="{{p.label}}" style="{{p.style}}">')
sub('''        </sc-for>
        </div>

        <!-- Zoom -->''', '''        </sc-for>
        <div id="fx" aria-hidden="true"></div>
        </div>

        <!-- Zoom -->''')
for lab in ('Zoomer', 'Dézoomer', "Revenir à la vue d'ensemble"):
    sub('aria-label="%s" style="width: 40px; height: 40px;' % lab, 'class="ib" aria-label="%s" style="width: 40px; height: 40px;' % lab)
sub('''<span style="position: absolute; z-index: 5; top: 22px; left: 66px; font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #a3a09a;">{{zoomHint}}</span>''',
    '''<span class="zhint" style="position: absolute; z-index: 5; bottom: 11px; left: 14px; right: 14px; font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; color: #a3a09a; pointer-events: none;">{{zoomHint}}</span>''')

# Fiche : fond opaque, bouton de fermeture, liens
sub('background: rgba(12,12,13,.97); border: 1px solid #333336; border-top: 2px solid #dd203c;', 'background: #0d0d0e; border: 1px solid #333336; border-top: 2px solid #dd203c;')
sub('aria-label="Fermer le détail" style="flex: none;', 'class="ib" aria-label="Fermer le détail" style="flex: none;')
sub('''font-size: 16px; line-height: 1.25; color: #dd203c;">{{sel.dateLong}} — {{sel.lieu}}</span>''',
    '''font-size: 16px; line-height: 1.25; color: #ea4d62;">{{sel.dateLong}} — {{sel.lieu}}</span>''')

# Lecture chronologique
sub('<div class="player" style=', '<div class="player" data-play="{{playState}}" style=')
for lab in ('Revenir au début de la veille', 'Jour précédent', 'Jour suivant', 'Afficher toute la période'):
    sub('aria-label="%s" style="width: 28px; height: 28px;' % lab, 'class="ib" aria-label="%s" style="width: 28px; height: 28px;' % lab)
sub('aria-label="{{playLabel}}" style="width: 32px; height: 32px;', 'class="ib playb" aria-label="{{playLabel}}" style="width: 32px; height: 32px;')
sub('''<input id="day-range" type="range" min="0" max="{{dayMax}}" step="1" value="{{dayVal}}" sc-camel-on-input="{{onSlide}}" style="flex: 1 1 auto; min-width: 60px; accent-color: #dd203c;">''',
    '''<span class="trk" style="{{trkStyle}}"><span class="trk-rail"><span class="trk-fill"></span></span><sc-for list="{{trkTicks}}" as="tk" hint-placeholder-count="0"><span class="trk-tick" style="{{tk.style}}"></span></sc-for><span class="trk-th"></span><input id="day-range" type="range" min="0" max="{{dayMax}}" step="1" value="{{dayVal}}" sc-camel-on-input="{{onSlide}}"></span>''')
sub('''font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: #dd203c;">{{dayLabel}}</span>''',
    '''font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: #ea4d62;">{{dayLabel}}</span>''')
sub('.player input{flex:1 1 calc(100% - 72px)!important;min-width:0!important;margin-left:6px}', '')

# Chronologie : indicateurs, hexagones
sub('<div class="stats" style=', '<div class="stats" data-rv="stats" style=')
sub('''<span class="stat-v" style="font-family: 'GC Sanomat', Georgia, serif; font-size: 44px; line-height: 1;">{{c.value}}</span>''',
    '''<span class="stat-v fig" style="font-size: 44px; line-height: 1;"><span data-n="{{c.value}}" data-count aria-hidden="true"></span><span class="sr-only">{{c.value}}</span></span>''')
sub('<span class="stat-n" style="font-size: 13.5px; line-height: 1.4; color: #dd203c;">{{c.note}}</span>',
    '<span class="stat-n" style="font-size: 13.5px; line-height: 1.4; color: #b9b6b0;">{{c.note}}</span>')
sub('<div style="{{weekGrid}}">', '<div data-rv="bars" style="{{weekGrid}}">', n=2, only=0)
sub('<button class="pt" sc-camel-on-click="{{dot.pick}}" aria-label="{{dot.label}}" style="{{dot.style}}"></button>',
    '<button class="pt wd" sc-camel-on-click="{{dot.pick}}" aria-label="{{dot.label}}" style="{{dot.style}}"><span style="{{dot.hex}}"></span></button>')

# Images
for lab in ('Images précédentes', 'Images suivantes'):
    sub('aria-label="%s" style="width: 44px; height: 44px;' % lab, 'class="ib" aria-label="%s" style="width: 44px; height: 44px;' % lab)
sub('<button sc-camel-on-click="{{m.open}}" aria-label="{{m.aria}}" style="flex: 0 0 clamp(250px, 26vw, 360px); scroll-snap-align: start; display: flex; flex-direction: column; padding: 0; border: 1px solid #333336; border-radius: 14px;',
    '<button class="mcard" sc-camel-on-click="{{m.open}}" aria-label="{{m.aria}}" style="flex: 0 0 clamp(250px, 26vw, 360px); scroll-snap-align: start; display: flex; flex-direction: column; padding: 0; border: 1px solid #333336; border-radius: 6px;')
sub('''<span style="font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: #dd203c;">{{m.date}}</span>''',
    '''<span style="font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: #ea4d62;">{{m.date}}</span>''')

# Journal
sub('<button sc-camel-on-click="{{toMap}}" style="border: 0; border-bottom: 1px solid #dd203c;', '<button class="lnk" sc-camel-on-click="{{toMap}}" style="border: 0; border-bottom: 1px solid #dd203c;')
sub('<button class="row" sc-camel-on-click="{{e.pick}}" aria-expanded="{{e.exp}}" style="{{e.style}}">', '<button class="row jrow" sc-camel-on-click="{{e.pick}}" aria-expanded="{{e.exp}}" style="{{e.style}}">')
sub('''<span style="width: 92px; flex: none; font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; color: #a3a09a;">{{e.dateShort}}</span>
          <span style="{{e.dot}}"></span>''', '''<span class="jd" style="width: 92px; flex: none; font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; color: #a3a09a;">{{e.dateShort}}</span>
          <span class="jdot" style="{{e.dot}}"></span>''')
sub('<span style="flex: 0 0 auto; white-space: nowrap; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; color: #dd203c;">{{e.pays}}</span>',
    '<span class="jpays" style="flex: 0 0 auto; white-space: nowrap; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; color: #ea4d62;">{{e.pays}}</span>')
sub('aria-hidden="true" style="{{e.chev}}">', 'class="jchev" aria-hidden="true" style="{{e.chev}}">')
sub('''          <div style="display: flex; flex-wrap: wrap; gap: 24px 40px; padding: 6px 8px 28px clamp(8px, 9vw, 126px);">''',
    '''          <div class="acc"><div style="display: flex; flex-wrap: wrap; gap: 24px 40px; padding: 6px 8px 28px clamp(8px, 9vw, 126px);">''')
sub('''Voir sur la carte</button>
            </div>
          </div>
        </sc-if>''', '''Voir sur la carte</button>
            </div>
          </div></div>
        </sc-if>''')
sub('<button sc-camel-on-click="{{e.show}}" style="align-self: flex-start;', '<button class="cta" sc-camel-on-click="{{e.show}}" style="align-self: flex-start;')
sub('<button sc-camel-on-click="{{toggleAll}}" style="align-self: flex-start;', '<button class="lnk" sc-camel-on-click="{{toggleAll}}" style="align-self: flex-start;')
sub('<button sc-camel-on-click="{{toMap}}" style="border: 0; border-bottom: 1px solid #3a3a3d;', '<button class="lnk" sc-camel-on-click="{{toMap}}" style="border: 0; border-bottom: 1px solid #3a3a3d;')

# Méthodologie : volets animés
sub('''      <div style="display: flex; flex-direction: column; padding: 6px 0 10px;">
        <sc-for list="{{methodSecs}}"''', '''      <div class="acc" id="methode-in"><div style="display: flex; flex-direction: column; padding: 6px 0 10px;">
        <sc-for list="{{methodSecs}}"''')
sub('''        </sc-for>
      </div>
    </sc-if>
  </section>''', '''        </sc-for>
      </div></div>
    </sc-if>
  </section>''')
sub('''              <div style="display: flex; flex-direction: column; gap: 14px; padding: 0 0 26px 52px; max-width: 74ch;">''',
    '''              <div class="acc"><div style="display: flex; flex-direction: column; gap: 14px; padding: 0 0 26px 52px; max-width: 74ch;">''')
sub('''                </sc-for>
              </div>
            </sc-if>
          </div>
        </sc-for>''', '''                </sc-for>
              </div></div>
            </sc-if>
          </div>
        </sc-for>''')
sub('''<span style="width: 34px; flex: none; font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #dd203c;">{{ms.num}}</span>''',
    '''<span style="width: 34px; flex: none; font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #ea4d62;">{{ms.num}}</span>''')

# ══════════════ Script ══════════════
sub("const RED = '#dd203c', RED_TXT = '#dd203c';", "const RED = '#dd203c', RED_TXT = '#ea4d62'; // RED_TXT : rouge éclairci pour les petits textes (contraste AA sur fond sombre)")
sub("const HEXP = 'clip-path:polygon(50% 0,97% 25%,97% 75%,50% 100%,3% 75%,3% 25%)';",
    "const HEXP = 'clip-path:polygon(50% 0,97% 25%,97% 75%,50% 100%,3% 75%,3% 25%)';\nconst HEXV = HEX.slice(10), HEXPV = HEXP.slice(10);")
sub('''  return ASP < .9 ? { ...f, cy: f.cy + 25 / (f.k * ASP) } : f;
};''', '''  if (ASP < .9) return { ...f, cy: f.cy + 25 / (f.k * ASP) };
  // sur ordinateur, la fiche occupe la droite de la carte : l'événement est centré dans la partie restée libre
  return MAPW > 700 ? { ...f, cx: f.cx + 202 / MAPW * 100 / f.k } : f;
};''')
sub('class Component extends DCLogic {', MOTION + '\nclass Component extends DCLogic {')

# — componentDidMount : glitch sans rerendu, en pause hors écran ; infobulle ; apparitions ; touche Échap
sub('''      const burst = () => {
        let n = Math.floor(R(2, 6));
        const tick = () => {
          if (n-- > 0) { this.setState({ gl: frame() }); this.gt = setTimeout(tick, R(45, 110)); }
          else { this.setState({ gl: null }); this.gt = setTimeout(burst, R(1600, 5200)); }
        };
        tick();
      };
      this.gt = setTimeout(burst, 2200);
    }''', '''      // Appliqué directement sur le titre et le calque des barres : la page n'est plus recalculée à chaque image du glitch
      const VARS = ['--ga-o', '--ga-x', '--ga-c', '--gb-o', '--gb-x', '--gb-c', '--gm'];
      const applyGl = G => {
        const h = document.querySelector('.glitch'), box = document.getElementById('glbars');
        if (!h || !box) return;
        const v = G ? [G.ga.o.toFixed(2), G.ga.x.toFixed(1) + 'px', G.ga.c, G.gb.o.toFixed(2), G.gb.x.toFixed(1) + 'px', G.gb.c, G.gm] : [];
        VARS.forEach((k, i) => { if (G) h.style.setProperty(k, v[i]); else h.style.removeProperty(k); });
        box.textContent = '';
        if (G) G.bars.forEach(b => { const s = document.createElement('span'); s.style.cssText = 'position:absolute;left:' + b.l.toFixed(1) + '%;top:' + b.t.toFixed(1) + '%;width:' + b.w.toFixed(1) + '%;height:' + b.h + 'px;background:' + b.c + ';opacity:' + b.o.toFixed(2); box.appendChild(s); });
      };
      this.heroOn = true;
      if (typeof IntersectionObserver !== 'undefined') {
        const watchHero = () => { const h = document.getElementById('hero'); if (!h) { setTimeout(watchHero, 300); return; } new IntersectionObserver(es => es.forEach(en => { this.heroOn = en.isIntersecting; h.classList.toggle('off', !en.isIntersecting); })).observe(h); };
        watchHero();
      }
      const burst = () => {
        // en pause quand l'ouverture n'est pas à l'écran ou que l'onglet est en arrière-plan
        if (!this.heroOn || document.hidden) { this.gt = setTimeout(burst, 1200); return; }
        let n = Math.floor(R(2, 6));
        const tick = () => {
          if (n-- > 0) { applyGl(frame()); this.gt = setTimeout(tick, R(45, 110)); }
          else { applyGl(null); this.gt = setTimeout(burst, R(1600, 5200)); }
        };
        tick();
      };
      this.gt = setTimeout(burst, 2200);
    }
    // Infobulle des hexagones, apparitions à l'entrée dans l'écran, fermeture de la fiche au clavier
    this.tip = makeTip();
    this.rv = makeReveal((el, anim) => this.onShow(el, anim));
    this.onKey = ev => { if (ev.key === 'Escape' && this.state.sel && this.closeSel) this.closeSel(); };
    document.addEventListener('keydown', this.onKey);''')

# — componentDidUpdate
sub('''  componentDidUpdate(prev, prevState) {
    this.paint();''', '''  componentDidUpdate(prev, prevState) {
    this.paint();
    // Le moteur ne transmet pas l'état précédent : on le garde nous-mêmes (sans cela, l'adresse #EVEN… n'était jamais mise à jour)
    prevState = this.prevSt || {}; this.prevSt = this.state;
    try { this.after(prevState); } catch (err) { if (typeof console !== 'undefined') console.error(err); }''')

# — méthodes ajoutées
sub('''  componentWillUnmount() {
    ['gesturestart', 'gesturechange', 'gestureend'].forEach(n => document.removeEventListener(n, this.onGesture));''', r'''  // Après chaque rendu : nombres animés, apparitions, mouvements des hexagones, volets
  after(prevState) {
    const st = this.state, root = document.querySelector('[data-document-role="page"]');
    if (!root) return;
    syncNums(root);
    if (this.rv) root.querySelectorAll('[data-rv]').forEach(el => this.rv.watch(el));
    if (this.tip) this.tip.sync();
    this.mapMotion();
    // Fiche : changement d'événement sans fermeture
    if (prevState.sel && st.sel && prevState.sel !== st.sel && !REDUCE()) { const f = document.querySelector('.fiche'); if (canAnim(f)) f.animate([{ opacity: .35, transform: 'translateY(5px)' }, { opacity: 1, transform: 'none' }], { duration: 240, easing: EASE }); }
    // Journal : le volet ouvert se déplie, le précédent se replie puis est retiré
    if (st.open && st.open !== prevState.open) { const el = document.getElementById('j-' + st.open); accOpen(el && el.querySelector('.acc')); }
    if (st.closing && st.closing !== prevState.closing) {
      const id = st.closing, el = document.getElementById('j-' + id);
      accClose(el && el.querySelector('.acc'), () => this.setState(s => (s.closing === id ? { closing: null } : {})));
    }
    // Méthodologie
    if (st.methodOpen && !prevState.methodOpen) accOpen(document.getElementById('methode-in'));
    if (this.accNext) { const sel = this.accNext; this.accNext = null; accOpen(document.querySelector(sel)); }
  }
  // Élément entré dans l'écran (ou affiché d'emblée si les apparitions sont coupées)
  onShow(el, anim) {
    const kind = el.getAttribute('data-rv');
    if (kind === 'map') { this.mapShown = true; if (anim) this.cascade(); return; }
    const nums = el.querySelectorAll('[data-count]');
    nums.forEach(n => { n.__seen = true; });
    // sous la chronologie : totaux et barres des semaines, qui se remplissent au rythme de la chute des hexagones
    const wkRow = kind === 'bars' ? el.nextElementSibling : null;
    if (wkRow) {
      const go = anim && canAnim(el) && !REDUCE();
      wkRow.querySelectorAll('[data-count]').forEach((n, i, all) => { n.__seen = true; if (go && n.__to !== undefined) tweenNum(n, 0, n.__to, 0, 800, 700 + i / all.length * 1500); });
      if (go) wkRow.querySelectorAll('.wkbar').forEach((b, i, all) => b.animate({ width: ['0%', b.style.width || '0%'] }, { duration: 800, delay: 700 + i / all.length * 1500, easing: EASE, fill: 'backwards' }));
    }
    if (!anim || !canAnim(el)) return;
    const up = [{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'none' }];
    if (kind === 'up') el.animate(up, { duration: 620, easing: EASE });
    if (kind === 'kf' || kind === 'stats') {
      Array.prototype.forEach.call(el.children, (c, i) => c.animate(up, { duration: 640, delay: i * 90, easing: EASE, fill: 'backwards' }));
      nums.forEach((n, i) => { if (n.__to !== undefined) tweenNum(n, 0, n.__to, n.__dec, kind === 'kf' ? 1400 : 900, i * 90); });
    }
    if (kind === 'bars') Array.prototype.forEach.call(el.children, (col, i) => col.querySelectorAll('.wd').forEach((d, j) => d.animate([{ opacity: 0, transform: 'translateY(8px) scale(.4)' }, { opacity: 1, transform: 'none' }], { duration: 380, delay: i * 70 + j * 22, easing: EASE, fill: 'backwards' })));
  }
  // Arrivée des hexagones dans l'ordre chronologique, la première fois que la carte est à l'écran
  cascade() {
    const now = this.mapNow, layer = document.getElementById('mapLayer');
    if (!now || !now.items.size || !layer || REDUCE()) return;
    let max = 1; now.items.forEach(b => { if (b.d > max) max = b.d; });
    layer.querySelectorAll('.pt[data-k],.gl[data-k]').forEach(el => {
      const b = now.items.get(el.getAttribute('data-k'));
      if (b && canAnim(el)) el.animate(el.classList.contains('gl') ? { opacity: [0, 1] } : popIn(b.size, .2), { duration: 460, delay: 150 + Math.max(0, b.d) / max * 1100, easing: EASE, fill: 'backwards' });
    });
  }
  // Hexagones de la carte : entrée, sortie et glissement vers leur nouvelle place quand la sélection ou le zoom change
  mapMotion() {
    const now = this.mapNow, prev = this.mapPrev;
    this.mapPrev = now;
    const layer = document.getElementById('mapLayer'), fx = document.getElementById('fx');
    if (!now || !prev || !layer || !fx || !canAnim(layer) || REDUCE() || !this.mapShown) return;
    if (!prev.items.size) { if (now.items.size) this.cascade(); return; }
    if (prev.w !== now.w || prev.h !== now.h) return;
    const r = now.k / prev.k, sx = now.w / 100, sy = now.h / 100;
    let nIn = 0; const dl = new Map();
    layer.querySelectorAll('.pt[data-k],.gl[data-k]').forEach(el => {
      const halo = el.classList.contains('gl');
      const key = el.getAttribute('data-k'), b = now.items.get(key), a = prev.items.get(key);
      // le moteur réemploie les éléments dans l'ordre : un élément passé à un autre événement repart sans animation en cours
      if (el.__k !== key) { if (el.__an) { el.__an.forEach(x => x.cancel()); el.__an = null; } el.__k = key; }
      if (!b) return;
      // hors du cadre : rien à animer
      const px = b.sx - now.cx * now.k + 50, py = b.sy - now.cy * now.k * now.asp + 50;
      if (px < -6 || px > 106 || py < -6 || py > 106) return;
      if (!a) {
        if (!dl.has(key)) dl.set(key, Math.min(nIn++ * 14, 240));
        el.__an = [el.animate(halo ? { opacity: [0, 1] } : popIn(b.size, .3), { duration: 380, delay: dl.get(key), easing: EASE, fill: 'backwards' })];
        if (b.fresh && !halo) this.ping(fx, b, now, b.c, 2.9, 760);
        return;
      }
      const dx = (a.sx * r - b.sx) * sx, dy = (a.sy * r - b.sy) * sy, d = Math.abs(dx) + Math.abs(dy);
      if (d > .75 && d < 420) (el.__an || (el.__an = [])).push(el.animate({ translate: [dx.toFixed(1) + 'px ' + dy.toFixed(1) + 'px', '0px 0px'] }, { duration: 360, easing: EASE, composite: 'add' }));
      if (el.__an && el.__an.length > 6) el.__an.splice(0, el.__an.length - 6);
    });
    let nOut = 0;
    prev.items.forEach((a, key) => {
      if (now.items.has(key) || nOut > 140) return;
      const x = a.sx * r - now.cx * now.k + 50, y = a.sy * r - now.cy * now.k * now.asp + 50;
      if (x < -4 || x > 104 || y < -4 || y > 104) return;
      nOut++;
      const g = fxHex(fx, x, y, a.size, a.c, a.clip);
      g.animate({ opacity: [1, 0], scale: [1, .25] }, { duration: 260, easing: 'cubic-bezier(.4,0,1,1)' }).onfinish = () => g.remove();
    });
    if (now.sel && now.sel !== prev.sel) now.items.forEach(b => { if (b.id === now.sel) this.ping(fx, b, now, '#ffffff', 3.4, 820); });
  }
  // Onde discrète autour d'un hexagone : événement du jour pendant la lecture, événement ouvert
  ping(fx, b, now, color, grow, dur) {
    const g = fxHex(fx, b.sx - now.cx * now.k + 50, b.sy - now.cy * now.k * now.asp + 50, b.size, color, b.clip);
    g.animate({ opacity: [.5, 0], scale: [1, grow] }, { duration: dur, easing: 'cubic-bezier(.2,.6,.3,1)' }).onfinish = () => g.remove();
  }
  componentWillUnmount() {
    document.removeEventListener('keydown', this.onKey);
    ['gesturestart', 'gesturechange', 'gestureend'].forEach(n => document.removeEventListener(n, this.onGesture));''')

# — renderVals
sub("style: 'display:inline-flex;align-items:center;gap:9px;padding:20px 0 17px;border:0;background:transparent;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:' + (on ? '#f3f1ec' : '#5f5d5a') + ';box-shadow:inset 0 ' + (on ? '-2px 0 ' + RED : '0 0 transparent')",
    "style: 'display:inline-flex;align-items:center;gap:9px;padding:20px 0 17px;border:0;background:transparent;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:' + (catsAll ? '#dedbd6' : on ? '#ffffff' : '#8a8884')")
sub('''    const cats = {};
    Object.entries(CATKEY).forEach(([label, k]) => {''', '''    const cats = {};
    // Tous les types actifs : aucun n'est souligné ; le soulignement rouge ne marque qu'une sélection
    const catsAll = Object.values(st.cats).every(Boolean);
    Object.entries(CATKEY).forEach(([label, k]) => {''')
sub("dot: 'width:13px;height:13px;flex:none;' + HEX + ';background:' + s.color + ';opacity:' + (on ? 1 : .25),",
    "dot: 'width:13px;height:13px;flex:none;' + HEX + ';background:' + s.color + ';opacity:' + (on ? 1 : .3),")
sub("font-size:15px;color:' + (on ? '#f3f1ec' : '#5f5d5a')", "font-size:15px;color:' + (on ? '#f3f1ec' : '#8a8884')")
sub("bar: 'display:block;height:100%;width:' + (n / rmax * 100) + '%;background:' + (on ? RED : '#8a8884'),",
    "bar: 'display:block;height:100%;width:' + (n / rmax * 100) + '%;background:' + (on ? RED : '#8a8884') + ';transition:width .5s cubic-bezier(.2,.7,.2,1),background-color .2s',")

# carte : position de chaque marqueur gardée pour les mouvements
sub('''    ASP = Math.min(1, .72 * wPx / hPx);''', '''    ASP = Math.min(1, .72 * wPx / hPx); MAPW = wPx;''')
sub('''      .sort((a, b) => (a.e.id === st.sel) - (b.e.id === st.sel));''', ';')
sub('''      .map((o, i) => ({ e: o.e, xy: [this.spreadVal[i][0] - Z.cx * Z.k + 50, this.spreadVal[i][1] - Z.cy * Z.k * ASP + 50] }))''',
    '''      .map((o, i) => ({ e: o.e, j: o.j, xy: [this.spreadVal[i][0] - Z.cx * Z.k + 50, this.spreadVal[i][1] - Z.cy * Z.k * ASP + 50] }))''')
sub('''    const animTo = target => {
      cancelAnimationFrame(this.zr);
      clearTimeout(this.ct);
      const from = this.view(), to = clampZ(target), t0 = performance.now(), dur = 260;
      const step = now => {''', '''    const animTo = (target, fly) => {
      cancelAnimationFrame(this.zr);
      clearTimeout(this.ct);
      const from = this.view(), to = clampZ(target), t0 = performance.now(), dur = 260;
      if (REDUCE()) { this.live = to; this.commit(); return; }
      if (fly) {
        // Trajet long (ouverture d'un événement, retour à la vue d'ensemble) : recul, déplacement et approche d'un seul geste
        const path = zoomPath(from, to), D = Math.max(480, Math.min(1050, path.dur));
        const stepF = now => {
          const t = Math.min(1, (now - t0) / D), e = t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
          if (t >= 1) { this.live = to; this.commit(); return; }
          this.live = clampZ(path(e)); this.paint();
          this.zr = requestAnimationFrame(stepF);
        };
        this.zr = requestAnimationFrame(stepF);
        return;
      }
      const step = now => {''')
sub('''    const panMove = ev => { const d = this.drag; if (!d) return; const [fx, fy] = rel(ev);''', '''    const panMove = ev => { const d = this.drag; if (!d) return; this.backZ = null; const [fx, fy] = rel(ev);''')
sub('''    const zoomAt = (f, fx, fy) => { const z = this.view();''', '''    const zoomAt = (f, fx, fy) => { this.backZ = null; const z = this.view();''')
sub('''      if (ev.ctrlKey || ev.metaKey) { ev.preventDefault(); const d =''', '''      if (ev.ctrlKey || ev.metaKey) { ev.preventDefault(); this.backZ = null; const d =''')
sub('''    const points = pts.map(({ e, xy }) => {
      const c = COLOR[e.seuil];
      const sel = e.id === st.sel;
      const fresh = st.day !== null && !e.passe && dayIdx(e.date) === st.day;
      const nc = e.cat === 'Actions non classifiables';
      const sz0 = sel ? size + 8 : fresh ? size + 10 : size;
      const sz = nc ? Math.round(sz0 * 0.72) : sz0;
      return {
        label: fShort(e.date) + ' — ' + e.nom,
        pick: () => set({ sel: sel ? null : e.id }),
        style: 'left:' + xy[0] + '%;top:' + xy[1] + '%;width:' + sz + 'px;height:' + sz + 'px;border:0;background:transparent;filter:drop-shadow(0 0 ' + (fresh ? 10 : 3) + 'px ' + c + (fresh ? '' : '99') + ')' + (fresh ? ' drop-shadow(0 0 3px #ffffff)' : '') + ';z-index:' + (sel ? 3 : fresh ? 2 : 1),''',
    '''    // Fermeture de la fiche : fondu, puis retour à la vue d'avant l'ouverture (sauf si la carte a été déplacée entre-temps)
    const closeSel = () => {
      const id = st.sel, back = this.backZ, f = document.querySelector('.fiche');
      this.backZ = null;
      const done = () => this.setState(s => (s.sel === id ? { sel: null } : {}));
      if (canAnim(f) && !REDUCE()) { const a = f.animate([{ opacity: 1, transform: 'none' }, { opacity: 0, transform: 'translateY(6px)' }], { duration: 160, easing: 'ease-in', fill: 'forwards' }); a.onfinish = done; a.oncancel = done; } else done();
      if (back) animTo(back, true);
    };
    this.closeSel = closeSel;
    // Ouverture d'un événement : la carte glisse et zoome jusqu'à lui
    const openSel = e => { if (!st.sel) this.backZ = this.view(); animTo(focusOf(e, this.view().k), true); };
    const items = new Map();
    raw.forEach((o, i) => {
      const nc = o.e.cat === 'Actions non classifiables';
      items.set(o.e.id + ':' + o.j, { id: o.e.id, sx: this.spreadVal[i][0], sy: this.spreadVal[i][1], c: COLOR[o.e.seuil], clip: nc ? HEXPV : HEXV, size: nc ? Math.round(size * 0.72) : size, d: o.e.passe ? 0 : dayIdx(o.e.date), fresh: st.day !== null && !o.e.passe && dayIdx(o.e.date) === st.day });
    });
    this.mapNow = { k: Z.k, cx: Z.cx, cy: Z.cy, asp: ASP, w: wPx, h: hPx, sel: st.sel, items };
    const points = pts.map(({ e, j, xy }) => {
      const c = COLOR[e.seuil];
      const sel = e.id === st.sel;
      const fresh = st.day !== null && !e.passe && dayIdx(e.date) === st.day;
      const nc = e.cat === 'Actions non classifiables';
      const sz0 = sel ? size + 8 : size;
      const sz = nc ? Math.round(sz0 * 0.72) : sz0;
      return {
        label: fShort(e.date) + ' — ' + e.nom,
        k: e.id + ':' + j, cls: sel ? 'pt is-sel' : 'pt',
        pick: () => { if (sel) { closeSel(); return; } set({ sel: e.id }); openSel(e); },
        style: 'left:' + xy[0] + '%;top:' + xy[1] + '%;width:' + sz + 'px;height:' + sz + 'px;border:0;background:transparent;z-index:' + (sel ? 3 : fresh ? 2 : 1) + (nc ? ';--hc:' + HEXPV : ''),''')

# chronologie : hexagone dans un bouton non rogné (focus visible), ouverture avec trajet
OLDPICK = '''              set(filtered.includes(e) ? { sel: e.id } : { sel: e.id, day: null, week: null });
              animTo(focusOf(e, this.view().k));'''
sub(OLDPICK, '''              set(filtered.includes(e) ? { sel: e.id } : { sel: e.id, day: null, week: null });
              openSel(e);''', n=2)
sub('''              if (selD) { set({ sel: null }); return; }''', '''              if (selD) { closeSel(); return; }''', n=2)
sub("style: 'position:relative;transform:none;flex:none;width:' + HX + 'px;height:' + HX + 'px;padding:0;border:0;' + HEX + ';background:' + (selD ? '#ffffff' : COLOR[e.seuil]) + ';opacity:' + (later ? .15 : 1) + ';transition:opacity .3s'",
    "style: 'position:relative;transform:none;flex:none;width:' + HX + 'px;height:' + HX + 'px;padding:0;border:0;background:transparent;opacity:' + (later ? .15 : 1) + ';transition:opacity .3s',\n            hex: HEX + ';background:' + (selD ? '#ffffff' : COLOR[e.seuil])")

# journal
sub('''      const open = st.open === e.id;
      const on = open;''', '''      // le volet en cours de fermeture reste affiché le temps de se replier
      const on = st.open === e.id;
      const open = on || st.closing === e.id;''')
sub('''        open, exp: String(open),
        pick: () => set({ open: open ? null : e.id }),''', '''        open, exp: String(on),
        pick: () => set(on ? { open: null, closing: e.id } : { open: e.id, closing: st.open || null }),''')
sub("chev: 'flex:none;align-self:center;color:#a3a09a;transition:transform .25s;transform:rotate(' + (open ? 180 : 0) + 'deg)',",
    "chev: 'flex:none;align-self:center;color:#a3a09a;transition:transform .3s cubic-bezier(.2,.7,.2,1),color .15s;transform:rotate(' + (on ? 180 : 0) + 'deg)',")
sub('''          this.setState({ sel: e.id, day: null, week: null });
          animTo(focusOf(e, this.view().k));''', '''          this.setState({ sel: e.id, day: null, week: null });
          openSel(e);''')
sub("this.setState({ open: e.id, showAll: true, ...(e.passe ? { passe: true } : {}) });", "this.setState({ open: e.id, closing: null, showAll: true, ...(e.passe ? { passe: true } : {}) });")
# carrousel : la position n'alimente plus rien à l'écran — plus de rerendu de la page à chaque pixel de défilement
sub("const carScroll = ev => { const el = ev.currentTarget; const max = el.scrollWidth - el.clientWidth; this.setState({ carP: max > 0 ? el.scrollLeft / max : 0 }); };",
    "const carScroll = () => {};")

# méthodologie
sub("toggleMethod: () => set({ methodOpen: !st.methodOpen, methodSec: null }),",
    "toggleMethod: () => { if (st.methodOpen) accClose(document.getElementById('methode-in'), () => set({ methodOpen: false, methodSec: null })); else set({ methodOpen: true, methodSec: null }); },")
sub('''          toggle: () => { const cur = st.methodSec || Object.fromEntries(METHODE.map((_, j) => [j, true])); set({ methodSec: { ...cur, [i]: !open } }); },''',
    '''          toggle: ev => {
            const cur = st.methodSec || Object.fromEntries(METHODE.map((_, j) => [j, true]));
            const box = ev && ev.currentTarget ? ev.currentTarget.parentElement : null;
            if (open) accClose(box && box.querySelector('.acc'), () => set({ methodSec: { ...cur, [i]: false } }));
            else { if (box) { box.setAttribute('data-ms', String(i)); this.accNext = '[data-ms="' + i + '"] .acc'; } set({ methodSec: { ...cur, [i]: true } }); }
          },''')

# valeurs renvoyées au gabarit
sub('''      playing: st.playing, notPlaying: !st.playing,''', '''      playing: st.playing, notPlaying: !st.playing, playState: st.playing ? 'on' : 'off', catsAll: String(catsAll),
      trkStyle: '--p:' + (LAST_DAY > 0 ? Math.min(1, curDay / LAST_DAY) : 1).toFixed(4),
      trkTicks: Array.from({ length: Math.max(0, NW - 1) }, (_, i) => weekStartDay(i + 1)).filter(d => d > 0 && d < LAST_DAY).map(d => ({ style: 'left:' + (d / LAST_DAY * 100).toFixed(2) + '%' })),''')
sub("hasSel: !!s, closeSel: () => set({ sel: null }),", "hasSel: !!s, closeSel,")
sub("zoomReset: () => animTo(defZ()),", "zoomReset: () => { this.backZ = null; animTo(defZ(), true); },")

exec(compile(open(os.path.join(ROOT, 'build/patch_v2.py'), encoding='utf-8').read(), 'patch_v2.py', 'exec'))
exec(compile(open(os.path.join(ROOT, 'build/patch_v3.py'), encoding='utf-8').read(), 'patch_v3.py', 'exec'))
exec(compile(open(os.path.join(ROOT, 'build/patch_v4.py'), encoding='utf-8').read(), 'patch_v4.py', 'exec'))
exec(compile(open(os.path.join(ROOT, 'build/patch_v5.py'), encoding='utf-8').read(), 'patch_v5.py', 'exec'))
exec(compile(open(os.path.join(ROOT, 'build/patch_v6.py'), encoding='utf-8').read(), 'patch_v6.py', 'exec'))
exec(compile(open(os.path.join(ROOT, 'build/patch_v7.py'), encoding='utf-8').read(), 'patch_v7.py', 'exec'))
open(os.path.join(ROOT, 'build/template.html'), 'w', encoding='utf-8').write(t)
print('gabarit écrit :', len(t), 'caractères')
