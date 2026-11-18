import asyncio, sys, time
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, path='observatoire_test.html#EVEN1642')
        await pg.wait_for_timeout(4500)
        cdp = await pg.context.new_cdp_session(pg)
        await pg.evaluate('''() => { window.__w = []; document.getElementById('carte').addEventListener('wheel', e => { setTimeout(() => window.__w.push([e.defaultPrevented, Math.round(scrollY)]), 0); }); }''')
        bb = await pg.locator('#carte').bounding_box(); x, y = bb['x'] + bb['width'] * 0.3, bb['y'] + bb['height'] * 0.5
        async def spin(n, dy, t0):
            for i in range(n):
                await cdp.send('Input.dispatchMouseEvent', {'type': 'mouseWheel', 'x': x, 'y': y, 'deltaX': 0, 'deltaY': dy, 'timestamp': t0 + i * 0.06})
        t = time.time()
        await spin(12, 100, t); await pg.wait_for_timeout(800)
        print('geste continu de 12 crans vers le bas :', await pg.evaluate('window.__w'))
        await pg.evaluate('window.__w = []')
        await spin(3, 100, t + 5); await pg.wait_for_timeout(800)
        print('geste suivant, à la vue d’ensemble :', await pg.evaluate('window.__w'))
        await b.close()
asyncio.run(main())
