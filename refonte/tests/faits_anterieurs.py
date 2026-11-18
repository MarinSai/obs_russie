import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        for path in ('observatoire_test.html', 'test_IT.html', 'test_ES.html'):
            b, pg, errs = await open_page(p, 1440, 1000, dsf=1.5, path=path)
            await pg.wait_for_timeout(2500)
            await pg.evaluate('scrollTo(0, 700)'); await pg.wait_for_timeout(1500)
            kf = await pg.evaluate('[...document.querySelectorAll(".kfc")].slice(0,4).map(e => e.innerText.replace(/\\s+/g, " ").slice(0, 140))')
            await pg.locator('#carte').scroll_into_view_if_needed(); await pg.evaluate('scrollBy(0,40)'); await pg.wait_for_timeout(2500)
            side = await pg.evaluate('document.querySelector(".side").innerText.split("\\n").slice(0,5).join(" | ")')
            print(path, kf[0], '||', kf[1][:40], '||', kf[2][:40]); print('   panneau :', side, '| case :', await pg.locator('#passe').count(), '| filtre actif :', await pg.locator('.fbar').count(), '| hexagones', await pg.locator('#carte .pt').count())
            if path == 'observatoire_test.html':
                bb = await pg.locator('#carte').bounding_box(); sb = await pg.locator('.side').bounding_box()
                await pg.screenshot(path=f'{ROOT}/shots/v13_carte.png', clip={'x': sb['x'], 'y': bb['y'], 'width': bb['x'] + bb['width'] - sb['x'], 'height': bb['height'] + 80})
                # Rejouer : les antérieurs restent visibles au 1er jour
                await pg.locator('.player button').nth(0).click(); await pg.wait_for_timeout(900)
                print('   Rejouer, premier jour :', await pg.locator('#carte .pt').count(), 'hexagones')
                await pg.locator('.player button').nth(4).click(); await pg.wait_for_timeout(900)
                # journal : mention sur un fait antérieur
                y = await pg.evaluate('document.querySelector(".jrow").getBoundingClientRect().top + scrollY')
                tags = await pg.evaluate('[...document.querySelectorAll(".jmeta")].filter(m => m.innerText.includes("ANTÉRIEUR") || m.innerText.toLowerCase().includes("antérieur")).length')
                print('   journal, mentions « antérieur » visibles :', tags)
                await pg.locator('.side-pays .row', has_text='Pologne').click(); await pg.wait_for_timeout(1800)
                print('   panneau Pologne :', await pg.evaluate('document.querySelector(".side").innerText.split("\\n").slice(0,3).join(" | ")'))
                await pg.locator('.side-pays .lnk, .side-reset button').first.click(); await pg.wait_for_timeout(1200)
                print('   après réinitialisation :', await pg.locator('#carte .pt').count(), 'hexagones')
            print('   erreurs', [e for e in errs if 'Failed' not in e and 'failed to load' not in e and 'mux' not in e])
            await b.close()
asyncio.run(main())
