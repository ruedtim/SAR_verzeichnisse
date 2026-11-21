# D151210 (VII.200., Schauspielhaus Zürich AG) – siebte Nachprüfung, Gruppe D1, PDF-Seiten 1–200, Stand 18:11

Excel 18:11: `$S/neu7/D151210_scope_import.xlsx`, Skript `$S/neu7/findmittel_zu_scope.py` (sha256 fde790ac…, 5943 Zeilen;
Zeilennummern unten beziehen sich darauf). Vergleich mit 15:43: `$S/neu6/D151210_scope_import.xlsx`. Für die Ursache habe
ich den Stand 8e2bd7f9 aus `stichproben/verbesserung/` zurückgerechnet (Vorschlag minus Patch, sha256 8e2bd7f9…), damit
Änderungen aus 8e2bd7f9 von den Änderungen 1–9 und dem Patch zu trennen sind.

## Zahlen

- **Bereich:** 200 Seiten, 1215 Einheiten mit PDF-Seite 1–200 (gleich viele wie 15:43); 30 Seiten mit geänderten Einheiten.
- **Geändert:** 201 Einheiten, 0 neu, 0 weggefallen. Alle 201 habe ich am PDF geprüft:
  - Die Signaturblöcke auf S. 178–201 habe ich mit pdfplumber gelesen (Parameter wie `woerter.py`) und über Signatur +
    Vorkommen den Einheiten zugeordnet.
  - Titel, Datum und Darin jeder Einheit habe ich automatisch gegen die PDF-Zeilen verglichen und die 48 Abweichungen
    einzeln angesehen. Alle 191 Einheiten in 5.2.4.x habe ich zusätzlich in einer kompakten Gegenüberstellung gelesen.
  - Die 10 Einheiten ausserhalb von 5.2.4.x (S. 19–147) habe ich einzeln mit pdftotext und den Wortpositionen geprüft.
- **Urteile:** 192 besser, 9 schlechter, 0 gleich, 0 unklar.
  - Ursachen: 8e2bd7f9 193, Regel 2 3, Regel 7 3, Regel 8 1, Regel 6 1; der Patch wirkt im Bereich nirgends.
  - Schlechter sind: IDs 60, 61, 62 (S. 19), 93 (S. 24), 141 (S. 33), 1155 und 1154 (S. 193), 1183 und 1180 (S. 196).
- **Fundzeilen aus Runde 6 (21):**
  - 6 behoben: Z260, Z261, N360, N363, N364, N366.
  - 3 teilweise: N367, N383, N429.
  - 12 offen: 11 bewusst offen (N357, N358, N359, N361, N365, N368, N372, N379, N380, N428, N430) und N362.
  - 0 schlechter.
- **Neue Zeilen:** 5 (4 mittel, 1 gering). Vier davon sind Verschlechterungen seit 15:43 (9 Einheiten), eine ist ein
  Altfehler von vor 15:43 (14 Fälle).
- **Prüfhinweise im Bereich:** 6 geändert.
  - Weg: ID 62 «Zeitraum … geschätzt», ID 1046 «Verschobene Zeilenumbrüche …».
  - Neu: ID 1028 «… geschätzt» (richtig); IDs 1154, 1180 «Untereinheiten reichen über den Zeitraum hinaus …» und ID 1183
    «Mehrere Zeitangaben im Titel …» (alle drei falsch, siehe unten).
- Vollständigkeit unverändert 100 %, «Nicht übernommen: nichts». Im ganzen Excel sind es 1482 statt 1483 Teile
  (8.1.1.44., nicht mein Bereich).

## Verbesserungen

1. **Produktionslisten 5.2.4.1.–5.2.4.11. (S. 179–200, 189 Teile), Ursache 8e2bd7f9:**
   - Der Strich nach der Signatur fällt weg (neu7 Z. 2210–2213). Die Produktionszeile wird damit Titel, das
     Klammerdatum wird Zeitraum (Z. 4225), und die Unterzeilen stehen je als eigener Darin-Eintrag.
   - Vorher trugen 155 Teile «Produktionen des Schauspielhauses und nicht realisierte Projekte, Teil n», 29 einen
     Nachbartitel und 5 einen Titel mit angehängten Unterlagen.
   - 179 Teile haben jetzt «=» Premierendatum statt der Spielzeit (bei 5.2.4.1. bisher 1963–1970). Ohne Datum im PDF bleibt
     die Spielzeit (7 Teile). ID 1028 «(nicht aufgeführt)» hat 1963–1964 aus dem Darin.
   - Damit sind Z261 (Nachbartitel, 29 → 0 im Bereich), N363, N364 (63 von 63 im Bereich) und N366 (5 von 5) behoben.
   - Beispiele:
     - ID 1161 (S. 193) «Der Ratenfänger. Eine Fabel von Carl Zuckmayer», = 22.02.1975, statt «Der Büchsenöffner …
       Besetzungsliste, Teil 8»;
     - ID 1088 (S. 186) «Early Morning (Trauer zu früh), Komödie von Edward Bond», = 02.10.1969;
     - ID 1073 (S. 184): «(03.05.1968) Bühnenpläne» / «und Skizzen» ist richtig getrennt;
     - ID 1118 (S. 189): «- - Die Hebamme» ist richtig.
