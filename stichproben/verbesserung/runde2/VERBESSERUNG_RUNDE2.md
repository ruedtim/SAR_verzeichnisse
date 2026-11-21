# Verbesserungsrunde 2 für findmittel_zu_scope.py

Der Patch ist ein unified diff gegen fde790ac (sha256 fde790ac3da62433…), den Stand von Nachprüfung 7, Stand
21.11.2026, 15:35.
- **Umfang:** mit der Hauptsession abgesprochen.
  - D3612 3.A./3.E. (erfundene Einheiten);
  - D3808 4. (Beilagen);
  - D176795 2.2.2. «(-1838)»;
  - D149628 `_an_tabstopp`.
  - Dazu kommen Fälle, die beim Prüfen der Nebenwirkungen aufgetaucht sind: D2853, D2623, D2655 und D152400.
- **Nicht angefasst (Hauptsession):**
  - D151210 (Teile, Doppelpunkt, Tabulator);
  - Änderung 2 (Fortsetzungen);
  - erster Listenpunkt;
  - Jubiläum;
  - D3793 5.9.3.;
  - « - »;
  - D3861 7.1.;
  - der Zeitraum der Teile mit eigenem Titel.
- Gearbeitet habe ich nur in Kopien im Scratchpad. Die Projektdatei, `findmittel_excel/` und `testdaten_excel/` sind
  unverändert.

## Dateien

- `findmittel_zu_scope_runde2.patch`: 130 geänderte Zeilen in 12 Abschnitten.
  - Auf fde790ac angewendet, ergibt er genau `findmittel_zu_scope_vorschlag_runde2.py` (sha256 e8a987ec…, 6051 Zeilen).
  - Er passt ohne Fuzz auch auf die neueren Projektstände 4abd90bd (15:08) und 5e333035 (15:12). Dort wirkt er gleich:
    dieselben 188 Einheiten in 66 Dateien, auch nach Art der Änderung.
- `aenderungen_korpus.csv`: die 188 Einheiten des Korpus, die sich gegenüber fde790ac ändern.
- `aenderungen_testdaten.csv`: dasselbe für die Testdaten (11 Einheiten).
- `textverlust.csv`: je Datei die Wörter, die nirgends mehr stehen, und die neuen Schlussvermerk-Zeilen (siehe unten).
- `werkzeug/`:
  - `runde2_faelle.csv` mit `pruefe_runde2.py`: 34 Fälle dieser Runde, davon 5 Kontrollfälle.
    - Geprüft werden Einheitenzahl, Vorkommen einer Signatur, Titel, Darin, von/bis, Schlussvermerke und «Nicht
      übernommen».
    - Die Einheiten werden über Signatur und n-tes Vorkommen gefunden, nicht über die ID.
  - `textverlust.py`: Wörter aus Titel, Darin, Anmerkung und Schlussvermerken, die im neuen Lauf in derselben Datei
    fehlen. Trennstriche in den Schlussvermerken zählen in beiden Lesarten.
  - `zeige_diff.py`: alle geänderten Felder einer Diff-Liste in zwei Läufen.
  - `wo_wort.py`: wo ein Wort in zwei Läufen steht.
  - Gesamtlauf und Vergleich wie in Runde 1 (`../werkzeug/`).

## Testergebnisse (fde790ac ohne bzw. mit Patch)

| Prüfung | ohne Patch | mit Patch |
|---|---:|---:|
| Fallset Runde 2 (`runde2_faelle.csv`, 34 Fälle) | 5 (nur die Kontrollfälle) | 34 |
| Fallset A (Runde 6) | 11 von 12 | 11 von 12 |
| Fallset B | 37 von 38 | 37 von 38 |
| Fallset C | 10 von 12 | 10 von 12 |
| Fallset F | 5 von 7 | 5 von 7 |

| Kennzahl | ohne Patch | mit Patch |
|---|---:|---:|
| Einheiten | 49'330 | 49'252 (D3612 −67, D2853 −8, D3505 −2, D2655 −1) |
| «[ohne Titel]» | 34 | 34 |
| «Text erfasst» 100 % | 695 | 695 |
| überzählige Zeilen bei doppelten Schlüsseln | 10 | 10 |

Auf 5e333035 gilt dasselbe: 49'320 → 49'242 Einheiten, «Text erfasst» 695 → 695, Fallset Runde 2 5 → 34.

