#!/usr/bin/env python3
"""Produit les versions italienne et espagnole des données de l'Observatoire.

- Lit observatoire-data.json (version française, générée par build_data.py).
- Traduit avec l'API DeepL (clé dans DEEPL_API_KEY) les titres, descriptifs, lieux et légendes des médias.
- Ne traduit que les textes nouveaux ou modifiés : les traductions sont gardées dans translations/cache.json
  (clé : empreinte du texte français). Un texte inchangé n'est jamais retraduit.
- Les noms de pays sont traduits par une table fixe ; seuils et catégories restent en français
  (ils servent de clés, l'interface les affiche dans chaque langue).
- Corrections manuelles : translations/corrections.json, {"it": {"texte français": "traduction"}, "es": {...}},
  prioritaires sur DeepL.
- En cas d'erreur DeepL (clé absente, quota…), le texte français est conservé pour les éléments non traduits
  et le script ne fait pas échouer la mise à jour.
Aucune dépendance : bibliothèque standard uniquement.
"""
import csv, hashlib, json, os, sys, time, urllib.parse, urllib.request

LANGS = {"it": "IT", "es": "ES"}
SRC = "observatoire-data.json"
CACHE = "translations/cache.json"
CORR = "translations/corrections.json"

PAYS = {
    "it": {"Allemagne": "Germania", "Autriche": "Austria", "Belgique": "Belgio", "Bulgarie": "Bulgaria", "Chypre": "Cipro",
           "Croatie": "Croazia", "Danemark": "Danimarca", "Espagne": "Spagna", "Estonie": "Estonia", "Finlande": "Finlandia",
           "France": "Francia", "Grèce": "Grecia", "Hongrie": "Ungheria", "Irlande": "Irlanda", "Italie": "Italia",
           "Lettonie": "Lettonia", "Lituanie": "Lituania", "Luxembourg": "Lussemburgo", "Malte": "Malta", "Pays-Bas": "Paesi Bassi",
           "Pologne": "Polonia", "Portugal": "Portogallo", "Roumanie": "Romania", "Slovaquie": "Slovacchia", "Slovénie": "Slovenia",
           "Suède": "Svezia", "Tchéquie": "Cechia", "Moldavie": "Moldavia", "Royaume-Uni": "Regno Unito", "Norvège": "Norvegia",
           "Ukraine": "Ucraina"},
    "es": {"Allemagne": "Alemania", "Autriche": "Austria", "Belgique": "Bélgica", "Bulgarie": "Bulgaria", "Chypre": "Chipre",
           "Croatie": "Croacia", "Danemark": "Dinamarca", "Espagne": "España", "Estonie": "Estonia", "Finlande": "Finlandia",
           "France": "Francia", "Grèce": "Grecia", "Hongrie": "Hungría", "Irlande": "Irlanda", "Italie": "Italia",
           "Lettonie": "Letonia", "Lituanie": "Lituania", "Luxembourg": "Luxemburgo", "Malte": "Malta", "Pays-Bas": "Países Bajos",
           "Pologne": "Polonia", "Portugal": "Portugal", "Roumanie": "Rumanía", "Slovaquie": "Eslovaquia", "Slovénie": "Eslovenia",
           "Suède": "Suecia", "Tchéquie": "Chequia", "Moldavie": "Moldavia", "Royaume-Uni": "Reino Unido", "Norvège": "Noruega",
           "Ukraine": "Ucrania"},
}

# Contexte donné à DeepL (n'est pas traduit ni facturé) : registre et termes à respecter
CONTEXT = ("Observatoire de la guerre russe en Europe, revue de géopolitique Le Grand Continent. "
           "Textes factuels et descriptifs sur des incidents (drones, sabotages, incendies, espionnage, ingérence). "
           "« l'Union » désigne l'Union européenne.")


def h(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:16]


def load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return default


