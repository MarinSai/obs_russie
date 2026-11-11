import json, re, math, os
from collections import Counter
PROJ = dict(lon0=13.973, lat0=51.938, scale=2039.565, ox=486.373, oy=386.614)
def project(lat, lon):
    r = math.radians; l, f, f0 = r(lon - PROJ["lon0"]), r(lat), r(PROJ["lat0"])
    k = 2 / (1 + math.sin(f0) * math.sin(f) + math.cos(f0) * math.cos(f) * math.cos(l))
    return PROJ["scale"] * k * math.cos(f) * math.sin(l) + PROJ["ox"], -PROJ["scale"] * k * (math.cos(f0) * math.sin(f) - math.sin(f0) * math.cos(f) * math.cos(l)) + PROJ["oy"]
C = {  # pays (repère interne, jamais affiché) : point d'étiquette, puis points de sonde (un par grande terre)
 'Allemagne': [(51.0,10.3)], 'Autriche': [(47.55,14.3)], 'Belgique': [(50.65,4.6)], 'Bulgarie': [(42.7,25.2)], 'Chypre': [(35.0,33.1)],
 'Croatie': [(45.6,16.3)], 'Danemark': [(56.1,9.2),(55.5,11.8),(55.3,10.4)], 'Espagne': [(40.2,-3.6),(39.6,2.95)], 'Estonie': [(58.8,25.7),(58.4,22.6)],
 'Finlande': [(62.6,26.2)], 'France': [(46.8,2.5),(42.2,9.1)], 'Grèce': [(39.6,21.9),(35.2,24.9),(37.5,22.3)], 'Hongrie': [(47.1,19.4)], 'Irlande': [(53.2,-8.0)],
 'Italie': [(43.0,12.4),(37.6,14.2),(40.1,9.1)], 'Lettonie': [(56.9,25.6)], 'Lituanie': [(55.35,23.9)], 'Luxembourg': [(49.75,6.1)], 'Malte': [(35.9,14.43)],
 'Pays-Bas': [(52.3,5.7)], 'Pologne': [(52.1,19.3)], 'Portugal': [(39.7,-8.0)], 'Roumanie': [(45.9,24.8)], 'Slovaquie': [(48.7,19.5)], 'Slovénie': [(46.1,14.8)],
 'Suède': [(61.5,15.3),(57.5,18.5)], 'Tchéquie': [(49.8,15.3)], 'Moldavie': [(47.25,28.5)], 'Royaume-Uni': [(52.8,-1.6),(54.6,-6.7)], 'Norvège': [(61.2,9.0)],
}
d = json.load(open(os.path.join(os.environ.get('OBS_WORK', os.path.expanduser('~/work')), 'data', 'observatoire-data.json')))
rings = [[tuple(map(float, p.split(','))) for p in re.findall(r'-?[\d.]+,-?[\d.]+', s)] for s in re.findall(r'M[^M]*', d['land'])]
def inside(pt, r):
    x, y = pt; c = False
    for i in range(len(r)):
        x1, y1 = r[i]; x2, y2 = r[i-1]
        if (y1 > y) != (y2 > y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c = not c
    return c
ring_of = lambda pt: next((i for i, r in enumerate(rings) if inside(pt, r)), None)
grp = {}; out = []
for name, pts in C.items():
    pr = [project(*p) for p in pts]; rs = [ring_of(p) for p in pr]
    print(f'{name:12s} étiquette ({pr[0][0]/10:6.2f}%, {pr[0][1]/7.2:6.2f}%) anneaux {rs}')
    for r in rs:
        if r is not None:
            assert r not in grp or grp[r] == name, (name, grp.get(r)); grp[r] = name
    out.append([round(pr[0][0]/10, 2), round(pr[0][1]/7.2, 2)] + [[round(p[0]/10, 2), round(p[1]/7.2, 2)] for p in pr])
# contrôle : les épingles votent-elles bien pour le bon pays ?
bad = Counter(); ok = 0; sea = 0
for e in d['events']:
    ps = [e['pos']] + [m['pos'] for m in e.get('more', [])]; pays = e['pays'].split(' / ')
    if len(ps) != len(pays): print('épingles ≠ pays', e['id'], len(ps), len(pays)); continue
    for p, n in zip(ps, pays):
        xy = p.get('raw') or p['eu']; r = ring_of((xy[0]*10, xy[1]*7.2))
        if r is None: sea += 1
        elif grp.get(r) == n: ok += 1
        else: bad[(e['id'], n, grp.get(r), r)] += 1
print('épingles conformes', ok, 'en mer', sea, 'non conformes', dict(bad))
print(json.dumps([[o[0], o[1], o[2:]] for o in out], separators=(',', ':')))
