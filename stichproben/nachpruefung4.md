# Vierte Nachprüfung am Excel-Stand 20.11.2026, 11:30

Geprüft wurde `findmittel_excel/` vom 20.11.2026, 11:30, dazu `testdaten_excel/` und `D151210_scope_import.xlsx`. Das Skript
hat sha256 `d477ff64c6a5eaa2…` und 4874 Zeilen.
- **Schnappschuss «neu4»:** `/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/neu4/`.
  Alle Zeilennummern beziehen sich auf das Skript dort. Beim Abschluss waren das Projektskript und `findmittel_excel/` noch
  unverändert.
- **Vergleich:** mit dem Stand 08:25 der dritten Nachprüfung (`…/scratchpad/neu3/`).
- **Geänderte Dateien:** Inhaltlich geändert sind 255 Dateien in `findmittel_excel/`, genau die Liste in
  `zellvergleich_0825_1130.txt`, dazu 6 Testdateien. D3031 fehlt in der Liste der Hauptsession. In 715 Dateien hat sich
  im Blatt Info nur die Zeile «Erzeugt» geändert; sie zählt nicht als Änderung.
- **Belege:** Jedes Urteil ist am PDF belegt.

## Kurzfazit

- **255 nachgeprüfte Zeilen:** 70 behoben, 36 teilweise, 146 offen, 3 schlechter.
  - 51 Zeilen liegen in PDFs, die seit 08:25 inhaltlich unverändert sind. Dort gilt der Befund von 08:25 weiter.
- **Kritische Zeilen: 40 von 58 behoben**, 14 teilweise, 4 offen, keine schlechter.
  - 11 der 18 nicht behobenen sind die bewusst offenen Punkte (Auftrag 4), unverändert und bestätigt.
  - Echte Restfehler sind 7 Zeilen, alle teilweise behoben:
    - D3060: die Porträtbilder von S. 8 stehen bei :6;
    - D3089 (dafür ist XI. neu erfunden);
    - D3105 «Band 1»;
    - D150689 1.2.4.;
    - D1880, Unterabschnitte a.–i.;
    - D3018: 08.9. und 09. sind wieder da, der Rest von S. 78 steht aber bei 08.8.;
    - D3099 1.2.5., Teil ohne Nummer.
  - Von den 15 kritischen Fehlern, die die 3. Nachprüfung neu gefunden hatte, sind 12 behoben und 3 teilweise (D1880,
    D3018 08.9./09., D3099). Behoben sind z. B.:
    - D10675: 742.100–117 als Einheiten, die Unter-Unterpositionen, «712.» und die Dubletten unter 440;
    - D3018 07.3.: die Zwischenüberschrift auf S. 67;
    - D2534 6.3.;
    - D3275, D3778, D4098: die Bestandssignatur;
    - D8945: der Schlussvermerk;
    - D3405: 6.5./6.6.
- **Mittel/gering in geänderten PDFs (148 Zeilen):** 30 behoben, 16 teilweise, 99 offen. Die offenen sind fast alle laut
  Diff unverändert. 3 Zeilen sind schlechter geworden:
  - Z95: D2951 1.22. hat jetzt den Titel der übergeordneten Einheit.
  - Z205: Die neuen Teile in D4054 nehmen den Zeitraum nur aus der ersten Datumszeile.
  - Z309: D3067 Schachtel 302 hat = 1958 statt 1943–1958.
- **Neue Fehler: 86**, davon 15 kritisch, 55 mittel und 16 gering.
  - Aus den Regeln a–h stammen 31, 4 davon kritisch:
    - D9983 5.6. → 5. (Regel c);
    - D3089 XI. erfunden (Regel h);
    - D3253 und D1880 «f. Heizamt» (Regel b).
  - Aus nicht angekündigten Änderungen stammen 31, davon 2 kritisch: D3018 02.3.l. und D1880 D.III./G.III.
  - Schon um 08:25 vorhanden, jetzt erst erfasst: 24, davon 9 kritisch, u. a. D3774, D49/D65/D67/D69, D2558, D3271 und D3466.
