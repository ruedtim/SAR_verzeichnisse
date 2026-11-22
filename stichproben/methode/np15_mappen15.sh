#!/bin/bash
# NP15 Schritt 2: Stichprobe 3 ziehen, Vergleiche (Runde 11 -> 12) für die geänderten Dateien, Kompaktmappen (> 60 Einheiten)
# und Strukturberichte (> 200 Einheiten) für die geänderten Dateien und die 60 Stichprobendateien. Die Prüfmappen aller
# 715 Dateien liegen schon in mappen_r12 (start15.sh).
S=/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad
V=$S/np15
X=(uv run --quiet --with openpyxl python -I)
# Stichprobe 3: die ersten 60 Kandidaten ab Rang 137 (kandidaten_ab137.txt, vor Runde 12 festgelegt), die Runde 12 nicht ändert
grep -v '^#' $V/kandidaten_ab137.txt | cut -d';' -f2 | grep -vxF -f $V/geaendert_r12.txt | head -60 > $V/zufall60_3.txt
echo "Stichprobe 3: $(wc -l < $V/zufall60_3.txt) Dateien, letzter Rang $(grep -F -f <(tail -1 $V/zufall60_3.txt) $V/kandidaten_ab137.txt | cut -d';' -f1)"
mkdir -p $V/vgl $V/mappen $V/mappen_kompakt $V/struktur
for d in $(cat $V/geaendert_r12.txt); do "${X[@]}" $S/np8/vgl.py $S/np14/aus_neu $V/aus_neu $d 170 > $V/vgl/$d.diff.txt 2>&1; done
ALLE=$(cat $V/geaendert_r12.txt $V/zufall60_3.txt | sort -u)
for d in $ALLE; do cp $V/mappen_r12/$d.txt $V/mappen/; done
"${X[@]}" - $V/aus_neu $V/einheiten.txt $ALLE <<'PY'
import sys, openpyxl
o, aus, *dd = sys.argv[1:]
with open(aus, "w") as f:
    for d in dd:
        ws = openpyxl.load_workbook(f"{o}/{d}_scope_import.xlsx", read_only=True)["scope-Import"]
        n = sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if r and r[0] is not None)
        f.write(f"{d}\t{n}\n")
PY
GROSS=""
while IFS=$'\t' read d n; do
  if [ "$n" -gt 60 ]; then "${X[@]}" $S/np12/mappe_kompakt.py $V/mappen/$d.txt $V/mappen_kompakt/$d.txt; fi
  if [ "$n" -gt 200 ]; then GROSS="$GROSS $d"; fi
done < $V/einheiten.txt
"${X[@]}" $S/np12/strukturbericht.py $V/aus_neu $V/mappen $V/struktur $GROSS > $V/struktur.log 2>&1
echo "Mappen: $(ls $V/mappen | wc -l), kompakt: $(ls $V/mappen_kompakt | wc -l), Struktur: $(ls $V/struktur | wc -l), Vergleiche: $(ls $V/vgl | wc -l)"
