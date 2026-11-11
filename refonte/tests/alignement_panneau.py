import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        for w in (390, 1440):
            b, pg, errs = await open_page(p, w, 900, path='observatoire_test.html', mobile=w < 500)
            await pg.wait_for_timeout(2500)
            print(w, await pg.evaluate('''() => { const L = s => { const e = document.querySelector(s); if (!e) return null; const r = document.createRange(); r.selectNodeContents(e); return Math.round(r.getBoundingClientRect().left * 10) / 10; };
              const t = n => [...document.querySelectorAll(n)].map(e => { const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let x; while ((x = w.nextNode())) if (x.textContent.trim()) { const r = document.createRange(); r.selectNodeContents(x); return Math.round(r.getBoundingClientRect().left * 10) / 10; } return null; });
              return { titreSeuil: t('.side-seuils>span')[0], hexSeuil: Math.round(document.querySelector('.side-seuils .row .hx').getBoundingClientRect().left * 10) / 10, case: Math.round(document.querySelector('#passe').getBoundingClientRect().left * 10) / 10, titrePays: t('.side-pays>div>span')[0], pays: t('.side-pays .row')[0] }; }'''))
            await b.close()
asyncio.run(main())