- **Regelstichprobe (Auftrag 3):** Am PDF geprüft wurden 676 Einheiten in 129 PDFs. 425 sind besser, 154 gleich, 85 schlechter
  und 12 unklar. Die Regeln wirken überwiegend wie angekündigt:
  - d ohne neuen Fehler; e nur mit kleinen Nebenwirkungen (1 mittel, 2 gering).
  - b, c und h je mit einem kritischen Ausreisser: b bei der Schriftgrösse (D3253, D1880), c in D9983, h in D3089.
  - Am meisten Nebenwirkungen haben a und g, vor allem beim Zeitraum.
- **Kennzahlen:**
  - Einheiten in `findmittel_excel/`: 49'191 → 49'314.
  - «[ohne Titel]»: 48 → 44.
  - «Text erfasst» 100 %: 693 → 694 von 715 PDFs.
  - «Nicht übernommen» steigt stark, vor allem durch Regel b und die Fussnoten, z. B. D10675 0 → 43 und D3684 22 → 32.
    Textverlust ist das nur bei den Fussnoten (siehe unten).
- **Gegenprobe:** 8 Urteile der Prüfagenten habe ich selbst am PDF nachgesehen, alle hielten (D9983, D3067 Z309, D3089 XI.,
  D49, D1880 f., D3253, D2979 8.1., D2558).

## Methode

- **Vergleich 08:25 → 11:30** über alle 727 Dateien (alles Hilfsdateien in `…/scratchpad/np4/`):
  - Blattweiser Inhaltsvergleich ohne die Zeile «Erzeugt» (`zellen.py`).
  - Einheitenvergleich je Datei mit `methode/diff_stand.py` (`np4/diff/`).
  - Geänderte Prüfhinweise (`np4/hinweise/`).
  - Art jeder Änderung (`regelart.py`: darin geteilt, titel->darin, text neu …).
  - Weitere Abgleiche:
    - Text, der nirgends mehr vorkommt;
    - gekürzte Titel mit Schnitt im Satz;
    - neue «; »-Verbindungen;
    - Bestandssignatur gegen den PDF-Kopf;
    - Vorspann, Schlussvermerke und «Nicht übernommen» im Blatt Info.
- **Auswahl** (`methode/np4_auswahl.py`, Liste `methode/np4_geaendert.txt`): alle Zeilen aus `funde_nachpruefung3.csv` mit
  Status ≠ behoben.
  - Alle 58 kritischen (Auftrag 1).
  - Alle 148 übrigen in geänderten PDFs (Auftrag 2).
  - 49 übrige in unveränderten PDFs; dort wurde der Befund übernommen, «neu» wird «offen».
  - Nummern: Z<n> = n-te Datenzeile von `funde_nachpruefung3.csv`.
- **Prüfung:** fünf Prüfagenten (Gruppen 1–5) und die Hauptprüfung (Gruppe 0) nach `methode/ANLEITUNG_NACHPRUEFUNG4.md`.
  - Jede Gruppe prüfte ihre Paketzeilen und für ihre Regeln die Beispiele der Hauptsession am PDF.
  - Dazu prüfte sie jede entfernte und neue Einheit ihrer PDFs sowie eine Stichprobe der geänderten.
  - Für Regel a kam eine Zufallsstichprobe von 8 weiteren PDFs dazu (Startwert 20261122).
  - Für Regel b wurden alle neuen Hinweise geprüft.
  - Gruppe 0 prüfte die Bestandssignaturen, die bewusst offenen Punkte und die Gesamtabgleiche, dazu geänderte PDFs ohne
    Paket mit Auffälligkeiten (D3774, D3357, D151399, D3612, D3321, D3470, D10744 …).
- **Urteile der Regelstichprobe:** je geprüfte Einheit besser / gleich / schlechter / unklar in
  `roh/np4_gruppe_N_regeln.csv`.
- **Regel eines neuen Fehlers:** Die Regel ist die vermutliche Ursache nach der Änderungsliste der Hauptsession. «Nicht
  angekündigt» steht für Änderungen, die im Vergleich sichtbar sind, aber nicht in a–h stehen. «vor 08:25» heisst, der
  Fehler bestand schon im Stand 08:25.

