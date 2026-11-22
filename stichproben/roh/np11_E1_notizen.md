# E1 – Notizen (Nachprüfung 11, erste Prüfung, Stand efe92c5f)

## Bilanz
- 40 Dateien, 570 Einheiten. **39 ohne kritischen Fehler, 1 kritisch (D175561).**
- 20 Fundzeilen: 1 kritisch, 18 mittel, 1 gering (`E1_funde.csv`); Urteile für alle 40 (`E1_dateien_urteil.csv`).
- Methode: jede Prüfmappe ganz gelesen (D539: Struktur, Warnzeichen, fette Zeilen; alle Zeilen per Skript). Dazu je Datei
  `tmp_E1/zuordnung.py` (jede PDF-Zeile muss bei der Einheit ihres PDF-Abschnitts stehen) und `tmp_E1/darinscan.py`
  (Darin-Zeilen mit Nummernform). PDF nur bei Zweifeln (D175561, D1237 S. 2), Spalten über den Zeilen-Cache.

## Kritischer Fund
- **D175561 (V.G.c.63.):** Die Bestandssignatur steht nur in der ersten Zeile («V.G. c.63. 1. Brunnen …»). Die Nummern
  2.–22. in derselben Nummernspalte (x 184) stehen als Liste im Darin der einzigen Einheit «V.G.c.63.1.». Soll: 22
  Einheiten V.G.c.63.:1.–:22. mit Titel und Jahren (Liste im Soll). Muster 1, neue Spielart «Vollsignatur nur in der
  ersten Zeile»; Folgen: Signatur ohne «:», Zeitraum 1889–1946 statt 1919–1934.
- Suchvorschlag: Dateien mit wenigen Einheiten, deren Darin fortlaufend mit «2.», «3.» … beginnt, die Signatur auf «1.».

## Mittel (gehäuft)
- **Zeitraum aus erwähnten Daten:** D539 (12 Schachteln über die Spanne der Schachtelüberschrift hinaus, z. B.
  «Stadtverfassung vom Jahre 1831»), D3682 (Fussnoten-Lebensdaten, Geburts- statt Ausstellungsdaten), D2925
  («† 17.9.1980» des Verfassers), D2665 (Tippfehler 1955 statt 1855), D3474 («1700 Ø und 1200 Ø»).
- **Zeitraum zu eng:** Datum der zweiten Zeile zählt nicht (D3614, D140974 «1984/1985», D1589 «1804 bis / 1812»,
  D1674 «1897-898», D2767 «16. bis 21. November»).
- **Tabellenspalten im Titel:** D3949 (Interpret | Titel), D3818 (Bände), D3474 (mehrzeilige Obergruppe); gering D1269.
- **Titel:** Folgezeilen im Titel (D2767 3., D140974 :4 Lagerungsvermerk), Titelrest im Darin (D1589 :2).
- **Schlussnotizen im Darin der letzten Einheit:** D1237 (Aufteilung des Bestandes), D539 («Dres. Robert Dünki und Max
  Schultheiss»); wie früher (M07) mittel, weil kein Anhang und keine Literatur.

## Warnzeichen
- [VOR]/[NACH] (D539 155, D3949, D1757, D842, D3998, D3474): Rauschen durch gleich lautende Anfänge («Weisung des
  Stadtrathes …», «(Single)», «Pergaminplan, beschädigt»), per Skript bestätigt.
- [SIG?]: D3474 = wiederholte Mappennummern in neuer Schachtel (richtig als Teile), D3614 = Schlussvermerk.
- [NICHT]: nur Titelblätter, Tabellenköpfe, Einleitungen, Schlussvermerke, Provenienz-/Biografienotizen im Info.

## Unsicherheiten / Hinweise
- D539 ID 15 «Drucksachen, Teil 2» = beabsichtigte Teilung eines Darin über der Zellgrenze (mit Hinweis).
- D3643 4., D3818 10., D1237 :3: 1./2./3. ohne eigene Signatur in der Inhaltsspalte = Darin (Konvention Runde 7);
  D3080 a)/b)/c) stehen in der Inhaltsspalte, nicht in einer eigenen Spalte «Bez.».
- D539: Ob erwähnte Vertragsdaten den Zeitraum erweitern dürfen, ist eine Regelfrage; Soll = ausdrückliche Spanne.
- Versehen: kurz /tmp/e1_soll.txt (nur Dateiliste) angelegt und sofort gelöscht; sonst nur in `pakete/` geschrieben.
