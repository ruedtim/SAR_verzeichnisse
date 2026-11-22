#!/bin/bash
# NP13 Schritt 1 (erst nach «Runde 10 installiert»): Stand sichern, Gesamtlauf, Testdaten, D151210, Vergleiche, Fallsets,
# Suchlauf Tippfehler. Alles schreibt nur ins Scratchpad; das Projekt wird nur gelesen.
set -u
S=/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad
P=/Users/stazh/Documents/GithubRemops_ruedtim/SAR_verzeichnisse
V=$S/np13
PY=(uv run --quiet --with pdfplumber --with openpyxl python -I)
mkdir -p $S/neu13 $V/proj_excel $V/proj_test $V/proj_d151
# 1. Skript und Projektstand als Kopie
cp $P/findmittel_zu_scope.py $S/neu13/
shasum -a 256 $S/neu13/findmittel_zu_scope.py | tee $V/skript_sha.txt
cp $P/findmittel_excel/*.xlsx $V/proj_excel/
cp $P/testdaten_excel/*.xlsx $V/proj_test/
cp $P/D151210_scope_import.xlsx $V/proj_d151/
ls $V/proj_excel | wc -l
# 2. Rechnen
sed "s#/np12\$#/np13#" $S/np12/lauf.sh > $V/lauf.sh
cd $V
bash lauf.sh $S/neu13/findmittel_zu_scope.py $V/aus_neu 8 > lauf.log 2>&1
"${PY[@]}" $S/neu13/findmittel_zu_scope.py $P/testdaten/*.pdf -o $V/test_neu --cache $S/verb2/cache_test \
  --katalog $P/findmittel_pdf/verzeichnis.csv > test.log 2>&1
"${PY[@]}" $S/neu13/findmittel_zu_scope.py $P/D151210.pdf -o $V/d151_a --cache $S/verb2/cache_test \
  --katalog $P/findmittel_pdf/verzeichnis.csv > d151.log 2>&1
cat lauf.log; tail -1 test.log; cat d151.log
# 3. Zellvergleiche: Projekt = eigener Lauf? Runde 9 -> Runde 10?
Z=(uv run --quiet --with openpyxl python -I $S/np4/zellen.py)
"${Z[@]}" $V/proj_excel $V/aus_neu $V/z_proj.json
"${Z[@]}" $V/proj_test $V/test_neu $V/z_test.json
"${Z[@]}" $V/proj_d151 $V/d151_a $V/z_d151.json
"${Z[@]}" $S/np12/aus_neu $V/aus_neu $V/z_r9_r10.json
"${Z[@]}" $S/np12/test_neu $V/test_neu $V/z_test_alt.json
"${Z[@]}" $S/np12/d151_a $V/d151_a $V/z_d151_alt.json
for f in z_proj z_test z_d151 z_test_alt z_d151_alt; do echo "$f: $(head -c 300 $V/$f.json)"; done
uv run --quiet python -I -c "import json; z=json.load(open('$V/z_r9_r10.json')); print('Runde 9 -> 10 geändert:', len(z))"
# 4. Fallsets (alt = Runde 9, neu = Runde 10)
F=$P/stichproben/verbesserung/werkzeug/faelle; R=$P/stichproben/verbesserung/runde2/werkzeug
for x in a b c f; do "${PY[@]}" $F/pruefe_faelle.py $F/${x}_faelle.csv $S/np12/aus_neu $V/aus_neu > $V/fall_$x.txt 2>&1; echo "Fallset $x: $(tail -1 $V/fall_$x.txt)"; done
"${PY[@]}" $R/pruefe_runde2.py $R/runde2_faelle.csv $S/np12/aus_neu $V/aus_neu > $V/fall_r2.txt 2>&1; echo "Runde 2: $(tail -1 $V/fall_r2.txt)"
"${PY[@]}" $R/pruefe_runde2.py $R/punkt2_faelle.csv $S/np12/aus_neu $V/aus_neu > $V/fall_p2.txt 2>&1; echo "Punkt 2: $(tail -1 $V/fall_p2.txt)"
# 5. Suchlauf Tippfehler (Runde 9 als Basis liegt in tipp_r9.csv)
"${PY[@]}" $V/suchlauf_tippfehler.py $V/cache $V/aus_neu $V/tipp_r10.csv
echo "fertig"
