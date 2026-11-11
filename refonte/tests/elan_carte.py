import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 390, 760, dsf=2, path='observatoire_test.html', mobile=True)
        await pg.wait_for_timeout(3000)
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(1500)
        await pg.locator('button[aria-label="Zoomer"]').click(); await pg.wait_for_timeout(900)
        await pg.evaluate('''() => { window.__f = []; const L = document.getElementById('mapLayer'); let last = performance.now(); const tick = () => { const n = performance.now(); window.__f.push(n - last); last = n; if (window.__f.length < 240) requestAnimationFrame(tick); }; requestAnimationFrame(tick); }''')
        pos = lambda: pg.evaluate('JSON.stringify([...document.querySelectorAll("#carte .pt")].slice(0,1).map(e => Math.round(e.getBoundingClientRect().left)))')
        bb = await pg.locator('#carte').bounding_box(); cx, cy = bb['x'] + bb['width'] * 0.3, bb['y'] + bb['height'] / 2 - 60
        cdp = await pg.context.new_cdp_session(pg)
        p0 = await pos()
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': cx, 'y': cy, 'id': 1}]})
        for i in range(1, 9):
            await cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': cx + 14 * i, 'y': cy, 'id': 1}]}); await pg.wait_for_timeout(16)
        p1 = await pos()
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); await pg.wait_for_timeout(1800)
        p2 = await pos()
        f = await pg.evaluate('window.__f'); f = sorted(f[5:])
        print('doigt : 112 px | carte pendant le geste', p0, '→', p1, '| après élan', p2, '| image médiane', round(f[len(f)//2], 1), 'ms, p95', round(f[int(len(f)*.95)], 1))
        print([e for e in errs if 'Failed' not in e and 'failed to load' not in e]); await b.close()
asyncio.run(main())