## Ergebnis nach Auswahl

| Auswahl | behoben | teilweise | offen | schlechter | Zeilen | davon PDF unverändert |
|---|---:|---:|---:|---:|---:|---:|
| kritische Zeilen (offen/teilweise/neu) | 40 | 14 | 4 |  | 58 | 2 |
| mittel/gering in geänderten PDFs | 30 | 16 | 99 | 3 | 148 |  |
| mittel/gering in unveränderten PDFs (übernommen) |  | 6 | 43 |  | 49 | 49 |
| **Summe** | **70** | **36** | **146** | **3** | **255** | **51** |

| Herkunft | behoben | teilweise | offen | schlechter | Zeilen |
|---|---:|---:|---:|---:|---:|
| aus früheren Runden, kritisch | 28 | 11 | 4 |  | 43 |
| aus früheren Runden, mittel | 11 | 17 | 109 | 2 | 139 |
| aus früheren Runden, gering |  |  | 4 |  | 4 |
| neu in der 3. Nachprüfung, kritisch | 12 | 3 |  |  | 15 |
| neu in der 3. Nachprüfung, mittel | 19 | 5 | 27 | 1 | 52 |
| neu in der 3. Nachprüfung, gering |  |  | 2 |  | 2 |

Die kritischen Zeilen sind behoben in D3067 (6), D10675 (6), D141005, D3018, D3672, D3060 (je 2) sowie in D10575, D2839,
D3063, D414, D3484, D71, D1739, D2990, D2708, D2729, D2589, D150689, D3466, D3684, D2534, D3275, D3405, D3778, D4098 und
D8945 (je 1).

## Bewusst offene Punkte (Auftrag 4) – bestätigt

| Punkt | Zeilen | Stand 11:30 |
|---|---|---|
| D3828 «1. 1.», «6. 5.» (Zählung je Abschnitt) | Z62, Z129, Z130, Z131 | unverändert; nur 12. hat jetzt Titel und Darin richtig getrennt |
| D3530 | Z61, Z123, Z124 | unverändert; nur in 2.2. zwei verklebte Darin-Zeilen getrennt |
| D141024 | Z65 | Excel unverändert |
| D512 | Z135, Z215, Z216, Z267 | Excel unverändert |
| D149622 | Z225 | Verteilung auf Schachtel 1–3 unverändert; die Jahreszeilen sind jetzt getrennt (Z281 behoben) |
| D3208 Abzeichensammlung, Hinweis vorhanden | Z254 | unverändert; die Abzeichen-Paare sind jetzt getrennt (Z323 teilweise) |
| D2614 Bestände nur mit Beschreibung | Z238 | unverändert; die Seminararbeiten sind getrennt (Z296 behoben) |
| D1739 «Mappe mit Grossformaten» | Z58 | weiter ohne eigene Einheit; die drei Zeilen stehen jetzt sauber getrennt im Darin. «Kläranlagen» behoben (Z57) |

## Regelstichprobe (Auftrag 3)

| Regel | PDFs | besser | gleich | schlechter | unklar | geprüfte Einheiten |
|---|---:|---:|---:|---:|---:|---:|
| a Absatzschwelle 7,5 pt | 49 | 106 | 43 | 17 |  | 166 |
| b Zwischenüberschrift → Hinweis | 17 | 44 | 1 | 3 |  | 48 |
| c Übersicht im Dezimalverzeichnis | 2 | 16 | 1 | 2 |  | 19 |
| d Gruppensignatur → Zwischenüberschrift | 4 | 11 | 3 |  |  | 14 |
| e Bereiche, Doppelnummern, Doppelpunkt | 6 | 20 |  | 3 |  | 23 |
| f Schachtellisten | 9 | 18 | 13 | 4 | 1 | 36 |
| g fetter Titel + Beschreibung | 9 | 28 | 11 | 14 | 3 | 56 |
| h kleinere Regeln | 15 | 38 | 6 | 1 |  | 45 |
| Bestandssignatur (nicht angekündigt) | 6 | 6 |  |  |  | 6 |
| Eltern-Zeitraum (nicht angekündigt) | 3 | 2 | 1 |  |  | 3 |
| übrige Änderungen (D1880, D10675, D4054, Teile, Zeitraum …) | 58 | 136 | 75 | 41 | 8 | 260 |
| **Summe** | 129 | **425** | **154** | **85** | **12** | **676** |

