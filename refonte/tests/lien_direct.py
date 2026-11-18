import asyncio, sys
sys.path.insert(0, '/home/claude/work/tools')
from pw import *
async def main():
    serve()
    async with async_playwright() as p:
        for path in ('observatoire.html', 'observatoire_test.html'):
            for w, mob in ((1440, False), (390, True)):
                b, pg, errs = await open_page(p, w, 900, dsf=1, path=path + '#EVEN048', mobile=mob)
                await pg.wait_for_timeout(4000)
                print(path, w, 'fiche ouverte :', await pg.evaluate('!!document.querySelector(".fiche:not(.fpays)") || !!document.querySelector("[id^=\\"j-\\"] .jbody, .jopen")'), await pg.evaluate('location.hash'), [e for e in errs if 'Failed' not in e and 'failed to load' not in e and 'mux' not in e.lower()][:2])
                await b.close()
asyncio.run(main())
