import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
from PIL import Image
async def main(path, tag):
    serve()
    async with async_playwright() as p:
        for w, mob in ((1440, False), (390, True)):
            b, pg, errs = await open_page(p, w, 900 if not mob else 844, dsf=1 if not mob else 2, path=path, mobile=mob)
            await pg.wait_for_timeout(3500)
            h = await pg.evaluate('document.documentElement.scrollHeight')
            for y in range(0, h, 500):
                await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(350)
            await pg.wait_for_timeout(1800)
            await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(500)
            h = await pg.evaluate('document.documentElement.scrollHeight')
            out = f'{ROOT}/shots/{tag}_{w}_full.png'
            await pg.screenshot(path=out, full_page=True)
            print(w, 'height', h, 'errors', errs[:6])
            im = Image.open(out); W, H = im.size; step = 1300 * (2 if mob else 1)
            for i, y in enumerate(range(0, H, step)):
                im.crop((0, y, W, min(H, y + step))).save(f'{ROOT}/shots/{tag}_{w}_{i:02d}.png')
            await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
