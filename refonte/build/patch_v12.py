# ════════════════════════════════════════════════════════════════════
#  DOUZIÈME PASSE : nouveau titre « Observatoire de la guerre politique en Europe »
#  (IT : « Osservatorio della guerra politica in Europa » ; ES : « Observatorio de la guerra política en Europa »)
#  Au passage en production, build_lang.py et i18n.py doivent suivre : voir refonte/i18n/.
#  La méthodologie (contenu éditorial) garde ses mentions de « guerre russe » : non modifiée.
# ════════════════════════════════════════════════════════════════════
sub("<title>Observatoire de la guerre russe en Europe</title>", "<title>Observatoire de la guerre politique en Europe</title>")
sub("const T1 = 'Observatoire de la guerre russe';", "const T1 = 'Observatoire de la guerre politique';")
sub('''sr-only">Observatoire de la guerre russe en Europe<''', '''sr-only">Observatoire de la guerre politique en Europe<''')
# titre plus long : même gabarit que les versions italienne et espagnole (un peu plus large, un peu plus petit)
sub("font-size: clamp(64px, 11vw, 176px); line-height: .94; letter-spacing: -.03em; max-width: 11ch;",
    "font-size: clamp(54px, 8.6vw, 138px); line-height: .94; letter-spacing: -.03em; max-width: 13.5ch;")
