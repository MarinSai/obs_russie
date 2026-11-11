import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 393, 660, dsf=2, path=sys.argv[1] if len(sys.argv) > 1 else 'observatoire_test.html', mobile=True)
        await pg.wait_for_timeout(4000)
        await pg.screenshot(path=f'{ROOT}/shots/v8_m_hero.png')
        print('haut ouverture :', await pg.evaluate('Math.round(document.getElementById("hero").getBoundingClientRect().height)'), 'chiffres clés à', await pg.evaluate('Math.round(document.querySelector(".kfg").getBoundingClientRect().top)'))
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(2600)
        bb = await pg.locator('#carte').bounding_box(); cl = {'x': 0, 'y': max(0, bb['y'] - 10), 'width': 393, 'height': bb['height'] + 20}
        c = pg.locator('#carte .pt.clu'); n = 0
        while await c.count() and n < 5:
            big = await pg.evaluate('[...document.querySelectorAll("#carte .pt.clu")].map(e => e.getBoundingClientRect().width).reduce((a, w, i, L) => w > L[a] ? i : a, 0)')
            await c.nth(big).click(); await pg.wait_for_timeout(2000); n += 1
            print('toucher', n, ': foyers', await c.count(), 'zoom', await pg.evaluate('document.querySelector("#carte").innerText.match(/×[0-9.]+/)?.[0]'))
        await pg.screenshot(path=f'{ROOT}/shots/v8_m_zoom.png', clip=cl)
        for i in range(3):
            await pg.locator('button[aria-label="Zoomer"]').click(); await pg.wait_for_timeout(700)
        print('au zoom maximum : foyers', await c.count())
        print([e for e in errs if 'Failed' not in e and 'failed to load' not in e]); await b.close()
asyncio.run(main())
