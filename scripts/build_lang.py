#!/usr/bin/env python3
"""Produit observatoire_russie_IT.html et observatoire_russie_ES.html à partir de observatoire.html (version française).

À relancer après chaque modification de la page française :  python3 scripts/build_lang.py
Les textes de l'interface sont dans scripts/i18n.py ; les données traduites (observatoire-data-it.json,
observatoire-data-es.json) sont produites automatiquement par la mise à jour horaire (translate_data.py).
Le script s'arrête si un texte français attendu est introuvable (page modifiée sans mettre à jour i18n.py).
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import i18n

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "observatoire.html")
DATA_FR = "https://marinsai.github.io/obs_russie/observatoire-data.json"


def esc_js(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def build(lang, k):
    s = open(SRC, encoding="utf-8").read()
    m = re.search(r'(<script type="__bundler/template">)(.*?)(</script>)', s, re.S)
    t = json.loads(m.group(2))
    missing = []

    def rep(a, b, need=1):
        nonlocal t
        c = t.count(a)
        if c < need:
            missing.append(a[:80])
        t = t.replace(a, b)

    # Méthodologie : tableau remplacé en entier
    m0 = t.find("const METHODE = ["); m1 = t.find("\n];", m0)
    if m0 < 0 or m1 < 0:
        sys.exit("Méthodologie introuvable")
    t = t[:m0] + "const METHODE = " + json.dumps(i18n.METHODE[lang], ensure_ascii=False, indent=1) + t[m1 + 2:]

    # Titre
    T1, T2 = i18n.TITLE[lang]
    full = T1 + " " + T2
    rep("Observatoire de la guerre russe en Europe", full)
    rep("const T1 = 'Observatoire de la guerre russe';", "const T1 = '" + esc_js(T1) + "';")
    rep("const T2 = 'en Europe';", "const T2 = '" + esc_js(T2) + "';")
    rep("const DATA_URL = '" + DATA_FR + "';", "const DATA_URL = '" + DATA_FR.replace(".json", "-" + lang + ".json") + "';")
    rep('<html lang="fr">', '<html lang="' + lang + '">')
    # Titre plus long qu'en français : un peu plus large et un peu plus petit dans l'ouverture
    rep("font-size: clamp(64px, 11vw, 176px); line-height: .94; letter-spacing: -.03em; max-width: 11ch;",
        "font-size: clamp(54px, 8.6vw, 138px); line-height: .94; letter-spacing: -.03em; max-width: 13.5ch;")

    # Libellés des seuils et catégories
    rep("const LBL = {};", "const LBL = " + json.dumps(i18n.LBL[lang], ensure_ascii=False) + ";")

    # Mois et dates
    court, longs = i18n.MOIS[lang]
    t, n1 = re.subn(r"const MOIS = \[[^\]]*\];", "const MOIS = " + json.dumps(court, ensure_ascii=False).replace('"', "'") + ";", t)
    t, n2 = re.subn(r"const MOISL = \[[^\]]*\];", "const MOISL = " + json.dumps(longs, ensure_ascii=False).replace('"', "'") + ";", t)
    if not (n1 and n2): missing.append("MOIS")
    if lang == "es":
        rep("const fLong = d => { const p = parse(d); return p.j + ' ' + MOISL[p.m - 1] + ' ' + p.y; };",
            "const fLong = d => { const p = parse(d); return p.j + ' de ' + MOISL[p.m - 1] + ' de ' + p.y; };")

    # Pluriel des images
    rep("withMedia.length + ' image' + (withMedia.length > 1 ? 's' : '')",
        "withMedia.length + (withMedia.length > 1 ? " + ("' immagini' : ' immagine')" if lang == "it" else "' imágenes' : ' imagen')"))

    # Textes de la page (entre balises), espaces insécables tolérées
    for fr, tr in i18n.MARKUP.items():
        pat = re.compile(r"(>\s*)" + re.escape(fr).replace(r"\ ", r"[  ]") + r"(\s*<)")
        t, n = pat.subn(lambda mm: mm.group(1) + tr[k] + mm.group(2), t)
        if not n: missing.append(fr[:80])
    for fr, tr in i18n.ATTRS.items():
        pat = re.compile(r'((?:aria-label|title|alt|data-label)=")' + re.escape(fr) + '"')
        t, n = pat.subn(lambda mm: mm.group(1) + tr[k] + '"', t)
        if not n: missing.append(fr[:80])
    # Chaînes du code : les plus longues d'abord
    for fr in sorted(i18n.JS, key=len, reverse=True):
        tr = i18n.JS[fr][k]
        rep("'" + fr + "'", "'" + esc_js(tr) + "'")

    if missing:
        print(lang.upper(), ": textes introuvables dans la page française :\n  - " + "\n  - ".join(missing))
        sys.exit(1)
    out = s[:m.start(2)] + json.dumps(t, ensure_ascii=False).replace("</", "<\\u002F") + s[m.end(2):]
    # Titre de l'onglet hors gabarit éventuel
    out = out.replace("<title>Observatoire de la guerre russe en Europe</title>", "<title>" + full + "</title>")
    out = out.replace("Observatoire de la guerre russe en Europe", full)
    path = os.path.join(ROOT, "observatoire_russie_" + lang.upper() + ".html")
    open(path, "w", encoding="utf-8").write(out)
    print("écrit", os.path.basename(path))


if __name__ == "__main__":
    for i, lang in enumerate(("it", "es")):
        build(lang, i)
