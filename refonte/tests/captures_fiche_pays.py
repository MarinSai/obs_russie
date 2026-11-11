import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, dsf=1.5, path=sys.argv[1] if len(sys.argv) > 1 else 'observatoire_test.html')
        await pg.wait_for_timeout(2500)
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.evaluate('window.scrollBy(0, 40)'); await pg.wait_for_timeout(2600)
        bb = await pg.locator('#carte').bounding_box(); cl = {'x': bb['x'], 'y': bb['y'], 'width': bb['width'], 'height': bb['height']}
        for name in ('Pologne', 'Roumanie', 'Lettonie'):
            await pg.locator('.side-pays .row', has_text=name).click(); await pg.wait_for_timeout(2300)
            await pg.screenshot(path=f'{ROOT}/shots/v5_{name}.png', clip=cl)
        print('fiche pays :', await pg.evaluate('''() => { const f = document.querySelector('.fpays'); return f ? [f.scrollHeight, f.clientHeight, f.querySelectorAll('.fj').length] : null; }'''))
        # ouvrir un événement depuis le journal de la fiche pays, puis fermer : retour à la fiche pays
        await pg.locator('.fpays .fj').first.click(); await pg.wait_for_timeout(1800)
        print('événement ouvert :', await pg.evaluate('''() => [!!document.querySelector('.fiche:not(.fpays)'), !!document.querySelector('.fpays')]'''))
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(1500)
        print('retour fiche pays :', await pg.evaluate('''() => [!!document.querySelector('.fiche:not(.fpays)'), !!document.querySelector('.fpays')]'''))
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(600)
        print('Échap ferme la fiche pays :', await pg.evaluate('''() => !document.querySelector('.fpays')'''))
        await pg.locator('.side-pays .lnk').click(); await pg.wait_for_timeout(1800)
        # légendes
        lg = await pg.locator('.lg-types').bounding_box()
        await pg.screenshot(path=f'{ROOT}/shots/v5_legende.png', clip={'x': lg['x'] - 10, 'y': lg['y'] - 40, 'width': lg['width'] + 20, 'height': 110})
        sb = await pg.locator('.side-seuils').bounding_box()
        await pg.screenshot(path=f'{ROOT}/shots/v5_seuils.png', clip={'x': sb['x'] - 10, 'y': sb['y'] - 10, 'width': sb['width'] + 20, 'height': sb['height'] + 20})
        print([e for e in errs if 'Failed' not in e and 'failed to load' not in e])
        await b.close()
        b, pg, errs = await open_page(p, 390, 800, dsf=2, path=sys.argv[1] if len(sys.argv) > 1 else 'observatoire_test.html', mobile=True)
        await pg.wait_for_timeout(2500)
        await pg.locator('.side-pays').scroll_into_view_if_needed(); await pg.wait_for_timeout(1500)
        await pg.locator('.side-pays .row', has_text='Pologne').click(); await pg.wait_for_timeout(2000)
        await pg.locator('.fpays').scroll_into_view_if_needed(); await pg.wait_for_timeout(600)
        fb = await pg.locator('.side-pays').bounding_box()
        await pg.screenshot(path=f'{ROOT}/shots/v5_mobile.png', full_page=True, clip={'x': 0, 'y': fb['y'] + await pg.evaluate('scrollY') - 10, 'width': 390, 'height': fb['height'] + 20})
        lg = await pg.locator('.lg-types').bounding_box()
        await pg.screenshot(path=f'{ROOT}/shots/v5_mobile_legende.png', full_page=True, clip={'x': 0, 'y': lg['y'] + await pg.evaluate('scrollY') - 60, 'width': 390, 'height': lg['height'] + 130})
        print('mobile largeur page :', await pg.evaluate('document.documentElement.scrollWidth'), [e for e in errs if 'Failed' not in e and 'failed to load' not in e])
        await b.close()
asyncio.run(main())
