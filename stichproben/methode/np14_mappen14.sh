#!/bin/bash
# NP13: Vergleiche (Runde 10 -> 11) für die 66 geänderten Dateien, Prüfmappen, Kompaktmappen (> 60 Einheiten),
# Strukturberichte (> 200 Einheiten) für die 66 geänderten Dateien und die 60 Stichprobendateien.
S=/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad
V=$S/np14
X=(uv run --quiet --with openpyxl python -I)
mkdir -p $V/vgl $V/mappen $V/mappen_kompakt $V/struktur
for d in $(cat $V/geaendert_r11.txt); do "${X[@]}" $S/np8/vgl.py $S/np13/aus_neu $V/aus_neu $d 170 > $V/vgl/$d.diff.txt 2>&1; done
ALLE=$(cat $V/geaendert_r11.txt $V/zufall60_2.txt | sort -u)
"${X[@]}" $S/np12/pruefmappe.py $V/cache $V/aus_neu $V/mappen $ALLE > $V/mappen.log 2>&1
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
