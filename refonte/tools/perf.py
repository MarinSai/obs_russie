import asyncio, sys, os
sys.path.insert(0, os.path.join(os.environ.get('OBS_WORK', os.path.expanduser('~/work')), 'tools'))
from pw import *
REC = '''(ms) => new Promise(res => { const d = []; let p = performance.now(), t0 = p; const f = n => { d.push(n - p); p = n; if (n - t0 < ms) requestAnimationFrame(f); else { d.shift(); d.sort((a, b) => a - b); res({ n: d.length, med: +d[d.length >> 1].toFixed(1), p95: +d[Math.floor(d.length * .95)].toFixed(1), max: +d[d.length - 1].toFixed(1), over25: d.filter(x => x > 25).length }); } }; requestAnimationFrame(f); })'''
async def main(path):
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, path=path)
        cdp = await pg.context.new_cdp_session(pg)
        await cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        await pg.wait_for_timeout(3000)
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(2500)
        async def run(label, action, ms=1300):
            fut = asyncio.ensure_future(pg.evaluate(REC, ms)); await asyncio.sleep(.05); await action(); print(path[:22], label, await fut)
        await run('repos (glitch)', lambda: asyncio.sleep(0), 6000)
        await run('filtre', lambda: pg.locator('nav .navbtn').nth(0).click())
        await run('filtre retour', lambda: pg.locator('nav .navbtn').nth(0).click())
        await run('ouverture', lambda: pg.locator('#carte .pt').nth(20).click(force=True))
        await run('lecture', lambda: pg.locator('.player button').nth(2).click(), 4000)
        await b.close()
asyncio.run(main(sys.argv[1]))
