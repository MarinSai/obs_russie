import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 390, 844, dsf=2, path='observatoire_test.html', mobile=True)
        await pg.wait_for_timeout(3500)
        print('chiffres clés :', await pg.evaluate('[...document.querySelectorAll(".knum .sr-only")].map(e => e.textContent)'))
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(2600)
        bb = await pg.locator('#carte').bounding_box(); cl = {'x': 0, 'y': max(0, bb['y'] - 10), 'width': 390, 'height': bb['height'] + 20}
        await pg.screenshot(path=f'{ROOT}/shots/v7_m_carte.png', clip=cl)
        print('foyers :', await pg.evaluate('[...document.querySelectorAll("#carte .pt.clu")].map(e => e.getAttribute("aria-label") + " " + Math.round(e.getBoundingClientRect().width))'), 'points :', await pg.locator('#carte .pt').count())
        c = pg.locator('#carte .pt.clu')
        if await c.count():
            big = await pg.evaluate('[...document.querySelectorAll("#carte .pt.clu")].map(e => e.getBoundingClientRect().width).reduce((a, w, i, L) => w > L[a] ? i : a, 0)')
            await c.nth(big).click(); await pg.wait_for_timeout(2000)
            await pg.screenshot(path=f'{ROOT}/shots/v7_m_zoom1.png', clip=cl)
            print('après un toucher : foyers', await c.count(), 'points', await pg.locator('#carte .pt').count())
            if await c.count():
                await c.first.click(); await pg.wait_for_timeout(2000); await pg.screenshot(path=f'{ROOT}/shots/v7_m_zoom2.png', clip=cl)
                print('après deux : foyers', await c.count())
        print([e for e in errs if 'Failed' not in e and 'failed to load' not in e]); await b.close()
        b, pg, errs = await open_page(p, 1440, 1000, dsf=1, path='observatoire_test.html')
        await pg.wait_for_timeout(3000)
        y = await pg.evaluate('document.getElementById("chrono").getBoundingClientRect().top + scrollY'); await pg.evaluate(f'window.scrollTo(0, {y - 420})'); await pg.wait_for_timeout(3800)
        await pg.screenshot(path=f'{ROOT}/shots/v7_chrono.png', clip={'x': 0, 'y': 120, 'width': 1440, 'height': 760})
        print('foyers sur ordinateur :', await pg.locator('#carte .pt.clu').count()); await b.close()
asyncio.run(main())