- **a) Absatzschwelle 7,5 pt**
  - Gemessen: Echte Absätze haben 7,7–8,0 pt Abstand, Folgezeilen 1,7–2,2 pt.
  - Getrennt wird also richtig, in D3466 (499 Einheiten «titel->darin»), D1180, D3470, D3525 usw. ohne Textverlust.
  - Nebenwirkung beim Zeitraum: Er nimmt die Datumsspalte der abgetrennten Zeile nicht mehr mit (`verarbeite` Z. 2636–2656).
    - D2979 8.1.–8.35. (33 Einheiten): «Personendossiers 1886» hatte 1886–1928, hat jetzt = 1886.
    - D151150 2.3. und 14.2.5.; D150589 2.3.35.
  - Weitere Nebenwirkungen:
    - D1180: Titel mit Datumsrest «Sechseläuten vom 19. /», 5 Fälle.
    - D3484 :365. und :596.: Fortsetzungszeilen mit 20 pt Abstand sind abgetrennt.
    - D2951 1.22.: Titel der übergeordneten Einheit (`ist_namensliste` Z. 2436).
    - D151150: Spaltenkopf «Sch.» im Darin, 26 Einheiten.
- **b) Zwischenüberschrift → Prüfhinweis**
  - 41 von 42 neuen Hinweisen sind echte Zwischenüberschriften, vollständig und bei der ersten folgenden Einheit.
  - Fehlgriff D3253 S. 2 (kritisch): Der Listeneintrag «Unidentifizierter Text ("Tirilin")» wird zum Hinweis bei 3. Ursache:
    `grund_groesse` (`baue_vorkommen` Z. 1788–1789) zählt die 10-pt-Einleitung mit, dadurch gilt jede 12-pt-Zeile als grösser
    (Z. 2048).
  - Fehlgriff D1880 «f. Heizamt» (kritisch, Z. 2045–2057): f.I.–IV. werden Teile von E.I.–E.IV. unter Kanzlei, das sind 11
    Einheiten; E.IV. gibt es im PDF nicht.
  - Lücken, schon vor 08:25: D4173 1.13., D9978 28.4.24., D3204 11.
- **c) Übersicht ins Darin**
  - D150689 hat keine doppelten Signaturen mehr; nichts ist verloren, und keine echte Einheit wird als Übersicht behandelt.
  - Bei D150689 7. endet die Übersicht zu früh (Z. 1972–1973), die Übersicht von 3.10. wird nicht erkannt (gering).
  - D9983 (kritisch): 53 Darin-Einträge von 5.6. stehen jetzt bei 5. Die Umleitung für «Weitere Handschriften:»
    (`baue_vorkommen` Z. 2163–2172, angewandt Z. 2195–2196) greift, weil 5. jetzt auf «Drucksachensammlung,
    Detailverzeichnis:» endet.
- **d) Gruppensignatur → Zwischenüberschrift**
  - D3067 VIII., D177460 C, D10675 712 und D3031 IV.q. sind richtig. Kein neuer Fehler.
- **e) Signaturformen**
  - Richtig umgesetzt: D3672 mit 6 Bereichen und 1.1.1018., D141005 20/21, D3484 594/595, D141020 5.4.2., D176060 14.3.16.,
    D2857 1.224.3.
  - Nebenwirkungen: D3672 1.1.1017. verliert die Genauigkeit des Zeitraums (21.05.1944 → 1944). Dazu kommen zwei
    irreführende Hinweise «nach N folgt N» (D2857 1.3., D3484 :595.).
