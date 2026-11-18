import asyncio, sys, json, copy
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
import pw
BASE = json.loads(pw.DATA)
def variant(name):
    D = copy.deepcopy(BASE); E = D['events']
    if name == 'sans_media':
        for e in E: e['sources'] = []; e.pop('img', None)
        D['media'] = {}
    if name == 'titre_long':
        E[0]['nom'] = 'Titre ' + 'très long ' * 30; E[0]['desc'] = 'Description ' * 300
    if name == 'un_nouveau':
        last = max(e['entree'] for e in E)
        n = 0
        for e in E:
            if e['entree'] == last:
                n += 1
                if n > 1: e['entree'] = '2026-10-01'
    if name == 'sans_anterieur':
        D['events'] = [e for e in E if not e['passe']]
    if name == 'peu':
        D['events'] = [e for e in E if not e['passe']][:3]
    if name == 'vide':
        D['events'] = []
    return json.dumps(D).encode()
async def open_v(p, w, h, body, mob=False, status=200, delay=0, path='observatoire_test.html'):
    br = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    ctx = await br.new_context(viewport={'width': w, 'height': h}, is_mobile=mob, has_touch=mob); await route(ctx)
    async def h_(r):
        if delay: await asyncio.sleep(delay)
        if status != 200: return await r.fulfill(status=status, body=b'not found')
        await r.fulfill(status=200, content_type='application/json', body=body, headers={'access-control-allow-origin': '*'})
    await ctx.route(lambda u: 'observatoire-data' in u, h_)
    pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append('JS ' + str(e)[:160])); pg.on('console', lambda m: errs.append('console ' + m.text[:160]) if m.type == 'error' and 'Failed to load' not in m.text and 'ERR_' not in m.text else None)
    await pg.goto('http://127.0.0.1:8765/' + path)
    return br, pg, errs
async def tour(pg):
    """parcours : défiler, filtres, ouvrir, rejouer, journal"""
    H = await pg.evaluate('document.documentElement.scrollHeight')
    for y in range(0, H, 700): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(120)
    await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(800)
    n = await pg.locator('#carte .pt').count()
    if n: await pg.locator('#carte .pt').first.click(force=True); await pg.wait_for_timeout(900); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
    if await pg.locator('.nwb').is_visible(): await pg.locator('.nwb').click(); await pg.wait_for_timeout(800); await pg.locator('.nwb').click(); await pg.wait_for_timeout(500)
    if await pg.locator('.player button').count(): await pg.locator('.player button').nth(2).click(); await pg.wait_for_timeout(1500); await pg.locator('.player button').nth(2).click()
    j = pg.locator('.jrow')
    if await j.count(): await j.first.scroll_into_view_if_needed(); await j.first.click(); await pg.wait_for_timeout(700)
    return n
