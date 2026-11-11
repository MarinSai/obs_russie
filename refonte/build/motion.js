// ───── Mouvement (version d'essai) : petites fonctions sans bibliothèque, toutes neutralisées par « prefers-reduced-motion » ─────
// Mettre REVEAL à false pour couper les apparitions à l'entrée dans l'écran (tout s'affiche alors d'emblée).
const REVEAL = true;
const REDUCE = () => typeof window !== 'undefined' && !!window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const EASE = 'cubic-bezier(.2,.7,.2,1)';
const canAnim = el => !!el && typeof el.animate === 'function';
// Apparition d'un marqueur de la carte : grandit depuis son centre (le bouton est recentré par translate(-50%,-50%), d'où la compensation)
const popIn = (size, s0) => { const o = (-(size / 2) * (1 - s0)).toFixed(2) + 'px'; return { opacity: [0, 1], scale: [s0, 1], translate: [o + ' ' + o, '0px 0px'] }; };
let MAPW = 0; // largeur réelle de la carte, en pixels
// Nombres animés : la valeur exacte reste dans un texte voisin pour les lecteurs d'écran
const fmtNum = (v, dec) => dec ? v.toFixed(dec).replace('.', ',') : String(Math.round(v));
function tweenNum(el, from, to, dec, dur, delay) {
  cancelAnimationFrame(el.__raf);
  if (REDUCE() || !dur || from === to) { el.textContent = fmtNum(to, dec); el.__cur = to; return; }
  const t0 = performance.now() + (delay || 0);
  el.textContent = fmtNum(from, dec); el.__cur = from;
  const step = now => {
    const t = Math.max(0, Math.min(1, (now - t0) / dur)), e = 1 - Math.pow(1 - t, 4);
    el.__cur = from + (to - from) * e; el.textContent = fmtNum(el.__cur, dec);
    if (t < 1) el.__raf = requestAnimationFrame(step); else el.__cur = to;
  };
  el.__raf = requestAnimationFrame(step);
}
function syncNums(root) {
  root.querySelectorAll('[data-n]').forEach(el => {
    const raw = el.getAttribute('data-n');
    if (el.__raw === raw) return;
    el.__raw = raw;
    const m = /^(\d+)(?:,(\d+))?$/.exec(raw);
    if (!m) { cancelAnimationFrame(el.__raf); el.textContent = raw; el.__cur = undefined; el.__to = undefined; return; }
    const to = parseFloat(raw.replace(',', '.')), dec = m[2] ? m[2].length : 0, wait = el.hasAttribute('data-count') && !el.__seen;
    el.__dec = dec; el.__to = to;
    tweenNum(el, wait || el.__cur === undefined ? to : el.__cur, to, dec, el.hasAttribute('data-count') ? 900 : 380);
  });
}
// Apparition à l'entrée dans l'écran. IntersectionObserver (déjà utilisé pour les vidéos) tient compte de la page parente,
// y compris dans l'iframe ; aucune lecture de la position de défilement, et l'état masqué n'est posé que si l'observateur répond.
function makeReveal(onShow) {
  if (!REVEAL || typeof IntersectionObserver === 'undefined' || REDUCE()) return { watch: el => { if (el.__rvw) return; el.__rvw = 1; onShow(el, false); } };
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    const el = en.target;
    if (en.isIntersecting) { io.unobserve(el); el.classList.remove('rv-pre'); onShow(el, true); }
    else if (!el.__rvp) { el.__rvp = 1; el.classList.add('rv-pre'); }
  }), { threshold: 0.18 });
  return { watch: el => { if (el.__rvw) return; el.__rvw = 1; io.observe(el); } };
}
// Trajet de zoom « van Wijk » (celui de d3.interpolateZoom, réécrit ici) : recul léger, déplacement, approche
function zoomPath(a, b) {
  const rho = 1.25, rho2 = rho * rho, rho4 = rho2 * rho2;
  const ux0 = a.cx * 10, uy0 = a.cy * 7.2, w0 = 1000 / a.k, ux1 = b.cx * 10, uy1 = b.cy * 7.2, w1 = 1000 / b.k;
  const dx = ux1 - ux0, dy = uy1 - uy0, d2 = dx * dx + dy * dy;
  const out = (x, y, w) => ({ k: 1000 / w, cx: x / 10, cy: y / 7.2 });
  let f, S;
  if (d2 < 1e-6) { S = Math.log(w1 / w0) / rho; f = t => out(ux0 + t * dx, uy0 + t * dy, w0 * Math.exp(rho * t * S)); }
  else {
    const d1 = Math.sqrt(d2), b0 = (w1 * w1 - w0 * w0 + rho4 * d2) / (2 * w0 * rho2 * d1), b1 = (w1 * w1 - w0 * w0 - rho4 * d2) / (2 * w1 * rho2 * d1);
    const r0 = Math.log(Math.sqrt(b0 * b0 + 1) - b0), r1 = Math.log(Math.sqrt(b1 * b1 + 1) - b1);
    S = (r1 - r0) / rho;
    f = t => { const s = t * S, c0 = Math.cosh(r0), u = w0 / (rho2 * d1) * (c0 * Math.tanh(rho * s + r0) - Math.sinh(r0)); return out(ux0 + u * dx, uy0 + u * dy, w0 * c0 / Math.cosh(rho * s + r0)); };
  }
  f.dur = Math.abs(S) * 520;
  return f;
}
// Hexagone éphémère posé sur le calque d'effets de la carte (sorties, ondes) : suit le zoom comme les marqueurs
function fxHex(layer, x, y, size, color, clip) {
  const d = document.createElement('span');
  d.style.cssText = 'position:absolute;left:' + x.toFixed(3) + '%;top:' + y.toFixed(3) + '%;width:' + size + 'px;height:' + size + 'px;margin:' + (-size / 2) + 'px 0 0 ' + (-size / 2) + 'px;transform:scale(var(--inv,1));clip-path:' + clip + ';background:' + color;
  layer.appendChild(d);
  return d;
}
// Chronologie : un hexagone tombe à sa place, en arc, depuis le haut à droite, avec un léger tassement à l'arrivée
function hexFall(el, delay, quick) {
  if (!canAnim(el) || REDUCE()) return;
  const T = quick ? 640 : 950 + Math.random() * 260, dx = 26 + Math.random() * 120, dy = -(64 + Math.random() * 96);
  el.animate({ translate: [dx.toFixed(0) + 'px 0px', '0px 0px'] }, { duration: T, delay, easing: 'cubic-bezier(.15,.6,.3,1)', fill: 'backwards' });
  el.animate([
    { transform: 'translateY(' + dy.toFixed(0) + 'px) scale(.5)', opacity: 0 },
    { opacity: .75, offset: .3 },
    { transform: 'translateY(0px) scale(1)', opacity: 1, offset: .84 },
    { transform: 'translateY(0px) scale(1.2,.82)', offset: .92 },
    { transform: 'translateY(0px) scale(1)', opacity: 1 }
  ], { duration: T, delay, easing: 'cubic-bezier(.5,0,.9,.62)', fill: 'backwards' });
}
// Volets : ouverture et fermeture en hauteur
function accOpen(el) {
  if (!canAnim(el) || REDUCE()) return;
  const h = el.offsetHeight; if (!h) return;
  el.style.overflow = 'hidden';
  const a = el.animate([{ height: '0px', opacity: 0 }, { height: h + 'px', opacity: 1 }], { duration: Math.min(460, 240 + h * .3), easing: EASE });
  a.onfinish = a.oncancel = () => { el.style.overflow = ''; };
}
function accClose(el, done) {
  if (!canAnim(el) || REDUCE()) { done(); return; }
  const h = el.offsetHeight;
  el.style.overflow = 'hidden';
  const a = el.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: Math.min(320, 180 + h * .2), easing: 'cubic-bezier(.4,0,.2,1)', fill: 'forwards' });
  let once = false; const fin = () => { if (once) return; once = true; done(); };
  a.onfinish = fin; a.oncancel = fin;
}
// Infobulle unique pour les hexagones (carte et chronologie) : reprend le libellé déjà lu par les lecteurs d'écran
function makeTip() {
  const tip = document.createElement('div');
  tip.id = 'gctip'; tip.setAttribute('aria-hidden', 'true');
  const d = document.createElement('span'), t = document.createElement('span');
  d.className = 'gctip-d'; t.className = 'gctip-t'; tip.appendChild(d); tip.appendChild(t);
  document.body.appendChild(tip);
  let cur = null, lab = '';
  const hide = () => { if (!cur) return; cur = null; tip.classList.remove('on'); };
  const show = el => {
    const s = el.getAttribute('aria-label') || '', i = s.indexOf(' — ');
    if (i < 0) { hide(); return; }
    cur = el; lab = s; d.textContent = s.slice(0, i); t.textContent = s.slice(i + 3);
    const r = el.getBoundingClientRect(), W = document.documentElement.clientWidth;
    tip.style.maxWidth = Math.min(300, W - 16) + 'px';
    const tw = tip.offsetWidth, th = tip.offsetHeight, mx = r.left + r.width / 2;
    const x = Math.max(8, Math.min(W - tw - 8, mx - tw / 2));
    const dn = r.top - th - 12 < 0;
    tip.classList.toggle('dn', dn);
    tip.style.setProperty('--ax', Math.max(12, Math.min(tw - 12, mx - x)).toFixed(1) + 'px');
    tip.style.left = (x + window.scrollX).toFixed(1) + 'px';
    tip.style.top = ((dn ? r.bottom + 12 : r.top - th - 12) + window.scrollY).toFixed(1) + 'px';
    tip.classList.add('on');
  };
  const sel = '.pt[aria-label]';
  document.addEventListener('pointerover', e => {
    if (e.pointerType !== 'mouse') return;
    const el = e.target && e.target.closest ? e.target.closest(sel) : null;
    if (el) { if (el !== cur) show(el); } else hide();
  });
  document.addEventListener('pointerdown', hide, true);
  document.addEventListener('focusin', e => { const el = e.target; if (el && el.matches && el.matches(sel) && el.matches(':focus-visible')) show(el); else hide(); });
  document.addEventListener('focusout', hide);
  window.addEventListener('scroll', hide, { passive: true });
  return { sync: () => { if (cur && (!cur.isConnected || cur.getAttribute('aria-label') !== lab)) hide(); }, hide };
}