**Gesamtlauf über alle 715 PDFs:** Es ändern sich 188 Einheiten in 66 Dateien. Ich habe jede angesehen. Die Tabstopp-Fälle
und die Strukturfälle habe ich am PDF-Text geprüft, alle 190 neuen Schlussvermerk-Zeilen gelesen und die Einheiten, die
ihren Zeitraum verlieren, am PDF nachgesehen.

| Gruppe | Einheiten | Dateien |
|---|---:|---:|
| D3612 (A, B, C, G) | 79 | 1 |
| C Schlussblock | 54 | 46 |
| F Datumsspalte am Tabstopp | 31 | 15 |
| D2853 (B) | 20 | 1 |
| A Initialen, Autorentabelle (D2623, D2655) | 3 | 2 |
| E Lebensdaten (D176795) | 1 | 1 |

**Textverlust: keiner.** Was nach `textverlust.py` nirgends mehr steht, ist:
- Text aus der Datumsspalte, der vorher mitten im Titel stand und jetzt in von/bis steht («1980-1983», «undatiert», «o. D.»);
- nicht mehr nötige Anmerkungen wie «1906-1907; Darin: 23.10.1945–07.03.1946»;
- die Tabellenköpfe «Nr. Gegenstand Datum» in D3612. Sie stehen jetzt in «Vollständigkeit» als Tabellenkopf.

Verschobener Text steht in den Schlussvermerken des Blatts Info, die «Text erfasst» nicht mitzählt.

**Testdaten (11 PDFs):** Es ändern sich nur:
- D149628: die 9 Tabstopp-Fälle wie im Korpus;
- D3186 11.32.: «Der Archivbestand umfasst gegenwärtig 24 Schachteln.» und «Urs Scherer / 11. November 1996» stehen jetzt in
  den Schlussvermerken;
- D9983 6.: Die «Bemerkungen zu diesem Teilbestand» stehen jetzt in den Schlussvermerken. Der Zeitraum geht von 1833–01.2010
  auf 1840–1873 (geschätzt aus dem verbleibenden Darin).

## Die Änderungen

### A. Initialen sind keine Buchstaben-Signaturen

Betroffen ist `baue_vorkommen` mit drei Prüfungen vor `lies_signatur`. Neu sind `ist_namenstabellenzeile` und
`_spaltenanfaenge`.
- **Initiale nach einer Personenbezeichnung:** Am Ende der Zeile davor steht eine Personenbezeichnung
  (`PERSONENBEZEICHNUNG_AM_ENDE_RE`, die es schon gibt).
  - Beispiel: «- Schreiben des Stadtpräsidenten R. Billeter an Herrn ¦ 25. Mai 1912» / «A. Bodmer» (D3612).
  - Es entstehen keine erfundenen Einheiten 3.A. und 3.E. mehr.
- **Zwei Initialen vor einem Nachnamen:**
  - «B. G. Mantegazzi, Hans Waldmann, Komposition (Marsch) …» unter «Mappe 6» (D3612): Es gibt keine Einheit 6.B. mehr.
  - «C. O. Gleim, Dr. K. Moser. O. O. u. J. …» als Folgezeile eines Listenpunkts (D2623).
    - Bisher entstand eine erfundene Einheit «C.», und 40 Zeilen standen als «Text vor der ersten Signatur» in keinem
      Blatt.
    - Jetzt gibt es eine Einheit V.L.170. mit 1871–1929, und alle 518 Wörter sind importiert.
- **Autorentabelle:** «D. Lasserre ⟨Tab⟩ Der 4. November 1440 ⟨Tab⟩ Dezember 1940, Heft 8» (D2655).
  - Die Zeile beginnt mit Initiale(n) und Namen und hat drei Spalten.
  - Mindestens zwei der 15 Zeilen davor haben keine Initiale, stehen am selben x und haben dieselbe Titelspalte («Ernst
    Fischer ⟨Tab⟩ Ibsen und das Dritte Reich ⟨Tab⟩ April 1940 …»).
  - Vorher gab es zwei erfundene Einheiten «E.» und «G.», und 60 Zeilen waren nicht importiert.
  - Jetzt folgt D2655 der Konvention «ohne Signaturen»: eine Zeile für den Bestand mit 1939–1942 und 1'391 Wörtern.
- Sonst ändert sich durch A keine Datei.

