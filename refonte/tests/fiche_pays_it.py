import asyncio, sys, os
sys.path.insert(0, os.path.join(os.environ.get('OBS_WORK', os.path.expanduser('~/work')), 'tools'))
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, dsf=1.5, path='test_IT.html')
        await pg.wait_for_timeout(2500)
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.evaluate('window.scrollBy(0, 40)'); await pg.wait_for_timeout(2600)
        await pg.locator('.side-pays .row', has_text='Polonia').click(); await pg.wait_for_timeout(2300)
        fb = await pg.locator('.fpays').bounding_box()
        await pg.screenshot(path=f'{ROOT}/shots/v5it_fiche.png', clip={'x': fb['x'], 'y': fb['y'], 'width': fb['width'], 'height': fb['height']})
        print(await pg.evaluate('''() => [...document.querySelectorAll('.fpays span')].filter(e => getComputedStyle(e).textTransform === 'uppercase').map(e => e.textContent.trim())'''))
        print(await pg.evaluate('''() => [...document.querySelectorAll('.lg-types > span')].map(e => e.textContent.trim())'''))
        print([e for e in errs if 'Failed' not in e and 'failed to load' not in e])
        await b.close()
asyncio.run(main())
