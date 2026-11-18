# Passe 22 : constat d'ouverture avec dates exactes, texte de la chronologie raccourci, moyenne par jour, médiathèque sans libellé Photo/Vidéo.
sub("label: 'Dernière semaine complète', note: 'semaine du ' + (d => d.getDate() + ' ' + MOIS[d.getMonth()])(dateOfDay(weekStartDay(lw))) + ' (' + (hN - hP >= 0 ? '+' : '−') + Math.abs(hN - hP) + ' par rapport à la précédente)',",
    "label: 'Dernière semaine', note: ((a, b) => 'du ' + a.getDate() + (a.getMonth() === b.getMonth() ? '' : ' ' + MOIS[a.getMonth()]) + ' au ' + b.getDate() + ' ' + MOIS[b.getMonth()])(dateOfDay(weekStartDay(lw)), dateOfDay(weekStartDay(lw) + 6)) + ' (' + (hN - hP >= 0 ? '+' : '−') + Math.abs(hN - hP) + ' par rapport à la précédente)',")
sub(" Cliquez sur une semaine pour filtrer la carte, ou sur un hexagone pour l'ouvrir. Les faits antérieurs au 23 septembre n'y figurent pas.</p>", " Cliquez sur une semaine pour filtrer la carte, ou sur un hexagone pour l'ouvrir.</p>")
sub("{ label: 'Moyenne hebdomadaire', value: avg, note: 'sur les semaines complètes' },",
    "{ label: 'Moyenne hebdomadaire', value: avg, note: 'sur les semaines complètes' + ' — ' + (fullW.reduce((a, b) => a + b, 0) / Math.max(1, fullW.length) / 7).toFixed(1).replace('.', ',') + ' par jour' },")
sub('          <span style="{{m.badge}}">{{m.kind}}</span>\n', '')
