import asyncio, sys, json, collections, datetime, os
sys.path.insert(0, os.path.join(os.environ.get('OBS_WORK', os.path.expanduser('~/work')), 'tools'))
from pw import *
D = json.loads(DATA); EV = D['events']
COL = {'Confirmé': '#dd203c', 'Attribué': '#f58c6c', 'Suspecté': '#e9d3a6', 'Non déterminé': '#77767b'}
ORD = ['Confirmé', 'Attribué', 'Suspecté', 'Non déterminé']
MOIS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
def fd(d): y, m, j = d.split('-'); return f'{int(j)} {MOIS[int(m)-1]} {y}'
def hx(c, s=13): return f'<span class="hx" style="--c:{c};position:relative;display:inline-block;width:{s}px;height:{s*1.12:.1f}px;clip-path:var(--mh);flex:none"></span>'
MONO = "font-family:'IBM Plex Mono',monospace"; LAB = MONO + ';font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#a3a09a'
TAG = f'<span style="{MONO};font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#0b0b0c;background:#e9d3a6;padding:3px 7px;border-radius:2px">Maquette</span>'

def fiche_pays(p):
    L = sorted([e for e in EV if e['pays'] == p], key=lambda e: e['date'])
    n = len(L); se = collections.Counter(e['seuil'] for e in L); ca = collections.Counter(e['cat'] for e in L).most_common()
    rk = [k for k, _ in collections.Counter(e['pays'] for e in EV).most_common()].index(p) + 1
    seg = ''.join(f'<span style="flex:{se[s]};background:{COL[s]};height:8px"></span>' for s in ORD if se[s])
    leg = ''.join(f'<span style="display:flex;align-items:center;gap:6px">{hx(COL[s], 10)}<span>{s}</span><span style="{MONO};color:#f3f1ec">{se[s]}</span></span>' for s in ORD if se[s])
    mx = ca[0][1]
    cats = ''.join(f'<div style="display:flex;align-items:center;gap:10px;font-size:14px"><span style="width:112px">{c}</span><span style="flex:1;height:5px;background:#1c1c1e"><span style="display:block;height:100%;width:{k/mx*100:.0f}%;background:#f3f1ec"></span></span><span style="{MONO};font-size:13px;width:16px;text-align:right">{k}</span></div>' for c, k in ca)
    # frise : un hexagone par événement, placé selon sa date (mars 2024 → nov. 2026)
    d0, d1 = datetime.date(2024, 3, 1), datetime.date(2026, 11, 30); span = (d1 - d0).days
    seen = collections.Counter(); dots = ''
    for e in L:
        x = (datetime.date.fromisoformat(e['date']) - d0).days / span * 100; b = round(x / 3.2); k = seen[b]; seen[b] += 1
        dots += f'<span style="position:absolute;left:calc({b*3.2:.1f}% - 6px);bottom:{2 + k*13}px">{hx(COL[e["seuil"]], 11)}</span>'
    ticks = ''.join(f'<span style="position:absolute;left:{(datetime.date(y,1,1)-d0).days/span*100:.1f}%;top:0;bottom:-16px;border-left:1px solid #2c2c30"><span style="position:absolute;bottom:0;left:5px;{MONO};font-size:10px;color:#77767b">{y}</span></span>' for y in (2025, 2026))
    last = ''.join(f'<div style="display:flex;gap:12px;padding:9px 0;border-top:1px solid #262628"><span style="{MONO};font-size:11px;color:#a3a09a;white-space:nowrap;padding-top:3px;width:62px">{fd(e["date"])[:-5]}</span><span style="font-family:\'GC Sanomat\',Georgia,serif;font-size:15.5px;line-height:1.25">{hx(COL[e["seuil"]], 9)}&nbsp; {e["nom"]}</span></div>' for e in L[-3:][::-1])
    return f'''<div id="mock" style="position:absolute;z-index:30;top:14px;right:14px;bottom:14px;width:400px;box-sizing:border-box;background:#0d0d0e;border:1px solid #333336;border-top:2px solid #dd203c;border-radius:6px;padding:22px 24px;display:flex;flex-direction:column;gap:15px;box-shadow:0 20px 60px rgba(0,0,0,.5);color:#f3f1ec;font-family:'GC National',sans-serif;overflow:hidden">
<div style="display:flex;justify-content:space-between;align-items:center"><span style="{LAB}">Fiche pays</span>{TAG}</div>
<div style="font-family:'GC Sanomat',Georgia,serif;font-size:40px;line-height:1;letter-spacing:-.01em">{p}</div>
<div style="display:flex;align-items:baseline;gap:12px;border-bottom:1px solid #262628;padding-bottom:14px"><span style="font-family:'GC Sanomat',Georgia,serif;font-size:54px;line-height:.9;color:#ea4d62">{n}</span><span style="font-size:14.5px;line-height:1.35;color:#c9c5bd">événements recensés<br>{rk}ᵉ pays le plus visé</span></div>
<div style="display:flex;flex-direction:column;gap:9px"><span style="{LAB}">Seuil d'attribution</span><div style="display:flex;gap:2px">{seg}</div><div style="display:flex;flex-wrap:wrap;gap:6px 16px;font-size:13px;color:#c9c5bd">{leg}</div></div>
<div style="display:flex;flex-direction:column;gap:7px"><span style="{LAB}">Type d'action</span>{cats}</div>
<div style="display:flex;flex-direction:column;gap:8px"><span style="{LAB}">Dans le temps</span><div style="position:relative;height:66px;border-bottom:1px solid #3a3a3d;margin-bottom:16px">{ticks}{dots}</div></div>
<div style="display:flex;flex-direction:column"><span style="{LAB};margin-bottom:8px">Derniers événements</span>{last}</div>
</div>'''

