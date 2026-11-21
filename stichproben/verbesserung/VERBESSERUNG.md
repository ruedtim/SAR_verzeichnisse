# Verbesserungsvorschlag B, C, A, E, N, O für findmittel_zu_scope.py

Dieser Patch ist ein unified diff gegen 8e2bd7f9 (sha256 8e2bd7f9191a11d6…), Stand 20.11.2026, 18:00.
- Den Umfang habe ich mit der Hauptsession abgesprochen: Regeln B, C, A («siehe auch», Nachruf) und danach N/O, also
  D3828 3.1., D3031 V.19. und D3324.
- Die Jubiläumsregel habe ich nur geprüft, nicht geändert. F, D3657, I, J, D151210 und die übrigen kritischen Fälle macht
  die Hauptsession.
- Gearbeitet habe ich nur in Kopien im Scratchpad. Die Projektdatei, `findmittel_excel/` und `testdaten_excel/` sind
  unverändert.

## Dateien

- `findmittel_zu_scope.patch`:
  - Wendet man ihn auf 8e2bd7f9 an, ergibt er genau `findmittel_zu_scope_vorschlag.py` (sha256 69d3eb38…, 5702 Zeilen).
  - Laut `patch --dry-run` passt er auch ohne Konflikt auf den Projektstand 3492fc3f von 18:00.
- `aenderungen_korpus.csv`: alle 83 Einheiten des Korpus, die sich gegenüber 8e2bd7f9 ändern.
- `aenderungen_testdaten.csv`: dasselbe für die Testdaten.
- `zusatz/`: zwei kleine Patches gegen 8e2bd7f9 für Bereiche der Hauptsession, nur als Anregung und **nicht** im Patch.
  - `F_fortsetzung.patch`: Fortsetzungen in `_ist_fortsetzung`.
  - `D3657_uebersichtszeile.patch`: Übersichtszeilen in `baue_einheiten`.
- `werkzeug/`: Gesamtlauf, Vergleiche und die Fallsets aus Runde 6 (unten).

## Testergebnisse (alle auf 8e2bd7f9 ohne bzw. mit Patch)

**Fallsets aus Runde 6.** Das Soll stammt aus den Befunden am PDF, gemessen wird am Lauf (`werkzeug/faelle/`):

| Fallset | ohne Patch | mit Patch |
|---|---:|---:|
| B und E: Zeiträume mit fernen Darin-Daten (`b_faelle.csv`) | 14 von 38 | 37 von 38 |
| C: Jahre im Text der Einträge ohne Spaltendatum (`c_faelle.csv`) | 2 von 12 | 10 von 12 |
| A: «siehe auch», Nachruf, dazu die 4 Jubiläumsfälle (`a_faelle.csv`) | 5 von 12 | 11 von 12 |

**N/O, kritische Fälle:**
- D3828 3.1.: «3. Freisinnige Partei Zürich 8, Ansprache über militärische Lage, o.D.» steht wieder im Darin. Er war um
  15:43 in keinem Blatt; jetzt sind 10 Wörter mehr erfasst.
- D3324: Die erfundene Signatur 2. ist weg; 1., 2., 3., 4. … tragen wieder ihre Titel.
- D3031 V.19. (Testdaten):
  - Die Posten «1 Äusseres …» bis «19 Anteilsschein …» stehen im Darin von «2. Photoarchiv».
  - «3. Diverses» und «4. Bauarchiv» (Posten 1–3, Schachteln 319–323, 1923–1986) sind eigene Einheiten.
  - Die Einheiten von D3031 gehen von 306 auf 291 zurück; der Rest der Datei ist unverändert.

**Gesamtlauf über alle 715 PDFs:**
- Es ändern sich 83 Einheiten in 33 Dateien. Ich habe jede angesehen: die Fälle aus Runde 6 über deren Befund, die übrigen
  am Darin bzw. an den Zeilen des PDFs. D3808 und D3324 habe ich am PDF-Text geprüft.

| Art | Einheiten |
|---|---:|
| Zeitraum weiter (B, A: echte Daten zurück) | 36 |
| Zeitraum enger (C: Vermerke und Folgezeilen weg; genauere Tage) | 17 |
| Struktur (D3324 umnummeriert) | 11 |
| nur Zeitraum-Quelle oder Prüfhinweis | 13 |
| anders / nur Darin | 6 |