- **f) Schachtellisten**
  - Richtig: D3060 :8 «Schachteln 8 und 9», D3725 :7 «Mappen 7 – 10», D3105 als Schachtelliste. Im Umfang stehen dabei
    Nummern statt einer Menge (Gestaltungsfrage).
  - D2534: Schachtel 1–6 fallen samt ihrer Zuordnung ganz weg (mittel). Schachtel 7–13 bleiben erfundene Einheiten (kritisch,
    schon vor 08:25).
  - D2735 Mappe 2 hat = 1912 statt 1912–2009. Bei D152781 wird die Übersicht ignoriert.
  - D2872 ist seit 08:25 unverändert; dort sind keine Einheiten verdrängt.
- **g) Fetter Titel + Beschreibung ins Darin**
  - Klare Korrektur in D2937 (31 Zeiträume) und D867 (28): Sie entsprechen jetzt der Datumsspalte.
  - Nebenwirkungen:
    - «undatiert» und «ca.» der Beschreibungszeile gehen verloren: D176060 12 Fälle, D3993, D3986, D408; insgesamt verlieren
      17 Einheiten «undatiert».
    - Titel werden bei «in:» abgeschnitten: D176060 1.68., 14.1.98., 14.3.16. Bei 1.68. wird der Zeitraum von 07.02.1990
      zu 1990 (`kopf_und_rumpf` Z. 2557–2567).
    - Die Darin-Schätzung liest Jahreszahlen aus dem Text: D2937 C.2.0. «Landi 1964», D151150 9. 1772–2024
      (`jahre_im_text` Z. 523).
    - D408 5. hat 1982–1984 statt 1860–1984.
    - D3774: Einträge werden mit «; » zusammengezogen.
  - 296 Einheiten wechseln von «Datumsspalte» zu «Darin (geschätzt)», 194 davon mit gleichem Wert. Das bringt nur mehr
    Prüfhinweise (gering).
- **h) Kleinere Regeln**
  - Richtig: D3089 (B./H./A./C. weg), D3684, D2589, D414, D3466 «Teil 1928», D71 «d) Rechnungen», D2708 und D2729.
    Ebenso D3612 und D3321, wo eine Initiale nach «und» stand.
  - D3089 (kritisch): VII.197.:XI. ist erfunden, aus «X. und / XI. Jahrbuch …» auf S. 37. Die Initialen-Regel
    (`baue_vorkommen` Z. 1848–1854) prüft nur einzelne Buchstaben.
  - D49, D65, D67, D69 sind seit 08:25 unverändert. «d)» hängt dort schon richtig, aber 11 leere Doppel-Kategorien
    III.x.:a.–:e. bestehen weiter (kritisch, schon vor 08:25).

## Neue Fehler am Stand 11:30, nach vermutlicher Ursache

| Vermutliche Ursache | kritisch | mittel | gering | Zeilen |
|---|---:|---:|---:|---:|
| a | | 9 | 2 | 11 |
| b | 2 | 1 | | 3 |
| c | 1 | | 2 | 3 |
| d | | | | 0 |
| e | | 1 | 2 | 3 |
| f | | 3 | | 3 |
| g | | 5 | 2 | 7 |
| h | 1 | | | 1 |
| nicht angekündigte Änderung («unklar») | 2 | 22 | 7 | 31 |
| schon um 08:25 vorhanden | 9 | 14 | 1 | 24 |
| **Summe** | **15** | **55** | **16** | **86** |

### Nicht angekündigte Änderungen (31 Zeilen, 2 kritisch)

| Änderung | kritisch | mittel | gering | PDFs |
|---|---:|---:|---:|---|
| Eltern-Zeitraum auch aus geschätzten Kindern (`ergaenze_zeitraeume` Z. 3466–3477) | | 5 | | D2534, D4054, D4175, D10585, D150589 |
| Doppelpunkt-Regel Titel/Darin (`kopf_und_rumpf` Z. 2557–2567) | | 4 | | D3271, D4173, D149628, D152781 |
| Fussnoten nicht mehr importiert (`baue_vorkommen` Z. 1809–1818) | | 3 | | D10675, D10744, D151217 |
| D1880 neu gegliedert | 1 | 2 | | D1880 |
| Positionen nur aus der Zusammenfassung (`einheiten_nur_im_vorspann` Z. 3290–3322) | 1 | 1 | | D3018 |
| Titelreparatur «(1807 –» / «1890)» (`kopf_und_rumpf` Z. 2549–2552) | | 2 | | D150689 |
| Teile wiederholter Signaturen ohne Teil-Nr. | | 1 | | D4054 |
| übrige Zeilen- und Darin-Logik | | 4 | 7 | D2632, D2717, D3018, D3271, D3316, D3357, D10585, D10675, D149888, D151399, D176795 |

