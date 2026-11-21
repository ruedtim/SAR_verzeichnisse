# Sechste Nachprüfung am Excel-Stand 20.11.2026, 15:43

Geprüft wurde `findmittel_excel/` vom 20.11.2026, 15:43, dazu `testdaten_excel/` und `D151210_scope_import.xlsx`. Das Skript
hat sha256 `c7c28ce25cc2b46a…` und 5475 Zeilen.
- **Schnappschuss «neu6»:** `/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/neu6/`.
  Alle Zeilennummern beziehen sich auf das Skript dort.
- **Stand beim Abschluss:** `findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` waren noch identisch mit dem
  Schnappschuss. Das Projektskript hat die Hauptsession inzwischen weiterentwickelt (sha256 8e2bd7f9…); diesen Stand habe ich
  nicht geprüft.
- **Vergleich:** mit dem Stand 13:15 der fünften Nachprüfung (`…/scratchpad/neu5/`).
- **Geänderte Dateien:** Inhaltlich geändert sind 199 Dateien in `findmittel_excel/`, genau die Liste in
  `zellvergleich_1315_1543.txt`. Die «200» der Nachricht sind diese 199 plus die Übersicht. Dazu kommen 9 Testdateien.
- **Belege:** Jedes Urteil ist am PDF belegt.
- **D151210:** Es ist diesmal vollständig geprüft, alle 424 Seiten und alle 3'162 Einheiten (eigener Abschnitt unten).

## Kurzfazit

- **343 nachgeprüfte Zeilen** (alle aus `funde_nachpruefung5.csv` mit Status ≠ behoben): 66 behoben, 60 teilweise,
  211 offen, 6 schlechter.
  - 70 Zeilen liegen in PDFs, die seit 13:15 inhaltlich unverändert sind; dort gilt der Befund von 13:15 weiter.
  - Die offenen Zeilen in geänderten PDFs sind meist laut Diff unverändert oder haben sich nur im Zeitraum bewegt.
- **Kritische Zeilen: 11 von 33 behoben**, 17 teilweise, 5 offen, keine schlechter.
  - 12 der 22 nicht behobenen sind die bewusst offenen Punkte samt D1858, bestätigt.
  - Echte Restfehler sind 10 Zeilen, alle teilweise:
    - D3060: Porträtbilder S. 8;
    - D3089: Rollen- und Textbücherliste;
    - D3105 «Band 1»;
    - D150689 1.2.4.;
    - D1880 a.–i.;
    - D3018 S. 78;
    - D3271 4.2.22.;
    - D3774: 2.4./2.5. und die Unternummern 2.31. ff.;
    - D140969: Gliederungszeilen im Darin;
    - D3808: Beilagen im Darin von 4.
  - Von den 11 kritischen Fehlern der Runde 5 sind 8 behoben (Regel N bzw. O):
    - D141: 26 Einheiten wieder da;
    - D151150 10.5.2.;
    - D3774 5.3./6.4.;
    - D3874;
    - D4057;
    - D442 26.2.;
    - D631: jetzt Bestandszeile;
    - D8949.
    Teilweise sind D140969 und D3808; offen ist D1858, jetzt bewusst offen.
  - Ganz behoben sind auch D65, D67, D69 (Regel P).
- **Die 3 «schlechter» aus Runde 5 sind jetzt teilweise behoben:**
  - D3018 02.3.1.21./22.: keine Plannummern als Jahre mehr; 02.3.1.19. hat aber weiter = 2022.
  - D3018 06.1.4.: Titel richtig, aber «1964» ist ein eigener Darin-Eintrag.
  - D3466: Der Datumsrest steht noch in 19 statt 210 Titeln.
- **Schlechter geworden sind 6 Zeilen**, 5 davon durch Regel B:
  - D175994 IV.A.65.: 1894–1896 statt 1894–1980;
  - D2735 9: nur noch 03.–06.09.1912;
  - D3018 05.2.1.: verliert 10.02.1872;
  - D3067 V.B. Teil 3: 1901–1909 statt 1901–1959;
  - D3225 9.: 04.1986 statt 1899–1986;
  - D4054 5.5.3./12.3.4. (Regel F): zu enges Ende.
- **Neue Fehler: 149**, davon 9 kritisch, 110 mittel und 30 gering.
  - Aus den Regeln A–P stammen 47, davon 2 kritisch:
    - D3828 3.1.: Der Listeneintrag «3. Freisinnige Partei …» wird als 3.2. gelesen und verworfen; er fehlt in allen Blättern
      (Regel N).
    - D3031 V.19.: Die Posten von «4. Bauarchiv» stehen im Darin von «Anteilsschein» (Regel O).
  - Nicht angekündigt: 1 (D151210 5.4.5.10.).
  - Schon um 13:15 vorhanden, jetzt erst erfasst: 101, davon 71 in D151210. Kritisch davon sind 7:
    - D1746: II.A)–O) fehlen;
    - D2737: Doppelschachteln 3/4, 7/8, 10/11;
    - D3012: 1)–8) fehlen;
    - D3324: erfundene 2.;
    - D3505: erfundene Teile von 7.3.;
    - D3657: 6. als Übersichtszeile verworfen;
    - D151210 8.1.1.44.: erfundener Teil 6.
- **Regelstichprobe:** Am PDF geprüft wurden 755 Einheiten in 156 PDFs. 528 sind besser, 140 gleich, 81 schlechter und
  6 unklar.
  - Wie angekündigt und fast ohne Nebenwirkung: D, E, G, H, J, K, L, M, N, O und P.
  - I überwiegend gut: 87 besser, 20 schlechter.
  - F gut mit Lücken: 71 besser, 7 schlechter.
  - **Regel B ist nicht tragfähig:** 10 besser, 20 schlechter. Sie verwirft öfter echte Daten als Tippfehler.
  - A und C haben deutliche Nebenwirkungen: A 28 besser und 12 schlechter, C 20 besser und 8 schlechter.
- **Kennzahlen** (eigene Zählung, gleich wie die Hauptsession):
  - Einheiten in `findmittel_excel/`: 49'311 → 49'331.
  - «[ohne Titel]»: 35 → 33.
  - «Text erfasst» 100 %: 694 → 695 von 715 PDFs.
  - Überzählige Zeilen bei doppelten Schlüsseln: 80 → 10, nur noch D2681 (PDF unverändert).
  - «Nicht übernommen»: 2'089 → 2'071 Zeilen.