| Kennzahl | ohne Patch | mit Patch |
|---|---:|---:|
| Einheiten | 49'331 | 49'330 (D3324: erfundene 2. weg) |
| «[ohne Titel]» | 34 | 34 |
| «Text erfasst» 100 % | 695 | 695 |
| überzählige Zeilen bei doppelten Schlüsseln | 10 | 10 |

Bei D149628 fehlt 1 Wort: «1935» steht jetzt nur noch in von/bis statt in der Anmerkung, weiter 100,00 %.

**Testdaten (11 PDFs):** Es ändern sich nur D149628 (dieselben 5 Zeiträume wie im Korpus) und D3031 (siehe oben).

**Neben den Testfällen sind mir aufgefallen:**
- D3018 02.2.1.: «Plan Kammerofen ¦ 28.05.1938» zählt jetzt (22.10.1893–28.05.1938); in Runde 6 «unklar».
- D3060 1: 1747–1979 statt 1783–1979; beide Anfänge kommen aus Lebensdaten in Registerauszügen, in Runde 6 «gleich».
- D3067 VI./VI.D.: 1684 statt 1744; Bildinhalt bzw. Lebensdaten, ebenfalls «gleich».
- D3718 4.2.2.: neuer Hinweis «Untereinheiten reichen über den Zeitraum hinaus (1897–1993)», richtig.
- Gruppen übernehmen die geänderten Zeiträume ihrer Untereinheiten (D1877 2./3./4., D3018 05.2., D3067 V., D150296 4.,
  D3718 4./4.2.).
- **Nebenwirkung D3808 4.:** Die «Beilagen» von 1945/46 nach der letzten Einheit stehen schon heute im Darin (Z350).
  Regel B hatte ihre Daten bisher verworfen; jetzt zählen sie: 1906–07.03.1946 statt 1906–1907. Ursache ist die
  Zuordnung der Schlussnotiz, nicht B.

## Jubiläum: nur geprüft (Stand 8e2bd7f9)

- **Richtig:**
  - D2534 2.1. = 1951;
  - D150589 16.2.10. = 1959;
  - D3620 6. 1902–2002 (die CD «100 Jahre … 1902 – 2002» zählt).
- **D2962 11.2.2.:** Das Ende 1962 stimmt («100 Jahre Männerchor St. Johann 1862-1962»), der Beginn 1821 nicht.
  - Er kommt aus «Der Männerchor Harmonie St. Gallen 1821-1921. Jubiläumsschrift zur Feier des 100-jährigen
    Vereinsbestandes».
  - Die Regel erkennt nur «N Jahre». In derselben Einheit gelten noch weitere Spannen als Laufzeit: «Hundert Jahre … 1841-1941»,
    «75jährigen Bestandes … 1852-1927», «75-jährigen Jubiläum … 1835-1910», «Jahrhundertfeier 1827-1927», «75jährigen
    Bestehens 1858-1933».
  - Das früheste echte Erscheinungsjahr in der Liste ist 1888. Ich habe nichts daran geändert.

## Die Änderungen

### 1. Regel B: Ausreisser nur noch bei Tippfehlern

Betroffen sind `_anschliessend`, neu `_tippfehler_jahre` und `RAHMEN_NACHLAUF`; dazu die Aufrufe in `zeitraum_aus_titel`
und `_darin_spalte`, die jetzt `rahmen` übergeben.
- **Bisher:** Ein Darin-Datum, das mehr als 35 Jahre vom Kern entfernt lag, fiel weg. Das traf in Runde 6 vor allem echte
  Daten (20 von 40 Fällen schlechter).
