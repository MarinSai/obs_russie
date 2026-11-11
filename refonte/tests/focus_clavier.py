import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, path='observatoire_test.html')
        await pg.wait_for_timeout(3000)
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(2500)
        # 1. Entrée sur un hexagone : où est le focus ensuite ?
        res = []
        for i in (5, 20, 40):
            el = pg.locator('#carte .pt').nth(i); await el.focus(); lab = await el.get_attribute('aria-label')
            await pg.keyboard.press('Enter'); await pg.wait_for_timeout(1800)
            act = await pg.evaluate('''() => { const a = document.activeElement; return a ? (a.tagName + ' | ' + (a.getAttribute('aria-label') || '').slice(0, 50)) : null; }''')
            res.append((lab[:50], act)); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(1500)
        for r in res: print('Entrée sur', r[0], '→ focus :', r[1])
        # 2. Carte zoomée + focus sur un hexagone hors cadre : défilement interne de #carte ?
        await pg.locator('button[aria-label="Zoomer"]').click(); await pg.wait_for_timeout(700); await pg.locator('button[aria-label="Zoomer"]').click(); await pg.wait_for_timeout(900)
        out = await pg.evaluate('''() => { const c = document.getElementById('carte').getBoundingClientRect(); return [...document.querySelectorAll('#carte .pt')].map((e, i) => [i, e.getBoundingClientRect()]).filter(([i, r]) => r.right < c.left || r.left > c.right || r.bottom < c.top || r.top > c.bottom).map(x => x[0]); }''')
        print('hexagones hors cadre mais présents :', len(out))
        if out:
            await pg.locator('#carte .pt').nth(out[0]).focus(); await pg.wait_for_timeout(500)
            print('défilement interne de #carte après focus :', await pg.evaluate('''() => { const c = document.getElementById('carte'); return [c.scrollLeft, c.scrollTop, getComputedStyle(c).overflow]; }'''))
        # 3. Glitch du titre : s'arrête-t-il ?
        await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(1500)
        n = await pg.evaluate('''() => new Promise(res => { let n = 0; const h = document.getElementById('hero') || document.body; const mo = new MutationObserver(m => { n += m.length; }); mo.observe(h, { subtree: true, attributes: true, childList: true, characterData: true }); setTimeout(() => { mo.disconnect(); res(n); }, 8000); })''')
        print('changements dans le bandeau de titre en 8 s (page en haut) :', n)
        await b.close()
asyncio.run(main())
