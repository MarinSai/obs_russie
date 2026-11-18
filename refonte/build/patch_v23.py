# Passe 23 : accords et élisions dans les trois langues (relecture IT/ES).
# PLW : formes singulier/pluriel par mot ; PL : nombre + forme (FR : pluriel au-delà de 1 ; IT/ES : singulier pour 1 seulement,
# réécrit par build_lang) ; EL : préposition + nombre (FR/ES : simple concaténation ; IT : élision all'/dell'/dall'/gli, réécrite par build_lang).
sub("const DOT = s =>", """const PLW = { pays: [' pays', ' pays'], evt: [' événement', ' événements'], aff: [' événement affiché', ' événements affichés'], affT: ['Événement affiché', 'Événements affichés'], ant: [' fait antérieur au 23 sept.', ' faits antérieurs au 23 sept.'] };
const PL = (n, w) => n + PLW[w][n > 1 ? 1 : 0];
const PLT = (n, w) => PLW[w][n > 1 ? 1 : 0];
const EL = (p, n) => p + n;
const DOT = s =>""")
# libellés « Événements affichés » accordés au nombre affiché
sub('''<span style="font-size: 12px; letter-spacing: .16em; text-transform: uppercase; color: #a3a09a;">Événements affichés</span>''', '''<span style="font-size: 12px; letter-spacing: .16em; text-transform: uppercase; color: #a3a09a;">{{affLbl}}</span>''')
sub('''<span class="fig" style="font-size: 54px; line-height: .86; color: #ea4d62;">{{cf.n}}</span>
              <span style="font-size: 11.5px; letter-spacing: .16em; text-transform: uppercase; color: #a3a09a; padding-bottom: 2px;">Événements affichés</span>''',
    '''<span class="fig" style="font-size: 54px; line-height: .86; color: #ea4d62;">{{cf.n}}</span>
              <span style="font-size: 11.5px; letter-spacing: .16em; text-transform: uppercase; color: #a3a09a; padding-bottom: 2px;">{{cf.aff}}</span>''', n=2)
sub("name: st.country || '', n: String(cfL.length),", "name: st.country || '', n: String(cfL.length), aff: PLT(cfL.length, 'affT'),")
sub('''{{nPays}} pays — {{scope}}</span>''', '''{{paysN}} — {{scope}}</span>''')
sub("    const nPays = new Set(filtered.flatMap(paysOf)).size;", "    const nPays = new Set(filtered.flatMap(paysOf)).size, paysN = PL(nPays, 'pays');")
sub("      vb, mapCities,", "      vb, mapCities, paysN, affLbl: PLT(filtered.length, 'affT'),")
sub("antLine = nPS ? 'dont ' + nPS + ' faits antérieurs au 23 sept.' : '';", "antLine = nPS ? 'dont ' + PL(nPS, 'ant') : '';")
sub("const fbarCount = nShown + (nShown > 1 ? ' événements affichés' : ' événement affiché');", "const fbarCount = PL(nShown, 'aff');")
sub("mapAria: 'Carte des ' + nShown + ' événements',", "mapAria: 'Carte : ' + PL(nShown, 'evt'),")
# deux-points : littéral à part, traduit sans espace en IT/ES
sub("aria: 'Semaine du ' + label + ' : ' + n + ' événements',", "aria: EL('Semaine du ', label) + SEP + PL(n, 'evt'),")
sub("aria: 'Semaine du ' + dateOfDay(weekStartDay(i)).getDate() + ' ' + MOIS[dateOfDay(weekStartDay(i)).getMonth()] + ' : ' + wCounts[i] + ' événements, ' + cv + ' au total',",
    "aria: EL('Semaine du ', dateOfDay(weekStartDay(i)).getDate() + ' ' + MOIS[dateOfDay(weekStartDay(i)).getMonth()]) + SEP + PL(wCounts[i], 'evt') + ', ' + cv + ' au total',")
sub("aria: sl + ', ' + (e.lieu || e.pays) + ' : ' + e.nom,", "aria: sl + ', ' + (e.lieu || e.pays) + SEP + e.nom,")
sub("const EL = (p, n) => p + n;", "const EL = (p, n) => p + n;\nconst SEP = ' : ';")
# élisions (IT) : prépositions suivies d'un nombre
sub("const cumLabel = doneN + ' au ' + String(lastSun.getDate()).padStart(2, '0')", "const cumLabel = doneN + EL(' au ', String(lastSun.getDate()).padStart(2, '0'))")
sub("note: ((a, b) => 'du ' + a.getDate() + (a.getMonth() === b.getMonth() ? '' : ' ' + MOIS[a.getMonth()]) + ' au ' + b.getDate() + ' ' + MOIS[b.getMonth()])",
    "note: ((a, b) => EL('du ', a.getDate()) + (a.getMonth() === b.getMonth() ? '' : ' ' + MOIS[a.getMonth()]) + EL(' au ', b.getDate()) + ' ' + MOIS[b.getMonth()])")
sub("note: totalT ? 'semaine du ' + wLab(wPeak) : 'aucun événement' },", "note: totalT ? EL('semaine du ', wLab(wPeak)) : 'aucun événement' },")
sub("note: 'semaine du ' + wLab(lw) + ' ('", "note: EL('semaine du ', wLab(lw)) + ' ('")
sub("if (st.week !== null) scope = 'semaine du ' + weeks[st.week].label;", "if (st.week !== null) scope = EL('semaine du ', weeks[st.week].label);")
sub("if (st.day !== null) scope = 'au ' + dayLabel + '.' + curDate.getFullYear();", "if (st.day !== null) scope = EL('au ', dayLabel) + '.' + curDate.getFullYear();")
sub("chips.push({ t: 'Semaine du ' + wd.getDate() + ' ' + MOIS[wd.getMonth()],", "chips.push({ t: EL('Semaine du ', wd.getDate()) + ' ' + MOIS[wd.getMonth()],")
sub("chips.push({ t: 'Jusqu’au ' + dd.getDate() + ' ' + MOIS[dd.getMonth()],", "chips.push({ t: EL('Jusqu’au ', dd.getDate()) + ' ' + MOIS[dd.getMonth()],")
sub("moreLabel: st.showAll ? 'Réduire le journal' : 'Afficher les ' + sorted.length + ' événements',", "moreLabel: st.showAll ? 'Réduire le journal' : EL('Afficher les ', sorted.length) + ' événements',")
# indice de zoom avec virgule décimale
sub("'×' + Z.k.toFixed(1) + ' — '", "'×' + Z.k.toFixed(1).replace('.', ',') + ' — '")
