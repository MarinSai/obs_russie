import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
from PIL import Image
async def strip(pg, sel, name, times, crop=None):
    el = pg.locator(sel).first; bb = await el.bounding_box()
    c = {'x': bb['x'], 'y': bb['y'], 'width': bb['width'], 'height': bb['height']}
    if crop: c = {'x': bb['x'] + crop[0], 'y': bb['y'] + crop[1], 'width': crop[2], 'height': crop[3]}
    ims = []; t = 0
    for ms in times:
        await pg.wait_for_timeout(ms - t); t = ms
        p = f'/tmp/f_{name}_{ms}.png'; await pg.screenshot(path=p, clip=c); ims.append(Image.open(p))
    W = sum(i.width for i in ims) + 8 * (len(ims) - 1); sh = Image.new('RGB', (W, ims[0].height), (60, 60, 60)); x = 0
    for i in ims: sh.paste(i, (x, 0)); x += i.width + 8
    if sh.width > 2400: sh = sh.resize((2400, int(sh.height * 2400 / sh.width)))
    sh.save(f'{ROOT}/shots/seq_{name}.png')
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, path='observatoire_test.html')
        await pg.wait_for_timeout(2600)
        await pg.locator('#carte').scroll_into_view_if_needed()
        await pg.evaluate('window.scrollBy(0, 60)')
        # cascade d'arrivée
        await strip(pg, '#carte', 'cascade', [150, 500, 900, 1500], crop=(250, 150, 760, 560))
        await pg.wait_for_timeout(800)
        # filtre : sorties puis entrées
        await pg.locator('nav .navbtn').nth(0).click()
        await strip(pg, '#carte', 'filtre_sortie', [40, 130, 240, 500], crop=(250, 150, 760, 560))
        await pg.locator('nav .navbtn').nth(0).click()
        await strip(pg, '#carte', 'filtre_entree', [40, 160, 320, 700], crop=(250, 150, 760, 560))
        # ouverture d'un événement : trajet
        await pg.wait_for_timeout(500)
        await pg.locator('#carte .pt').nth(20).click(force=True)
        await strip(pg, '#carte', 'trajet', [90, 300, 520, 760, 1300])
        # infobulle
        await pg.locator('#carte .pt').nth(30).hover(force=True); await pg.wait_for_timeout(300)
        await strip(pg, '#carte', 'infobulle', [50], crop=(0, 0, 760, 600))
        # fermeture : retour
        await pg.keyboard.press('Escape')
        await strip(pg, '#carte', 'retour', [100, 400, 1300])
        # lecture
        await pg.locator('.player button').nth(2).click()
        await strip(pg, '.mapsec', 'lecture', [1200, 1390, 1580, 3000], crop=(250, 150, 880, 800))
        print([e for e in errs if 'Failed to load' not in e and 'resource failed' not in e])
        await b.close()
asyncio.run(main())
