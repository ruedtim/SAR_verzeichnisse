# np7 O2 – die übrigen 48 Dateien (ohne D151210, D149628), Stand 18:11 gegenüber 15:43

Grundlage: `$S/neu7/alle_excel/D<id>_scope_import.xlsx`, Vergleich mit `$S/neu6/alle_excel/`, Diffs `$S/np7/diff/`,
PDFs `findmittel_pdf/pdf/D<id>.pdf`. Skript 18:11: `$S/neu7/findmittel_zu_scope.py` (5943 Zeilen); Zeilennummern unten
beziehen sich darauf. Paket: `O2_aenderungen.csv` (166 Einheiten), `O2_funde6.csv` (48 Zeilen), `O2_textverlust.csv` (54).

## Zahlen
- **Einheiten:** alle 166 beurteilt, **alle am PDF**.
  - Einzeln mit Titel, Darin und Datum am PDF: die Einheiten in 44 der 48 Dateien.
  - Bei den vier grossen Teil-Gruppen sind die Kopfzeilen aller Teile am PDF geprüft, die Darin-Listen stichprobenweise:
    - D1437, 20 Einheiten, S. 1–2;
    - D3231 3.1./3.5./3.7., 21 Teile, S. 25–51;
    - D32837 1.2.1.1., 12 Teile, S. 17–22;
    - D3357 4.7.2./4.7.4., 9 Teile, S. 25–33.
- **Seiten:** rund 120 PDF-Seiten. Davon gehören etwa 95 zu den 48 Dateien; die übrigen sind Belegseiten für die
  Fundzeilen in D3060, D3105, D3225, D3808, D2737, D3067, D3324, D3657, D150296, D2940, D4054 und D3718.
- **Urteile:** besser 137 · gleich 26 · schlechter 3 · unklar 0.
  - Nach Ursache:
    - 8e2bd7f9 85 (besser 77, gleich 6, schlechter 2);
    - Änderung 2: 46 (besser 30, gleich 15, schlechter 1);
    - Änderung 4: 13 (besser 8, gleich 5 – nur weggefallene Prüfhinweise);
    - Änderung 8: 12 (alle besser);
    - Änderung 6: 8 (alle besser);
    - Änderung 5: 2 (besser).
  - Keiner Einheit sind die Änderungen 1, 3, 7 oder 9 als Ursache zuzuordnen (zu Änderung 1 siehe D3861). Die
    Ursache ist aus `herkunft` (vor/nach 8e2bd7f9) und dem Skriptvergleich 15:43 ↔ 18:11 erschlossen.
  - Von den 6 Einheiten mit nur geändertem Prüfhinweis sind 5 «gleich» (Hinweis «Verschobene Zeilenumbrüche in Listen
    repariert» weg, das Darin ist jeweils unverändert und richtig) und D3321 6. «besser» (Hinweis «Untereinheiten
    reichen über den Zeitraum hinaus» zu Recht weg).
- **Fundzeilen Runde 6 (48):** behoben 12 · teilweise 21 · offen 14 · schlechter 1.
  - Die Statuswechsel kommen fast alle aus dem Patch der Prüfsession (B, C, A, F, N, O, D3657).
  - Aus den Änderungen der Hauptsession stammen:
    - Z247 behoben;
    - Z203 und Z438 durch die Jubiläumsregel;
    - Z294 und Z302 teilweise durch Änderung 2;
    - Z144 teilweise durch Änderung 6.
  - Die 5 Zeilen mit Status «schlechter» von 15:43 stehen jetzt so: Z70 behoben, Z105 teilweise, Z161 teilweise, Z154
    offen (Rückfall weg, Fund wie 13:15), Z293 offen (Zeitraum wieder richtig, Titel wie 13:15).
  - Neu «schlechter»: Z320 (D3808), siehe unten.
- **Neue Zeilen:** 7.
  - Durch Änderungen seit 15:43:
    - mittel: 4 (D176795 2.2.2., D3793 5.9.3./5.9., D3861 7.1. Teil 2, D3808 4. – Letzteres aus dem Patch);
    - gering: 1 (D3709).
  - Schon vor 15:43, beim Prüfen gefunden, nicht in Runde 6: 2 kritische (D3612 3.A./3.E., D3861 7.1.).
