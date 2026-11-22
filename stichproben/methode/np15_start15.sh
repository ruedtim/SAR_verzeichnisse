#!/bin/bash
# NP15 Schritt 1 (erst nach «Runde 12 installiert»): Stand sichern, Gesamtlauf, Testdaten, D151210, Zellvergleiche, Fallsets,
# Suchläufe, Prüfmappen und Durchsichtsblöcke. Alles schreibt nur ins Scratchpad; das Projekt wird nur gelesen.
set -u
S=/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad
P=/Users/stazh/Documents/GithubRemops_ruedtim/SAR_verzeichnisse
V=$S/np15
A=$S/np14   # Stand Runde 11
PY=(uv run --quiet --with pdfplumber --with openpyxl python -I)
X=(uv run --quiet --with openpyxl python -I)
mkdir -p $S/neu15 $V/proj_excel $V/proj_test $V/proj_d151
ln -sfn $S/verb2/cache $V/cache
# 1. Skript und Projektstand als Kopie
cp $P/findmittel_zu_scope.py $S/neu15/
shasum -a 256 $S/neu15/findmittel_zu_scope.py | tee $V/skript_sha.txt
cp $P/findmittel_excel/*.xlsx $V/proj_excel/
cp $P/testdaten_excel/*.xlsx $V/proj_test/
cp $P/D151210_scope_import.xlsx $V/proj_d151/
ls $V/proj_excel | wc -l
# 2. Rechnen
sed "s#/np14\$#/np15#" $A/lauf.sh > $V/lauf.sh
cd $V
bash lauf.sh $S/neu15/findmittel_zu_scope.py $V/aus_neu 8 > lauf.log 2>&1
"${PY[@]}" $S/neu15/findmittel_zu_scope.py $P/testdaten/*.pdf -o $V/test_neu --cache $S/verb2/cache_test \
  --katalog $P/findmittel_pdf/verzeichnis.csv > test.log 2>&1
"${PY[@]}" $S/neu15/findmittel_zu_scope.py $P/D151210.pdf -o $V/d151_a --cache $S/verb2/cache_test \
  --katalog $P/findmittel_pdf/verzeichnis.csv > d151.log 2>&1
cat lauf.log; tail -1 test.log; cat d151.log
# 3. Zellvergleiche: Projekt = eigener Lauf? Runde 11 -> Runde 12?
Z=(uv run --quiet --with openpyxl python -I $S/np4/zellen.py)
"${Z[@]}" $V/proj_excel $V/aus_neu $V/z_proj.json
"${Z[@]}" $V/proj_test $V/test_neu $V/z_test.json
"${Z[@]}" $V/proj_d151 $V/d151_a $V/z_d151.json
"${Z[@]}" $A/aus_neu $V/aus_neu $V/z_r11_r12.json
"${Z[@]}" $A/test_neu $V/test_neu $V/z_test_alt.json
"${Z[@]}" $A/d151_a $V/d151_a $V/z_d151_alt.json
for f in z_proj z_test z_d151 z_test_alt z_d151_alt; do echo "$f: $(head -c 300 $V/$f.json)"; done
uv run --quiet python -I -c "import json; z=json.load(open('$V/z_r11_r12.json')); print('Runde 11 -> 12 geändert:', len(z)); open('$V/geaendert_r12.txt','w').write(''.join(d+chr(10) for d in sorted(z)))"
# 4. Fallsets (alt = Runde 11, neu = Runde 12)
F=$P/stichproben/verbesserung/werkzeug/faelle; R=$P/stichproben/verbesserung/runde2/werkzeug
for x in a b c f; do "${PY[@]}" $F/pruefe_faelle.py $F/${x}_faelle.csv $A/aus_neu $V/aus_neu > $V/fall_$x.txt 2>&1; echo "Fallset $x: $(tail -1 $V/fall_$x.txt)"; done
"${PY[@]}" $R/pruefe_runde2.py $R/runde2_faelle.csv $A/aus_neu $V/aus_neu > $V/fall_r2.txt 2>&1; echo "Runde 2: $(tail -1 $V/fall_r2.txt)"
"${PY[@]}" $R/pruefe_runde2.py $R/punkt2_faelle.csv $A/aus_neu $V/aus_neu > $V/fall_p2.txt 2>&1; echo "Punkt 2: $(tail -1 $V/fall_p2.txt)"
# 5. Suchläufe über alle Dateien (Runde 11 als Basis in np14/*_r11.*)
"${PY[@]}" $S/np13/suchlauf_tippfehler.py $V/cache $V/aus_neu $V/tipp_r12.csv
"${PY[@]}" $S/np13/suchlauf_tippfehler.py $S/verb2/cache_test $V/test_neu $V/tipp_test_r12.csv
"${PY[@]}" $A/suchlauf_info_stuecke.py $V/aus_neu $V/info_stuecke_r12.csv
"${PY[@]}" $S/np13/suchlauf_buchstaben_titelspalte.py $V/cache $V/aus_neu $V/buchstaben_titelspalte_r12.csv
"${PY[@]}" $V/suchlauf_gruppenende.py $V/cache $V/aus_neu $V/gruppenende_r12_f1.3.csv 1.3
"${PY[@]}" $V/suchlauf_gruppenende.py $V/cache $V/aus_neu $V/gruppenende_r12_f1.0.csv 1.0
"${PY[@]}" $A/suchlauf_nummern_im_darin.py $V/cache $V/aus_neu $V/nummern_im_darin_r12.csv
"${X[@]}" $A/suchlauf_na_kind.py $V/aus_neu > $V/na_kind_r12.txt
# 6. Prüfmappen aller 715 Dateien: Runde-11-Mappen übernehmen, geänderte Dateien neu
rm -rf $V/mappen_r12; cp -R $V/mappen_r11 $V/mappen_r12
if [ -s $V/geaendert_r12.txt ]; then "${X[@]}" $S/np12/pruefmappe.py $V/cache $V/aus_neu $V/mappen_r12 $(cat $V/geaendert_r12.txt) > $V/mappen_r12.log 2>&1; fi
"${X[@]}" $V/durchsicht_schluss_info.py $V/aus_neu $V/mappen_r12 $V/durchsicht_r12 8
echo "fertig"
