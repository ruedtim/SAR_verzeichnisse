# Z2 – dritte Zufallsstichprobe der NP15 (19 Dateien, 575 Einheiten), Stand Skript 439a6fbf (Runde 12)

## Bilanz
- Alle 19 Dateien ganz geprüft: Prüfmappe (über 60 Einheiten Kompaktmappe plus volle Mappe an jeder Verdachtsstelle), Excel aller
  Einheiten mit ganzem Darin, Info und Vollständigkeit, PDF bei jedem Zweifel. Per Skript (`tmp_Z2/`): jede PDF-Zeile gegen die
  Einheit nach ihrer Lage (`poscheck.py`), jede Datumsspalte gegen ihren Darin-Eintrag (`datecol.py`), Vermerk-Suche in Titel und
  Darin (`vermerk.py`), dazu die Suchlauf-Listen der NP15 (Gruppenende, Vermerk, Info-Stücke, Nummern im Darin) für meine Dateien.
- **19 ohne kritischen Fehler, 0 kritisch.** Rate 0/19 (95 %-Intervall 0–17,6 %). Keine Strukturberichte nötig (keine Datei über
  200 Einheiten).
- Neue Funde: 0 kritisch, 6 mittel, 6 gering. Dazu 15 bekannte, unverändert offene Zeilen (mittel/gering) mit Vermerk «kein neuer
  Fund» bestätigt. Keine Zeile aus `bekannt.csv` betrifft Z2.
- Behoben bestätigt: D3781 «chr Stand: 27.08.1993» steht jetzt im Info (NP11), D2850 «SATUS» und Pokal-Bestandszeile, D140969 50a./57./88./89.

## Wichtigste Funde (alle mittel)
- Z2-06 D2839: Bei 5 Zeichnungen fehlt Tag und Monat der Datumsspalte, weil das Jahr schon im Titel steht («42. Miss Milk 1960»
  ohne «19. Okt. 1960»). Das ist seit der Stichprobe vom 19.11. bekannt (M05, dort nur «Posen 1956»), aber nie behoben.
  Suchlauf über alle 19 Dateien: nur hier.
- Z2-05 D151735: Die Inhaltsangabe für alle 12 Schachteln («Inhalt: Alphabetische Listen der Ferienkinder …») steht nur im Blatt
  Vollständigkeit, nicht einmal im Info.
- Z2-01 D140969 6./24., Z2-02 D3718 8.2.2./9.5.5., Z2-04 D3599 3.3.: Folgezeile oder Datum mitten im Titel, Titel am Doppelpunkt
  abgebrochen. Z2-03 D3718 4.2.17./5.2.1.: zweizeilige Datumsspalte bzw. «Mai und Juli 1900» falsch gelesen.

## Muster
- Kein Fall der Muster 1–8 (keine Unterstufe im Darin, kein Gruppenende bei der letzten Untereinheit, kein Stück ohne Nummer nur im
  Info, keine erfundene oder fehlende Einheit). Alle Gruppenende-Kandidaten (D2850 48.B., D3718 4.2.2.3./5.1.5./5.2.10./9.8.) sind
  Einträge der letzten Untereinheit in deren Einzug.
- Häufigster Restfehler: Spalteninhalt (Datum, «Sch. n», «(1 Band)», Bände-Zahl) im Titel statt im eigenen Feld (D1578, D3398, D3718,
  D3791, D140969), dazu zusammengezogene Darin-Zeilen (D141056, D2850, D3599). Alles mittel/gering, Text in der richtigen Einheit.

## Unsicherheiten
- Z2-06 ist ein Grenzfall: Nach dem Wortlaut «Verzeichnistext in keinem Feld» wäre es kritisch (wie K45 D512). Ich folge der
  Ersteinstufung vom 19.11. (gleichartige D2839-Fälle dort «Schwere angepasst: kritisch → mittel»). Stuft die Hauptsession um, wird
  D2839 kritisch (1/19).
- D140969: «(neu archiviert von Prof. Werner G. Zimmermann im August 1990)» steht im Darin der Gruppe 59-81. Ich werte es als
  Gruppenbeschreibung (Klammersatz unter dem Gruppenkopf) und nicht als K169-Bearbeitervermerk. «[Photokopie in der 1. Schachtel
  dieses Bestandes]» im Info gehört zum Literaturhinweis; ich werte es nicht als Stück ohne Nummer.
- D3398 Z2-09: «Teil 2» = Schachtel 1 folgt der späteren Teile-Konvention. Das Soll vom 19.11. war «Teil 1 = Schachtel 1».
- D140969 13. «… Landesausstellung 1939 Allgemeine Akten»: «Allgemeine Akten» kann zum Titel gehören, darum nicht gemeldet.