- **D151210:**
  - Gliederung, Signaturen, Hierarchie, Stufen und Text sind vollständig richtig; Vorspann und Schlussvermerke ebenfalls.
  - Die Teil-Nummern sind eindeutig und in PDF-Reihenfolge (Z290 behoben), bis auf 8.1.1.44.
  - Offen bleiben 121 Teile mit dem Titel des Nachbarteils (Z291).
  - Dazu kommen 74 neue Fundzeilen: 1 kritisch, 56 mittel, 17 gering. Fast alle bestanden schon um 13:15.
- **Gegenprobe und Kreuzbestätigung:**
  - 4 alte kritische Funde der Prüfer habe ich selbst am PDF nachgesehen, alle hielten: D3657, D1746, D3012, D3324.
  - 18 Fehler haben zwei oder drei Gruppen unabhängig voneinander gefunden.
    - Dreimal: D176795 5., D149628 26.2.4. und D3793 5.8.23.
    - Zweimal z. B. D2620 10.2., D2534 2.1., D1739 27, D9983 5.8.1. und D3225 9.
    Die 20 doppelten Zeilen sind entfernt; jeder dieser Fehler zählt einmal.

## Methode

1. **Schnappschuss «neu6».** `findmittel_excel/` (716 Dateien), `testdaten_excel/` (13), `D151210_scope_import.xlsx` und
   `findmittel_zu_scope.py` sind nach `…/scratchpad/neu6/` kopiert. Die sha256-Werte aller Dateien stimmen mit der Quelle
   überein. Geprüft wurde nur dieser Schnappschuss.
2. **Vergleich 13:15 ↔ 15:43.**
   - Inhaltsvergleich aller Blätter ohne die Zeile «Erzeugt»: 199 Dateien in `findmittel_excel/` und 9 Testdateien.
   - Einheitenvergleich je PDF über (Signatur, n-tes Vorkommen), wie in Runde 5. Über alle 715 Dateien sind 46'677 Einheiten
     unverändert, 2'597 geändert, 37 entfernt und 57 neu.
   - Dazu ausgewertet:
     - die Art jeder Zeitraum-Änderung (1'305 Einheiten: 362 nur Anmerkung, 279 enger, 247 weiter, 209 gleiche Jahre/anders,
       182 nur Quelle, 14 weg, 5 verschoben);
     - die geänderten Prüfhinweise;
     - Text aus 13:15, der nirgends mehr steht;
     - gekürzte und kaputt endende Titel;
     - die Teil-Nummern über alle Dateien;
     - die Info-Kennzahlen.
   - Werkzeuge liegen in `…/scratchpad/np6/werkzeug/`, die Ergebnisse in `…/scratchpad/np6/`.
3. **Prüfliste** (`methode/np6_pruefliste.csv`, `np6_auswahl.py`). Ausgewählt sind alle 343 Zeilen aus
   `funde_nachpruefung5.csv` mit Status ≠ behoben:
   - 33 kritische;
   - die 3 «schlechter»;
   - 242 mittel/gering in geänderten PDFs;
   - 65 mittel/gering in unveränderten PDFs.
   In unveränderten PDFs ist der Befund von 13:15 übernommen (`roh/np6_vorbewertet.csv`, 70 Zeilen, davon 5 kritische).
4. **Prüfung am PDF.** Sechs Prüfagenten mit je einem Paket und eigenen Regeln, vier Prüfer nur für D151210, dazu ich als
   Gruppe 0:
   - G0: bewusst und bekannt offene Punkte, Beispiele A in D512/D3530, Gesamtabgleiche, Z290/Z291;
   - G1: Signaturen N/O/P;
   - G2: Zeitraum A/B/D/J;
   - G3: Zeitraum C/E;
   - G4: Titel und Datumsformen I/J/K/L/M;
   - G5: Teile und Fussnoten F/G/H;
   - G6: übrige Zeitraum-Fälle;
   - D1–D4: D151210 Seite für Seite (S. 1–106, 107–212, 213–318, 319–424).
   Anleitung: `methode/ANLEITUNG_NACHPRUEFUNG6.md`.
5. **Regelstichprobe.**
   - Die Beispiele der Hauptsession und weitere betroffene Einheiten, je Einheit besser, gleich, schlechter oder unklar.
   - Zufallsstichproben (Startwert 20261121):
     - G3: 40 Zeitraum-Änderungen in 25 sonst nicht vergebenen PDFs;
     - G6: 30 Fälle «enger», «weg», «verschoben», «genauer» in 26 weiteren PDFs;
     - G5: Teile in D3398 und D3038 zusätzlich.
   - G3 hat zusätzlich alle 47 Einheiten mit der neuen Quelle «Datumsspalte und Darin (geschätzt)» und alle Anmerkungen
     beider Stände gegen von/bis abgeglichen.
6. **D151210-Vollprüfung.**
   - Für jede der 424 Seiten liegt eine Vergleichsdatei vor: PDF-Text und alle Excel-Einheiten der Seite mit allen Feldern
     (`…/np6/d151210/seiten/`). Dazu gibt es eine automatische Vorprüfung.
   - Die vier Prüfer sind jede Seite durchgegangen; die Seitenlisten stehen in `roh/np6_d151210_Dn_seiten.csv`.
7. **Zusammenführen** mit `methode/np6_zusammenfuehren.py`.
   - Spalten wie in `funde_nachpruefung5.csv`; `ist` ist der Stand 13:15, `neu_ist` der Stand 15:43.
   - Neue Zeilen tragen «Regel: A … P | nicht angekündigt | vor 13:15».
   - 20 doppelt gemeldete Zeilen (18 Fehler, von zwei oder drei Gruppen gefunden) sind entfernt (`WEG`). Wenn der Fehler in
     einer Sammelzeile einer anderen Gruppe steht, nennt diese die übrigen Gruppen (`VERMERK`, 7 Zeilen).
   - Die 12 bewusst offenen Zeilen tragen vorn in `neu_ist` die Marke «[bewusst offen]».
   - Die 17 Nachbartitel-Zeilen von D2–D4 sind bei Z291 zusammengefasst.
   - Bei D151210-Funden steht, ob die betroffenen Einheiten in der neueren Ausgabe «regress92» (16:16) noch gleich sind.
   - Doppelte Urteile derselben Einheit zählen einmal (74).

