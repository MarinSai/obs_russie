import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main(w, mob):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width': w, 'height': 900}, is_mobile=mob, has_touch=mob)
        await route(ctx); pg = await ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/parent.html'); await pg.wait_for_timeout(5000)
        fr = pg.frames[1]
        async def H():
            return await pg.evaluate('document.getElementById("f").getBoundingClientRect().height'), await fr.evaluate('Math.ceil(document.querySelector("[data-document-role=page]").getBoundingClientRect().bottom)'), await fr.evaluate('innerHeight')
        st = lambda: fr.evaluate('''() => ({kf: document.querySelector('.kfg').className, kfTxt: document.querySelector('.kfg [data-n]').textContent, carte: document.getElementById('carte').className, bars: document.querySelector('[data-rv=bars]').className, heads: [...document.querySelectorAll('header[data-rv]')].map(h => h.className).join('|')})''')
        print(w, 'hauteurs (iframe, contenu, fenêtre interne):', await H())
        print('  en haut de page   :', await st())
        y = await pg.evaluate('document.getElementById("f").offsetTop')
        await pg.evaluate(f'window.scrollTo(0, {y + 500})'); await pg.wait_for_timeout(1800)
        print('  parent défilé +500:', await st())
        await pg.evaluate(f'window.scrollTo(0, {y + 1200})'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{ROOT}/shots/iframe_{w}_cascade.png')
        await pg.wait_for_timeout(1800)
        for yy in range(y + 1200, y + 6500, 600):
            await pg.evaluate(f'window.scrollTo(0, {yy})'); await pg.wait_for_timeout(350)
        await pg.wait_for_timeout(1200)
        print('  bas de page       :', await st())
        h0 = await H()
        await fr.locator('#journal .row').nth(1).click(); await pg.wait_for_timeout(1200); h1 = await H()
        await fr.locator('#journal .row').nth(3).click(); await pg.wait_for_timeout(1200); h2 = await H()
        await fr.locator('#journal .row').nth(3).click(); await pg.wait_for_timeout(1200); h3 = await H()
        await fr.locator('#methode > button').click(); await pg.wait_for_timeout(1500); h4 = await H()
        await fr.locator('#methode > button').click(); await pg.wait_for_timeout(1500); h5 = await H()
        print('  journal ouvert/changé/fermé, méthodo ouverte/fermée :', h0[:2], h1[:2], h2[:2], h3[:2], h4[:2], h5[:2])
        print('  volets restants :', await fr.evaluate('document.querySelectorAll("#journal .acc").length'), 'erreurs', errs)
        await b.close()
serve()
asyncio.run(main(1440, False)); asyncio.run(main(390, True))