def etape():
    ro = [e for e in EV if e['pays'] in ('Roumanie', 'Moldavie', 'Bulgarie')]; n = len(ro); aero = sum(e['cat'] in ('Aéronef', 'Frappes de navires') for e in ro)
    dots = ''.join(f'<span style="width:{22 if i == 1 else 7}px;height:3px;background:{"#dd203c" if i == 1 else "#3a3a3d"}"></span>' for i in range(5))
    btn = 'width:38px;height:38px;border:1px solid #3a3a3d;background:#18181a;color:#f3f1ec;border-radius:50%;display:grid;place-items:center;font-size:17px'
    return f'''<div id="mock" style="position:absolute;z-index:30;left:92px;bottom:54px;width:430px;box-sizing:border-box;background:rgba(13,13,14,.94);border:1px solid #333336;border-left:2px solid #dd203c;padding:20px 22px 18px;display:flex;flex-direction:column;gap:11px;box-shadow:0 20px 60px rgba(0,0,0,.55);color:#f3f1ec;font-family:'GC National',sans-serif">
<div style="display:flex;justify-content:space-between;align-items:center"><span style="{LAB}">Parcours — 2 / 5</span>{TAG}</div>
<div style="font-family:'GC Sanomat',Georgia,serif;font-size:27px;line-height:1.12">Mer Noire et bouches du Danube</div>
<div style="font-size:15.5px;line-height:1.5;color:#d9d5cd">{n} événements en Roumanie, en Moldavie et en Bulgarie, dont {aero} concernent des aéronefs ou des navires. <span style="color:#8f8c86">[Texte d'exemple tiré des données — à écrire par la rédaction.]</span></div>
<div style="display:flex;align-items:center;justify-content:space-between;margin-top:4px"><div style="display:flex;gap:5px;align-items:center">{dots}</div><div style="display:flex;gap:8px"><span style="{btn}">←</span><span style="{btn};background:#f3f1ec;color:#0b0b0c;border-color:#f3f1ec">→</span></div></div>
</div>'''