## Ergebnis nach Auswahl

| Auswahl | behoben | teilweise | offen | schlechter | entfällt | Zeilen | davon PDF unverändert |
|---|---:|---:|---:|---:|---:|---:|---:|
| kritische Zeilen | 11 | 17 | 5 |  |  | 33 | 5 |
| «schlechter» aus Runde 5 |  | 3 |  |  |  | 3 |  |
| mittel/gering in geänderten PDFs | 55 | 32 | 149 | 6 |  | 242 |  |
| mittel/gering in unveränderten PDFs (übernommen) |  | 8 | 57 |  |  | 65 | 65 |
| **Summe** | **66** | **60** | **211** | **6** | **0** | **343** | **70** |

| Befund 13:15 | behoben | teilweise | offen | schlechter | Zeilen |
|---|---:|---:|---:|---:|---:|
| neu in Runde 5, kritisch | 8 | 2 | 1 |  | 11 |
| neu in Runde 5, mittel | 39 | 8 | 34 | 1 | 82 |
| neu in Runde 5, gering | 5 | 2 | 2 |  | 9 |
| teilweise, kritisch | 3 | 15 |  |  | 18 |
| teilweise, mittel | 8 | 28 | 2 | 5 | 43 |
| teilweise, gering | 1 | 1 |  |  | 2 |
| offen, kritisch |  |  | 4 |  | 4 |
| offen, mittel | 1 | 1 | 151 |  | 153 |
| offen, gering | 1 |  | 17 |  | 18 |
| schlechter, mittel |  | 3 |  |  | 3 |

Von den 102 neuen Fehlern der Runde 5 sind 52 behoben und 12 teilweise. Dazu gehören:
- die Regel-a-Fehler D512 1.19., D3530 1., D151150 9., D3018 02.3.1.21./22., D67, D69, D4175 1.C.1., D3063 1.9., D9985
  27.2.1.;
- die Fussnoten (H);
- die Teile-Fehler F und G (D3828, D3589, D1343, D152390, D152810).

## D151210

**Umfang:** alle 424 Seiten, alle 3'162 Einheiten (D1: 547, D2: 776, D3: 801, D4: 1'038), jede Einheit am PDF.
- Auf 168 Seiten gibt es mindestens einen Fund, insgesamt rund 430 Fundstellen einschliesslich Kosmetik.
- Daraus sind 74 neue Fundzeilen geworden, viele davon Sammelzeilen.
- Dazu kommen die 121 Teile mit Nachbartitel bei Z291.

**Was stimmt:**
- Alle Nummern des PDFs sind Einheiten, keine ist erfunden (ausser 8.1.1.44. Teil 6). Hierarchie, Ebene und Stufe stimmen.
- Kein Text fehlt; jedes Wort steht in Reihenfolge bei der richtigen Einheit.
- Die Vorspann-Grenze ist richtig (S. 1–9): Alle 208 Nummern aus Übersicht und Inhaltsverzeichnis sind Einheiten, und die
  15 Abschnitte der Übersicht entsprechen den 15 Teilbeständen.
- Die 5 Schlussvermerke stehen vollständig im Blatt Info, «Nicht übernommen» ist richtig leer.
- Die Schachteln in 11.x stimmen.
- **Regel G wirkt:** Um 13:15 gab es 49 doppelte Teil-Schlüssel und 21 Folgen ausser Reihenfolge, jetzt keine mehr ausser
  8.1.1.44. Die Nummer «…, Teil n» im Titel stimmt überall mit der Spalte Teil. Z290 ist behoben.

**Fehler nach Art (neue Zeilen, ohne die 121 Nachbartitel):**

| Art | kritisch | mittel | gering | Zeilen |
|---|---:|---:|---:|---:|
| Gliederung / Teil-Nummer | 1 |  |  | 1 |
| Titel/Darin |  | 18 | 5 | 23 |
| Darin |  | 22 | 9 | 31 |
| Zeitraum |  | 16 | 1 | 17 |
| Anmerkung |  |  | 2 | 2 |
| **Summe** | **1** | **56** | **17** | **74** |

Nach Ursache: 71 schon um 13:15, 1 Regel I, 1 Regel J, 1 nicht angekündigt (5.4.5.10.: Darin-Daten vom Nov. 1996 fehlen
im Zeitraum, der Hinweis darauf ist seit 15:43 weg).

**Beispiele:**
- **Kritisch, 8.1.1.44. (S. 356):** Im PDF steht die Signatur jeweils eine Zeile über ihrem «Teil n».
  - Daraus entsteht ein erfundener «Teil 6 Don Carlos» (ID 2444); Teil 1 bleibt leer.
  - Die Teile 2–5 heissen «Don Carlos …, Teil n».
  - In zwei Darin-Einträgen klebt «8.1.1.44.» am Ende. Dieselbe angeklebte Signatur, aber mit richtiger Nummerierung, gibt es
    noch 8-mal.
- **Titel vom Nachbarteil (Z291, offen, 121 Teile):**
  - 30 in 5.2.4.1./.2./.5./.6./.13.;
  - 84 in 5.2.4.21.–.26., 5.2.4.35., 5.2.5.3./.4., 6.4.;
  - 7 in 6.62., 8.1.1.44., 8.3.2.14.
  - Beispiele: ID 1161 «Der Büchsenöffner …, Teil 8» ist «Der Rattenfänger». ID 1904 «… König Johann, Teil 5» ist Schiller,
    «Die Braut von Messina».
  - Ursache ist `ergaenze_titel` Z. 4154–4157 (`basis = quelle.titel`). Eine Produktion ohne «- » wird zum Teil-Titel (die
    Breitenprüfung in `ist_umbruch` Z. 2534), und die folgenden Teile erben ihn.