- **Textverlust:** 54 Stücke, **kein echter Verlust, keine falsche Zuordnung** (Tabelle unten).

## Verbesserungen (Hauptmuster)
1. **Strich nach der Signatur (8e2bd7f9).** Einheiten wie «1.1.1. - Protokolle und Akten» tragen jetzt ihren eigenen
   Text als Titel. Bis 15:43 hatten sie den Titel der Serie, ihr Text stand im Darin.
   - D1437: alle 20 Dossiers, S. 1–2;
   - D3793 5.9.1.–5.9.3.: vorher «Verschiedene Publikationen» (bei 5.9.3. aber Zeitraum verloren, siehe unten);
   - D175827 6.2.: «Kostümrapporte der Kostümchefs», 1996–2013;
   - D3472 1948.40: vorher [ohne Titel].
2. **Jubiläumsspannen zählen mit dem Endjahr (8e2bd7f9)**, 31 Einheiten (26 besser, 5 «gleich» mit nur neuer Anm),
   z. B.:
   - D2534 6.3. «1351 - 1951. Zürich 600 Jahre …»: = 1951;
   - D150589 16.2.9. Jubiläumsteller: = 1959;
   - D3587 2.: = 1945;
   - D2935 1.35./10.3.: = 1943;
   - D3321 6.1.: = 1931 (dazu fällt bei 6. der Hinweis «Untereinheiten reichen über den Zeitraum hinaus» richtig weg).
   - Z438 ist für die vier Hauptfälle behoben: D2534 2.1. = 1951, D3620 6. 1902–2002, D2962 11.2.2. bis 1962,
     D150589 16.2.10. = 1959.
3. **Datum in Klammern am Titelende (8e2bd7f9)**, 18 Titel, z. B. D3718 9.3.12.–9.3.27., D141020 5.4.2./8.3.1./9.8.,
   D1533 1.–4., D4173 1.29. Der Zeitraum war schon richtig, oft mit Tag/Monat aus dem Titel.
4. **Unterlagen nach dem Titel (8e2bd7f9).**
   - D176772 2.1. Teil 3 «Opus 34 …» / Darin «Skizzen Akt I-IV, Bleistift».
   - D1395 15.1. Teile 2–5: der eigene Kopf ist Titel, Teil 5 heisst jetzt richtig «Seeuntersuchungen: Walensee» (Z247).
   - D176795 2.3.6./2.3.11.1./2.3.12.2.: Briefe mit eigenem Datum; die irreführenden Anmerkungen «1936; Darin: …»
     fallen weg.
5. **Änderung 2 (Titel der Einheit statt Nachbartitel)**, 30 Teile besser:
   - D3231 2.8. Teile 9/10: vorher «Nationalstrassen»;
   - D3231 3.1.: 10 Teile mit falschen Buchstabengruppen-Titeln;
   - D3231 3.7. Teile 5–13: vorher «b) Repertoire von Yvette Guilbert», die Teile sind Komponistengruppen unter
     «c) Chansons, Cabaret, Lieder»;
   - D3357 4.7.2. Teile 8/14 und 4.7.4. (7 Teile).
   - Rest: Der eigene Kopf dieser Teile («E Egg-Powder …», «Der sanfte Heinrich (Hörspiel)», «Jacques, Peter (1979)» …)
     bleibt erster Darin-Eintrag. Z294 und Z302 sind deshalb nur teilweise behoben.
6. **Anführungen (Änderung 6)**, 8 Einheiten:
   - D2123: 12 Einträge «"Sonderklassen - Allgemeines"» usw.;
   - D174277 21/22/30;
   - D10675 745.52 (Z144 teilweise);
   - D2937 B.3.0.;
   - D4175 1.C.3.;
   - D3709 2.2.
7. **Namenslisten / Initial nach Personenbezeichnung (Änderung 8)**, 12 Einheiten:
   - D3612 (6 Einträge «… an den Stadtpräsidenten R. Billeter, Datum»);
   - D260 25 («Referenten F. Zollinger»);
   - D2853 1. («Herren H. Gladenbach»);
   - D2935 3.54. (Titel wieder ganz);
   - D2857 2.1.;
   - D4058 19.2.9.;
   - D4175 2.B.1.;
   - D512 1.8./1.9./1.18. (Spaltenmischung D512 bewusst offen).