### B. Nummernlisten ohne Punkt sind keine Signaturen

Betroffen sind drei Stellen:
- `lerne_punktnummern`: zählt nur noch die Signaturspalte.
- `lies_signatur`: Die `gl.punktnummern`-Regel erkennt die Kette über `gl.listen_nr`.
- `baue_vorkommen`: Die Regel «fette Zwischenüberschrift» greift nicht bei einer Listenzeile.

**D3612:** unter «2. Numerierte Akten und Materialien» die Liste «Nr. Gegenstand Datum» / «1 Hans Waldmann …» bis «59».
- **Bisher:** 3–8 wurden zu Signaturen und die echten 3.–8. zu deren Teil 2.
- **Warum es nicht schon an `punktnummern` scheiterte:** Die Regel war aus. Tagesangaben umbrochener Zeilen («24. Juli 1935
  …», eingerückt) unterbrachen die Folge 1., 2., 3.
  - Jetzt zählt nur die linkeste Spalte mit mindestens 3 Nummern.
  - Eine blosse Zahl, die die Kette der eben verworfenen Listennummer fortsetzt (gleiche Spalte, gleiche oder vorige
    Seite), ist ebenfalls keine Signatur.
- **Ergebnis:** D3612 hat 12 Einheiten statt 79.
  - Die Liste steht im Darin von 2., die Korrespondenz mit 84 Schreiben im Darin von 3.
  - Der Schlussvermerk steht im Blatt Info.

**D2853:** der Aktenplan «Nummer Inhalt Mappen» / «4 Rechtsverhältnisse zur Stadt Zürich 13» … «11 Denkschrift 33, 34,
35» unter «3. Akten».
- **Bisher:** Daraus wurden die Einheiten 4.–11., zweimal mit 4.
- **Jetzt:** Die Zeilen stehen im Darin von 3., und D2853 hat 14 statt 22 Einheiten.
- **Letzte Zeile:** «11 Denkschrift …» ist fett und steht direkt vor «4. Drucksachen». Sonst hätte die Regel
  «fette Zwischenüberschrift» sie zur Überschrift von 4. gemacht.
  - Darum gilt jetzt: Eine Zeile, deren Nummer gerade als Listenpunkt verworfen wurde und deren Vorgängernummer im Darin
    steht, ist keine Überschrift.

### C. Schlussblock nach der letzten Einheit

Neu sind `SCHLUSSNOTIZ_RE` und eine Regel in `baue_vorkommen` direkt nach `ist_schlussvermerk`.

**Bedingungen:**
- Die Zeile steht in der Signaturspalte der letzten Einheit, deren Text eingerückt ist (mehr als 15 pt).
- Davor ist ein Absatz (mehr als 25 pt).
- Sie ist kein Aufzählungspunkt.
- Sie beginnt wie eine Notiz zum Bestand: «Anmerkungen:», «Beilagen:», «Literatur», «Zu diesem Bestand vgl. auch»,
  «Der Bestand wurde … übergeben», «Lagerung», «Total:», «Stand: …», «Name / Datum».
- Sie steht auf der letzten Seite oder in den letzten 15 Zeilen.
- Danach folgt keine Signatur mehr.

**Wirkung:** 190 Zeilen in 47 Dateien stehen jetzt in den Schlussvermerken statt im Darin der letzten Einheit. Ich habe
alle gelesen. Es sind Übergabe- und Bearbeitervermerke, Anmerkungen, Literatur, Benützung, Lagerung und Umfang, also
Notizen zum Bestand. Beispiele:
- **D3808 4.:** Die Beilagen von 1945/46 zählen nicht mehr. Statt 1906–07.03.1946 gilt 1906–1907 (Z350, Nebenwirkung aus
  Runde 1).
- **D3505 7.3.:** Die Schachtelübersicht im Schlussblock («1. Protokolle 1840 - 1994», «5. Protokoll und Rechnungen …»)
  erfindet keine Teile 2 und 3 mehr.
- **D3793 8.:** «Dubletten» hat jetzt keinen Zeitraum mehr. Das PDF nennt keinen, 1929–1934 kam aus den «Anmerkungen zu
  diesem Bestand».