- **Titel/Darin (23):**
  - Bei Produktionen ohne «- » wird die erste Unterzeile an den Titel gehängt (IDs 1096, 1107, 1141, 1160, 1251).
  - Titelfortsetzungen stehen im Darin (4.1.4.35. «Benning» / «1990–1991», 5.2.4.10.).
  - Darin-Text steht im Titel (IDs 1350, 1398, 1412, 1432, 1626–1629 «Blutspuren», 1691, 1757, 1763, 1962; ID 95
    «Todesanzeigen»).
  - 6 Plakat- und Publikationstitel sind am Doppelpunkt mitten im Satz geteilt.
- **Darin (31):**
  - Nach « - » mit Kleinbuchstaben wird nicht getrennt (5 Fälle, `teile_inline` Z. 2655). ID 779 ist dagegen an « - » in einer
    Anführung geteilt.
  - Rollenbücher: 5 Einträge verschmolzen, 3 falsch geteilt («Wallenstein de» / «Vega, Lope…»).
  - In 8.1.1.x bleiben 39 vom PDF verschobene Zeilenumbrüche unrepariert, 26-mal sind ganze Zeilen zu einem Eintrag verbunden
    (`ist_umbruch` Z. 2533–2534, `flicke_listen` Z. 2703–2723).
  - 10 Darin-Einträge tragen die Signatur des nächsten Teils.
  - Gering: Trennzeichen «; » fehlt bei rund 150 Unterzeilen oder steht mitten im Namen («Gert; Westphal»). Ursache ist
    `baue_eintraege` Z. 2633/2636; dort entscheidet ein Einzug von etwa 1 pt.
- **Zeitraum (17):**
  - Das Datum des ersten Dokuments gilt für die ganze Mappe (IDs 14, 15, 359).
  - ID 50 «Zum Tod von Oskar Wälterlin» hat 1933–1945; das Todesdatum wird verworfen.
  - ID 93, ein titelloser Teil, hat = 02.11.1957 aus der Kopie eines Ehevertrags.
  - ID 182 hat 1938–1960 aus dem Inhaltsverzeichnis, das Darin reicht aber bis 1999.
  - Vier Teile erhalten den Zeitraum der Serie statt ihres eigenen (IDs 1423, 1435, 1439, 1824).
  - Publikationen 11.1./11.2. nehmen Themenzeitraum oder Lebensdaten aus dem Buchtitel (Mittenzwei 1933–1979 statt 1979;
    Wälterlin 30.08.1895–04.04.1961).
  - Weitere falsche Quellen: 14.3.3. «geb. 26.04.1940», 7.3.50./51. «sec, 07.12.2023», 8.1.7.1. Ausstellungsdatum 06.1988
    für Fotos von 1932–1938.
- **Kosmetik:** Bei 1332, 1726 und 1987 bleibt das Datum im Titel; dazu «literarischmusikalisches» und 12.1.x/12.2.1.x
  (Titel/Darin-Grenze).

**Stand in der neueren Ausgabe «regress92» (16:16, Kopie im Scratchpad, sha256 f5abb0a3…, nur verglichen, nicht am PDF
geprüft):**
- Bei 56 der 74 Funde sind die betroffenen Einheiten dort unverändert; diese Fehler bestehen also weiter.
- Bei 18 Funden, meist in den Produktionen 5.2.4.x, sind die Einheiten geändert.
- Die Zahl der Teile mit dem Titel eines vorangehenden Teils sinkt von 126 auf 33 (automatische Zählung); 11 davon sind
  dieselben wie um 15:43.
- Jede D151210-Zeile in der CSV trägt dazu einen Vermerk «[regress92 (16:16): …]».

## Bewusst und bekannt offene Punkte (Auftrag 4) – bestätigt

- **D3828:**
  - Gliederung unverändert.
  - Regel F nimmt die fremden Zeiträume der Erstnennungen wieder heraus (Z351 behoben).
  - Neu: 3.1. Eintrag «3.» fehlt (kritisch, Regel N) und 3.16. 1940–1946 (Regel C).
- **D3530:** Gliederung unverändert; 1. ohne den falschen Zeitraum (Z338 behoben); 42. = 1970, das Erscheinungsjahr (Regel J).
- **D141024, D149622, D2614, D1858, D1395, D2681:** PDF bzw. Excel inhaltlich unverändert.
- **D512:**
  - Struktur unverändert.
  - 1.19. hat jetzt 1976–1977 (Z362 behoben); 50 von 51 Saisons haben den Saison-Zeitraum (Z120 behoben).
  - Die Folgedaten im Eintrag (Z54): 2 sind wieder da (1.5. «28. April 1963», 1.24. «17. Mai 1982»), dafür fehlen 3
    (1.29. «20./27.Okt. 1986/», 1.37. «Okt. 1994 –» und «Okt./ Nov. 1994»).
- **D3208:** unverändert (nur der Hinweis nennt «3 Folgen» statt «4 Folgen»).
- **D1739:** «Mappe mit Grossformaten» weiter ohne eigene Einheit. Neu zu eng ist Schachtel 27: «Seeauffüllung 1830 – 1925»
  wird zerlegt (Regel B, in der B-Sammelzeile).
- **D258 9.:**
  - Der Zeitraum ist jetzt richtig 02.–03.09.1911 (Regel I).
  - Der Titel bleibt abgeschnitten: «Protokoll des schweizerischen», Darin «Städtetages in Glarus» (bekannt).
  - 12. hat jetzt den richtigen Titel.
- **D2853 (Archivplan-Tabelle):**
  - Besser: Die Zeilen 1–3b sind keine falschen Teile von 1./2./3. mehr, sondern stehen im Darin von «3. Akten», wohin sie
    gehören (Regel O).
  - Ab Zeile 4 kollidieren die Tabellennummern weiter mit den Abschnitten 4./5.
- **D3089:** Rollen- und Textbücherliste S. 16–35 weiter im Darin von X. (Z2 teilweise).
- **D1395 15.1. Teil 5:** unverändert.

## Regelstichprobe

