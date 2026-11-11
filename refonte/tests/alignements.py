import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 390, 800, path='observatoire_test.html', mobile=True)
        await pg.wait_for_timeout(2500)
        H = await pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0, H, 600): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(150)
        await pg.locator('label:has-text("Faits antérieurs") input').first.check(); await pg.wait_for_timeout(1200)
        await pg.locator('.jrow').first.click(); await pg.wait_for_timeout(1200)
        res = await pg.evaluate('''() => { const out = {}; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let x;
          while ((x = w.nextNode())) { const t = x.textContent.trim(); if (!t) continue; const el = x.parentElement; if (el.closest('#carte,#hero,.sr-only,#chr-sc,#carrousel,script,style,[aria-hidden=true]')) continue;
            const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
            const r = document.createRange(); r.selectNodeContents(x); const b = r.getClientRects()[0]; if (!b || !b.width) continue;
            const L = Math.round(b.left); if (L > 4 && L < 44 && L !== 16) { const k = L + ''; (out[k] = out[k] || []).push(t.slice(0, 40)); } }
          return out; }''')
        for k in sorted(res, key=int): print(k, len(res[k]), res[k][:6])
        await b.close()
asyncio.run(main())
