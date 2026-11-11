import asyncio, sys, os
sys.path.insert(0, os.path.join(os.environ.get('OBS_WORK', os.path.expanduser('~/work')), 'tools'))
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, dsf=2, path='observatoire_test.html')
        await pg.context.grant_permissions(['clipboard-read', 'clipboard-write'])
        await pg.wait_for_timeout(2500)
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.evaluate('window.scrollBy(0, 40)'); await pg.wait_for_timeout(2600)
        bb = await pg.locator('#carte').bounding_box(); cl = {'x': bb['x'], 'y': bb['y'], 'width': bb['width'], 'height': bb['height']}
        await pg.screenshot(path=f'{ROOT}/shots/v4_carte.png', clip=cl)
        await pg.screenshot(path=f'{ROOT}/shots/v4_hex.png', clip={'x': bb['x'] + 640, 'y': bb['y'] + 330, 'width': 420, 'height': 330})
        await pg.locator('#carte .pt').nth(20).click(force=True); await pg.wait_for_timeout(1700)
        await pg.screenshot(path=f'{ROOT}/shots/v4_zoom.png', clip=cl)
        await pg.locator('.cpl').click(); await pg.wait_for_timeout(300)
        print('lien copié :', await pg.evaluate('navigator.clipboard.readText()'), '| état :', await pg.evaluate('document.querySelector(".cpl").textContent.trim()'))
        # clic sur la carte de situation
        mb = await pg.locator('.mini').bounding_box(); await pg.mouse.click(mb['x'] + mb['width'] * .3, mb['y'] + mb['height'] * .45); await pg.wait_for_timeout(1300)
        await pg.screenshot(path=f'{ROOT}/shots/v4_mini.png', clip=cl)
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(600)
        await pg.locator('button[aria-label="Revenir à la vue d\'ensemble"]').click(); await pg.wait_for_timeout(1400)
        y = await pg.evaluate('document.getElementById("chrono").getBoundingClientRect().top + scrollY'); await pg.evaluate(f'window.scrollTo(0, {y - 300})'); await pg.wait_for_timeout(3800)
        await pg.screenshot(path=f'{ROOT}/shots/v4_chrono.png', clip={'x': 0, 'y': 230, 'width': 1440, 'height': 300})
        print([e for e in errs if 'Failed' not in e and 'failed to load' not in e])
        await b.close()
asyncio.run(main())
