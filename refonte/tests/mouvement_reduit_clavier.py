import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 900, path='observatoire_test.html', reduce=True)
        await pg.wait_for_timeout(2500)
        print('mouvement réduit :', await pg.evaluate('''() => ({pre: document.querySelectorAll('.rv-pre').length, kf: [...document.querySelectorAll('.kfg [data-n]')].map(e => e.textContent).join(' '), total: document.querySelector('.side-count [data-n]').textContent, anims: document.getAnimations().length})'''))
        await pg.locator('nav .navbtn').nth(2).click(); await pg.wait_for_timeout(150)
        print('  après filtre :', await pg.evaluate('''() => ({total: document.querySelector('.side-count [data-n]').textContent, fx: document.getElementById('fx').children.length, anims: document.getAnimations().filter(a => a.playState === 'running').length})'''))
        await b.close()
        b, pg, errs = await open_page(p, 1440, 900, path='observatoire_test.html')
        await pg.wait_for_timeout(2500)
        # clavier : curseur de lecture
        await pg.locator('#day-range').focus(); await pg.keyboard.press('ArrowLeft'); await pg.keyboard.press('ArrowLeft'); await pg.wait_for_timeout(500)
        print('curseur au clavier :', await pg.evaluate('''() => ({val: document.getElementById('day-range').value, p: document.querySelector('.trk').style.getPropertyValue('--p'), lab: document.querySelector('.player').lastElementChild.textContent})'''))
        await pg.locator('.trk').scroll_into_view_if_needed(); bb = await pg.locator('.player').bounding_box()
        await pg.screenshot(path=f'{ROOT}/shots/apres_focus_player.png', clip={'x': bb['x'] - 8, 'y': bb['y'] - 10, 'width': bb['width'] + 16, 'height': bb['height'] + 20})
        # clic au milieu de la piste
        tb = await pg.locator('.trk').bounding_box(); await pg.mouse.click(tb['x'] + tb['width'] * .5, tb['y'] + tb['height'] / 2); await pg.wait_for_timeout(400)
        print('clic au milieu :', await pg.evaluate('''() => document.getElementById('day-range').value + ' / ' + document.getElementById('day-range').max'''))
        # focus clavier sur un hexagone de la chronologie + infobulle
        await pg.locator('.wd').nth(3).focus(); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(300)
        bb = await pg.locator('[data-rv=bars]').bounding_box()
        await pg.evaluate('window.scrollBy(0,-200)'); await pg.wait_for_timeout(600); bb = await pg.locator('[data-rv=bars]').bounding_box()
        await pg.screenshot(path=f'{ROOT}/shots/apres_focus_chrono.png', clip={'x': 0, 'y': max(0, bb['y'] - 90), 'width': 700, 'height': bb['height'] + 100})
        print('infobulle au clavier :', await pg.evaluate('document.getElementById("gctip").className'))
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(1500)
        print('ouverture au clavier :', await pg.evaluate('!!document.querySelector(".fiche")'))
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
        print('Échap ferme :', await pg.evaluate('!document.querySelector(".fiche")'), [e for e in errs if 'Failed' not in e and 'failed to load' not in e])
        await b.close()
asyncio.run(main())
