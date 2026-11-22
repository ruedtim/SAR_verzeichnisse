"""Letzte Einheit jeder Ausgabe: Darin-Zeilen, die wie die Überschrift eines Schlussabschnitts aussehen.
Aufruf: python -I schluss_darin_scan.py <ausgabeordner>"""
import glob
import re
import sys

import openpyxl

KOPF = re.compile(
    r"^(?:(?:[A-ZÄÖÜ][a-zäöü]+(?:e|en|er)\s+)?(?:Literatur|Quellen|Bibliogra(?:f|ph)ie)\b"
    r"|(?:Quer)?[Vv]erweise?\s+(?:auf|zu)\b|Hinweise?\s+(?:auf|zu)\b"
    r"|(?:Bemerkung|Anmerkung|Hinweis|Notiz|Nachbemerkung|Vorbemerkung)(?:en|e)?\s*(?::|$|zu[mr]?\b)"
    r"|(?:Zur\s+)?(?:Bestands|Überlieferungs|Archiv)geschichte\b|Geschichte des (?:Bestandes|Nachlasses|Archivs)\b"
    r"|(?:Verwandte|Weitere|Ergänzende|Andere)\s+(?:Bestände|Unterlagen|Quellen)\b"
    r"|.{0,60}\bin der Bibliothek des Stadtarchivs\b|Benut?zung(?:sbestimmungen)?\s*:?$|Provenienz\s*:?$)")
SATZ = re.compile(r"^(?:Der (?:Archiv)?[Bb]estand (?:umfasst|wurde|stammt|enthält|besteht)|Der Nachlass (?:wurde|umfasst|stammt)"
                  r"|Die Benut?zung\b|Letzte Änderung|Weitere Publikationen befinden sich"
                  r"|.{0,80}\bdem Stadtarchiv\b.{0,40}\b(?:übergeben|geschenkt|überlassen|abgeliefert)\b)")
for p in sorted(glob.glob(sys.argv[1] + "/D*_scope_import.xlsx")):
    wb = openpyxl.load_workbook(p, read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    if len(rows) < 2:
        continue
    d = dict(zip(h, rows[-1]))
    darin = (d["Darin"] or "").split("\n")
    for n, z in enumerate(darin):
        t = z.lstrip("; ").strip()
        if KOPF.match(t) or SATZ.search(t):
            print(p.split("/")[-1].split("_")[0], d["Signatur"], f"Z{n + 1}/{len(darin)}", "|", t[:80])
            break