- **D134644 16.:** bis 1992 statt 05.09.2006 (Bearbeitervermerk).
- **Datumslose Einheiten:** D2940 12. «Diverses» und D3329 6. «Bibliographie» haben im PDF kein Datum. Ihre bisherigen
  Zeiträume kamen nur aus den Schlussnotizen.

**Kontrollfälle:** Eine erste, breitere Fassung ohne `SCHLUSSNOTIZ_RE` hatte echten Inhalt verschoben. Diese Fälle
bleiben jetzt im Darin:
- D149825 272. «Messingpokal, versilbert, mit Deckel»;
- D149835 7. «Nc 4-6 mit Beilage …»;
- D3089 X. Textbücherliste.

### D. Spalten bleiben im Schlussvermerk

Neu ist `schlusszeile`, eingesetzt an den drei Stellen, die in `baue_vorkommen` Schlussvermerke anhängen.
- **Bisher:** Die Datums-, Umfang- und Schachtelspalte einer Schlussvermerk-Zeile fiel weg, zum Beispiel bei «V.J.
  b.202.17. Städtisches Waisenhaus Entlisberg ¦ 1947-1956» (D152400).
- **Jetzt:** Die Spalte wird angehängt.
- Betroffen sind nur die Schlussvermerke im Blatt Info: D152400, D3293 und 14 Zeilen in D2850 (dazu unten).

### E. Lebensdaten «(-1838)» sind keine Laufzeit

Betroffen sind `PERSON_RE` (erweitert), neu `LEBENSDATEN_KLAMMER_RE`, `zeitraum_aus_titel` und `texte_c` in
`verarbeite`.
- **D176795 2.2.2.:** «Ludwig Heinrich Friedrich von Podewils (-1838)» / «Vertrag über das Rittergut Weisdorf, 1810» ergibt
  1810 statt 1810–1838.
- **Was als Lebensdaten gilt:** nur eindeutige Angaben wie «(geb. 1865)», «(-1838)» oder «(1765-)».
  - Sie fallen aus den Titeldaten und aus dem Text der Einträge ohne Spaltendatum.
  - Ein blosses «(1937)» bleibt Ereignisdatum, zum Beispiel bei den Streiks 1937 in D1180 5.1.–5.4.
  - Eine erste Fassung über `PERSON_RE` hatte 60 Einheiten in 22 Dateien den Zeitraum genommen.

### F. Datumsspalte nach einer Präposition (`_an_tabstopp`)

- **Bisher:** Nach «vom», «von», «im», «an», «und» … wurde nie an einem Tabstopp getrennt, auch bei grosser Lücke.
- **Jetzt:** Das gilt nur noch bei einer Lücke unter 10 pt.
- **Wirkung:** 31 Einheiten in 15 Dateien, alle am PDF geprüft. Die Datumsspalte steht nicht mehr mitten im Titel:
  - D149628 20.1.1.7. «… im 1980-1983 Ausland …»;
  - D109662 2.3.2., D3833 10., D3545 3.2.6. und D149825 131.;
  - D460 1.5. «… am 1927 – 1955 1. März“, Zürich» → «… am 1. März“, Zürich 1927»;
  - D1880 H.II. «Bullinger-Denkmal am Schachtel 360 Grossmünster»;
  - D3828 14.: «o. D.» steht nicht mehr im Titel;
  - D3761 2.2.: «Dez. 1991» steht nicht mehr im Text, bis 12.1991;
  - D150829 6.4.: Der Titel ist wieder vollständig.
- **D3672 1.1.1020.:** Die Einheit hat jetzt den Titel «Gertrude Emerson Sen (??) an Alice Boner, Almora», von 13.06.1944
  und das Darin «Krankheit von Alice, …».
  - Wie bei den Nachbarn 1.1.1018., 1.1.1019. und 1.1.1021. steht das Datum in von/bis und nicht mehr im Titel.
  - 1.1.1017. behält es wegen des Doppelpunkts. Das war schon vorher so.
- **D149628 23.1.1.829.:** von/bis ist jetzt 01.1983–02.1983 aus dem Titel («Januar / Februar 1983»), die Spielzeit
  1982-1983 steht in der Anmerkung.
  - 23.1.1.410. behält dagegen die Spielzeit 1950–1951 trotz «10. Juni 1951».
  - Das gehört zur Regel «Zeitraum der Teile» der Hauptsession. Ich habe es nicht geändert.

### G. Tabellenkopf «Gegenstand»

