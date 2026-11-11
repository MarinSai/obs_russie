import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        for f in ('test_IT.html', 'observatoire_test.html'):
            b, pg, errs = await open_page(p, 1440, 900, path=f); await pg.wait_for_timeout(2500)
            print(f, await pg.evaluate('''() => [...document.querySelectorAll('.mlab')].map(e => e.textContent).join(', ')'''))
            print('   ', await pg.evaluate('''() => [document.querySelector('.jmeta').textContent, document.querySelectorAll('#chrono .wd').length, document.querySelectorAll('#chrono > div').length]'''), [e for e in errs if 'Failed' not in e and 'failed to load' not in e])
            await b.close()
asyncio.run(main())
