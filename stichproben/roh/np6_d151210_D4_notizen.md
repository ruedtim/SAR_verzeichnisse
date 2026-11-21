# D151210 (VII.200. Schauspielhaus Zürich AG) – Vollprüfung D4, PDF-Seiten 319–424, Stand 15:43

## Überblick

- **Umfang:** 106 Seiten, 1038 Einheiten mit PDF-Seite 319–424. Dazu kommt ID 2124 (6.52.), die auf S. 318 beginnt und auf S. 319 weiterläuft. Der Bereich reicht von 6.52. (Rollenbücher) über 7.–15. bis zu den Schlussvermerken.
- **Vorgehen:**
  - Die PDF-Zeilen wurden mit pdfplumber gelesen, mit denselben Parametern wie das Skript.
  - Daraus entstanden 1039 Blöcke: Signaturzeilen sowie «Teil n»-Zeilen ohne Signatur.
  - Diese Blöcke wurden der Reihe nach 1:1 den Excel-Einheiten zugeordnet.
  - Automatisch abgeglichen wurden: Signaturfolge, Wörter je Block (Textverlust oder Text bei der falschen Einheit), Hierarchie, Ebene, Stufe, Teil-Nummern, Titel/Darin-Grenze, Zeilenverbindungen und Zeiträume.
  - Danach wurde jede Seite neben dem Excel gelesen.
  - Hilfsdateien liegen in `$S/np6/tmp_d4/`, unter anderem `review_k.txt` (Seite für Seite).
- **Gliederung und Signaturen:**
  - Alle Signaturen des PDFs sind da und in PDF-Reihenfolge. Keine Signatur ist erfunden.
  - Parent, Ebene, Stufe und übergeordnete Signatur stimmen bei allen 1039 Einheiten.
  - Einzige Ausnahme ist 8.1.1.44., siehe unten.
  - Die 58 Treffer «nur Excel» in `vp_signaturen.csv` sind Fehlalarme. Gründe: ausdrückliche «Teil 1»-Zeilen ohne Signatur (8.1.1.x) und «7.2.1»/«15.2» ohne Schlusspunkt. Im Excel stehen dafür korrekt VII.200.:7.2.1. und VII.200.:15.2.
- **Text:** Wort für Wort ist jeder PDF-Block bei der richtigen Einheit. Es gibt keinen Textverlust. Was in einer Einheit fehlt, sind nur Datumswörter (stehen in von/bis bzw. Anm) und «Schachtel» (steht in der Schachtel-Spalte).
- **Teil-Nummern (Regel G):** Überall eindeutig und aufsteigend, ausser bei 8.1.1.44. Die Titel «…, Teil n» haben dieselbe Nummer, und die im PDF genannten «Teil n» stimmen mit dem Excel überein.
  - Seit 13:15 wurden 90 Teile neu nummeriert (6.61., 6.62., 8.1.7.1., 8.3.1.x, 8.3.2.x). Das ist richtig: die erste Nennung ist Teil 1, die Teile folgen ab 2.
  - Bei 8.1.1.x steht die Serie ohne Teil-Nummer neben dem ausdrücklichen «Teil 1» des PDFs. Das ist kein doppelter Schlüssel.
- **Schachteln** (nur in 11.1./11.2./11.3.) sind alle richtig, auch die Wechsel in den Zeilen «11.1. Schachtel 2» und «Schachtel 3». Umfang ist in D151210 nirgends gesetzt.
- **Schluss und Schlussvermerke:**
  - Die letzte Einheit ist VII.200.:15.5.3. «Schauspielhaus Extra, lose» (1984–1989). Sie hat kein Darin.
  - Im Blatt Info stehen genau die 5 Zeilen des PDFs (S. 424), vollständig und in der richtigen Reihenfolge, von «Der Bestand VII.200. umfasst 2159 Schachteln und 4 Mappen.» bis «Überarbeitung Verzeichnis: Anja Huber, Oktober 2019».
  - Nichts aus dem Verzeichnis ist in die Schlussvermerke geraten, und kein Schlussvermerk steht im Darin.
- **Ergebnis:** 28 Fundzeilen für 137 Einheiten. Davon 1 kritisch (2 Einheiten), 19 mittel (111 Einheiten, inkl. 7 Folgeeinheiten bei Gruppen-Zeiträumen) und 8 gering (29 Einheiten).
  - Fast alles bestand schon um 13:15 (Regel «vor 13:15»).
  - Neu seit 15:43 ist nur die halbe Datumsangabe im Titel (Regel J, 4 Fälle).
  - Bereits bekannt war M13 aus Z292 (Runde 5). In diesem Bereich sind es noch 7 Fälle.

## Fehler nach Art

1. **Gliederung / Teil-Nummer (kritisch, 1 Zeile):** VII.200.:8.1.1.44. (S. 356).
   - Im PDF steht die Signatur jeweils eine Zeile über ihrem «Teil n». Für Teil 2 steht sie auf der Zeile «Don Carlos von Friedrich Schiller», für Teil 3 und 5 am Zeilenende.
   - Das Skript macht daraus ID 2444 «Teil 6» mit dem Titel «Don Carlos …». Teil 1 (ID 2443) bleibt leer, und die Teile folgen in der Reihenfolge –/1/6/2/3/4/5.
   - Das PDF kennt nur Teil 1–5. Die Hauptsession wurde dazu schon informiert.
