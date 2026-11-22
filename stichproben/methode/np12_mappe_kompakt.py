"""Kompakte Strukturmappe aus einer Prüfmappe (für grosse Dateien): behält Kopf, jede EINHEIT-Zeile, jede Zeile mit
Warnzeichen, jede Zeile mit Ziel Vollst./Info/?/Vorspann/Titel/Umfang, jede fette oder kursive Zeile, jede Zeile, die mit
einer Signaturform beginnt, und die erste sowie die letzten zwei Seiten vollständig. Unauffällige Darin-Zeilen dazwischen
werden je Einheit gezählt. Aufruf: python -I mappe_kompakt.py <mappe.txt> <aus.txt>"""
import re, sys
src, aus = sys.argv[1:3]
zeilen = open(src, encoding="utf-8").read().split("\n")
SIGART = re.compile(r"^\s*(?:[A-Z]{1,3}\s?\d|[IVXL]+[.)]|\d+[a-z]?[.:)]|\d+\s*[:.]\s*\d|[a-z][.)]\s|[A-Z][.)]\s|\(?[A-Z]\.[A-Z]|[IVX]+\.[A-Z])")
PDF = re.compile(r"^S(\d+)\s+\d+\s+\|\s+x\s*\d+\s+[\d.]*(\S*)\s*\|\s(.*?)\s+→ (.*)$")
seiten = [int(m.group(1)) for z in zeilen for m in [PDF.match(z)] if m]
letzte = max(seiten) if seiten else 0
out, zaehl, aktiv = [], 0, None
def flush():
    global zaehl, aktiv
    if zaehl:
        out.append(f"      … {zaehl} unauffällige Darin-Zeilen → ID {aktiv} …")
    zaehl, aktiv = 0, None
teil = "kopf"
for z in zeilen:
    if z.startswith("== PDF"):
        teil = "pdf"; out.append(z + "  [KOMPAKT: unauffällige Darin-Zeilen nur gezählt, ausser auf S. 1 und den letzten zwei Seiten]"); continue
    if z.startswith("== Excel"):
        flush(); teil = "xl"; out.append(z); continue
    if teil != "pdf":
        out.append(z); continue
    m = PDF.match(z)
    if not m:
        if "weitere unauffällige Zeilen" in z:
            mm = re.search(r"… (\d+) weitere unauffällige Zeilen → ID (\d+)", z)
            if mm:
                if aktiv not in (None, mm.group(2)):
                    flush()
                aktiv = mm.group(2); zaehl += int(mm.group(1)); continue
        flush(); out.append(z); continue
    seite, stil, text, ziel = int(m.group(1)), m.group(2), m.group(3), m.group(4)
    darin = re.match(r"ID (\d+) Darin \d+\s*$", ziel)
    behalten = (not darin or seite == 1 or seite >= letzte - 1 or "B" in stil or "K" in stil or SIGART.match(text))
    if behalten:
        flush(); out.append(z)
    else:
        if aktiv not in (None, darin.group(1)):
            flush()
        aktiv = darin.group(1); zaehl += 1
flush()
open(aus, "w", encoding="utf-8").write("\n".join(out))
