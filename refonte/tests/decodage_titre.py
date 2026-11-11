import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 393, 760, dsf=2, path='observatoire_test.html', mobile=True, wait=False) if False else await open_page(p, 393, 760, dsf=2, path='observatoire_test.html', mobile=True)
        await b.close()
        # suivre le décodage dès le chargement
        br = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = await br.new_context(viewport={'width': 393, 'height': 760}, device_scale_factor=2, is_mobile=True, has_touch=True); await route(ctx)
        pg = await ctx.new_page(); E = []; pg.on('pageerror', lambda e: E.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/observatoire_test.html')
        S = []
        for i in range(40):
            S.append(await pg.evaluate('''() => { const h = document.querySelector('h1.glitch'); if (!h) return null; const o = h.querySelector('.tscr'); const lead = document.querySelector('.hlead'); return [h.classList.contains('dec'), Math.round(h.getBoundingClientRect().height), lead ? Math.round(lead.getBoundingClientRect().top) : null, o && o.textContent ? Math.round(Math.max(...[...o.getClientRects()].map(r => r.right))) : null, document.documentElement.scrollWidth]; }'''))
            if i == 12: await pg.screenshot(path=f'{ROOT}/shots/v10_decode.png')
            await pg.wait_for_timeout(80)
        S = [s for s in S if s]
        print('pendant le décodage : hauteur titre', sorted(set(s[1] for s in S)), '| position du constat', sorted(set(s[2] for s in S)), '| largeur page', sorted(set(s[4] for s in S)), '| décodage vu', sum(1 for s in S if s[0]), 'fois')
        print('erreurs', E); await br.close()
asyncio.run(main())
