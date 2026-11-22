# NP14 – Vorbereitung (22.11.2026, vor der Installation von Runde 11)

## Zweite Zufallsstichprobe (festgelegt vor Runde 11)

- **Reihenfolge:** dieselbe wie in NP13, `zufall_reihenfolge.txt`, `random.Random(20261122)` über die 715 Dateien.
- **Stichprobe 2:** die ersten 60 Dateien ab Rang 74, die
  - nicht in der ersten Stichprobe sind (`np13/zufall60.txt`);
  - von Runde 11 nicht geändert sind;
  - nicht in `offen_kritisch.csv` stehen (Stand nach NP13 mit Nachtrag: 33 Zeilen in 28 Dateien).
- **Prüfung:** ganz, wie Z1–Z3 der NP13.
- **Auswertung:** Rate je Stichprobe und gemeinsam (120 Dateien). Die Grundgesamtheit der zweiten Stichprobe ist kleiner (ohne
  die erste Stichprobe, ohne die in NP13 gefundenen Dateien, ohne die von Runde 11 geänderten). Beide Raten schätzen den
  Anteil der Dateien mit übersehenem kritischem Fehler unter den Dateien ohne bekannte K-Zeile.

## Ablauf nach «Runde 11 installiert»

1. `bash start14.sh`: Stand sichern, Gesamtlauf, Testdaten, D151210, Zellvergleiche (Projekt = eigener Lauf? Runde 10 → 11),
   Fallsets (alt = Runde 10 in `np13/aus_neu`), Suchlauf Tippfehler.
2. `stichproben/runde11/` lesen; `vorher/` gegen `np13/aus_neu` vergleichen.
3. Suchläufe über alle 715 Dateien:
   - Tippfehler (`np13/suchlauf_tippfehler.py`), Stück ohne Nummer im Info (`np13/suchlauf_info_stuecke.py`), Buchstaben in
     der Titelspalte (`np13/suchlauf_buchstaben_titelspalte.py`);
   - neu: `suchlauf_gruppenende.py` (Muster D2620/K196) und `suchlauf_nummern_im_darin.py` (Muster D151150/K144).
4. G-Pakete für die von Runde 11 geänderten Dateien, mit den 23 nicht bewusst offenen K-Zeilen als Altzeilen; Z-Pakete für
   die Stichprobe 2.
5. Zusammenführen mit `np13/zusammen13.py` (Kopie als `zusammen14.py`, K-Nummern stabil, neue ab K203).

## Ablauf am 22.11.2026 (nach «Runde 11 installiert»)

1. `np14_start14.sh`: Stand sichern, Gesamtlauf, Testdaten, D151210, Zellvergleiche, Fallsets, alle Suchläufe. Ergebnis:
   zellgleich, 18 Dateien geändert (= Liste der Hauptsession), `runde11/vorher/` zellgleich mit dem eigenen Lauf der Runde 10.
2. Suchläufe an Runde 10 (Probe) und Runde 11: `np14_suchlauf_gruppenende.py`, `np14_suchlauf_nummern_im_darin.py` (dritte
   Verankerungsstufe: letzte Stelle von «Nr. im PDF», sonst fehlen D151150-Dossiers), `np14_suchlauf_na_kind.py` (Skript von G3
   der NP13), `np14_suchlauf_info_stuecke.py` (um «umfasst neben … noch», «enthält noch», «noch eine Schachtel» erweitert).
3. Stichprobe 2 nach der festen Regel: Rang 74–136, Grundgesamtheit 628 Dateien (`roh/np14_zufall60_2.txt`).
4. Pakete nach `roh/np14_AUFTRAG14.md`: G1, G2 (Gegenprüfung), Z1–Z3 (57 kleinere Stichprobendateien), ZL1 (D151210), ZL2
   (D175996, D3466), S1 (36 Kandidaten aus den Suchläufen «Gruppenende» und «n.a als Kind»).
5. `np14_zusammen14.py <pakete> <offen_kritisch_alt.csv> <aus>`: K-Nummern stabil, neue ab K203; K200–K202 entfallen nach dem
   Entscheid der Hauptsession (AENDERUNGEN_RUNDE11, Konvention 2).
