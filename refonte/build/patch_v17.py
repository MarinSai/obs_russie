# Passe 17 : point blanc au centre des hexagones « Confirmé » (choix A de Marin), quand le pictogramme n'est pas affiché.
sub("const kLo = () =>", "const DOT = s => s === 'Confirmé' ? ';--d:1' : '';\nconst kLo = () =>")
sub("(sel ? ';background:#ffffff' : ';--c:' + c + ';--f:' + FILL[e.seuil])", "(sel ? ';background:#ffffff' : ';--c:' + c + ';--f:' + FILL[e.seuil] + (sz >= 18 || e.passe ? '' : DOT(e.seuil)))")
sub("hex: HEX + (selD ? ';background:#ffffff' : ';--c:' + COLOR[e.seuil] + ';--f:' + FILL[e.seuil])", "hex: HEX + (selD ? ';background:#ffffff' : ';--c:' + COLOR[e.seuil] + ';--f:' + FILL[e.seuil] + (HXC >= 17 ? '' : DOT(e.seuil)))", n=2)
sub("';--f:' + FILL[s.id] + ';opacity:'", "';--f:' + FILL[s.id] + DOT(s.id) + ';opacity:'")
sub("';--c:' + sv.color + ';--f:' + FILL[sv.id] }));", "';--c:' + sv.color + ';--f:' + FILL[sv.id] + DOT(sv.id) }));")
sub("';--c:' + COLOR[c] + ';--f:' + FILL[c];", "';--c:' + COLOR[c] + ';--f:' + FILL[c] + DOT(c);")
# fait antérieur « Confirmé » : le point blanc se place dans le cœur sombre
sub("';background:' + (sel ? c : '#0f0f10')", "';background:' + (sel ? c : e.seuil === 'Confirmé' ? 'radial-gradient(closest-side,#fff 40%,#0f0f10 48%)' : '#0f0f10')")
