import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, dsf=1.5, path='observatoire_test.html')
        await pg.wait_for_timeout(4000)
        await pg.screenshot(path=f'{ROOT}/shots/v6_hero.png')
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.evaluate('window.scrollBy(0, 40)'); await pg.wait_for_timeout(2600)
        bb = await pg.locator('#carte').bounding_box(); cl = {'x': bb['x'], 'y': bb['y'], 'width': bb['width'], 'height': bb['height'] + 90}
        await pg.screenshot(path=f'{ROOT}/shots/v6_carte.png', clip=cl)
        await pg.locator('#carte .pt').nth(20).hover(); await pg.wait_for_timeout(500)
        print('infobulle :', await pg.evaluate('document.getElementById("gctip").innerText'))
        await pg.locator('#carte .pt').nth(20).click(force=True); await pg.wait_for_timeout(1800)
        await pg.screenshot(path=f'{ROOT}/shots/v6_zoom.png', clip=cl)
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(1500)
        await pg.locator('button[aria-label="Revenir à la vue d\'ensemble"]').click(); await pg.wait_for_timeout(1400)
        y = await pg.evaluate('document.getElementById("chrono").getBoundingClientRect().top + scrollY'); await pg.evaluate(f'window.scrollTo(0, {y - 420})'); await pg.wait_for_timeout(3800)
        await pg.screenshot(path=f'{ROOT}/shots/v6_chrono.png', clip={'x': 0, 'y': 120, 'width': 1440, 'height': 760})
        print([e for e in errs if 'Failed' not in e and 'failed to load' not in e])
        await b.close()
        b, pg, errs = await open_page(p, 390, 844, dsf=2, path='observatoire_test.html', mobile=True)
        await pg.wait_for_timeout(4000)
        await pg.screenshot(path=f'{ROOT}/shots/v6_m_hero.png')
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(2600)
        await pg.screenshot(path=f'{ROOT}/shots/v6_m_carte.png')
        await b.close()
asyncio.run(main())
