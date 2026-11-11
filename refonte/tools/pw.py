"""Outils communs : serveur local + navigateur avec données locales."""
import asyncio, json, os, re, http.server, socketserver, threading, functools
from playwright.async_api import async_playwright
ROOT = os.environ.get('OBS_WORK', os.path.expanduser('~/work'))
DATA = open(os.path.join(ROOT, 'data/observatoire-data.json'), 'rb').read()
PNG1 = bytes.fromhex('89504e470d0a1a0a0000000d4948445200000001000000010806000000'
                     '1f15c4890000000d49444154789c6360606060000000050001a5f645400000000049454e44ae426082')
def serve(port=8765):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=os.path.join(ROOT, 'site'))
    class Q(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=os.path.join(ROOT, 'site'), **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv
async def route(ctx, log=None):
    async def handler(r):
        u = r.request.url
        if u.startswith('http://127.0.0.1') or u.startswith('http://localhost'): return await r.continue_()
        if 'observatoire-data-it' in u: return await r.fulfill(status=200, content_type='application/json', body=open(ROOT + '/repo/obs_russie/observatoire-data-it.json','rb').read(), headers={'access-control-allow-origin': '*'})
        if 'observatoire-data' in u:
            return await r.fulfill(status=200, content_type='application/json', body=DATA, headers={'access-control-allow-origin': '*'})
        if log is not None: log.append(u)
        if re.search(r'\.(jpg|jpeg|png|webp)(\?|$)', u) or 'image.mux.com' in u:
            return await r.fulfill(status=200, content_type='image/png', body=PNG1)
        return await r.abort()
    await ctx.route('**/*', handler)
async def open_page(p, width, height=900, dsf=1, path='observatoire.html', reduce=False, log=None, mobile=False):
    b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    ctx = await b.new_context(viewport={'width': width, 'height': height}, device_scale_factor=dsf,
                              reduced_motion='reduce' if reduce else 'no-preference', is_mobile=mobile, has_touch=mobile)
    await route(ctx, log)
    pg = await ctx.new_page()
    errs = []
    pg.on('console', lambda m: errs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    await pg.goto('http://127.0.0.1:8765/' + path)
    await pg.wait_for_selector('.pt', timeout=20000)
    return b, pg, errs
