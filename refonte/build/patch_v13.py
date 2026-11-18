# ════════════════════════════════════════════════════════════════════
#  TREIZIÈME PASSE : le premier chiffre clé garde sa phrase d'origine (« documentées depuis le 23 septembre 2026 ») ;
#  la règle des faits antérieurs, reprise de la méthodologie, est donnée dans la fiche de chaque fait antérieur.
#  Texte nouveau (dans i18n_production.py), à la place de « Fait antérieur au 23 septembre 2026. »
# ════════════════════════════════════════════════════════════════════
sub('''padding: 8px 10px; line-height: 1.4;">Fait antérieur au 23 septembre 2026.</span>''',
    '''padding: 8px 10px; line-height: 1.4;">Fait antérieur au 23 septembre 2026, date du début de la veille, intégré parce qu’il a été révélé ou a connu un développement nouveau après cette date.</span>''')

# lien direct #EVEN… : l'adresse n'est effacée que si un événement était réellement ouvert
# (au premier rendu, l'état précédent est inconnu : sur téléphone, l'ancre était effacée avant l'arrivée des données)
sub("    if (prevState && prevState.sel !== this.state.sel) {", "    if (prevState && 'sel' in prevState && prevState.sel !== this.state.sel) {")

# ── Molette : une fois la carte zoomée, elle zoome et dézoome autour du curseur (comme une carte en ligne) ;
#    revenue à la vue d'ensemble, elle fait de nouveau défiler la page. Un défilement latéral (pavé tactile) déplace la carte. ──
sub("""      const z = this.view();
      const pad = ev.deltaMode === 0 && (ev.deltaX !== 0 || Math.abs(ev.deltaY) < 50);
      if (!pad || z.k <= ZMIN + 0.05) return;""",
    """      // un même geste de molette (événements à moins de 350 ms d'intervalle) qui a commencé par zoomer continue de zoomer :
      // arrivé à la vue d'ensemble, il ne se met pas à faire défiler la page ; le geste suivant, lui, la fait défiler
      const z = this.view(), host = ev.currentTarget || {}, t = ev.timeStamp || performance.now();
      const same = host.__wt && t - host.__wt < 350; host.__wt = t;
      if (!same) host.__wzoom = z.k > ZMIN + 0.05;
      if (!host.__wzoom) return;
      if (Math.abs(ev.deltaY) >= Math.abs(ev.deltaX)) {
        ev.preventDefault();
        if (z.k <= ZMIN + 0.05 && ev.deltaY > 0) return;
        this.backZ = null; this.cBack = null;
        const d = Math.max(-25, Math.min(25, ev.deltaY * u)); this.zoomBy(Math.exp(-d * 0.018), fx, fy); return;
      }""")

# ── Bouton de lien : libellé visible ──
sub('''aria-label="Copier le lien" title="Copier le lien" style="{{sel.cplStyle}}">''', '''style="{{sel.cplStyle}}">''')
sub('''<path d="M4.5 12.5l5 5 10-11"></path></svg></sc-if>
            </button>''', '''<path d="M4.5 12.5l5 5 10-11"></path></svg></sc-if>
              <span>Copier le lien de l’événement</span>
            </button>''')
sub("cplStyle: 'align-self:flex-start;display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;box-sizing:border-box;margin-top:2px;padding:0;",
    "cplStyle: 'align-self:flex-start;display:inline-flex;align-items:center;gap:9px;min-height:36px;box-sizing:border-box;margin-top:2px;padding:7px 12px;")