- **Eltern-Zeitraum aus geschätzten Kindern** (358 Einheiten mit Quelle «Untereinheiten (geschätzt)»)
  - Behebt den Fund aus Runde 3, z. B. D3099 7., D3018 Z299, D177460 D/F.
  - Übernimmt aber falsche Schätzungen der Kinder:
    - D10585 3.16. 1798–1953 (Lebensdaten), 8. ab 1758;
    - D4175 1. ab 1805 (Medaille);
    - D150589 16. ab 1664;
    - D2534 3. 1827–2002 (Bibliotheksnummern «Na …»);
    - D4054 9.24.2.
- **Doppelpunkt-Regel**
  - Gekürzt wurden 48 Titel, meist richtig («Bücher:», «Ehrungen:»).
  - Falsch geschnitten:
    - D149628 23.1.1.873. «… Sergej Rachmaninow», 23.1.1.942. «… [Peter Schlegel»;
    - D4173 1.32. (das gleich gebaute 1.33. behält den Inhalt im Titel);
    - D3271 3.4.2./3.4.3.
- **Fussnoten**
  - Sie stehen nicht mehr bei der falschen Einheit, gehen aber dem Import ganz verloren; nur das Blatt Vollständigkeit
    nennt sie als «Fussnote».
  - Betroffen: D10675 mit 41 Zeilen (Fn. 1–27), D10744 mit 9, D151217 mit 2.
  - Bei Fussnoten mit Dossierbezug fehlt damit Inhalt, z. B. bei D10744 der Umplatzierungsvermerk zu 430.1.601.9.
- **D1880** ist neu gegliedert: 44 → 146 Einheiten, Vorspann 542 → 168 Zeilen. Das ist eine grosse Korrektur (Z292 teilweise).
  Neu bzw. weiter fehlerhaft:
  - D.III. und G.III. nach der Bereichsmarke «I.-II.» werden nicht erkannt (kritisch).
  - Die 41 Unterabschnitte a.–i. unter F.III./H.II. fehlen.
  - Die Schachteln werden nicht weitergezogen.
  - Serienköpfe stehen im Darin von R.
- **D3018**
  - «09 NACHTRÄGE» und 08.9. sind wieder da.
  - Aus dem Tippfehler «3.l.» der Zusammenfassung entsteht aber die Doppel-Einheit 02.3.l. (kritisch).
  - 09. bekommt = 15.04.2009 aus dem Ergänzungsvermerk.
- **D10675:** Der Registraturplan ist sonst eine grosse Korrektur (Z60, Z272, Z274–Z278 behoben). Neu sind die abgeschnittenen
  Titel von 742.105 und 742.113 (`ist_umbruch` Z. 2287–2289).
- **Übrige Zeilen- und Darin-Logik**
  - Beginnt eine Folgezeile mit einer Zahl, wird sie mit «; » angehängt: «Zürich; 1840 [16]», «geb.; 16. Dezember 1857»,
    «7. August; 1800» (D2632, D3525, D149622, D2947).
  - D3357 4.6.1.: Die neuen Teile zu 1953, 1966 und 1978 haben den ersten Listeneintrag als Titel.
  - D151399 7.3.: Der Titel beginnt mit «, inkl. …». Dort sind 7.2.–7.10. jetzt richtig eigene Einheiten.
  - D3316 1.: «bis» als Anschlusswort (Z. 2244).
  - D176795 5.: endet am Übergabedatum 2017.

### Schon um 08:25 vorhanden, jetzt erst erfasst (24 Zeilen, 9 kritisch)

- **Kritisch**
  - **D3774:**
    - Die Einleitungskapitel 1.–7. sind als Einheiten VII.47.:1.–:7. importiert.
    - Die echten Abteilungen «VII. 47.:2. Akten», «:3. Organisation und Verwaltung» usw. hängen als gleichnamige Kinder
      darunter.
    - Alle Unternummern 1.1.–3.53 stehen nur im Darin.
  - **D49, D65, D67, D69:** 11 leere Doppel-Kategorien III.x.:a.–:e.
  - **D2534:** Schachtel 7–13 sind erfundene Einheiten.
  - **D2558:** 3. «Werbematerial» fehlt.
  - **D3271:** Die Bereichszeile «4.2.22. bis 4.2.67.» wird zur Serie.
  - **D3466:** 168 «div. O. Kühltürme etc.» fehlt (klein_ok Z. 1287).
- **Mittel**
  - Bestandszeitraum D3778: 1778–20.08.1992 statt der genannten Laufzeit «1778 - 1939».
  - Bestandszeitraum D3275: 1741–2023, mit Lebensdaten und Bibliotheksnummer.
  - D3628 4.1.2.: nur die letzte Zeile der Datumsspalte zählt.
  - Umfang «(2 Schachteln)» in Klammern wird nie erkannt (UMFANG_RE Z. 571, ca. 250 Einheiten).
  - D3466: Datumsformate «1924 / 25» und «1921 & / 1922» werden nicht erkannt (ca. 181 Titel).
  - Bei D176060 waren schon 72 Titel über `teile_langen_titel` abgeschnitten, bei D1180 69 Titel «vom 19. /».
  - Regel-b-Lücken bei D4173, D9978 und D3204.
  - D867 3., D67 und D3067 IV.A.d.

## Nach Hauptmuster

| Hauptmuster | behoben | teilweise | offen | schlechter | neu |
|---|---:|---:|---:|---:|---:|
| M01 Vorspann/Schlussvermerk verworfen | 9 | 5 | 2 |  | 3 |
| M02 Echte Signatur nicht erkannt | 10 | 1 | 2 |  | 3 (3 krit.) |
| M03 Zahl/Marke als Signatur | 9 | 3 |  |  | 4 (4 krit.) |
| M04 Gliederungsebene nicht erkannt | 8 | 2 | 2 |  | 2 (2 krit.) |
| M05 Mehrzeilige Datumsspalte |  | 3 | 18 | 1 | 1 |
| M06 Rechte Spalte nicht abgetrennt | 1 | 4 | 17 |  | 2 |
| M07 Fremdtext im Darin | 5 | 1 | 20 |  | 6 |
| M08 Zeilenumbruch falsch | 10 | 5 | 10 |  | 9 |
| M09 Zeitraum aus falscher Quelle | 7 | 6 | 20 | 1 | 22 |
| M10 Darin falsch getrennt | 5 | 1 | 10 |  | 9 |
| M11 Schachtel-Nr. | 1 | 1 | 18 |  | 3 |
| M12 Datumsformat nicht erkannt | 1 | 1 | 14 | 1 | 3 |
| M14 Mappen/Schachteln: Titel aus Überschrift |  |  | 1 |  | 1 |
| M15 Umfang |  |  | 1 |  | 1 |
| M16 Zerrissene Wörter |  |  | 1 |  |  |
| M17 Kosmetik |  |  | 3 |  | 6 |
| M19 Sonstiges | 4 | 3 | 7 |  | 11 (6 krit.) |

Die neuen Fehler häufen sich beim Zeitraum (M09: 22). Die Umbauten an Titel und Darin (Regeln a, g und die Doppelpunkt-Regel)
verschieben Datumszeilen aus dem Kopf ins Darin. Die Zeitraumbildung hat das noch nicht nachvollzogen.

## PDFs mit kritischen offenen oder neuen Fehlern

| PDF | kritisch offen/teilweise | davon bewusst offen | neu kritisch |
|---|---:|---:|---:|
| D1880 | 1 |  | 2 |
| D3018 | 1 |  | 1 |
| D3089 | 1 |  | 1 |
| D3828 | 3 | 3 |  |
| D3530 | 2 | 2 |  |
| D150689, D3060, D3099, D3105 | je 1 |  |  |
| D141024, D149622, D1739, D2614, D3208, D512 | je 1 | je 1 |  |
| D2534, D2558, D3253, D3271, D3466, D3774, D49, D65, D67, D69, D9983 |  |  | je 1 |

## Wichtigste offene Punkte

1. **Neu und kritisch, mit klarer Ursache**
   - D9983 5.6. → 5.: Umleitung «Weitere Handschriften:» nach Regel c.
   - D3089 XI. erfunden: Initialen-Regel nur für Buchstaben.
   - D3253 und D1880 «f. Heizamt»: `grund_groesse` und Schriftgrössen-Test bei Regel b.
   - D3018 02.3.l.: Tippfehler aus der Zusammenfassung.
2. **Zeitraum nach den Titel/Darin-Umbauten**
   - Spaltendaten abgetrennter Zeilen sollten mitzählen (D2979 mit 33 Einheiten, D151150, D150589).
   - «undatiert» und «ca.» sollten erhalten bleiben (17 Einheiten mit «undatiert», D176060).
   - Die Darin-Schätzung sollte nur Spaltendaten statt allen Jahreszahlen im Text nehmen (D2937, D151150 9.).
   - Eltern sollten falsch geschätzte Kinder nicht übernehmen (D10585, D4175, D150589, D2534, D4054).
3. **Titel-Schnitte durch die Doppelpunkt-Regel**
   - D149628, D4173, D3271.
   - «in:» in D176060, dazu die 72 alten Fälle über `teile_langen_titel`.
4. **Fussnoten:** Sie sollten beim Fussnotenzeichen der Einheit ins Darin statt nur ins Blatt Vollständigkeit (D10744 mit dem
   Umplatzierungsvermerk, D10675 Fn. 4, 5, 20).
5. **Alt und kritisch, jetzt erst gefunden**
   - D3774: die ganze Gliederung;
   - D49/D65/D67/D69: Doppel-Kategorien;
   - D2534: Schachtel 7–13, dazu Schachtel 1–6 jetzt weg;
   - D2558 3.;
   - D3271 4.2.22.;
   - D3466 168.
6. **Kritische Restfehler aus früheren Runden**
   - D1880: a.–i., D.III./G.III.;
   - D3099 1.2.5.: Teil ohne Teil-Nummer und doppelter Schlüssel;
   - D3060: Porträtbilder von S. 8 bei :6;
   - D3105 «Band 1»;
   - D150689 1.2.4.;
   - D3018: Rest von S. 78 bei 08.8.
7. **Schlechter geworden:** Z95 D2951 1.22., Z205 D4054 (Teile nur mit erster Datumszeile), Z309 D3067 V.B. 302.

## Dateien

- `funde_nachpruefung4.csv`:
  - 341 Zeilen: 255 nachgeprüfte und 86 neue.
  - Spalten wie `funde_nachpruefung3.csv`, Trennzeichen Semikolon.
  - `ist` = Stand 08:25 (bei nachgeprüften Zeilen = `neu_ist` der 3. Nachprüfung), `neu_ist` = Stand 11:30.
  - Neue Zeilen tragen «Regel: a–h | unklar (…) | vor 08:25» in der Bemerkung.
  - Eine Sammelzeile über zwei PDFs (D150689/D9983) steht unter D150689, mit Vermerk.
- `methode/`:
  - `ANLEITUNG_NACHPRUEFUNG4.md`;
  - `np4_auswahl.py` mit `np4_pruefliste.csv` und `np4_geaendert.txt`;
  - `np4_zusammenfuehren.py`.
- `roh/`:
  - `np4_vorbewertet.csv` (51 Zeilen);
  - `np4_gruppe_0.csv` bis `np4_gruppe_5.csv`, dazu je `_regeln.csv` (676 Regelurteile) und `_notizen.md`.
- **Scratchpad** `…/scratchpad/np4/`:
  - `diff/`, `hinweise/`;
  - `zellen.py`, `regelart.py`, `textverlust.py`, `titelschnitt.py`, `semikolon_scan.py`, `bestand_scan.py`, `tabellen4.py`.
