import asyncio, sys, os
sys.path.insert(0, os.path.join(os.environ.get('OBS_WORK', os.path.expanduser('~/work')), 'tools'))
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        for i in range(14):
            b, pg, errs = await open_page(p, 1440, 1000, path='observatoire_test.html')
            await pg.wait_for_timeout(3000 + (i % 4) * 400)
            await pg.evaluate('''() => { window.__log = []; document.addEventListener('click', e => window.__log.push('click:' + e.target.tagName + '.' + (e.target.className.baseVal ?? e.target.className) + ' k=' + (e.target.closest('.pt') ? e.target.closest('.pt').getAttribute('data-k') : '-')), true); }''')
            el = pg.locator('#carte .pt').nth(20)
            await el.scroll_into_view_if_needed()
            k0 = await el.get_attribute('data-k')
            pre = await pg.evaluate('''() => { const el = document.querySelectorAll('#carte .pt')[20], r = el.getBoundingClientRect(); const cx = r.left + r.width / 2, cy = r.top + r.height / 2; const t = document.elementFromPoint(cx, cy); return {box: [r.left, r.top, r.width, r.height].map(v => +v.toFixed(1)), hit: t ? t.tagName + '.' + (t.className.baseVal ?? t.className) : null, anims: el.getAnimations().map(a => a.playState + ':' + Object.keys(a.effect.getKeyframes()[0]).filter(k => !['offset','easing','composite','computedOffset'].includes(k)).join('+')), y: scrollY, carteCls: document.getElementById('carte').className}; }''')
            await el.click(force=True)
            await pg.wait_for_timeout(900)
            r = await pg.evaluate('''() => ({fiche: !!document.querySelector('.fiche'), log: window.__log, hash: location.hash})''')
            print(i, r['fiche'], r['log'], pre, [e for e in errs if 'Failed' not in e and 'failed to load' not in e])
            await b.close()
asyncio.run(main())
