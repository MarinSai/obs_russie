import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        for w, mob in ((390, True), (1440, False)):
            b, pg, errs = await open_page(p, w, 800, dsf=2 if mob else 1, path='observatoire_test.html', mobile=mob)
            await pg.wait_for_timeout(2500)
            await pg.locator('.jrow').first.scroll_into_view_if_needed(); await pg.locator('.jrow').first.click(); await pg.wait_for_timeout(1300)
            y = await pg.evaluate('document.querySelector(".jrow").getBoundingClientRect().top + scrollY'); await pg.evaluate(f'scrollTo(0,{y-140})'); await pg.wait_for_timeout(600)
            await pg.screenshot(path=f'{ROOT}/shots/v10_journal_{w}.png', clip={'x': 0, 'y': 0, 'width': min(w, 900), 'height': 560})
            await b.close()
asyncio.run(main())