2. **Regel 7 (Strich am Zeilenende)** trennt jetzt richtig: IDs 99 (S. 25), 147 (S. 34), 216 (S. 51). Damit ist N383 zu 3/5
   behoben.
3. **Regel 6:** In ID 779 (S. 147) bleibt «"Frankenstein - Entstehung …"» ganz (N360).
4. **Regel 8:** In ID 534 (S. 105) steht jetzt «Friedrich Schütze» ohne «; » (N429 zu 1/3 behoben).

## Verschlechterungen und neue Fehler (je eine Zeile in `np7_d151210_D1.csv`)

1. **Regel 2 – Fortsetzungsteile tragen jetzt den Serientitel** (mittel, 3 Fälle).
   - Betroffen: ID 61 (S. 19, 2.3.2.3. T4), ID 93 (S. 24, 2.3.2.9. T3), ID 141 (S. 33, 2.4.2.1. T5).
   - Im PDF sind es Signatur + Strichpunkt im Textzug (x 142–152), direkt nach der Strichliste des vorigen Teils.
     Runde 6 hatte sie als echte Fortsetzungen bestätigt.
   - Statt «Biografisches über Leopold Lindtberg, Teil 4», «Korrespondenz und Akten, Teil 3» und «Protokolle des
     Verwaltungsrates 1950–1955 mit Beilagen, Teil 5» steht jetzt der Serientitel, z. B. «Harry Buckwitz (1904–1987),
     Direktor des Schauspielhauses 1970–1977, Teil 3».
   - Bei ID 93 widerspricht das «1970–1977» im Titel zusätzlich dem Zeitraum «= 02.11.1957» (N379).
   - Ursache: `ergaenze_titel` Z. 4620–4626 nimmt immer `k.titel`.
   - Vorschlag: Bei `_ist_fortsetzung` oder bei einem Strichpunkt im Textzug den Titel des vorigen Teils behalten.
2. **8e2bd7f9 – Fortsetzung einer Strichliste wird Titel** (mittel, 2 Fälle).
   - Betroffen: ID 60 «Nachtessen aus Anlass … Tischordnung» und ID 62 «Zeitungsberichte» (Anm «ab 1922 bis 1972»), beide
     S. 19 mit leerem Darin.
   - Der Strich steht bei x 152 bzw. 142, also im Textzug der Liste, die Titelspalte liegt bei x 139.
   - Die Strichregel prüft nur, ob darunter ein weiterer Punkt folgt (`_liste_folgt` Z. 3038), nicht die Einrückung und
     nicht die Liste davor.
3. **8e2bd7f9 – Jahreszahl im Produktionstitel wird Zeitraum** (mittel, 2 Fälle und 2 Folgehinweise).
   - ID 1183 (S. 196) «Travesties oder Zürich 1917 … (03.02.1977)» hat 1917–03.02.1977, Soll ist «= 03.02.1977».
   - ID 1155 (S. 193) «… (Wiederaufnahme von 1973)» hat «= 1973», Soll ist die Spielzeit 1974–1975 wie um 15:43.
   - Folge: falsche Hinweise bei den Serien 5.2.4.6. (ID 1154) und 5.2.4.8. (ID 1180).
   - Der Art nach sind die Fälle wie der bewusst offene #71 («Chile 1984»). Ich melde sie trotzdem, weil sie neue
     Verschlechterungen sind. Der Vorschlag ist, dass ein Klammerdatum am Titelende allein gilt. D2 meldet
     gleichartige Fälle auf S. 209/215.
4. **8e2bd7f9 – Unterlagen im Titel** (mittel, 1 Fall; die Einheit ist trotzdem besser als 15:43, weil der Nachbartitel
   weg ist).
   - ID 1167 (S. 194) heisst «Worte Gottes, Tragikomödie von Ramon del Valle-Inclán Szenarium, Besetzungsliste,
     Aktennotizen», das Darin ist leer.
   - Im PDF ist «Szenarium,» ans Ende der Produktionszeile gerutscht. `m_k`/`m_u` (Z. 3292–3300) trennen nur nach einem
     Klammerdatum oder nach «von X:».
5. **Vor 15:43 – zwei PDF-Zeilen in einem Darin-Eintrag** (gering, 14 Fälle; neu erfasst).
   - Seit jede Unterzeile ein eigener Eintrag ist, fallen die Fugen auf, an denen `ist_umbruch` zwei vollständige Zeilen
     verbindet:
     - Breitentest Z. 2622 (10 Fälle), z. B. ID 1017 «… einzelnen Requisiten Bilderfolge zu „Die Geier“»;
     - Kleinbuchstabe am Zeilenanfang (4 Fälle: «einzelne …», «kurze …»), z. B. ID 1138 «Bühnenpläne und Skizzen
       einzelne Briefe, …».
   - Dazu kommt umgekehrt ID 1197 mit «; ».
   - Die PDF-Fehler ohne «)» (IDs 1126, 1157) habe ich wie in Runde 6 nicht gezählt.
   - Grenzfall, nicht gemeldet: ID 1097 «Skizzen zum Bühnenbild Liste der Möbel etc.», wo im PDF «Liste» ans Zeilenende
     gerutscht ist.