- **Jetzt:** Der Kern wird wie bisher bestimmt. Ein fernes Datum fällt aber nur noch weg, wenn es wie ein Tippfehler
  aussieht. Dafür muss eine andere Ziffer oder zwei vertauschte Nachbarziffern ein Jahr im Kern ergeben.
  Dazu muss mindestens eines dieser Kennzeichen zutreffen:
  - Ein einzelnes Datum liegt nach dem Ende des Bestandszeitraums laut Online-Archiv, mit 5 Jahren Spielraum:
    «25.09.1990» zwischen 1920 und 1922 (VII.197.); «1987» unter Postkarten 1897–1914 (VII.31.).
  - Eine ungewöhnlich lange Spanne hat ein Ende im Kern, und das ferne Ende liegt nach dem Bestandszeitraum
    («1902-1991», «1872-1991» in VII.83.) oder ergibt berichtigt eine kurze Spanne («Oktober 1846 bis März 1947» →
    1846–1847, VII.12.A.; «1857 - 1962» → 1957–1962, VII.174.).
- **Ausdrücklich echt** sind:
  - ganze ferne Spannen: «1961–1980» unter 1894 (IV.A.), «1989 – 1990» (V.G.c.43.);
  - Gruppen von fernen Einträgen: Bücher 1948–1959 unter 1901 (VII.191.), 16 Gasverträge 1898–1923 (V.G.c.43.);
  - einzelne Stücke vor dem Kern («Kochbuch ¦ 1746», VII.388.) und Nachträge im Bestandszeitraum («Kleber … ¦ 1987»,
    VII.190.);
  - lange Spannen ohne Tippfehler-Merkmal («Seeauffüllung 1830 – 1925», V.G.c.105.).
- Offen: D2735 9. «Januar 1950 - September 1967» erweitert den Titelzeitraum nicht, weil die Darin-Spalte nicht «trägt»
  (eine Jahreszeile unter drei Einträgen).

### 2. Regel E: Ein genaueres Titeldatum ersetzt die Darin-Erweiterung nicht

Betroffen ist die Erweiterungsstelle in `zeitraum_aus_titel`, neu das Feld `Einheit.darin_erweiterung`.
- **Bisher:** Wurde die Spalte um das Darin erweitert und dann durch ein genaueres Titeldatum ersetzt, ging die Erweiterung
  verloren. Die Anmerkung widersprach dann von/bis.
- **Jetzt:** Die Erweiterung bleibt:
  - D149628 26.2.4.: 09.1935–1938 statt 09.–10.1935 mit Anmerkung «1935; Darin: 1938»;
  - ebenso D149628 18.1.4. und D4054 12.4. Teil 2.
- Der Titelschnitt darunter ist unverändert.

### 3. Regel C: Nur Einträge ohne Spaltendatum, keine Vermerke

Betroffen sind der darin_daten-Block in `verarbeite` sowie neu `VERMERK_RE` und `SPIELZEIT_KOPF_RE`. `baue_eintraege`
bleibt unverändert.
- **Folgezeilen datierter Einträge zählen nicht mehr.** Die Datumsspalte steht auf der ersten Zeile eines Eintrags. Als
  Folgezeile gilt nur, was danach kommt und klar weiterläuft:
  - eingerückt, klein oder mit Anführungszeichen beginnend, nach Trennstrich oder Komma;
  - ohne Aufzählungszeichen, ohne Absatz und ohne eigenes Datum.

  Beispiele:
  - «Amtsperiode 1942 – 1946» unter «10. Referat … ¦ 1942» (VII.76.);
  - «Das Wetter am Sechseläuten 1864 – 1978» (VII.371.);
  - «Betriebszeit: April 1990 bis März 1991» im Buchtitel (VII.423.);
  - «Zürich 1930, Kopie» (VII.371.).
- **Eigene Einträge, die der Parser mit dem nächsten verbindet, behalten ihre Jahre.** Beispiele: «Finanzinspektorat, …
  Prüfungen 1983+1984» (V.C.c.81.), «Verschiedene fremde Inserate 1947-1954» vor «Saks Fifth Avenue ¦ 1956» (VII.409.).
- **Vermerke zählen nicht**, auch über zwei, drei Zeilen. Gemeint sind Übergabe-, Zuordnungs- und Archivvermerke sowie
  «Stand:»-Zeilen:
  - «Die Bücher wurden am 24. März 2017 … dem Stadtarchiv übergeben.» (VII.388.);
  - «… wurden im April 2009 vom Planbestand … zugeordnet» (VII.141.);
  - «bis 2006 unter der Archivsignatur» (VII.409.);
  - «Stand: 05.07.1994» (VII.2.);
  - «Ende 1995 wurde die Kommission …» (V.F.c.77.).
