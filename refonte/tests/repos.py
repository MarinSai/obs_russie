import asyncio, sys, os
sys.path.insert(0, os.path.join(os.environ.get('OBS_WORK', os.path.expanduser('~/work')), 'tools'))
from pw import *
async def main(path):
    serve()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p, 1440, 1000, path=path)
        cdp = await pg.context.new_cdp_session(pg); await cdp.send('Performance.enable')
        await pg.wait_for_timeout(3000)
        await pg.locator('#carte').scroll_into_view_if_needed(); await pg.wait_for_timeout(3000)
        async def m():
            r = await cdp.send('Performance.getMetrics'); return {x['name']: x['value'] for x in r['metrics']}
        a = await m(); await pg.wait_for_timeout(4000); c = await m()
        print(path, {k: round(c[k] - a[k], 3) for k in ('LayoutCount', 'RecalcStyleCount', 'LayoutDuration', 'RecalcStyleDuration', 'ScriptDuration', 'TaskDuration')})
        print('   animations en cours:', await pg.evaluate('''() => { const m = {}; document.getAnimations().forEach(a => { if (a.playState !== 'running') return; const k = (a.animationName || a.transitionProperty || 'waapi') + '@' + (a.effect.target ? a.effect.target.className : ''); m[k] = (m[k] || 0) + 1; }); return m; }'''))
        await b.close()
asyncio.run(main(sys.argv[1]))
