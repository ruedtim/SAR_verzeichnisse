# SAR-Findmittel → scope-Import

Wandelt die Findmittel-PDFs des Stadtarchivs Zürich (Bestände, die in scope noch nicht erschlossen sind) in
Excel-Dateien für den scope-Import um: eine Datei je Findmittel mit den Blättern «scope-Import», «Prüfliste»,
«Vollständigkeit» und «Info», dazu eine Übersicht über alle Findmittel.

## Inhalt

- `findmittel_zu_scope.py` – Umwandlung PDF → Excel.
- `findmittel_laden.py` – lädt das Verzeichnis und die Findmittel-PDFs aus dem Online-Archiv.
- `findmittel_pdf/verzeichnis.csv` – Verzeichnis der Findmittel (Signatur, Titel, Datei) aus dem Online-Archiv.
- `stichproben/` – Stichprobenprüfung und Nachprüfungen am PDF: Berichte, Fundlisten, Werkzeuge.

Nicht im Repository: die PDFs (Quelle: Online-Archiv des Stadtarchivs) und vorerst die erzeugten Excel-Dateien –
sie kommen mit einer stabilen Konvertierungsfassung dazu.

## Aufruf

```bash
uv run --with pdfplumber --with openpyxl python findmittel_zu_scope.py findmittel_pdf/pdf -o findmittel_excel \
    --cache cache --katalog findmittel_pdf/verzeichnis.csv
```