- **Spielzeit-Überschriften zählen nicht:** «Spielzeit 1965/66» (VII.209.) ergibt wieder 05.1966–05.2005.
- **Offen:**
  - D4054 14.3.3.: «… mit Fotos des Kapellmeisters 1865 und 1906» ist Bildinhalt.
  - D3231 3.10.: «e) Presseartikel 1930-1999» steht im Darin der Einheit; das ist eine Strukturfrage.

### 4. Regel A: «siehe auch» und Nachruf

Betroffen sind `VERWEIS_ZEILE_RE` (neu daneben `VERWEIS_AUCH_RE`), die Funktion `todesjahr` im darin_daten-Block und
`NACHRUF_RE`, dessen Gebrauch sich ändert.
- **«siehe auch», «s. auch» und «vgl.» sind zusätzliche Hinweise.** Sie verwerfen weder die eigene Zeile noch die Zeile
  davor. Nur der Text ab dem Hinweis zählt nicht für Regel C. Beispiele:
  - «- Protokolle der Vorsteherschaft ¦ 2000 – 2001» / «Siehe auch Akten …» → 1925–2001 (VII.371. 2.3.);
  - «… 4. April 2007 …; siehe» / «auch Sign. …» → 1985–04.04.2007 (VII.298. 4.3.1.).
  - Echte Verweise wie «siehe Abteilung V.H. b.3.», «Fortsetzung im …» und «eingegliedert» wirken wie bisher.
- **Die Nachruf-Regel** (nur das Todesjahr zählt) gilt nur bei einer Spanne ab 20 Jahren. Eine kurze Laufzeit mit einem
  Nachruf darin bleibt: «… mit Plänen und Nachruf auf Dr. Hermann Fietz ¦ 1928 – 1938» (V.B.c.59.).
  - Neu gilt die Regel auch für eine einzelne Jahreszeile unter dem Nachruf («In Memoriam Hans Fretz» / «1863 – 1925» →
    11.9.2. 1915–1932, VII.12.B.).
  - Sie gilt nicht für eine chronologische Liste unter «… enthalten u. a. Todesanzeigen» (VII.151. 7.5.1.).
- Offen: D2850 A. «30. Mai bis» / «1. Juni 1925» über zwei Zeilen ist eine Datumsform (Regel I, Hauptsession).

### 5. Regel N: Listenpunkt statt Tippfehler-Signatur

Betroffen ist die Tippfehler-Regel «26.» → 26.2. im Dezimalzweig von `lies_signatur`, neu das Feld
`Gliederung.listen_nr`.
- «3. Freisinnige Partei Zürich 8, …» direkt nach den Listenpunkten «1.» und «2.» unter «3.1.» wurde als Tippfehler für
  3.2. gelesen. Danach fiel er als Übersichtszeile weg und fehlte in allen Blättern.
- Jetzt gilt eine solche Nummer als nächster Listenpunkt, wenn direkt davor (gleiche Spalte, gleiche oder vorige Seite)
  die vorherige Nummer als Listenpunkt stand. Diese Nummer merkt sich der Dezimalzweig beim Zurückweisen.
- Der Fall V.B.c.54. «26. Tätigkeitsberichte» nach «26.1.» bleibt wie bisher.

### 6. Regel O: Stückzahlen statt Signaturen

Betroffen ist in `lies_signatur` die Regel mit `gl.punktnummern`; `lerne_punktnummern` selbst bleibt.
- Eine blosse Zahl ohne Punkt gilt jetzt auch dann als Stückzahl, wenn sie die Folge der Signaturen fortsetzt, aber
  eingerückt in der Textspalte steht (mehr als 12 pt rechts der letzten Signatur).
- **D3324:** «1. Caspar Wehrli» / «2 Rechnungen der Zehntloskaufkommission ¦ 1834, 1846» erfindet keine Signatur 2. mehr.
- **D3031 V.19.:** Die Posten 1–19 unter «2. Photoarchiv» sind keine Signaturen V.3.–V.19. mehr, die echten «3. Diverses»
  und «4. Bauarchiv» sind Einheiten. Die Aufzählung nach «… enthält:» war dafür nicht nötig.