| Regel | PDFs | besser | gleich | schlechter | unklar | geprüfte Einheiten |
|---|---:|---:|---:|---:|---:|---:|
| A | 30 | 28 | 4 | 12 |  | 44 |
| B | 28 | 10 | 8 | 20 | 2 | 40 |
| C | 30 | 20 | 20 | 8 | 1 | 49 |
| D | 27 | 50 | 7 | 1 |  | 58 |
| E | 37 | 46 | 47 | 4 |  | 97 |
| F | 25 | 71 | 16 | 7 | 3 | 97 |
| G | 7 | 24 | 8 |  |  | 32 |
| H | 3 | 18 |  |  |  | 18 |
| I | 38 | 87 | 13 | 20 |  | 120 |
| J | 19 | 25 | 7 | 2 |  | 34 |
| K | 8 | 11 | 3 |  |  | 14 |
| L | 1 | 2 | 1 |  |  | 3 |
| M | 5 | 6 | 1 |  |  | 7 |
| N | 10 | 50 | 2 | 2 |  | 54 |
| O | 10 | 68 | 3 | 5 |  | 76 |
| P | 3 | 12 |  |  |  | 12 |
| **Summe** | 156 | **528** | **140** | **81** | **6** | **755** |

### Zeitraum: A, B, C, D, E

- **A (Darin-Zeiträume plausibel):**
  - Die Beispiele stimmen: Satzenden, halbe Bereiche, «seit 1401», Verweise, Plannummern und Fussnoten zählen nicht mehr
    (D512 1.19., D3530 1., D151150 9., D3018 02.3.1.21./22., D67, D69, D4175 1.C.1., D3063 1.9., D9985 27.2.1.).
  - Ausnahme: D3018 02.3.1.19. hat weiter = 2022 (Plannummer).
  - **Lücken:**
    - Der Jubiläumsfilter (Z. 563–567) löscht auch das Jubiläumsjahr: D2534 2.1., D150589 16.2.10., D3620 6., D2962 11.2.2.
      sind jetzt ohne oder mit falschem Zeitraum.
    - «siehe auch» löscht echte Daten (Z. 3056–3063): D176151 2.3., D150296 4.3.1., D450 13.
    - Die Nachruf-Regel kürzt ein ganzes Dossier (D452 7. 1928–1938 → 1938). Sie greift nicht, wenn die Lebensdaten auf eigener
      Zeile stehen (D149628 11.9.2. bleibt 1863–1932, D3861 4.).
- **B (Ausreisser ≤ 35 Jahre):**
  - Richtig nur bei echten Tippfehlern: D9983 5.6., D3087, D2960 11., D141056 6.1./9.2., D3018 03.6., D3842 1.
  - Sonst verwirft B echte Daten. Das betrifft 17 Fälle in der Sammelzeile, dazu D3063 40.1. und D3067 VIII.B.8. sowie 5
    Paketzeilen, die jetzt «schlechter» sind.
  - Ursachen:
    - Basis ist das Datum der Titelzeile, bei Teilen und Schachteln oft nur der erste Eintrag (Z. 3763–3772).
    - Bei reiner Spalte reicht eine Mehrheit von 3 zu 1 (Z. 4078–4080).
    - Lange echte Spannen werden zerlegt (Z. 4059–4062): D1739 27 «1830 – 1925».
  - Beispiele: D1877 1. 1916–1917 statt 18.08.1916–1990; D3727 10.2. bis 1939 statt 2005; D176795 5. verliert 1746, das ist ein
    Rückfall von Z213 aus Runde 5.
- **C (Jahre im Text der Einträge ohne Spaltendatum):**
  - Die Paketbeispiele sind richtig, insgesamt rund 30 von 47 Einheiten.
  - C zählt aber Zeilen, nicht Einträge (Z. 3089–3094). So kommen Jahre aus diesen Quellen herein:
    - Folgezeilen datierter Einträge: D3828 3.16. «Amtsperiode 1942 – 1946», D176060 7.3.4., D176151 11.1.;
    - Übergabe- und Zuordnungsvermerke: D176795 5. «24. März 2017», D2940 6. «April 2009»;
    - Publikationstitel und Lebensdaten: D3067 VIII.B.10., D4054 14.3.3. «1865»;
    - Archivvermerke: D3718 4.2.6. «bis 2006 unter der Archivsignatur»;
    - Spielzeit-Überschriften: D3170 6.4., wo die Monate verloren gehen.
  - Hat die Einheit ein Titeldatum, greift C gar nicht (D867 45., D3063 4.3.).
- **D (Gruppen):** Die Werte bleiben fast überall gleich, die Quelle ist genauer. Einziger Verlust: D2620 10.2. hat keinen
  Zeitraum mehr («1917 ff.» trägt nicht, Gruppen ohne Teile schätzen ihr Darin nicht, Z. 3876–3899).
- **E (Anmerkung):**
  - Um 13:15 gab es 371 Anmerkungen ohne Erklärung, die enger waren als von/bis; jetzt keine mehr (Z317 behoben).
  - 310 von 314 Anmerkungen mit «Darin:» passen genau.
  - Drei widersprechen von/bis, weil ein genaueres Titeldatum die erweiterte Spalte ersetzt (Z. 3798–3816): D149628 26.2.4.
    hat 09.–10.1935 statt 1935–1938, ebenso 18.1.4. und D4054 12.4. Teil 2.
  - Dazu kommt 4× ein Komma vor «;».

### Teile, Fussnoten: F, G, H

- **F:**
  - Die Erstnennungen haben wieder ihr eigenes Datum (Z351 D3828, Z276, Z293, Z296, Z337), und die überholten
    Inhaltsverzeichnis-Hinweise sind weg (Z353).
  - Echte Fortsetzungen mit eigenem, oft fehlerhaftem Titel werden aber nicht mehr vereinigt (`_ist_fortsetzung`
    Z. 4119–4129): D4054 5.5.3./12.3.4. (Z110 schlechter), D3861 3.2.1., D3352 1.2., D3186 3.1., D150296 4.3.2., D3063 6.2.
  - Nicht-Fortsetzungen mit gleichem Titel werden weiter vereinigt (D3466 :270., D3589 :1.).
  - «erste Nennung: …» fehlt bei einem Einzeljahr am Rand (D3484 :219./:349.).
- **G:** Die Teil-Nummern sind überall eindeutig, in PDF-Reihenfolge und gleich der Nummer im Titel. Die Titel vom Nachbarteil
  bleiben aber stehen: D151210 (121), D3231, D3357.
- **H:**
  - Alle 38 Fussnoten stehen beim Zeichen, auch bei einem Zeichen auf der Vorseite.
  - Fussnotenjahre zählen nicht mehr für Zeiträume (Z191, Z204, Z272, Z273, Z292 behoben).
  - Das Fussnotenzeichen bleibt im Titel stehen (D10744, gering, schon vor 13:15).

