import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        for w, h, mob in ((1440, 1000, False), (390, 800, True)):
            b, pg, errs = await open_page(p, w, h, dsf=1.5 if not mob else 2, path=sys.argv[1] if len(sys.argv) > 1 else 'observatoire_test.html', mobile=mob)
            await pg.wait_for_timeout(3000)
            await pg.locator('#carte').scroll_into_view_if_needed(); await pg.evaluate('window.scrollBy(0, 40)' if not mob else 'window.scrollBy(0, -20)'); await pg.wait_for_timeout(2500)
            btn = pg.locator('.nwb')
            print(w, 'bouton :', (await btn.inner_text()).replace('\n', ' | '), await btn.get_attribute('aria-pressed'))
            await btn.click(); await pg.wait_for_timeout(2200)
            print('   nouveaux', await pg.locator('#carte .pt.is-new').count(), 'estompés', await pg.locator('#carte .pt.is-dim').count(), 'foyers', await pg.locator('#carte .pt.clu').count(), 'pressé', await btn.get_attribute('aria-pressed'))
            if mob:
                await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(600)
                await pg.screenshot(path=f'{ROOT}/shots/v11_m.png')
            else:
                bb = await pg.locator('#carte').bounding_box(); sb = await pg.locator('.side').bounding_box()
                await pg.screenshot(path=f'{ROOT}/shots/v11_d.png', clip={'x': sb['x'], 'y': bb['y'], 'width': bb['x'] + bb['width'] - sb['x'], 'height': bb['height']})
            await pg.locator('#carte .pt.is-new').first.click(force=True); await pg.wait_for_timeout(1500)
            print('   ouverture d\'un nouveau :', await pg.evaluate('!!document.querySelector(".fiche:not(.fpays)")'))
            await pg.keyboard.press('Escape'); await pg.wait_for_timeout(900)
            await btn.click(); await pg.wait_for_timeout(1800)
            print('   désactivé : estompés', await pg.locator('#carte .pt.is-dim').count(), [e for e in errs if 'Failed' not in e and 'failed to load' not in e])
            await b.close()
asyncio.run(main())
