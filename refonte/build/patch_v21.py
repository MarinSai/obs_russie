# Passe 21 : fond de l'ouverture au codage de la carte (remplissage selon le seuil, point blanc des Confirmé,
# faits antérieurs inclus avec leur cœur sombre, halo plus discret).
sub('<span class="hdot" style="{{h.style}}"><span style="{{h.hex}}"></span></span>',
    '<span class="hdot" style="{{h.style}}"><span class="hx" style="{{h.hex}}"></span><span class="hcore" style="{{h.core}}"></span></span>')
sub("    const heroDots = EV.filter(e => !e.passe).map((e, i) => {", "    const heroDots = EV.map((e, i) => {")
sub("return { style: 'left:' + xy[0] + '%;top:' + xy[1] + '%;background:radial-gradient(closest-side,' + c + '70,' + c + '1c 55%,' + c + '00);animation-delay:' + (0.5 + Math.max(0, dayIdx(e.date)) / Math.max(1, LAST_DAY) * 3.2).toFixed(2) + 's', hex: HEX + ';background:' + SHEEN + c };",
    "return { style: 'left:' + xy[0] + '%;top:' + xy[1] + '%;background:radial-gradient(closest-side,' + c + '3a,' + c + '10 55%,' + c + '00);animation-delay:' + (0.5 + Math.max(0, dayIdx(e.date)) / Math.max(1, LAST_DAY) * 3.2).toFixed(2) + 's', hex: HEX + ';--c:' + c + ';--f:' + FILL[e.seuil] + (e.passe ? '' : DOT(e.seuil)), core: e.passe ? HEX + ';background:' + (e.seuil === 'Confirmé' ? 'radial-gradient(closest-side,#fff 40%,#0f0f10 48%)' : '#0f0f10') : 'display:none' };")
