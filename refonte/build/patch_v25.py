# ── Passe 25 (19/11/2026) : vignette des vidéos du carrousel posée par le script.
# Dans le gabarit, poster="{{m.poster}}" était lu par le navigateur avant le remplissage des données :
# requête inutile vers l'adresse littérale /{{m.poster}} (erreur 404) à chaque chargement. La vignette passe
# en data-poster et le script la copie dans poster une fois la valeur remplie, comme data-src pour la vidéo.
sub(' poster="{{m.poster}}"', ' data-poster="{{m.poster}}"', 1)
sub("document.querySelectorAll('video.lazyv').forEach(v => { if (!v.dataset.obs) {",
    "document.querySelectorAll('video.lazyv').forEach(v => { const ps = v.dataset.poster; if (ps && ps.indexOf('{{') < 0 && v.getAttribute('poster') !== ps) v.poster = ps; if (!v.dataset.obs) {")
sub("document.querySelectorAll('video.lazyv:not([src])').forEach(v => { v.src = v.dataset.src; v.autoplay = true; });",
    "document.querySelectorAll('video.lazyv:not([src])').forEach(v => { if (v.dataset.poster && v.dataset.poster.indexOf('{{') < 0) v.poster = v.dataset.poster; v.src = v.dataset.src; v.autoplay = true; });")
