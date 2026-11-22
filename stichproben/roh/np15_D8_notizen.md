# D8 – Durchsicht Schluss, Info und «Nicht übernommen» (NP15, Runde 12)

**Umfang.** `durchsicht_r12/teil_8.txt` ganz gelesen (83 Blöcke, 1773 Zeilen). Bei jedem Verdacht: volle Prüfmappe, Excel und PDF.
Dazu Auszüge in `tmp_D8/`: `info_alle.txt` (Info-Felder der 83 Dateien), `vermerk_scan.py` (Bearbeitervermerke in Titel und Darin
der 83 Dateien), `monat_jahr_scan.py` (Form «Monat Jahr / Name» über alle 715 Dateien).

**Bilanz.** 80 Dateien ohne kritischen Fehler, 3 kritisch: D631 und D414 neu, D512 nur mit bekannt K45. Neu: 2 kritisch, 1 mittel.

**Funde**
- **D8-1 D631, kritisch (Inhalt bei falscher Einheit).** «Ende Juli 2004 / Dr. Robert Dünki» (S. 2 y732) ist Darin 40 der
  Bestandszeile; Info-Schlussvermerk «–». Ursache: `SCHLUSS_DATUM_RE` verlangt eine Tageszahl. Wie K169 und der K156-Rest; NP12 P4
  hatte es noch als mittel notiert. Die Suche über alle 715 Dateien findet nur diesen Fall.
- **D8-2 D414, kritisch (Text weg).** Der Absatz «Der Inhalt der einzelnen Faszikel ist nicht verzeichnet. Ein rotes D + Datum …
  Zeitungsausschnitte hin.» (S. 2 y478–562) steht nur im Info. Er setzt nach der Gruppenliste I.–XV. die «Hinweise und Uebersicht»
  von Schachtel 5 fort. Soll: Darin von V.B.c.34.:5 mit Hinweis wie Regel 9. Seit NP13 unverändert; G4 hat es nicht beanstandet.
- **D8-3 D9983, mittel.** «Kopien» unter «5.2. Theaterzettel …» steht nur als Prüfhinweis bei 5.2.1. Bei 5.1. steht das
  Gegenstück «Originale, lose» im Darin.

**Muster.** (1) Ein Bearbeitervermerk ohne Tageszahl wird nicht erkannt, auch nicht im Pfad «ohne Signaturen». (2) Eine
Gruppenbeschreibung, die am Dateiende nach der Liste der Untereinheiten weitergeht, landet als Schlussvermerk im Info; die
Gruppenende-Regeln greifen nur vor einer nächsten Nummer. (3) Die einzige Beschreibungszeile einer Gruppe direkt vor der ersten
Untereinheit wird Zwischenüberschrift (nur Hinweis).

**Bekannt, noch da, nicht neu gemeldet.**
- bekannt K45: D512, Datumsspalte, bewusst offen; das sind die «fehlt»-Zeilen. Aus der Liste «Bekannt»: D3943 99,9 %, D406
  Vermerk nur im Hinweis, D9978 28.4.25. Zeitraum.
- Mittel (NP11–NP13): D3951 «(Band)»; D3898 «Ledermesse …» nur bei 111.; D406 Vorname «August»; Eltern in einer anderen Datei
  bei D4057, D4058 («19.»), D9978 («28.»), D9985; D4173 Benziger-Block; D8952 Farbfotokopien im Vorspann; D817/D821/D867.
- Gering: D3943 Zeichenerklärung in der Bestandszeile, D537 «Seite. ( Expl.)». Konvention: D49/D71 «e) Akten keine».

**Runde 12.** D49, D65, D67 und D69 hat Regel 7 geändert (Lückenvermerke als Hinweis). Laut Diff richtig, kein Text verloren.
**Rauschen der Prüfmappe, kein Fund** (am Excel geprüft): D4057 «Mappe 2», D4058 «A 4», D8651 «STADTARCHIV ZÜRICH», D860
[ID 25], D3943 «(2 Stück)», D4024 «Alfred-Escher-Strasse». Die «fehlt»-Zeilen in D4054 sind Silbenreste; in D537, D4007 und
D860 ist der Text vorhanden.

**Unsicherheiten, nicht gezählt.** – D414 ist ein Grenzfall, wenn man den Absatz als Bemerkung zum Bestand liest; importiert wäre er auch dann nicht.
- D4054: «66 Normschachteln (Verbrauchsmaterial)» steht nur im Umfangsblock (Konvention Info).
- D73: Lagerung je Schachtel nur im Vorspann, Schachtel-Nr. leer (höchstens mittel).
- Einzeilige Bestände (D631, D4098, D8651, D8947): Übergabe und Herkunft im Darin der Bestandszeile, wie bisher akzeptiert.
**Spalten in D8_dateien.csv.** «ok» = kein neuer Fund (Bekanntes in der Bemerkung). «leer» = Abschnitt ohne Zeilen.