// ───── Étiquettes de pays sur la carte ─────
// Repères géographiques fixes des 30 pays suivis, en % du cadre de la carte (projection de build_data.py) :
// [x, y de l'étiquette, points de sonde (un par grande terre : îles, Irlande du Nord…), nom français].
// Le nom affiché vient des données (donc traduit dans les versions IT/ES) : c'est le pays des événements épinglés dans les
// contours qui contiennent les sondes. Le nom français ne sert que si aucun événement propre à ce pays n'y est épinglé.
const PAYS_REP = [[40.41,58.05,[[40.41,58.05]],'Allemagne'],[49.42,75.4,[[49.42,75.4]],'Autriche'],[27.52,58.19,[[27.52,58.19]],'Belgique'],[78.14,96.5,[[78.14,96.5]],'Bulgarie'],[105.4,128.81,[[105.4,128.81]],'Chypre'],[54.45,84.94,[[54.45,84.94]],'Croatie'],[39.15,32.67,[[39.15,32.67],[44.25,35.99],[41.39,36.82]],'Danemark'],[0.57,104.46,[[0.57,104.46],[18.1,111.98]],'Espagne'],[70.26,17.19,[[70.26,17.19],[64.75,20.33]],'Estonie'],[68.75,-1.7,[[68.75,-1.7]],'Finlande'],[20.69,76.15,[[20.69,76.15],[35.7,101.4]],'France'],[70.61,113.41,[[70.61,113.41],[81.06,134.04],[72.51,123.75]],'Grèce'],[61.8,76.97,[[61.8,76.97]],'Hongrie'],[2.3,37.53,[[2.3,37.53]],'Irlande'],[44.52,97.92,[[44.52,97.92],[49.29,124.96],[35.23,111.86]],'Italie'],[71.21,26.55,[[71.21,26.55]],'Lettonie'],[68.7,34.87,[[68.7,34.87]],'Lituanie'],[30.55,63.17,[[30.55,63.17]],'Luxembourg'],[49.98,133.51,[[49.98,133.51]],'Malte'],[30.66,50.48,[[30.66,50.48]],'Pays-Bas'],[60.28,52.3,[[60.28,52.3]],'Pologne'],[-11.81,102.68,[[-11.81,102.68]],'Portugal'],[75.48,80.91,[[75.48,80.91]],'Roumanie'],[61.63,69.04,[[61.63,69.04]],'Slovaquie'],[50.68,82.57,[[50.68,82.57]],'Slovénie'],[50.91,6.28,[[50.91,6.28],[57.31,25.79]],'Suède'],[51.69,64.23,[[51.69,64.23]],'Tchéquie'],[83.66,72.16,[[83.66,72.16]],'Moldavie'],[15.3,44.42,[[15.3,44.42],[6.42,31.96]],'Royaume-Uni'],[40.06,7.37,[[40.06,7.37]],'Norvège']];
const LAB_OFF = (() => { const o = []; for (let dy = -4; dy <= 4; dy++) for (let dx = -4; dx <= 4; dx++) o.push([dx * 22, dy * 15]); return o.sort((a, b) => (a[0] * a[0] * .55 + a[1] * a[1] * 1.5) - (b[0] * b[0] * .55 + b[1] * b[1] * 1.5)); })();
const ringsOf = path => path.split('M').slice(1).map(s => {
  const r = s.replace('Z', '').split('L').map(p => { const c = p.split(','); return [+c[0], +c[1]]; });
  let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
  r.forEach(p => { if (p[0] < x0) x0 = p[0]; if (p[0] > x1) x1 = p[0]; if (p[1] < y0) y0 = p[1]; if (p[1] > y1) y1 = p[1]; });
  return { r, x0, x1, y0, y1 };
});
const inRing = (x, y, r) => { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) { const a = r[i], b = r[j]; if ((a[1] > y) !== (b[1] > y) && x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]) c = !c; } return c; };
function paysLabels(D) {
  if (D.__lab) return D.__lab;
  const out = []; D.__lab = out;
  try {
    const rings = ringsOf(D.land);
    const find = (x, y) => { for (let i = 0; i < rings.length; i++) { const q = rings[i]; if (x >= q.x0 && x <= q.x1 && y >= q.y0 && y <= q.y1 && inRing(x, y, q.r)) return i; } return -1; };
    const grp = new Map();
    PAYS_REP.forEach((a, g) => a[2].forEach(p => { const i = find(p[0] * 10, p[1] * 7.2); if (i >= 0) grp.set(i, g); }));
    const all = new Set(D.events.flatMap(paysOf));
    const votes = PAYS_REP.map(() => new Map()), cand = PAYS_REP.map(() => null);
    D.events.forEach(e => {
      const ps = paysOf(e);
      allPos(e).forEach(q => {
        const xy = q.raw || q.eu, g = grp.get(find(xy[0] * 10, xy[1] * 7.2));
        if (g === undefined) return;
        // événement d'un seul pays : son épingle nomme le contour ; événement de plusieurs pays : il restreint seulement les noms possibles
        if (ps.length === 1) votes[g].set(ps[0], (votes[g].get(ps[0]) || 0) + 1);
        else cand[g] = cand[g] ? cand[g].filter(n => ps.includes(n)) : ps.slice();
      });
    });
    const name = PAYS_REP.map((a, g) => { let best = null, n = 0; votes[g].forEach((v, k) => { if (v > n) { n = v; best = k; } }); return best || (all.has(a[3]) ? a[3] : null); });
    for (let again = true; again;) {
      again = false;
      const used = new Set(name.filter(Boolean));
      cand.forEach((c, g) => { if (name[g] || !c) return; const left = c.filter(n => !used.has(n)); if (left.length === 1) { name[g] = left[0]; used.add(left[0]); again = true; } });
    }
    const seen = new Set();
    const own = PAYS_REP.map(() => []); grp.forEach((g, i) => own[g].push(rings[i]));
    name.forEach((n, g) => { if (n && !seen.has(n)) { seen.add(n); out.push({ x: PAYS_REP[g][0], y: PAYS_REP[g][1], name: n, rings: own[g] }); } });
  } catch (err) {}
  return out;
}

