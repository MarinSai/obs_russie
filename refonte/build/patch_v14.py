# Passe 14 : accord du bouton des derniers événements quand une seule nouveauté.
#  Chaîne nouvelle : ' dernier événement' (ajoutée à i18n_production).
sub("label: nFresh + ' derniers événements',", "label: nFresh + (nFresh > 1 ? ' derniers événements' : ' dernier événement'),")
