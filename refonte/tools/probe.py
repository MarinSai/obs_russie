import asyncio, sys, os
sys.path.insert(0, os.path.join(os.environ.get('OBS_WORK', os.path.expanduser('~/work')), 'tools'))
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 900, path=sys.argv[1])
        await pg.wait_for_timeout(2500)
        print(await pg.evaluate('''() => { const W = innerWidth; const out = []; document.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect(); if (r.right > W + 2 && r.width > 0) out.push(el.tagName + '#' + el.id + '.' + (el.className.baseVal ?? el.className) + ' ' + Math.round(r.left) + '→' + Math.round(r.right)); }); return [document.documentElement.scrollWidth, out.slice(0, 25)]; }'''))
        await b.close()
asyncio.run(main())
