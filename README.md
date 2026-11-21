# SAR-Findmittel → scope-Import

Wandelt die Findmittel-PDFs des Stadtarchivs Zürich (Bestände, die in scope noch nicht erschlossen sind) in
Excel-Dateien für den scope-Import um: eine Datei je Findmittel mit den Blättern «scope-Import», «Prüfliste»,
«Vollständigkeit» und «Info», dazu eine Übersicht über alle Findmittel.

## Inhalt

- `findmittel_zu_scope.py` – Umwandlung PDF → Excel.
- `findmittel_laden.py` – lädt das Verzeichnis und die Findmittel-PDFs aus dem Online-Archiv.
- `findmittel_pdf/verzeichnis.csv` – Verzeichnis der Findmittel (Signatur, Titel, Datei) aus dem Online-Archiv.
- `stichproben/` – Stichprobenprüfung und Nachprüfungen am PDF: Berichte, Fundlisten, Werkzeuge.
- `findmittel_excel/` – die Excel-Dateien aller 715 Findmittel und die Übersicht `uebersicht_scope_import.xlsx`.
- `testdaten_excel/` und `D151210_scope_import.xlsx` – Testdaten und das Findmittel VII.200.

Die Excel-Dateien sind mit dem Skript dieses Stands erzeugt (Gliederungsrunde mit Nachtrag, 22.11.2026). Geprüft
wurden sie in `stichproben/nachpruefung8.md`; Änderungen und offene Punkte stehen in
`stichproben/runde7/AENDERUNGEN_RUNDE7.md`. Jede Excel-Datei enthält im Blatt «Prüfliste» die Einheiten mit
Prüfhinweisen.

Nicht im Repository: die PDFs (Quelle: Online-Archiv des Stadtarchivs).

## Aufruf

```bash
uv run --with pdfplumber --with openpyxl python findmittel_zu_scope.py findmittel_pdf/pdf -o findmittel_excel \
    --cache cache --katalog findmittel_pdf/verzeichnis.csv
```