8. **Listen je Zeile (Änderung 4)**, z. B. D3190 1.3., D2962 11.1.1./11.1.2., D150689 5.4.1./6.1.7., D3231 2.8. Teil 3,
   D3231 3.10.
9. **Vornamen-Stoppliste (Änderung 5):** D149888 6.4. «II:» / «Presseberichte», D32837 1.6.1. Teil 2 «Gilberte de» /
   «Courgenay».

## Verschlechterungen und neue Fehler
- **D176795 VII.388.:2.2.2. (ID 18, S. 6) – mittel, Zeitraum, 8e2bd7f9.**
  - Der Zeitraum war = 1810 und ist jetzt 1810–1838; das Todesjahr im Personentitel «(-1838)» gilt als Laufzeit.
  - Auslöser ist die Unterlagen-Regel (`kopf_und_rumpf` Z. 3093–3099): Sie greift wegen « von » im Namen und macht
    «Vertrag über das Rittergut Weisdorf ¦ 1810» zum Inhalt; das ist für sich richtig.
  - Danach liest `zeitraum_aus_titel` (Z. 4132 ff.) «(-1838)» als «bis 1838», weil `PERSON_RE` (Z. 375) nur Klammern
    mit Jahr am Anfang erkennt.
  - Vorschlag: `PERSON_RE` um «(-JJJJ)» / «(†JJJJ)» erweitern.
- **D3793 VII.55.:5.9.3. (ID 206) und 5.9. (ID 203), S. 28 – mittel, Zeitraum, 8e2bd7f9.**
  - Der eigene Titel ist jetzt richtig. Das Datum «… vom 14. August 1938 in Stäfa» steht aber mitten im langen Titel
    und wird nicht zum Zeitraum: kein Zeitraum (vorher 14.08.1938 aus dem Darin).
  - Folge: Die Serie 5.9. endet am 09.04.1932 statt am 14.08.1938.
- **D3861 VII.93.:7.1. Teil 2 (ID 34, S. 10) – mittel, Titel, Änderung 2.**
  - Titel jetzt «Johannes Weber (1871 – 1949) …, Teil 2» = Titel von Teil 3.
  - Grund: Die Serie 7.1. hat beim Ergänzen noch keinen eigenen Titel, und `ergaenze_titel` (Z. 4624–4625) nimmt dann den
    ersten Teil mit Titel – also doch einen Nachbartitel.
  - Vorschlag: Ohne Titel der Einheit lieber deren späteren Fallback (Titel der übergeordneten Einheit) abwarten oder
    leer lassen.
- **D3808 VII.65.:4. (ID 4, S. 1) – mittel, Zeitraum, Patch.**
  - Jetzt 1906–07.03.1946 statt 1906–1907. Die Beilagen 1945/46, die zum Bestand gehören (Z320), erweitern über das
    Darin den Zeitraum.
  - Z320 ist deshalb «schlechter».
  - D2737 :9. (ebenfalls Patch, jetzt 1914–1987) ist dagegen richtig: Die eigenen Einträge von Schachtel 9 reichen bis 1987.
- **D3709 VII.403.:2.2. (ID 17, S. 2) – gering, Darin, Änderung 6.**
  - PDF: «„Damen Volley-» / «Ball …“» wird zu «Volley - Ball».
  - Gleiches Muster wie O1 bei D149628 (« - » statt «-»).
