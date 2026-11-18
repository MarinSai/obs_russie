# ════════════════════════════════════════════════════════════════════
#  ONZIÈME PASSE : l'identifiant de l'événement (EVEN…) n'est plus affiché ; le bouton de lien est une icône,
#  nommée « Copier le lien » (texte nouveau, dans i18n_production.py)
# ════════════════════════════════════════════════════════════════════
sub('''<button class="cpl" sc-camel-on-click="{{copyLink}}" aria-label="{{sel.id}}" style="{{sel.cplStyle}}">''',
    '''<button class="cpl" sc-camel-on-click="{{copyLink}}" aria-label="Copier le lien" title="Copier le lien" style="{{sel.cplStyle}}">''')
sub('''              <span>{{sel.id}}</span>
            </button>''', '''            </button>''')
sub("cplStyle: 'align-self:flex-start;display:inline-flex;align-items:center;gap:8px;margin-top:2px;padding:7px 10px;",
    "cplStyle: 'align-self:flex-start;display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;box-sizing:border-box;margin-top:2px;padding:0;")