## Hinweise an die Hauptsession

- **`baue_eintraege` am Stand d94d7ecf bzw. 5813fd78:** Die neue Regel hängt einen Punkt «- …» an einen Eintrag mit offenem
  „ an (gedacht für «„Hans Sahl» / «– Ein Narr der Aufrichtigkeit“», VII.200.). Bei einem nie geschlossenen „ verbindet
  sie die folgenden Punkte.
  - Beispiel an d94d7ecf: In D150536 9.3. bleiben 8 statt 23 Einträge, weil alles an «Acht Taschentücher „75 Jahre Zunft …»
    hängt. Insgesamt waren es 23 Einheiten in 13 Dateien.
  - An 5813fd78 sind es noch 15 Einheiten in 8 Dateien, zum Beispiel:
    - D2123 V.H.c.107. (390 → 375);
    - D174277 VII.275.:21/22/30;
    - D149628 4.1.41., 4.1.55., 6.5.6., 20.1.2.6., 20.1.2.13.;
    - D2937 B.3.0., D3709 2.2., D4175 1.C.3., D10675 745.52;
    - D151210 4.2.6.8., 6.32.
  - Die Zählung ist automatisch: weniger Einträge und neu « - » im Darin, gegenüber 8e2bd7f9, nicht am PDF geprüft.
- **`zusatz/F_fortsetzung.patch`**, allein auf 8e2bd7f9 getestet: 6 Einheiten ändern sich; das Fallset `f_faelle.csv`
  geht von 0 auf 5 von 7.
  - Neu gilt als Fortsetzung: ein gleicher Titel ohne Jahreszahlen, Zählung «(I)»/«(II)» und «Nachtrag» (VII.269.
    «Konzerte (I)» / «Konzerte 1926 - 1967 (II), Nachtrag»; VII.212. Jahresberichte); ein Titel aus blosser Zählung oder
    Zeitangabe (VII.151. 5.5.3. «(I)», VII.298. «Saison 1985/86»); der eigene Titel mit Zeitangabe (VII.93. «Akten 2000 –
    2005»).
  - Der Hinweis «zweimal hintereinander – Tippfehler?» schliesst nicht mehr aus.
  - Ein zeitlicher Anschluss allein ist zu breit: Er vereinigte Locher-Objekte (VII.308.) und ergab in X.G.188.
    1780–1975.
- **`zusatz/D3657_uebersichtszeile.patch`**, allein auf 8e2bd7f9 getestet: Eine erste Nennung, unter der schon
  Untereinheiten mit Darin oder Datum stehen, fällt nicht als Übersichtszeile weg. Es ändert sich nur D3657: 6. Anbau
  1950–1953 mit 6.1.–6.3., die zweite «6.» wird Teil 2.

## Anwenden und nachprüfen

```bash
patch findmittel_zu_scope.py < stichproben/verbesserung/findmittel_zu_scope.patch
```

Danach ein Gesamtlauf in einen eigenen Ordner und die Fallsets:

```bash
uv run --with openpyxl python -I stichproben/verbesserung/werkzeug/faelle/pruefe_faelle.py stichproben/verbesserung/werkzeug/faelle/b_faelle.csv <alter_ordner> <neuer_ordner>
```

Die Werkzeuge in `werkzeug/`:
- `lauf.sh`: paralleler Gesamtlauf in einen Scratchpad-Ordner, 8 Prozesse. Der Zeilen-Cache ist über `CACHE=…` wählbar;
  ein erster Lauf dauert rund 90 s, mit Cache rund 25 s.
- `vergleich.py`: Einheiten zweier Läufe über die ID, mit Art der Zeitraum-Änderung.
- `vergleich_sig.py`: dasselbe über (Signatur, n-tes Vorkommen), für Strukturänderungen.
- `kennzahlen.py`: Einheiten, «[ohne Titel]», Text erfasst, doppelte Schlüssel.
- `zeige.py`: eine Einheit in zwei Läufen.
- `faelle/*.csv` mit `pruefe_faelle.py`: Soll-Zeiträume aus Runde 6, je PDF und ID im Korpus `findmittel_pdf/pdf`.
  Die Datei `f_faelle.csv` gehört zum F-Zusatz.
