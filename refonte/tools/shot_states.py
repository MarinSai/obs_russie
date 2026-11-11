import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def clip(pg, sel, out, pad=10):
    el = pg.locator(sel).first
    await el.scroll_into_view_if_needed()
    await pg.wait_for_timeout(250)
    bb = await el.bounding_box()
    vp = pg.viewport_size
    await pg.screenshot(path=out, clip={'x': max(0, bb['x'] - pad), 'y': max(0, bb['y'] - pad), 'width': min(vp['width'], bb['width'] + 2 * pad), 'height': min(1400, bb['height'] + 2 * pad)})
async def main(path, tag):
    serve()
    async with async_playwright() as p:
        for w, mob in ((1440, False), (390, True)):
            b, pg, errs = await open_page(p, w, 1000 if not mob else 844, dsf=1 if not mob else 2, path=path, mobile=mob)
            await pg.wait_for_timeout(3000)
            S = f'{ROOT}/shots/{tag}_{w}_'
            # fiche ouverte
            await pg.locator('#carte .pt').nth(20).scroll_into_view_if_needed()
            await pg.locator('#carte .pt').nth(20).click(force=True)
            await pg.wait_for_timeout(900)
            await clip(pg, '#carte', S + 'fiche.png')
            await pg.locator('button[aria-label="Fermer le détail"]').click()
            # filtre : sabotages
            await pg.locator('nav .navbtn').nth(2).click()
            await pg.wait_for_timeout(900)
            await pg.locator('nav').first.scroll_into_view_if_needed()
            await pg.evaluate('window.scrollBy(0,-20)')
            await pg.wait_for_timeout(200)
            await pg.screenshot(path=S + 'filtre.png')
            await pg.locator('nav .navbtn').nth(2).click()
            # lecture
            await pg.locator('.player button').nth(2).click()
            await pg.wait_for_timeout(4200)
            await clip(pg, '.mapsec', S + 'lecture.png')
            await pg.locator('.player button').nth(2).click()
            await pg.locator('.player button').nth(4).click()
            # journal ouvert
            await pg.locator('#journal .row').nth(1).click()
            await pg.wait_for_timeout(700)
            await clip(pg, '#journal', S + 'journal.png')
            # méthodologie
            await pg.locator('#methode > button').click()
            await pg.wait_for_timeout(700)
            await clip(pg, '#methode', S + 'methode.png')
            if not mob:
                await pg.locator('nav .navbtn').nth(1).hover(); await pg.wait_for_timeout(300)
                await clip(pg, 'nav', S + 'hover_nav.png')
                await pg.keyboard.press('Tab'); await pg.keyboard.press('Tab')
                await pg.locator('.side-seuils .row').nth(1).focus()
                await pg.keyboard.press('Tab'); await pg.wait_for_timeout(200)
                await clip(pg, '.side', S + 'focus_side.png')
            print(w, errs[:4])
            await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
