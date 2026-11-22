#!/bin/bash
# Aufruf: bash vorab.sh "P1 P5 P6 P7 ..."  – kritische Funde der fertigen Pakete nach stichproben/roh/np12_vorab_kritisch.csv
S=/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/np12
P=/Users/stazh/Documents/GithubRemops_ruedtim/SAR_verzeichnisse
rm -rf $S/vorab_pakete $S/vorab_aus; mkdir -p $S/vorab_pakete $S/vorab_aus
for pk in $1; do cp $S/pakete/${pk}_* $S/vorab_pakete/ 2>/dev/null; done
uv run --quiet python -I $S/zusammen12.py $S/vorab_pakete $P/stichproben/offen_kritisch.csv $S/vorab_aus > $S/vorab_aus/log.txt 2>&1
python3 -I - "$1" <<'PY'
import csv, sys
S = "/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/np12"
P = "/Users/stazh/Documents/GithubRemops_ruedtim/SAR_verzeichnisse"
r = list(csv.DictReader(open(f"{S}/vorab_aus/funde_nachpruefung12.csv", encoding="utf-8"), delimiter=";"))
F = ["paket", "datei", "seite", "signatur_id", "feld", "befund_jetzt", "soll", "muster", "ursache_bemerkung", "entscheid"]
out = []
for x in r:
    if x["schwere"] == "kritisch" and x["status"] in ("neu", "offen", "teilweise", "schlechter"):
        out.append({"paket": x["paket"], "datei": x["pdf"].replace(".pdf", ""), "seite": x["seite"], "signatur_id": x["signatur"], "feld": x["feld"],
                    "befund_jetzt": x.get("neu_ist") or x["ist"], "soll": x["soll"], "muster": x.get("muster", ""),
                    "ursache_bemerkung": x["bemerkung"], "entscheid": x.get("entscheid", "")})
with open(f"{P}/stichproben/roh/np12_vorab_kritisch.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=F, delimiter=";"); w.writeheader(); w.writerows(out)
print(len(out), "kritische Zeilen aus", sys.argv[1], "in", len({x["datei"] for x in out}), "Dateien")
PY
