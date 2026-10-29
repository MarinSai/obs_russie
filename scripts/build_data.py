#!/usr/bin/env python3
"""Génère observatoire-data.json (événements) à partir de la feuille Google publiée en CSV.

- Lit le CSV (adresse dans SHEET_CSV_URL, ou --csv pour un fichier local).
- Vérifie chaque ligne (colonnes, valeurs autorisées, dates, coordonnées, sources).
- Reprend telles quelles les données fixes du fichier existant (fond de carte, grille, cadrages).
- Garde la position sur la carte des événements déjà présents si leurs coordonnées n'ont pas changé ;
  calcule la position des nouveaux, en les écartant des points voisins.
- Si une seule ligne est invalide, rien n'est écrit et le script échoue (le site garde l'ancienne version).
Aucune dépendance : bibliothèque standard uniquement.
"""
import argparse, csv, io, json, math, os, sys, time, urllib.request
from datetime import datetime

HEADERS = ["ID", "Type", "Année", "Date événement", "Date entrée", "Nom", "Seuil d'attribution",
           "Catégorie", "Pays", "Ville / Région", "Descriptif", "Lat", "Lon",
           "Source 1", "Source 2", "Source 3"]
SEUILS = {"Non déterminé", "Suspecté", "Attribué", "Confirmé"}
CATS = {"Sabotage", "Incendie", "Aéronef", "Renseignement", "Ingérence", "Drones"}
TYPES = {"Nouveau": False, "Passé": True}

# Projection de la carte (stéréographique), ajustée sur les positions du fichier de départ.
# Les positions sont en % de la largeur (1000) et de la hauteur (720) du cadre "eu".
PROJ = dict(lon0=13.973, lat0=51.938, scale=2039.565, ox=486.373, oy=386.614)
W, H = 1000.0, 720.0
MIN_DIST = 17.7  # distance minimale entre deux points, en pixels du cadre (celle du fichier de départ : ~17,7)


def project(lat, lon):
    r = math.radians
    l, f, f0 = r(lon - PROJ["lon0"]), r(lat), r(PROJ["lat0"])
    k = 2 / (1 + math.sin(f0) * math.sin(f) + math.cos(f0) * math.cos(f) * math.cos(l))
    x = PROJ["scale"] * k * math.cos(f) * math.sin(l) + PROJ["ox"]
    y = -PROJ["scale"] * k * (math.cos(f0) * math.sin(f) - math.sin(f0) * math.cos(f) * math.cos(l)) + PROJ["oy"]
    return x, y  # pixels


def fetch(url):
    if url.startswith("file://"):
        url = url[7:]
    if os.path.exists(url):
        return open(url, encoding="utf-8-sig", newline="").read()
    last = None
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "observatoire-bot"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8-sig")
        except Exception as e:  # noqa
            last = e
            time.sleep(3 * (i + 1))
    raise SystemExit(f"Impossible de télécharger la feuille : {last}")


def parse_date(s):
    s = s.strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None


def parse_num(s):
    s = s.strip().replace(" ", "").replace(" ", "")
    if "," in s and "." not in s:
        s = s.replace(",", ".")  # feuille en paramètres régionaux français
    try:
        v = float(s)
    except ValueError:
        return None
    return v if math.isfinite(v) else None


def read_rows(text, errors):
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise SystemExit("Feuille vide.")
    head = [h.strip() for h in rows[0]]
    if head[:16] != HEADERS:
        raise SystemExit("En-têtes inattendus.\n  attendu : %s\n  reçu    : %s" % (HEADERS, head[:16]))
    out = []
    for n, r in enumerate(rows[1:], start=2):
        r = [c.strip() for c in r] + [""] * (16 - len(r))
        if not any(r[:16]):
            continue
        out.append((n, r[:16]))
    return out


def build_events(rows, errors):
    events, seen = [], set()
    for n, r in rows:
        (id_, typ, annee, d_ev, d_en, nom, seuil, cat, pays, lieu, desc, lat, lon, s1, s2, s3) = r
        loc = f"ligne {n} ({id_ or 'sans ID'})"
        if not id_:
            errors.append(f"{loc} : ID manquant"); continue
        if id_ in seen:
            errors.append(f"{loc} : ID en double")
        seen.add(id_)
        if typ not in TYPES: errors.append(f"{loc} : Type « {typ} » (attendu Nouveau ou Passé)")
        if seuil not in SEUILS: errors.append(f"{loc} : Seuil « {seuil} » inconnu")
        if cat not in CATS: errors.append(f"{loc} : Catégorie « {cat} » inconnue")
        for label, val in (("Nom", nom), ("Pays", pays), ("Descriptif", desc)):
            if not val: errors.append(f"{loc} : {label} vide")
        date = parse_date(d_ev); entree = parse_date(d_en)
        if not date: errors.append(f"{loc} : Date événement illisible « {d_ev} »")
        if not entree: errors.append(f"{loc} : Date entrée illisible « {d_en} »")
        la, lo = parse_num(lat), parse_num(lon)
        if la is None or lo is None or not (30 <= la <= 75 and -25 <= lo <= 50):
            errors.append(f"{loc} : coordonnées invalides (Lat « {lat} », Lon « {lon} »)")
        srcs = [s for s in (s1, s2, s3) if s]
        if not srcs: errors.append(f"{loc} : aucune source")
        for s in srcs:
            if not s.startswith(("http://", "https://")):
                errors.append(f"{loc} : source qui n'est pas un lien « {s[:50]} »")
        if date and annee and annee.isdigit() and int(annee) != int(date[:4]):
            errors.append(f"{loc} : Année {annee} ≠ année de la date {date}")
        events.append({"id": id_, "passe": TYPES.get(typ, False), "date": date, "entree": entree, "nom": nom,
                       "seuil": seuil, "cat": cat, "pays": pays, "lieu": lieu, "desc": desc,
                       "lat": la, "lon": lo, "sources": srcs})
    return events


