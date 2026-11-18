#!/bin/sh
# Simule le commit de passage en production et l'automatisation « build-lang » de GitHub, sans rien pousser.
set -e
rm -rf /tmp/sim && git clone -q /home/claude/obs_russie /tmp/sim
cp /home/claude/work/site/observatoire_test.html /tmp/sim/observatoire.html
cp /home/claude/work/build/i18n/i18n.py /home/claude/work/build/i18n/build_lang.py /tmp/sim/scripts/
cd /tmp/sim && python3 scripts/build_lang.py
git diff --stat -- observatoire_russie_IT.html observatoire_russie_ES.html