// ───── Pictogrammes des types d'action, dessinés dans les hexagones assez grands (carte zoomée, chronologie) ─────
// [tracé dans une boîte 24 × 24, 0 = forme pleine, 1 = trait]
const GLYPH = {
  aero: ['M12 2.2l1.9 7 7.9 4.2v2.3l-7.6-2.1-.5 5 2.5 2v1.6L12 21l-4.2 1.2v-1.6l2.5-2-.5-5-7.6 2.1v-2.3l7.9-4.2z', 0],
  drone: ['M2.5 14h19l-2.7 6.2H5.2zM10.8 3.5h2.4v4h4.3V12.5h-11V7.5h4.3z', 0],
  sabo: ['M13.4 1.8 3.6 14.4h7l-1.1 7.8 10-12.9h-7.1z', 0],
  feu: ['M12 22.4c4.3 0 7.5-2.9 7.5-7 0-3.6-2.4-6-3.8-7.9-.6 1.9-1.7 3.1-3.1 3.6.2-3.7-1.2-6.9-4.4-9.5C8.4 6 4.5 8.500 4.5 15.1c0 4.300 3.200 7.300 7.5 7.300z', 0],
  rens: ['M12 4.6c6.800 0 10.600 7.400 10.600 7.400s-3.800 7.400-10.600 7.400S1.400 12 1.400 12 5.200 4.600 12 4.600zm0 3.600a3.800 3.800 0 1 0 0 7.600 3.800 3.800 0 0 0 0-7.600z', 0],
  ing: ['M12 10.300a1.700 1.700 0 1 0 0 3.400 1.700 1.700 0 0 0 0-3.400M7.700 7.700a6.100 6.100 0 0 0 0 8.600M16.300 7.700a6.100 6.100 0 0 1 0 8.600M4.300 4.300a10.900 10.900 0 0 0 0 15.400M19.700 4.300a10.900 10.900 0 0 1 0 15.400', 1],
  nc: ['M8.800 9a3.300 3.300 0 1 1 4.900 2.900c-1.100.600-1.700 1.400-1.700 2.600M12 18.400v.01', 1]
};
const glyphStyle = (k, on) => !on || !GLYPH[k] ? 'display:none' : GLYPH[k][1] ? 'fill:none;stroke:#0b0b0c;stroke-width:2.7;stroke-linecap:round;stroke-linejoin:round' : 'fill:#0b0b0c;stroke:none';

// Halo des seuils (suspecté, attribué, confirmé) repris sur les pastilles des légendes
const HALO = { 'Confirmé': 'e6', 'Attribué': 'b8', 'Suspecté': '8c' };
const haloStyle = (id, color, on) => 'display:inline-flex;flex:none' + (on && HALO[id] ? ';filter:drop-shadow(0 0 4px ' + color + HALO[id] + ') drop-shadow(0 0 9px ' + color + '59)' : '');