### Titel und Datumsformen: I, J, K, L, M

- **I:**
  - 323 von 325 entfernten neuen Datumsformen ergeben genau von/bis. Die 125 Spaltendaten in D438 stimmen, und der Datumsrest
    in D3466 sinkt von 210 auf 19 Titel (verbleibend «1921 & / 1922»).
  - Fehler:
    - D438 6.2.1.: «16. bis 19.» wird ins Datum gezogen, Titel «… vom Jahrhundert».
    - D3672 1.1.59.: «März / April 1932» verdrängt das Briefdatum.
    - D149628 23.1.1.280.: «1./ 5./ 7. Juni 1946» ergibt einen Zeitraum ab dem 5. Juni.
    - D149628 7.2.1.12.: Titel «… 1935 1931-1943 / 21.».
    - D3018 06.1.4.: «1964» ist ein eigener Darin-Eintrag.
    - D152401 1.: Das Darin ist zu einer Zeile verschmolzen, «ca.» geht verloren (so auch D152400 4.).
    - D512 1.29.: «20./27.Okt. 1986/» fehlt.
  - In D3466 bekommen Einheiten mit «JJJJ / JJ» den schmalen Spaltenrand (Z. 2914–2915). Das repariert rund 25 Umbrüche,
    verschmilzt aber 14 Einheiten; bei :249. rutscht «Rohrkanal» in den Titel.
- **J:**
  - Richtig: «WS», «SS», «Jg.» und «Semester» bleiben im Titel, «;» am Ende fällt weg, Bezüge wie 1351 oder 1805 zählen nicht.
  - Reste: «Zürich, den» (D9983 5.8.1.) und «(vom» (D3793 5.8.23.) am Titelende. Die Bibliothekssignaturen «(Bb 1686)» in
    D150589 zählen weiter als Jahr (schon vor 13:15).
- **K:**
  - Die angekündigten Fälle stimmen: D3581 1.1., D867 5., D152817 1-2, D152781 3.3., D149628-Werklisten. D3271 3.4.2. bleibt
    wie gewünscht.
  - Zusätzlich richtig: D2850 29. ist jetzt getrennt.
- **L:** 18 «dito»-Fälle in D3466 sind richtig. Ein «dito» nach Seitenwechsel bleibt im Titel (ID 1026, gering).
- **M:** D408 1.2.1. und D2857 1.3. sind richtig, der Hinweis bei D3484 595. stimmt.

### Signaturen: N, O, P

- **N:** Richtig:
  - D141 mit 26 Einheiten und «120Referendum»;
  - D140969 «3:1-3»;
  - D151150 10.5.2.;
  - D177448 8.1.4.5.;
  - D4057 20.2.;
  - D442 26.2.;
  - D3774 5.3./6.4.;
  - die Gegenbeispiele D3505 und D3170 bleiben unverändert.
  Fehler:
  - **D3828 3.1. (kritisch):** Der Listeneintrag «3.» direkt nach «2.» unter «3.1.» wird als Tippfehler für 3.2. gelesen
    (Z. 1424–1447). Weil später die echte 3.2. folgt, wird die Zeile als Übersichtszeile verworfen. Sie fehlt in allen
    Blättern, «Text erfasst» bleibt trotzdem 100 %.
  - D3774 6.4.: Der Titel beginnt mit «ohne Datum».
  - D3774 5.: Der Zeitraum ist auf 1865–1921 verengt (`vereinige` Z. 521–533).
- **O:**
  - Keine echte Signatur ist unterdrückt; alle 37 entfernten Einheiten waren erfunden. Richtig sind D631 (jetzt
    Bestandszeile), D3808, D8949, D3874 und D3204 36.–51.
  - **D3031 V.19. (kritisch):** Die Posten «4. Bauarchiv» (Schachteln 319–323) stehen im Darin von «Anteilsschein», das
    dadurch 1923–1986 bekommt.
  - D3204 42./51.: Schlussnotizen stehen bei der letzten Einheit.
  - D3324: «2 Rechnungen …» bleibt Signatur 2., weil O nur die Folge prüft, nicht die Spalte (Z. 1386–1389). Das ist ein alter
    kritischer Fehler.
- **P:** D65 III.P.:e., D67 III.Q.:a., D69 III.R.:b./:e. sind richtig (Z265, Z266, Z268 behoben).

## Gesamtabgleiche (Auftrag 3)

- **Bestandssignaturen:** unverändert; derselbe Abgleich mit dem PDF-Kopf wie in Runde 5.
- **«Nicht übernommen»:** 2'089 → 2'071 Zeilen.
  - D631 32 → 1 (Regel O, jetzt Bestandszeile).
  - D8949 9 → 23: Die Einleitung S. 1 steht nicht mehr im Darin der erfundenen 6.; das ist richtig, kein Verlust.
  - D3204 10 → 11, D3808 2 → 1, D2853 1 → 0.
- **«Text erfasst»:** D152817 99,98 → 100 % (Regel K), D512 99,87 → 99,86 % (Folgedaten).
- **«Wörter im Detailverzeichnis»:**
  - D3828 −10: Der Eintrag «3. Freisinnige Partei …» fehlt; die Prozentzahl merkt es nicht.
  - D8949 −100 (Einleitung, richtig), D631 +222, D3204 −3, D2853 +3.
- **Text, der nirgends mehr steht** (`textverlust.csv`, 329 Treffer):
  - Fast alles sind gewollte Datumsentfernungen aus Titeln (Regel I, z. B. D2767, D2975, D3793, D982, D258 12.) oder
    Umstellungen («…, Jan. – März 1969»).
  - Echter Verlust: D3828 3.1., D438 6.2.1. (Titel), D512 1.29./1.37. und das verschmolzene Darin in D152401.
- **Einheitenzahl:** 49'311 → 49'331 (+57 neu, −37 entfernt). Alle Zu- und Abgänge sind am PDF geprüft, alle nach N, O und P
  erwartet.
- **«[ohne Titel]»:** 35 → 33 (D4057 4./6. entfernt).
- **Doppelte Schlüssel:** 80 → 10 überzählige Zeilen, nur D2681 (PDF unverändert).
- **Titel, die nach dem Entfernen des Datums kaputt enden:**
  - Über alle geänderten Dateien gesucht (Funktionswort, Satzzeichen, Tageszahl, offene Klammer am Ende), neu kaputt ist nur
    D149628 7.2.1.12.
  - Dazu kommen aus der Wortprüfung «Zürich, den» (D9983 5.8.1.) und «(vom» (D3793 5.8.23.).
  - D438 6.2.108. «… stellen aus» ist richtig.
  - Von 315 gekürzten Titeln haben 20 Anzeichen; davon sind 18 «dito»-Fälle richtig.

## Neue Fehler am Stand 15:43, nach vermutlicher Ursache

| Vermutliche Ursache (Regel) | kritisch | mittel | gering | Zeilen |
|---|---:|---:|---:|---:|
| A |  | 6 | 1 | 7 |
| A/C |  | 1 |  | 1 |
| B |  | 4 |  | 4 |
| C |  | 7 | 1 | 8 |
| D |  | 1 |  | 1 |
| E |  |  | 2 | 2 |
| F |  | 2 | 1 | 3 |
| I |  | 8 | 3 | 11 |
| J |  |  | 2 | 2 |
| N | 1 | 2 |  | 3 |
| O | 1 | 3 | 1 | 5 |
| nicht angekündigt |  | 1 |  | 1 |
| vor 13:15 | 7 | 75 | 19 | 101 |
| **Summe** | **9** | **110** | **30** | **149** |

Die Zeile B ist eine Sammelzeile mit 17 Fällen. Die 5 Paketzeilen, die durch B schlechter wurden, stehen bei den
nachgeprüften Zeilen. Von den 101 Zeilen «vor 13:15» stammen 71 aus der D151210-Vollprüfung.

**Kritisch, schon um 13:15 vorhanden:**
- D1746: II.A)–O) und VII.1)/2) sind keine Einheiten.
- D2737: Die Doppelschachteln «3/4», «7/8», «10/11» werden nicht erkannt; ihre Einträge stehen bei der vorherigen Schachtel.
- D3012: Die Gliederung 1)–8) wird nicht erkannt.
- D3324: «2 Rechnungen …» wird Signatur 2. mit dem Inhalt von 1.
- D3505: Schlussteil und Schachtelliste sind erfundene Teile 2/3 von 7.3.
- D3657: «6. Anbau eines Ausstellungsraumes» wird als Übersichtszeile verworfen.
- D151210 8.1.1.44.: siehe oben.