- **Änderung:** `KOPFWORTE` enthält jetzt «gegenstand». Damit steht «Nr. ¦ Gegenstand ¦ Datum» nicht mehr im Darin von
  D3612 2., 3. und 4.
- **Fehler im bestehenden Muster:** `TABELLENKOPF_RE` beginnt mit `^(?:Signatur|Saison|Nr\.)\b`. «Nr.» vor einem
  Leerzeichen passt nie, weil zwischen «.» und « » keine Wortgrenze liegt.
  - Ich habe das nicht geändert. Richtig gestellt würde jede Zeile «Nr. … Titel …» zum Tabellenkopf.

## Neue Funde ausserhalb dieser Runde (nicht geändert)

1. **D2850 (VII.109., Nachlass Emil Klöti), kritisch.** Der Fehler steckt schon in fde790ac und in der Excel von 18:09.
   - **Was falsch läuft:** Ab Einheit 48 entgleist die Gliederung.
     - Die Unterlisten «A.» und «B.» der Publikationen werden zu Signaturen: VII.109.:A. (zweimal), B. und B.5.
     - Ebenso die Daten «2.1939» und «12.1961» der Referate-Liste: B.2.1939. und B.12.1961.
   - **Folge:** Die echten Einheiten 49–66 fehlen als Einheiten.
     - Das sind «49 Schriften zum Proportionalwahlrecht» bis «66 Schweizer Armee- und Zivilschutzgasmaske».
     - Ihr Text steht im Darin von B.12.1961. und in 135 Schlussvermerk-Zeilen, ab «Stadtarchiv Zürich» in der Liste der
       Briefe N–Z.
   - **Warum es nicht auffällt:** «Text erfasst» zeigt 100 %, weil Schlussvermerke nicht mitzählen. D2850 hat 54
     Einheiten.
   - In den bisherigen Nachprüfungen kam D2850 nur mit einem Zeitraumfund vor (VII.109.:A., Runde 5/6).
2. **`TABELLENKOPF_RE`:** `Nr\.\b` passt nie (siehe G).
3. **D3672 1.1.1017.:** «21.5.1944:» bleibt im Titel, bei den Nachbarn nicht (gering).

## Hinweise an die Hauptsession

- **D3505 7.3.:** C löst den Fall aus Runde 1 (Teile 2/3). Falls es dafür schon eine eigene Änderung gibt, bitte
  abgleichen.
- **D3808 4.:** C löst Z350 aus Nachprüfung 7.
- **Neuere Projektstände:** Der Patch passt auf 5e333035. Die Änderungen der Hauptsession seit fde790ac berühren keine
  der Stellen. Getestet habe ich das mit Gesamtläufen 4abd90bd bzw. 5e333035 ohne und mit Patch.

## Nachtrag: Punkt 2 (Zeitraum der Teile mit eigenem Titel) und D3793 5.9.3.

Den Nachtrag hat die Hauptsession nach diesem Bericht in Auftrag gegeben. Er steht in `punkt2/`:
- `VERBESSERUNG_PUNKT2.md`;
- `findmittel_zu_scope_punkt2.patch` gegen «5e333035 + Runde 2»;
- `findmittel_zu_scope_runde2_punkt2_auf_5e333035.patch`: beide Teile in einem Patch gegen den Projektstand 5e333035.

Punkt 2 ändert 35 Einheiten in 7 Dateien. Das Fallset `werkzeug/punkt2_faelle.csv` geht von 12 auf 38 von 38; die übrigen
Fallsets und die Kennzahlen bleiben gleich.

## Anwenden und nachprüfen

```bash
patch findmittel_zu_scope.py < stichproben/verbesserung/runde2/findmittel_zu_scope_runde2.patch
```

Danach einen Gesamtlauf in einen eigenen Ordner machen (`../werkzeug/lauf.sh`) und das Fallset prüfen:

```bash
uv run --with openpyxl python -I stichproben/verbesserung/runde2/werkzeug/pruefe_runde2.py stichproben/verbesserung/runde2/werkzeug/runde2_faelle.csv <alter_ordner> <neuer_ordner>
```

Den Textverlust gegenüber dem alten Lauf prüft dieser Aufruf:

```bash
uv run --with openpyxl python -I stichproben/verbesserung/runde2/werkzeug/textverlust.py <alter_ordner> <neuer_ordner> textverlust.csv
```
