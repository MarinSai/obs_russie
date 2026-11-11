import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        for h in (660, 760):
            b, pg, errs = await open_page(p, 393, h, dsf=2, path='observatoire_test.html', mobile=True)
            await pg.wait_for_timeout(2500)
            st = lambda: pg.evaluate('(() => { const k = document.querySelector(".kfg"); return [Math.round(k.getBoundingClientRect().top), getComputedStyle(k).opacity]; })()')
            a = await st()
            for dy in (60, 120, 200, 300):
                await pg.evaluate(f'scrollTo(0,{dy})'); await pg.wait_for_timeout(400)
                if (await st())[1] != '0': break
            print('fenêtre', h, ': au chargement', a, '→ visible après', dy, 'px', await st())
            await b.close()
        b, pg, errs = await open_page(p, 1440, 900, path='observatoire_test.html'); await pg.wait_for_timeout(3000)
        print('ordinateur :', await pg.evaluate('getComputedStyle(document.querySelector(".kfg")).opacity'), await pg.evaluate('Math.round(document.querySelector(".kfg").getBoundingClientRect().top)'))
        await pg.evaluate('scrollTo(0,300)'); await pg.wait_for_timeout(800); print('après 300 px :', await pg.evaluate('getComputedStyle(document.querySelector(".kfg")).opacity'))
        await b.close()
asyncio.run(main())