- **Schon vor 15:43 – kritisch, beim Prüfen gefunden:**
  - **D3612 VII.37.:3.A. / 3.E. (IDs 7–13, S. 7–9):** Die Folgezeilen «A. Bodmer» und «E. Hafner-Tobler» von
    Darin-Einträgen («Schreiben … an Herrn / A. Bodmer») werden als Buchstaben-Signaturen gelesen.
    - Ergebnis: 7 erfundene Einheiten («Bodmer», «Hafner-Tobler»); 46 Schreiben stehen dort statt bei 3. Teil 2.
    - Den Einträgen fehlt der Empfänger, z. B. «… an Herrn, 4. Juni 1912».
    - Änderung 8 greift hier nicht, weil die Zeile schon als Signatur gilt.
  - **D3861 VII.93.:7.1. (IDs 33–35, S. 10):** Die Bereichszeilen «7.1.–26. Detailverzeichnis …» und «7.1.–8. Sammelrahmen I»
    werden zur Serie 7.1. bzw. zu Teil 2; die echte 7.1. «Johannes Weber …» ist nur Teil 3.
    - Die Hauptsession nennt «VII.93. 7.1. – 26.» bei Änderung 1 als Bereich. Das betrifft aber nur das Abtrennen des
      Strichs (`_zahl_nach_strich` Z. 3026 ff.); die Einheiten entstehen weiter.

## Bewusst «gleich» bewertet (Nebenwirkungen, kein neuer Fund)
- **Änderung 2 ersetzt auch Nachbartitel, die inhaltlich stimmten.**
  - D32837 1.2.1.1., 12 Teile: Der Kopf im PDF ist «Programme 1980/81» usw., wie bei den Nachbarteilen mit Titel
    «Programme».
    - Bis 15:43 hiessen sie «Programme, Teil n», jetzt «Aufführungen und diverse Veranstaltungen mit Anne-Marie Blanc,
      Programmhefte, Teil n».
    - Der eigentliche Fehler bleibt: Der Kopf steht weiter als erster Darin-Eintrag, darum sind die Titel der Teile
      uneinheitlich.
  - D3231 3.5. Teile 3/4 (S. 43/44): Sie setzen die Liste «b) Cornichon-Texte» fort (N…, S…). Der alte Titel
    «b) Cornichon-Texte, Teil n» passte, der neue ist der Titel der Einheit.
  - D4054 13.3.1. Teil 5: gleichbedeutend.
- **Jubiläumsspanne nur als Anmerkung bei Spaltendatum:** D151150 13.2., D3545 2.6./2.7. («1924 – 1964» neben = 1964),
  D177448 9.1.7.3./9.1.7.6. (Spanne aus dem Titel in die Anm verschoben).
  - Wortlaut nach Absicht des Skripts (`_jubilaeum_ende` Z. 576). Eine Anm wie «1924 – 1964» bei = 1964 kann aber als
    Entstehungszeitraum missverstanden werden; vielleicht mit «Jubiläum: …» kennzeichnen.
- **D2935 1.14. (S. 4):** Die Unterlagen-Regel greift ausserhalb von VII.200., weil «Gemeindebehörden von Zürich» ein
  « von » enthält.
  - «Einladung, dat. 3. Mai 1888.» ist jetzt Darin; dafür fehlt im Titel der Rest «dat.» nicht mehr.
  - Die Bedingung « von » + Unterlagenwort am Zeilenanfang ist breit: Hier ist das Ergebnis vertretbar, bei D176795
    2.2.2. führt sie zum Fehler oben.

## Restpunkte bei den Verbesserungen (Hinweise, keine eigenen Zeilen)
- **Jubiläum + Druckjahr:** Das Jubiläumsende kommt zum Druckjahr dazu.
  - D150589 14.2.56. 1944–1945 (Druck 1945); D177460 H 25 1998–1999 (Druck 1998, Jubiläumsende 1999 erst danach).
  - Besser wäre: Gibt der Titel ein Druckjahr an, gilt nur dieses.
- **Das Endjahr verdrängt das genaue Datum** (wie O1 23.4.4.3.; vorher auch nicht genutzt):
  - D2620 3.2.20. = 1974 trotz «7. März 1974»;
  - D3528 4.1.28. = 1966 trotz Darin «31. Januar 1966».
- **Das Titeljahr schliesst Darin-Texte aus** (bisherige Regel: kein Darin-Text neben einem Titeldatum):
  - D4054 9.24.1.3. = 1963 trotz «Zeitungsberichte 1962 – 1967»;
  - D2935 10.4. = 1993 trotz Zeitungsserie ab 25.11.1992.
  - Gegenüber 1863–1963 bzw. 1893–1993 trotzdem klar besser.
