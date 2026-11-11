import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 390, 760, dsf=2, path='observatoire_test.html', mobile=True)
        await pg.wait_for_timeout(3500)
        # chronologie
        await pg.locator('#chr-sc').scroll_into_view_if_needed(); await pg.wait_for_timeout(2500)
        print('chrono :', await pg.evaluate('(() => { const c = document.getElementById("chr-sc"); return [c.clientWidth, c.scrollWidth, Math.round(c.scrollLeft), document.documentElement.scrollWidth]; })()'))
        y = await pg.evaluate('document.querySelector(".chr").getBoundingClientRect().top + scrollY'); await pg.evaluate(f'scrollTo(0,{y-80})'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'{ROOT}/shots/v9_m_chrono.png')
        # pan à un doigt sur la carte zoomée
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(1500)
        await pg.locator('button[aria-label="Zoomer"]').click(); await pg.wait_for_timeout(900)
        bb = await pg.locator('#carte').bounding_box(); cx, cy = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
        cdp = await pg.context.new_cdp_session(pg)
        before = await pg.evaluate('[scrollY, JSON.stringify([...document.querySelectorAll("#carte .pt")].slice(0,3).map(e => Math.round(e.getBoundingClientRect().left)))]')
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': cx, 'y': cy}]})
        for i in range(1, 11):
            await cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': cx + 8 * i, 'y': cy + 10 * i}]}); await pg.wait_for_timeout(16)
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); await pg.wait_for_timeout(600)
        after = await pg.evaluate('[scrollY, JSON.stringify([...document.querySelectorAll("#carte .pt")].slice(0,3).map(e => Math.round(e.getBoundingClientRect().left)))]')
        print('un doigt (zoomé) : défilement page', before[0], '→', after[0], '| carte déplacée :', before[1] != after[1])
        await pg.locator('button[aria-label="Revenir à la vue d\'ensemble"]').click(); await pg.wait_for_timeout(1200)
        bb = await pg.locator('#carte').bounding_box(); cx, cy = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
        s0 = await pg.evaluate('scrollY')
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': cx, 'y': cy}]})
        for i in range(1, 11):
            await cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': cx, 'y': cy - 15 * i}]}); await pg.wait_for_timeout(16)
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); await pg.wait_for_timeout(600)
        print('un doigt (vue d\'ensemble) : défilement page', s0, '→', await pg.evaluate('scrollY'))
        # filtres actifs : barre de la carte et barre du journal
        await pg.locator('.side-seuils input[type=checkbox], label:has-text("Faits antérieurs") input').first.check(); await pg.wait_for_timeout(1500)
        fb = pg.locator('.fbar').first; await fb.scroll_into_view_if_needed(); await pg.wait_for_timeout(500)
        await fb.screenshot(path=f'{ROOT}/shots/v9_m_fbar1.png')
        fb2 = pg.locator('.fbar').last; await fb2.scroll_into_view_if_needed(); await pg.wait_for_timeout(500)
        await fb2.screenshot(path=f'{ROOT}/shots/v9_m_fbar2.png')
        print('barres :', await pg.locator('.fbar').count())
        await pg.screenshot(path=f'{ROOT}/shots/v9_m_full.png', full_page=True)
        print([e for e in errs if 'Failed' not in e and 'failed to load' not in e]); await b.close()
asyncio.run(main())
