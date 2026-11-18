# Passe 14 : accord du bouton des derniers événements quand une seule nouveauté.
#  Chaîne nouvelle : ' dernier événement' (ajoutée à i18n_production).
sub("label: nFresh + ' derniers événements',", "label: nFresh + (nFresh > 1 ? ' derniers événements' : ' dernier événement'),")
# Téléphone : la vue d'ensemble a un zoom minimal plus élevé (0.57 / ASP) que ZMIN ;
# le test « carte zoomée » comparait à ZMIN, si bien que la carte bloquait le défilement de la page.
sub("const clampZ = z => {", "const kLo = () => Math.max(ZMIN, 0.57 / ASP) + 0.05;\nconst clampZ = z => {")
sub("ZMIN + 0.05", "kLo()", n=t.count("ZMIN + 0.05"))