**Mittel, schon um 13:15 vorhanden, u. a.:**
- D141: 44× Jahr mitten im Titel, abgeschnittene Titel, «, Schachtel 01» im Titel.
- D2630: Schachtel fehlt.
- D3505 2.1./2.2.
- D4057: Darin verschmolzen.
- D3466: zweizeilige Ortsnamen.
- D3672 4.31./4.32.
- D150589 17.x: Bibliothekssignaturen als Jahr.
- D3581 2.2.
- D867 24./26./31./45.: Spaltendatum der Titelzeile verloren.
- D2975: «seit 1798» im Vorlesungstitel; «(spätestens) SS 1908».
- D3316 3.1.
- D1343, D3589: Teile erben bzw. übernehmen fremde Zeiträume.
- D4054 10.3.4. Teil 15.
- D3861 3.2.1. Teil 2.

## Nach Hauptmuster

| Hauptmuster | behoben | teilweise | offen | schlechter | neu |
|---|---:|---:|---:|---:|---:|
| M01 Vorspann/Schlussvermerk verworfen | 2 | 5 | 2 |  | 1 (1 krit.) |
| M02 Echte Signatur nicht erkannt | 4 | 1 | 3 |  | 2 (2 krit.) |
| M03 Zahl/Marke als Signatur | 4 | 5 |  |  | 2 (2 krit.) |
| M04 Gliederungsebene nicht erkannt |  | 3 | 3 |  | 2 (2 krit.) |
| M05 Mehrzeilige Datumsspalte | 2 | 4 | 13 | 3 | 3 |
| M06 Rechte Spalte nicht abgetrennt | 3 | 3 | 24 | 1 | 4 |
| M07 Fremdtext im Darin | 2 | 1 | 31 |  | 1 |
| M08 Zeilenumbruch falsch | 2 | 7 | 15 |  | 22 |
| M09 Zeitraum aus falscher Quelle | 30 | 11 | 42 | 2 | 44 |
| M10 Darin falsch getrennt |  | 1 | 20 |  | 31 |
| M11 Schachtel-Nr. |  | 2 | 21 |  | 1 |
| M12 Datumsformat nicht erkannt | 4 | 7 | 11 |  | 6 |
| M13 Teile: Titel vom Nachbarteil |  | 2 | 2 |  | 1 |
| M14 Mappen/Schachteln: Titel aus Überschrift |  |  | 3 |  |  |
| M15 Umfang |  |  | 3 |  |  |
| M16 Zerrissene Wörter |  |  | 1 |  | 1 |
| M17 Kosmetik | 5 | 1 | 7 |  | 18 |
| M19 Sonstiges | 8 | 7 | 10 |  | 10 (2 krit.) |

## PDFs mit kritischen offenen oder neuen Fehlern