2. **Titel vom Nachbarteil, M13 (mittel, 7 Einheiten):**
   - 6.62. T5/T6 «Gorki, Maxim: Nachtasyl, Teil 5/6»
   - 8.1.1.44. T2–T5 «Don Carlos von Friedrich Schiller, Teil n»
   - 8.3.2.14. T5 «Die Ratten (…), Teil 5»
   - Ursache ist immer ein vorangehender Teil, dessen «eigener Titel» nur ein Listeneintrag ist (Punkt 3).
3. **Listeneintrag als Teil-Titel (mittel, 5 Einheiten):** 6.62. T4, 8.3.1.18. T3 «Porträts von L. Versell», 8.3.1.19. T3 «Ein Bruderzwist in Habsburg (…)», 8.3.2.6. T3 (zwei Einträge als Titel) und 8.3.2.14. T4 «Die Ratten (…)».
   - Folgefehler beim Zeitraum: 2682 hat Genau 30.12.1959, 2726 hat Genau 11.09.1965.
4. **Darin falsch getrennt, M10 (mittel, 60 Einheiten in 7 Sammelzeilen).** Das ist der grösste Block.
   - **a) Verschobener Zeilenumbruch des PDFs nicht repariert (39 Einheiten).** Der Anfang des nächsten Eintrags steht am Zeilenende, vor allem in den Stücklisten «Titel von Autor» unter 8.1.1.x (28). Beispiele:
     - «Der lebende Leichnam von Leo N. Tolstoi Regen und Wind von Merton Hodge»
     - «… Priestley Santa» / «Cruz von Max Frisch»
     - «Elektra von Sophokles Don» / «Juan von Molière»
     - ebenso in 8.2.3.x, in 6.53./6.54. und in den Klammerlisten 8.3.1.4./10./11. («Mira Bell (…) König» / «Johann (…)»)
     - Gut gelöst ist die Reparatur bei den Rollenbuch-Listen «Name, Vorname: Werk» (12 Fälle) und bei vollständigen Klammereinträgen in 8.3.x (rund 30 Fälle).
   - **b) Zwei oder mehr vollständige PDF-Zeilen zu einem Eintrag verbunden (26 Einheiten):** Die erste Zeile reicht fast bis an den Rand, oder eine Klammer bleibt offen. Beispiele:
     - «Göttin, versuche … Treichlinger Penthesilea von Heinrich von Kleist»
     - 8.1.8. mit drei Paaren
     - 8.2.3.39. mit drei Plakaten in einem Eintrag
     - 8.3.1.8. T4 mit fünf Einträgen in einem; im PDF fehlt dort «)» nach «Steckel»
     - 14.1. «Korrespondenz … Zürich Korrespondenz über Schenkungen»
