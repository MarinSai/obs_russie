# Passe 18 : « Passer la chronologie », intertitre de la chronologie par jour, noms de pays traduits sur la carte (via i18n.JS).
sub('      <div class="chr-sc" id="chr-sc">', '      <button class="skip" sc-camel-on-click="{{skipChr}}">Passer la chronologie</button>\n      <div class="chr-sc" id="chr-sc">')
sub('      <div style="{{weekGrid}}">', '      <div id="sk-wk" tabindex="-1" style="{{weekGrid}}">')
sub("skipMap: () => {", "skipChr: () => { const el = document.getElementById('sk-wk'); if (el) el.focus(); }, skipMap: () => {")
sub(">Événements par semaine<", ">Événements par jour<")