async def main():
    serve()
    async with async_playwright() as p:
        R = {}
        class P(dict):
            def __setitem__(self, k, v): print(k, '→', v, flush=True); super().__setitem__(k, v)
        R = P()
        # 3. filtres extrêmes + 4. enchaînements rapides
        br, pg, errs = await open_v(p, 1440, 900, pw.DATA); await pg.wait_for_timeout(3000)
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(1500)
        for i in range(await pg.locator('.side-seuils .row').count()): await pg.locator('.side-seuils .row').nth(i).click(); await pg.wait_for_timeout(150)
        vide = dict(hexagones=await pg.locator('#carte .pt').count(), journal=await pg.locator('.jrow').count(), total=await pg.evaluate('document.querySelector(".side-count").innerText.split("\\n")[0]'))
        vide['boutons_reset'] = await pg.evaluate('[...document.querySelectorAll("button")].filter(b => /initialiser/i.test(b.textContent)).map(b => b.textContent.trim() + (b.offsetParent ? "" : " (caché)"))')
        await pg.reload(); await pg.wait_for_timeout(3000); await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(1500)
        # rapides
        pts = pg.locator('#carte .pt')
        for i in range(6): await pg.evaluate(f'document.querySelectorAll("#carte .pt")[{i*7}].click()'); await pg.wait_for_timeout(60)
        await pg.evaluate('document.querySelectorAll(".player button")[2].click()'); await pg.wait_for_timeout(200)
        await pg.evaluate('document.querySelectorAll("#carte .pt")[3].click()'); await pg.wait_for_timeout(100)
        await pg.evaluate('document.querySelectorAll("nav .navbtn")[1].click()'); await pg.wait_for_timeout(100)
        for i in range(4): await pg.keyboard.press('Escape'); await pg.wait_for_timeout(50)
        await pg.evaluate('document.querySelector(".side-pays .row").click()'); await pg.wait_for_timeout(100); await pg.evaluate('document.querySelector(".nwb").click()'); await pg.wait_for_timeout(100)
        await pg.mouse.dblclick(700, 500); await pg.wait_for_timeout(1500)
        b = pg.locator('button:visible', has_text='initialiser')
        if await b.count(): await b.first.click(); await pg.wait_for_timeout(1200)
        R['filtres tous décochés'] = vide
        R['enchaînements rapides'] = dict(hexagones_après_reset=await pg.locator('#carte .pt').count(), erreurs=errs[:4])
        # 7. lien vers un événement inexistant
        await br.close()
        br, pg, errs = await open_v(p, 1440, 900, pw.DATA, path='observatoire_test.html#EVEN999999'); await pg.wait_for_timeout(3500)
        R['lien vers événement inexistant'] = dict(fiche=await pg.evaluate('!!document.querySelector(".fiche:not(.fpays)")'), hexagones=await pg.locator('#carte .pt').count(), erreurs=errs[:3])
        await br.close()
        # 6. données qui changent pendant que la page est ouverte (rechargement avec un événement de plus)
        D2 = copy.deepcopy(BASE); e = copy.deepcopy(D2['events'][0]); e['id'] = 'EVEN000001'; e['entree'] = '2026-11-19'; e['date'] = '2026-11-18'; D2['events'].append(e)
        br, pg, errs = await open_v(p, 1440, 900, pw.DATA); await pg.wait_for_timeout(3000)
        await pg.context.unroute(lambda u: 'observatoire-data' in u)
        await pg.context.route(lambda u: 'observatoire-data' in u, lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps(D2).encode(), headers={'access-control-allow-origin': '*'}))
        await pg.reload(); await pg.wait_for_timeout(3500); await pg.evaluate('scrollTo(0,700)'); await pg.wait_for_timeout(1200)
        R['nouvelle version des données'] = dict(premier_chiffre=await pg.evaluate('document.querySelector(".kfc .sr-only").textContent'), bouton=await pg.evaluate('document.querySelector(".nwb").innerText'), erreurs=errs[:3])
        await br.close()
        # 5. largeurs intermédiaires
        for w, h, mob in ((768, 1024, True), (1024, 768, True), (1280, 800, False), (844, 390, True), (1920, 1080, False)):
            br, pg, errs = await open_v(p, w, h, pw.DATA, mob=mob); await pg.wait_for_timeout(3000)
            try: n = await tour(pg)
            except Exception as ex: errs.append('PARCOURS ' + str(ex)[:120]); n = -1
            await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'{ROOT}/shots/edge_{w}x{h}.png', full_page=True)
            R[f'fenêtre {w}×{h}'] = dict(largeur_page=await pg.evaluate('document.documentElement.scrollWidth'), hexagones=n, erreurs=errs[:3])
            await br.close()
        # 8. console sur parcours complet en IT et ES
        for path in ('test_IT.html', 'test_ES.html'):
            br, pg, errs = await open_v(p, 1440, 900, open(ROOT + '/repo/obs_russie/observatoire-data-it.json', 'rb').read() if 'IT' in path else pw.DATA, path=path); await pg.wait_for_timeout(3000)
            try: await tour(pg)
            except Exception as ex: errs.append('PARCOURS ' + str(ex)[:120])
            R['parcours ' + path] = dict(erreurs=errs[:3]); await br.close()
asyncio.run(main())