## Fundzeilen aus Runde 6 (Kurzfassung)

- **Z290/Z291** sind nicht in meinem Paket. Die entsprechenden D151210-Zeilen sind Z260 (Teil-Nummern) und Z261
  (Nachbartitel). Ich habe sie für S. 1–200 mit Zahlen beurteilt:
  - Z260 behoben: 355 Teile, keine Dublette, Folge in PDF-Reihenfolge, «…, Teil n» passt in 24 von 24 Fällen.
  - Z261 behoben: 29 → 0. Nebenwirkung: siehe Punkt 1 oben.
- **Teilweise:**
  - N367: ID 1100 behält «(undatiert)» im Titel.
  - N383: IDs 261 (S. 58) und 424 (S. 81) mit « - » mitten in der Zeile.
  - N429: IDs 287 und 452 behalten «; ».
- N362 bleibt unverändert offen.

## Textverlust (55 Stücke aus `D1_textverlust.csv`)

Ich finde keinen echten Verlust und keine falsche Zuordnung. Alle Wörter stehen bei derselben Einheit (Titel, von/bis,
Anm, Darin), soweit sie PDF-Text sind:
- 29 frühere Darin-Zeilen «Produktion (Datum); Unterzeilen» sind jetzt Titel + von/bis + Darin.
- 18 frühere Nachbartitel sind zu Recht verschwunden (Z261).
- 3 frühere Titel mit angehängten Unterlagen sind jetzt Titel + Darin (N366: IDs 1096, 1107, 1141).
- 1 Stück ist jetzt Titel + Anm (ID 62 «Zeitungsberichte ab 1922 bis 1972»).
- 4 erzeugte Teil-Titel («Biografisches über Leopold Lindtberg, Teil 3/4/5», «Korrespondenz und Akten, Teil 3») sind
  kein PDF-Text. Ihr Wegfall ist aber genau der Titelverlust der neuen Zeilen 1 und 2.

## Bewusst offen – gleichartige weitere Fälle (nicht als neu gemeldet)

- **Datumsreste in Titeln: 2.**
  - Betroffen: ID 1210 «… Stück von Jürg Laederach 14.12.1978)» und ID 1211 «Gross und Klein, Szenen von Botho Strauss
    01.06.1979)» (S. 200).
  - Im PDF fehlt «(». Der Zeitraum ist richtig gesetzt, der Rest steht jetzt am Titelende (15:43 im Darin).
- **Titel über mehrere Zeilen:** 0 weitere.
- **Inhaltliche Zeitraumfälle:** 0 weitere unveränderte. Die zwei neuen Fälle dieser Art (IDs 1155, 1183) sind
  Verschlechterungen und deshalb oben gemeldet.

## Auffällig ausserhalb meines Bereichs (nur am Excel gesehen, für D2)

- S. 201–211: Dieselben Darin-Fugen mit zwei Unterzeilen gibt es in den IDs 1223, 1225, 1231, 1234, 1236, 1259, 1266,
  1297 und 1307.
- ID 1308 (S. 211): Das Darin «Komödie von Fritz von Herzmanovsky-Orlando: Korrespondenz, …» enthält das Titelende, weil
  die Zeile im PDF unter «Bühnenpläne und Skizzen» gerutscht ist.
- N364 auf S. 201–211: 26 IDs. Am Excel steht nirgends mehr «(Datum) Unterlagen».

## Wichtigste Punkte

1. Die Umstellung der Produktionslisten 5.2.4.x (8e2bd7f9) ist im Bereich ein klarer Gewinn: 189 Teile mit eigenem Titel und
   Premierendatum, 29 Nachbartitel weg, N363/N364/N366 behoben.
2. **Regel 2** (`ergaenze_titel` Z. 4624) nimmt echten Fortsetzungsteilen den Titel des fortgesetzten Dossiers (IDs 61, 93,
   141). Die Info-Konvention («… bzw. des vorherigen Teils») sieht das anders vor.
3. **Strichregel** (Z. 2210): Ein eingerückter Strichpunkt, der die Liste des vorigen Teils fortsetzt, wird zum Titel
   (IDs 60, 62).
4. **Titeldatum** (zeitraum_aus_titel Z. 4132 ff.): Jahre im Stücktitel («Zürich 1917») bzw. «Wiederaufnahme von 1973»
   werden Zeitraum (IDs 1183, 1155) und erzeugen Serien-Hinweise.
5. Darin-Fugen (`ist_umbruch` Breitentest Z. 2622 und Kleinbuchstabe) verbinden in 14 Teilen zwei Zeilen, gering.