| PDF | kritisch offen/teilw./schlechter | neu kritisch | behoben | teilweise | offen | schlechter | neu |
|---|---:|---:|---:|---:|---:|---:|---:|
| D3828 | 3 | 1 | 1 | 1 | 2 |  | 2 |
| D3530 | 2 | 0 | 1 | 1 | 2 |  |  |
| D151210 | 0 | 1 | 1 |  | 1 |  | 74 |
| D140969 | 1 | 0 | 1 | 2 | 1 |  |  |
| D141024 | 1 | 0 |  | 1 |  |  |  |
| D149622 | 1 | 0 |  | 1 |  |  |  |
| D150689 | 1 | 0 |  | 2 | 7 |  |  |
| D1739 | 1 | 0 |  |  | 1 |  |  |
| D1746 | 0 | 1 | 1 |  |  |  | 1 |
| D1858 | 1 | 0 |  |  | 1 |  |  |
| D1880 | 1 | 0 |  | 1 | 3 |  |  |
| D2614 | 1 | 0 |  | 1 |  |  |  |
| D2737 | 0 | 1 |  |  |  |  | 1 |
| D3012 | 0 | 1 |  |  |  |  | 1 |
| D3018 | 1 | 0 | 1 | 4 | 7 | 1 | 2 |
| D3031 | 0 | 1 |  |  | 1 |  | 1 |
| D3060 | 1 | 0 |  | 1 | 3 |  |  |
| D3089 | 1 | 0 |  | 2 | 8 |  |  |
| D3105 | 1 | 0 |  | 1 |  |  |  |
| D3208 | 1 | 0 |  | 2 |  |  |  |
| D3271 | 1 | 0 |  | 2 | 5 |  |  |
| D3324 | 0 | 1 |  |  |  |  | 1 |
| D3505 | 0 | 1 |  |  |  |  | 2 |
| D3657 | 0 | 1 |  |  |  |  | 1 |
| D3774 | 1 | 0 | 1 | 1 | 6 |  | 2 |
| D3808 | 1 | 0 |  | 1 |  |  |  |
| D512 | 1 | 0 | 2 | 1 | 1 |  |  |

## Wichtigste offene Punkte

Die Zeilennummern beziehen sich auf `…/scratchpad/neu6/findmittel_zu_scope.py`.
1. **Regel B überarbeiten** (`_anschliessend` Z. 4049–4084, zeitraum_aus_titel Z. 3763–3772):
   - nur einzelne, chronologisch herausfallende Werte verwerfen (Nachbarn in Listenreihenfolge), nie mehrere Einträge;
   - Basis nur ein echtes Titel- oder Abschnittsdatum;
   - lange Spannen nicht zerlegen.
   Heute macht B in 20 von 40 geprüften Einheiten den Zeitraum falsch und 5 Paketzeilen schlechter.
2. **Regel C eintragsweise statt zeilenweise** (Z. 3089–3094). Folgezeilen datierter Einträge, Übergabe-, Zuordnungs- und
   Archivvermerke, Publikationstitel und Lebensdaten nicht mitzählen; C auch bei Einheiten mit Titeldatum anwenden.
3. **Regel A nachschärfen:**
   - Bei einem Jubiläum das Jubiläumsjahr behalten (Z. 563–567).
   - «siehe auch» nur für die Verweiszeile selbst gelten lassen (Z. 3056–3063).
   - Die Nachruf-Regel auch für Lebensdaten auf eigener Zeile anwenden, aber nicht für ganze Dossiers.
4. **Regel N** (Z. 1424–1447): Die Lesung «26.» nach «26.1.» als 26.2. nur ausserhalb nummerierter Listen anwenden (D3828 3.1.
   kritisch). Eine als Tippfehler gelesene Zeile nie als Übersichtszeile verwerfen.
5. **Regel O:**
   - D3031 V.19. (kritisch): «4. Bauarchiv» mit seinen Posten erkennen.
   - D3324: die Spalte prüfen, nicht nur die Folge (Z. 1386–1389).
   - Schlussnotizen nicht bei der letzten Einheit ablegen (D3204, D2630, D3808).
6. **Regel F** (`_ist_fortsetzung` Z. 4119–4129): Fortsetzungen auch an Schachtel- bzw. Seitenfolge und Datumsanschluss
   erkennen, nicht nur am Titel; Nicht-Fortsetzungen mit gleichem Titel trennen.
7. **Regel I:**
   - D438 6.2.1. «16. bis 19.» korrigieren.
   - Den schmalen Spaltenrand bei «JJJJ / JJ» in D3466 korrigieren.
   - «ca.» in der Anmerkung behalten (D152400, D152401).
   - Das Darin in D152401 wieder trennen.
   - Den Titel von D149628 7.2.1.12. korrigieren.
8. **D151210:**
   - Titel vom Nachbarteil (Z291, 121 Teile; `ergaenze_titel` Z. 4154–4157).
   - 8.1.1.44.: verrutschte Signatur.
   - Darin-Trennung in 8.1.1.x (`ist_umbruch`, `flicke_listen`) und bei Rollenbüchern.
   - Zeiträume aus dem ersten Dokument bzw. aus Buchtiteln.
   - Laut Vergleich bestehen 56 der 74 Funde in regress92 unverändert weiter.
9. **Alte kritische Fehler:** D1746 II.A)–O), D2737 Doppelschachteln, D3012 1)–8), D3324, D3505 7.3., D3657 6.
10. **Bewusst offen** wie besprochen: D3828, D3530, D141024, D512, D149622, D3208, D2614, D1739, D1858.

## Dateien

- `stichproben/nachpruefung6.md` – dieser Bericht.
- `stichproben/funde_nachpruefung6.csv`:
  - 492 Zeilen: 343 nachgeprüft (in der Reihenfolge von `methode/np6_pruefliste.csv`), 149 neu, davon 74 aus der
    D151210-Vollprüfung.
  - Spalten `pdf;seite;signatur;feld;schwere;soll;ist;bemerkung;status;neu_ist`.
  - `ist` = Stand 13:15, `neu_ist` = Stand 15:43. Status behoben / teilweise / offen / schlechter / neu.
  - D151210-Zeilen tragen den Vermerk «Art: …» und «[regress92 (16:16): …]».
- `stichproben/methode/`: `ANLEITUNG_NACHPRUEFUNG6.md`, `np6_auswahl.py`, `np6_pruefliste.csv`, `np6_geaendert.txt`,
  `np6_zusammenfuehren.py`.
- `stichproben/roh/`:
  - `np6_vorbewertet.csv`;
  - `np6_gruppe_0.csv` … `np6_gruppe_6.csv`, je mit `_regeln.csv` und `_notizen.md`;
  - `np6_d151210_D1.csv` … `D4.csv`, je mit `_seiten.csv` und `_notizen.md`;
  - `np6_d151210_regress92.txt` (Stand der Funde in regress92).
- Scratchpad `…/np6/`:
  - `diff/`, `diff_test/`, `hinweise/`;
  - `zeitraum.csv`, `familien.csv`, `textverlust.csv`, `titelschnitt.csv`, `titelende.csv`, `teile.json`;
  - `gesamt.json`, `zaehlung.json`, `skript.diff`;
  - `d151210/seiten/`, `regress92/`.