5. **Angeklebte Signatur (gering, 10 Einheiten):** «Weh dem, der lügt von Franz Grillparzer 8.1.1.22.» usw. Die Signatur steht im PDF am Zeilenende, «Teil n» folgt bei x=82. Teil und Nummer sind trotzdem richtig.
6. **Titel/Darin-Grenze (mittel):**
   - Doppelpunkt-Teilung mitten im Satz, 6 Einheiten: 11.1. T19 «… Neuen Schauspiel AG von» / Autorenliste, die Plakate 13.3.3. T5/T10, 13.3.8. T4, 13.3.9. T11 und 13.5. T2.
   - Titel nach der ersten Zeile abgeschnitten: 11.1. T17 («… Therese Giehse, Ernst» / «Ginsberg, …»).
   - Titeldatum mitten aus dem Satz entfernt, 2 Einheiten: 13.3.3. T2 «Premiere: (Grafik …», 14.3.3. «Schoch geb., Schweizer …».
7. **Zeitraum (mittel):**
   - **Publikationen 11.1./11.2. (11 Einheiten):** Themenzeitraum oder Lebensdaten im Buchtitel werden mit dem Erscheinungsjahr vereinigt, z. B. Mittenzwei 1933–1979 statt 1979 und «Oskar Wälterlin, 30. August 1895–4. April 1961. Ansprachen …» 30.08.1895–04.04.1961. Folgen: 11.1. 1933–2008, 11.2. 30.08.1895–1997 und ein Hinweis bei 11.
   - **14.3.3.:** «geb. 26.04.1940» wird als Zeitraum genommen; 14.3. und 14. beginnen dadurch 1940.
   - **7.3.50./7.3.51.:** «Signatur nicht belegt (sec, 07.12.2023)» ergibt Genau 07.12.2023, 7.3. reicht bis 2023.
   - **8.1.7.1.:** Das Ausstellungsdatum «Juni 1988» gilt als Zeitraum. Die Teile 2–12 («Fotos 1932» … «Fotos 1938») erben es.
   - **11.3. T2:** «ab 18. Juni bis 23. August 1961» wird nur zu «bis 23.08.1961».
   - **13.3.9. T11:** Genau 1984 aus dem Stücktitel «Chile 1984» statt der Premiere 10.02.1989.
8. **Gering:**
   - Regel J, neu seit 15:43: Bei 7.4.1.9. und 15.2.3./5./6. bleibt die erste Zeitangabe im Titel, die zweite steht nur in der Anm.
   - Datumsreste im Titel: 12.1.3.x/12.1.5.x («Nr. 2, Febr. 1978–Nr. 16 (lose)»).
   - Kommarest: 12.2.1.x («in: Züri Leu, (gebunden)»).
   - 9.1.1.: zwei Angaben in einer Nummer, Titel mit Datum in der Mitte.
   - 7.2.3.4.: offenes Ende «1997/98–» verloren.
   - 13.5./13.5. T2: «(undatiert)» ohne Anm.
   - 8.3.2.14. T3: «Fot. René Haury» steht als eigener Darin-Eintrag.

## Geprüft und in Ordnung, oder fraglich und nicht gemeldet

- **In Ordnung:**
  - 7.1.–7.4. und 9.1.–9.4.: Zeiträume aus «1938/39–1941/42» usw. richtig, Titel ohne Datumsreste.
  - 12.1.1.1.–4.: Anm «1943/44, August – September 1948» ist seit 15:43 besser (Regel I).
  - 12.1.5.x: von 09.1997 statt 10.1997 (Regel I).
  - 13.3.9.: Die Serie hat jetzt 1988–1989.
- **Fraglich, nicht gemeldet:**
  - 8.1.7.2. «Kassiererin … ab 1933» und 8.1.7.5. «Sekretärin … ab 1957». Das Jahr gehört eigentlich zur Anstellung, die Widmungsfotos sind 1942–1949 datiert.
  - 12.1.2.1./.2. haben 1970–1971 statt 09.1970–06.1971; die Anm nennt die Monate.
  - 8.3.1.14.: «4. April 1961» erweitert 1955–1956 nicht (Regel B).
  - 13.4.7.: Das Plakat «Juni-Festwochen 1952» ohne Signatur steht im Darin, deshalb Genau 1952.

## Ursachen im Skript

Zeilennummern beziehen sich auf `$S/neu6/findmittel_zu_scope.py` (c7c28ce2…).

- **Zeilenverbindung, `ist_umbruch` Z. 2500–2534:**
  - Z. 2533–2534 «erstes Wort hätte nicht mehr Platz gehabt» verbindet getrennte Einträge, deren erste Zeile bis ~540 pt reicht (Rand ~556).
  - Z. 2528–2531 hängen eine klein beginnende Folgezeile an, ebenso eine Zeile hinter einer offenen Klammer («… Steckel Post»).
- **Listenreparatur, `flicke_listen` / `flicke_klammerlisten` Z. 2703–2723:**
  - Sie kennt nur Namenslisten «Name: Werk» und Klammerlisten.
  - Stücklisten «Titel von Autor» (8.1.1.x) und Plakatlisten (8.2.3.x) werden nicht repariert.
  - `KLAMMERGRENZE_RE` Z. 2706 trennt nur, wenn der ganze nächste Eintrag samt Klammer auf derselben Zeile steht. Ein einzelnes verrutschtes Wort («König», «Meine», «Herr», «Faust») bleibt deshalb hängen.
- **Teil-Titel, `kopf_und_rumpf` Z. 2973–2983:**
  - Teile mit nur einem Eintrag (`len(geflickt) == 1`) oder mit weniger als 60 % Klammereinträgen bekommen den ersten Eintrag als Titel.
  - `ergaenze_titel` Z. 4154–4158 (`quelle = t`) gibt diesen Titel an die folgenden titellosen Teile weiter (M13).
  - Z. 4141–4148 vergibt die «nächste freie Nummer» auch an den durch die verrutschte Signatur entstandenen Teil (8.1.1.44. Teil 6).
- **Zeitraum, `zeitraum_aus_titel` Z. 3821–3824:**
  - Bei mehreren Zeitangaben im Titel wird die Vereinigung genommen, mit dem Hinweis «Mehrere Zeitangaben im Titel».
  - `PERSON_RE` Z. 349 erkennt Lebensdaten nur in Klammern mit Jahreszahl, nicht «geb. 26.04.1940», «30. August 1895–4. April 1961» oder «Buckwitz 1904–1987».
  - Notiz- und Ausstellungsdaten («sec, 07.12.2023», «Ausstellung … vom Juni 1988») gelten als Titeldatum.
- **Doppelpunkt-Titelregel in `kopf_und_rumpf`:** Sie teilt Plakat- und Publikationstexte am ersten «: ». Regel K verhindert das bei 11.1. T19 nicht, obwohl nach «von:» eine Namensliste folgt.
- **Regel J** (Z. 3780–3788, 3843–3854): Seit 15:43 wird bei zwei Zeitangaben die zweite aus dem Titel entfernt und die erste bleibt mitten im Titel (7.4.1.9., 15.2.3./5./6.).
