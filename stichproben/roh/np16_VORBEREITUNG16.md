# NP16 – Vorbereitung (22.11.2026, während der Installation von Runde 13)

Ohne Blick auf Runde 13 geschrieben. Gearbeitet wurde nur mit der eigenen Kopie von Runde 12 (`np15/aus_neu`, Skript 439a6fbf),
nicht mit `findmittel_excel/`.

## Vierte Zufallsstichprobe (festgelegt vor dem ersten Blick auf Runde 13)

- **Reihenfolge:** dieselbe wie in NP13–NP15 (`np14/zufall_reihenfolge.txt`, `random.Random(20261122)` über die 715 Dateien).
  Die Stichproben 1–3 belegen die Ränge 1–196.
- **Kandidaten:** `kandidaten_ab197.txt` (auch `stichproben/roh/np16_kandidaten_ab197.txt`), sha256 `b3bd7213…`.
  - Das sind 501 Dateien ab Rang 197, ohne die Stichproben 1–3 und ohne die 22 Dateien in `offen_kritisch.csv` (Stand NP15).
  - Ab Rang 197 fallen dadurch 18 Dateien weg.
- **Stichprobe 4:** die ersten 60 Kandidaten, die Runde 13 nicht ändert (`mappen16.sh` zieht sie).
- **Prüfung:** ganz, wie Z1–Z3/ZL1 der NP15.
- **Grundgesamtheit:** 715 − 180 − 22 = 514 Dateien, davon abgezogen die Dateien, die Runde 13 ändert.
- **Auswertung:**
  - Rate der Stichprobe 4 allein und mit 1–3 zusammen (240 Dateien), Wilson-Intervall.
  - Die Rate getrennt nach Art: Schluss/Info, Gruppenende und Gliederung. Schluss/Info und Gruppenende sind seit NP15
    systematisch durchgesehen.

## Neuer Suchlauf «leere Teile» (Muster K220)

`suchlauf_leere_teile.py`:
- **KOPF:** ein Teil ohne Darin und ohne Kinder, dessen erste Nennung auf einer früheren Seite steht und eigene Untereinheiten
  hat, von denen mindestens 80 % im PDF nach dem Teil stehen. An Runde 12 trifft das genau die fünf Teile von D845 (K220).
- **LEER:** übrige Teile ohne Darin, Kinder, Schachtel, Zeitraum und Umfang. An Runde 12 sind es 148 in 9 Dateien, davon 118 in
  D149628 und 15 in D1880. Das ist zur Sichtung, meist echte Teile mit nur einem Titel.

## Ablauf nach «Runde 13 installiert»

1. `bash start16.sh`:
   - Stand sichern, Gesamtlauf, Testdaten, D151210;
   - Zellvergleiche (Projekt = eigener Lauf? Runde 12 → 13);
   - Fallsets (alt = `np15/aus_neu`);
   - alle Suchläufe, auch die neuen der NP15 und «leere Teile»;
   - Prüfmappen (Runde-12-Mappen übernommen, geänderte neu), Durchsichtsblöcke der geänderten Dateien.
2. `stichproben/runde13/` lesen; `vorher/` gegen `np15/aus_neu` vergleichen; die Antworten der Hauptsession zu den Fragen der
   NP15 eintragen.
3. `bash mappen16.sh`: Stichprobe 4 ziehen, Vergleiche, Kompaktmappen und Strukturberichte.
4. Prüfpakete:
   - G für die von Runde 13 geänderten Dateien, Altzeilen K209–K220;
   - Z für Stichprobe 4;
   - S für die Treffer der Suchläufe, die neu sind gegenüber Runde 12.
5. Zusammenführen mit `zusammen16.py` (aus `np15/zusammen15.py`, K-Nummern stabil, neue ab K221).