def place(events, old):
    """Ajoute 'pos' à chaque événement (raw = projection exacte ; eu = raw écarté des voisins)."""
    old_by_id = {e["id"]: e for e in old}
    fixed, todo = [], []
    for e in events:
        o = old_by_id.get(e["id"])
        if o and o.get("pos") and abs(o["lat"] - e["lat"]) < 1e-9 and abs(o["lon"] - e["lon"]) < 1e-9:
            e["pos"] = o["pos"]; fixed.append(e)
        else:
            todo.append(e)
    taken = [(e["pos"]["eu"][0] * W / 100, e["pos"]["eu"][1] * H / 100) for e in fixed]
    for e in todo:
        x, y = project(e["lat"], e["lon"])
        raw = [round(x / W * 100, 3), round(y / H * 100, 3)]
        px, py = x, y
        if any(math.hypot(px - tx, py - ty) < MIN_DIST for tx, ty in taken):
            done = False
            for ring in range(1, 400):
                r = ring * 0.5
                steps = max(12, int(2 * math.pi * r / 1.5))
                for s in range(steps):
                    a = 2 * math.pi * s / steps
                    cx, cy = x + r * math.cos(a), y + r * math.sin(a)
                    if all(math.hypot(cx - tx, cy - ty) >= MIN_DIST for tx, ty in taken):
                        px, py, done = cx, cy, True; break
                if done: break
        taken.append((px, py))
        e["pos"] = {"eu": [round(px / W * 100, 2), round(py / H * 100, 2)], "raw": raw}
    return events


def ordered(e):
    return {k: e[k] for k in ("id", "passe", "date", "entree", "nom", "seuil", "cat", "pays", "lieu", "desc",
                              "lat", "lon", "sources", "pos")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="fichier CSV local (sinon : SHEET_CSV_URL)")
    ap.add_argument("--out", default="observatoire-data.json")
    ap.add_argument("--summary", help="écrit un résumé des changements (message de commit)")
    ap.add_argument("--allow-shrink", action="store_true", help="accepter une forte baisse du nombre de lignes")
    a = ap.parse_args()

    src = a.csv or os.environ.get("SHEET_CSV_URL", "")
    if not src: raise SystemExit("SHEET_CSV_URL non défini.")
    old_json = json.load(open(a.out, encoding="utf-8")) if os.path.exists(a.out) else {}
    old = old_json.get("events", [])

    errors = []
    events = build_events(read_rows(fetch(src), errors), errors)
    if errors:
        print("La feuille contient %d problème(s) ; rien n'a été écrit :" % len(errors), file=sys.stderr)
        for m in errors[:60]: print(" -", m, file=sys.stderr)
        sys.exit(1)
    if old and len(events) < 0.7 * len(old) and not a.allow_shrink:
        raise SystemExit(f"{len(events)} lignes contre {len(old)} avant : baisse suspecte, rien n'est écrit.")
    for k in ("land", "east", "grat", "vb"):
        if old and k not in old_json: raise SystemExit(f"Le fichier existant n'a pas la clé « {k} ».")

    events = [ordered(e) for e in place(events, old)]
    new_json = dict(old_json) if old_json else {}
    new_json["events"] = events
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(new_json, f, ensure_ascii=False, separators=(",", ":"))

    oldm = {e["id"]: e for e in old}; newm = {e["id"]: e for e in events}
    added = [i for i in newm if i not in oldm]; removed = [i for i in oldm if i not in newm]
    changed = [i for i in newm if i in oldm and
               {k: v for k, v in newm[i].items() if k != "pos"} != {k: v for k, v in oldm[i].items() if k != "pos"}]
    lines = [f"Données de l'Observatoire : {len(events)} événements"]
    if added: lines.append("Ajoutés : " + ", ".join(added))
    if removed: lines.append("Supprimés : " + ", ".join(removed))
    if changed: lines.append("Modifiés : " + ", ".join(changed))
    msg = "\n".join(lines)
    print(msg)
    if a.summary: open(a.summary, "w", encoding="utf-8").write(msg + "\n")


if __name__ == "__main__":
    main()