def deepl(texts, target, key):
    host = "https://api-free.deepl.com" if key.endswith(":fx") else "https://api.deepl.com"
    data = [("source_lang", "FR"), ("target_lang", target), ("preserve_formatting", "1"), ("context", CONTEXT)]
    data += [("text", t) for t in texts]
    req = urllib.request.Request(host + "/v2/translate", data=urllib.parse.urlencode(data).encode(),
                                 headers={"Authorization": "DeepL-Auth-Key " + key,
                                          "User-Agent": "observatoire-bot",
                                          "Content-Type": "application/x-www-form-urlencoded"})
    last = None
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return [x["text"] for x in json.load(r)["translations"]]
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code} {e.read()[:200]!r}"
            if e.code in (403, 456):  # clé refusée / quota dépassé : inutile d'insister
                break
        except Exception as e:  # noqa
            last = str(e)
        time.sleep(3 * (i + 1))
    raise RuntimeError(last)


def main():
    src = load(SRC, None)
    if not src:
        sys.exit("observatoire-data.json introuvable")
    key = os.environ.get("DEEPL_API_KEY", "").strip()
    cache = load(CACHE, {})
    corr = load(CORR, {})
    report = []

    for lang, target in LANGS.items():
        c = cache.setdefault(lang, {})
        fix = corr.get(lang, {})
        texts = set()
        for e in src["events"]:
            for f in ("nom", "desc", "lieu"):
                if e.get(f): texts.add(e[f])
        for m in (src.get("media") or {}).values():
            if m.get("alt"): texts.add(m["alt"])
        todo = [t for t in sorted(texts) if t not in fix and h(t) not in c]
        done = 0
        if todo and key:
            try:
                for i in range(0, len(todo), 40):
                    batch = todo[i:i + 40]
                    for t, tr in zip(batch, deepl(batch, target, key)):
                        c[h(t)] = tr
                        done += 1
            except Exception as err:  # noqa
                report.append(f"{lang} : erreur DeepL ({err}) ; {len(todo) - done} textes restent en français")
        elif todo:
            report.append(f"{lang} : pas de clé DEEPL_API_KEY ; {len(todo)} textes restent en français")
        if done:
            report.append(f"{lang} : {done} textes traduits")

        def tr(s):
            if not s: return s
            return fix.get(s) or c.get(h(s)) or s

        out = dict(src)
        out["lang"] = lang
        evs = []
        for e in src["events"]:
            e2 = dict(e)
            for f in ("nom", "desc", "lieu"):
                e2[f] = tr(e.get(f))
            e2["pays"] = " / ".join(PAYS[lang].get(p.strip(), p.strip()) for p in e["pays"].split("/"))
            evs.append(e2)
        out["events"] = evs
        if src.get("media"):
            out["media"] = {k: {**m, "alt": tr(m.get("alt"))} for k, m in src["media"].items()}
        with open(f"observatoire-data-{lang}.json", "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
        # Tableau lisible (français / traduction côte à côte), importable dans Google Sheets avec IMPORTDATA
        LN = {"it": "IT", "es": "ES"}[lang]
        with open(f"traductions-{lang}.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ID", "Date", "Nom (FR)", f"Nom ({LN})", "Descriptif (FR)", f"Descriptif ({LN})",
                        "Ville / Région (FR)", f"Ville / Région ({LN})", f"Pays ({LN})"])
            for e, e2 in sorted(zip(src["events"], evs), key=lambda p: p[0]["date"], reverse=True):
                w.writerow([e["id"], e["date"], e["nom"], e2["nom"], e["desc"], e2["desc"], e.get("lieu", ""), e2.get("lieu", ""), e2["pays"]])
            for k, m in (src.get("media") or {}).items():
                w.writerow([k, "", "Légende du média : " + (m.get("alt") or ""), tr(m.get("alt")), "", "", "", "", ""])

    # Le cache ne garde que les textes encore utilisés (évite qu'il grossisse indéfiniment)
    live = set()
    for e in src["events"]:
        for f in ("nom", "desc", "lieu"):
            if e.get(f): live.add(h(e[f]))
    for m in (src.get("media") or {}).values():
        if m.get("alt"): live.add(h(m["alt"]))
    for lang in cache:
        cache[lang] = {k: v for k, v in cache[lang].items() if k in live}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=0, sort_keys=True)
    if not os.path.exists(CORR):
        with open(CORR, "w", encoding="utf-8") as f:
            json.dump({"it": {}, "es": {}}, f, ensure_ascii=False, indent=1)
    print("\n".join(report) or "Traductions à jour.")


if __name__ == "__main__":
    main()