- **Jubiläen ohne «N Jahre» werden nicht erkannt:**
  - D2534 2.4.1./6.10. 1351–1951 (deshalb Z203 nur teilweise);
  - D2894 9.1.2. «75-Jahre-Jubiläum … 1887−1962» (deshalb Serie 9.1. weiter 1887–1987);
  - D2962 11.2.2. Beginn 1821 aus «… 1821-1921 … 100-jährigen».
- **D2123:** Über den Seitenwechsel S. 10/11 bleiben zwei Einträge verschmolzen: «"Grippe - Epidemie" … 32
  "Infektionskrankheiten - Grippe" …» (vor 15:43).
- **D176795 2.3.11.1.:** Die Unterpunkte unter «Briefe:» sind uneinheitlich: «Von der Mutter» ist mit «; » an den
  nächsten Punkt gehängt, «An Tante Bertha» ist ein eigener Eintrag.

## Die 54 Textstücke aus `O2_textverlust.csv`
| Gruppe | Zahl | Befund |
|---|---|---|
| D3231 2.8./3.1./3.5./3.7. «…, Teil n» | 18 | alte Nachbartitel, Text steht weiter beim richtigen Teil bzw. beim Titel der Einheit (Änderung 2) |
| D32837 1.2.1.1. «Programme, Teil n» | 12 | Kopf «Programme <Saison>» steht weiter als 1. Darin-Eintrag |
| D3612 3./3.A./3.E. «…, Datum; R. Billeter» | 6 | jetzt «… an den Stadtpräsidenten R. Billeter, Datum» (Änderung 8) |
| D1395 15.1. «Seeuntersuchungen: Zürichsee, Teil n» | 4 | eigener Titel ohne «, Teil n», Teil 5 «Walensee» |
| D3718 9.3.12./13./14./27. «(Januar 1948)» usw. | 4 | Datum in von/bis (01.1948, 22.–23.02.1951, 07.1952, 10.1964) |
| D141020 5.4.2./9.8. Klammerdatum | 2 | 12.1967 bzw. 06.12.1975 in von/bis |
| D1437 4.1.3./4.1.4. «…; Vgl. V.F. c.76.x.» | 2 | Titel + eigener Darin-Eintrag «Vgl. …» |
| D3357 4.7.2. Teile 8/14 | 2 | alte Nachbartitel |
| D175827 6.2. «Kostümrapporte … 1996 – 2013» | 1 | Titel + 1996–2013 |
| D176795 2.3.6. «… Geschwister Tagebuch (2 Bde.), 1844-1853» | 1 | zwei Einträge mit je eigenem Datum |
| D3793 5.9.1. «Statuten (11. September 1909)» | 1 | Titel «Statuten», 11.09.1909 |
| D4054 13.3.1. Teil 5 | 1 | Titel der Einheit «…, nach Saison geordnet, Teil 5» |

## Auffällige Fälle ausserhalb des Auftrags (nicht als Zeile erfasst)
- **D2940 VII.141.:2. (S. 2):** «2 Handwerkskundschaften … (Überformate)» ist eine Stückzahl unter 1. «Persönliche
  Unterlagen», wird aber Serie 2. Die echte «2. Vorträge …» ist dann nur Teil 2. Schon vor 15:43; Z437 deutet das nur
  an. Patch O greift nicht, weil die Zahl nicht eingerückt ist.
- **D3060 VII.189.:1 (Patch B):** Jetzt 1747–1979; 1747 ist das Geburtsjahr in «Auszüge aus Bürgerregister Wollishofen:
  a) I 27 Asper Johannes ¦ 1747-1819». 15:43 war es 1783, auch aus Lebensdaten. Echt alt sind «Urkunden zu diversen
  Geburten ¦ 1700/1800» und «Urkunde tapferer Soldat ¦ 14.03.1804».
- **D3321 6.2.:** Darin «2» ist die Seitenzahl «-2-» (vor 15:43).
- **D3520 6.1.:** Zeitraum 1964–2000; 2000 kommt aus dem Programmnamen «Opus 2000» (1992), soll 1964–1997 (vor 15:43).
