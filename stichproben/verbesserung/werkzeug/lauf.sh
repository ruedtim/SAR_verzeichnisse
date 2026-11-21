#!/bin/bash
# Aufruf: bash lauf.sh <skript> <ausgabeordner> [teile] [pdfliste]
# Wandelt alle PDFs aus findmittel_pdf/pdf (oder die Liste) in <ausgabeordner> um, in <teile> parallelen Prozessen.
SKRIPT=$1; AUS=$2; N=${3:-6}; LISTE=$4
P=/Users/stazh/Documents/GithubRemops_ruedtim/SAR_verzeichnisse
V=/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/verb
case "$AUS" in "$V"/*) ;; *) echo "Ausgabe muss im Scratchpad liegen"; exit 2;; esac
mkdir -p "$AUS"
if [ -n "$LISTE" ]; then sed "s#^#$P/findmittel_pdf/pdf/#" "$LISTE" > "$AUS/_liste.txt"; else ls "$P/findmittel_pdf/pdf"/*.pdf > "$AUS/_liste.txt"; fi
rm -f "$AUS"/_teil*.txt
awk -v n="$N" -v d="$AUS" '{print > (d "/_teil" (NR % n) ".txt")}' "$AUS/_liste.txt"
start=$(date +%s)
for t in "$AUS"/_teil*.txt; do
  k=$(basename "$t" .txt)
  uv run --quiet --with pdfplumber --with openpyxl python -I "$SKRIPT" $(cat "$t") -o "$AUS" --cache "${CACHE:-$V/cache}" \
     --katalog "$P/findmittel_pdf/verzeichnis.csv" > "$AUS/_log_$k.txt" 2>&1 &
done
wait
echo "fertig nach $(( $(date +%s) - start )) s: $(ls "$AUS"/*_scope_import.xlsx | wc -l) Dateien, Fehler: $(cat "$AUS"/_log_*.txt | grep -c FEHLER)"
