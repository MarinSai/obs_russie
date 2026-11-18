# Sources de la page test de l'Observatoire

La page test (`observatoire_test.html`) est produite à partir de `observatoire.html` (production), jamais modifiée.

    python3 tools/unpack.py     # extrait le gabarit de observatoire.html dans unpacked/
    python3 build/patch.py      # applique les dix passes (patch.py enchaîne patch_v2 à patch_v10)
    python3 tools/pack.py       # réécrit le gabarit dans site/observatoire_test.html

- `build/extra.css`, `build/assets.css` : styles ajoutés (hexagones, grain, mouvement réduit).
- `build/motion.js` : animations, étiquettes de pays, pictogrammes.
- `tools/pw.py` : serveur local + navigateur avec les données servies en local.
- `tools/perf.py`, `tools/iframe_test.py`, `tests/*.py` : vérifications (fluidité, hauteur d'iframe,
  mouvement réduit, clavier, clics, étiquettes FR/IT, activité au repos, captures, maquettes).

Les scripts supposent la racine `/home/claude/work` (constante `ROOT`) : src/observatoire.html,
data/observatoire-data.json, repo/obs_russie (clone en lecture), site/, shots/.
Chaque remplacement de `patch.py` vérifie son nombre d'occurrences : si la page de production change,
le script s'arrête sur le remplacement à revoir au lieu de produire une page fausse.

## Passage en production
`i18n/i18n_production.py` est la version de `scripts/i18n.py` à mettre en place dans le même commit que la nouvelle
`observatoire.html` : elle retire la case « Faits antérieurs au 23 sept. ({{nPasse}}) » et la pastille « Avec les faits
antérieurs au 23 sept. », et ajoute le nouveau texte du premier chiffre clé et le résumé « dont N faits antérieurs ».
Sans elle, `build_lang.py` s'arrête (une entrée de la page de production a disparu).