def multiples():
    w0 = datetime.date(2026, 9, 21); NW = 8
    L = [e for e in EV if e['date'] >= '2026-09-21']
    cats = [c for c, _ in collections.Counter(e['cat'] for e in L).most_common()]
    head = ''.join(f'<span style="flex:1;{MONO};font-size:10.5px;color:#77767b;letter-spacing:.06em;padding-left:8px;border-left:1px solid #2c2c30">{(w0+datetime.timedelta(7*i)).day} {MOIS[(w0+datetime.timedelta(7*i)).month-1]}</span>' for i in range(NW))
    rows = ''
    for c in cats:
        cells = ''
        for i in range(NW):
            a, b = (w0 + datetime.timedelta(7*i)).isoformat(), (w0 + datetime.timedelta(7*i+7)).isoformat()
            E = sorted([e for e in L if e['cat'] == c and a <= e['date'] < b], key=lambda e: ORD.index(e['seuil']))
            cells += f'<span style="flex:1;display:flex;flex-wrap:wrap-reverse;align-content:flex-start;gap:2px 2px;padding:6px 8px;border-left:1px solid #2c2c30;min-height:36px;box-sizing:border-box">{"".join(hx(COL[e["seuil"]], 13) for e in E)}</span>'
        k = sum(e['cat'] == c for e in L)
        rows += f'<div style="display:flex;align-items:stretch;border-top:1px solid #262628"><span style="width:200px;flex:none;display:flex;align-items:center;font-size:15px">{c}</span><div style="flex:1;display:flex">{cells}</div><span style="width:54px;flex:none;display:flex;align-items:center;justify-content:flex-end;{MONO};font-size:15px">{k}</span></div>'
    leg = ''.join(f'<span style="display:flex;align-items:center;gap:6px">{hx(COL[s], 10)}{s}</span>' for s in ORD)
    return f'''<div id="mock" style="width:1180px;margin:40px auto;padding:30px 34px 26px;box-sizing:border-box;color:#f3f1ec;font-family:'GC National',sans-serif;border:1px solid #262628;background:#0d0d0e">
<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px"><span style="font-family:'GC Sanomat',Georgia,serif;font-size:26px">Chronologie par type d'action</span>{TAG}</div>
<div style="display:flex;gap:18px;font-size:12.5px;color:#a3a09a;margin-bottom:18px"><span style="{LAB}">Un hexagone = un événement</span>{leg}</div>
<div style="display:flex"><span style="width:200px;flex:none;{LAB}">Semaine du</span><div style="flex:1;display:flex">{head}</div><span style="width:54px;flex:none;text-align:right;{LAB}">Total</span></div>
<div style="margin-top:8px;border-bottom:1px solid #262628">{rows}</div>
<div style="{MONO};font-size:11px;color:#77767b;margin-top:12px">{len(L)} événements depuis le 21 septembre 2026 — données de l'Observatoire au 11 novembre 2026.</div>
</div>'''

async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, dsf=1.5, path='observatoire_test.html')
        await pg.wait_for_timeout(2500)
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.evaluate('window.scrollBy(0, 40)'); await pg.wait_for_timeout(2600)
        bb = await pg.locator('#carte').bounding_box(); cl = {'x': bb['x'], 'y': bb['y'], 'width': bb['width'], 'height': bb['height']}
        async def inject(html): await pg.evaluate('''h => { const o = document.getElementById('mock'); if (o) o.remove(); document.getElementById('carte').insertAdjacentHTML('beforeend', h); }''', html)
        await pg.locator('.side-pays .row', has_text='Pologne').click(); await pg.wait_for_timeout(2200)
        await inject(fiche_pays('Pologne')); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{ROOT}/shots/mock/m1_fiche_pays.png', clip=cl)
        await pg.evaluate('document.getElementById("mock").remove()')
        await pg.locator('.side-pays .row', has_text='Pologne').click(); await pg.wait_for_timeout(1800)
        await pg.locator('.side-pays .row', has_text='Roumanie').click(); await pg.wait_for_timeout(2200)
        await inject(etape()); await pg.evaluate('''() => { const m = document.querySelector('.mini'); if (m) m.style.display = 'none'; }'''); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{ROOT}/shots/mock/m2_parcours.png', clip=cl)
        await pg.evaluate('''h => { document.getElementById('mock').remove(); const d = document.createElement('div'); d.innerHTML = h; d.style.cssText = 'position:absolute;left:0;top:0;width:1440px;z-index:99;background:#0b0b0c'; d.id = 'mockwrap'; document.querySelector('.pg').appendChild(d); window.scrollTo(0, 0); }''', multiples()); await pg.wait_for_timeout(400)
        mb = await pg.locator('#mockwrap #mock').bounding_box()
        await pg.screenshot(path=f'{ROOT}/shots/mock/m3_types.png', clip={'x': mb['x'] - 20, 'y': mb['y'] - 20, 'width': mb['width'] + 40, 'height': mb['height'] + 40})
        print([e for e in errs if 'Failed' not in e and 'failed to load' not in e])
        await b.close()
asyncio.run(main())
