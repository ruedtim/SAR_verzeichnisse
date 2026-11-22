# Nachprüfung 12: Gegenprüfung der Runde 9 und Durchgang über die 208 nur teilweise geprüften Dateien (22.11.2026)

Geprüft sind:
- **Runde 9:** Skript `66c0fb74…` gegen bb4c9588 (Nachtrag 2 der Runde 8). Das ist der Stand jetzt im Projekt.
- **Durchgang:** alle Dateien, die bisher nur teilweise auf kritische Fehler geprüft waren. Das sind 207 Dateien mit 31'760
  Einheiten. D151210 fehlt, weil sie schon in NP6 ganz geprüft wurde.
- **Nachprüfung R1:** 41 Dateien aus NP11, in denen ein Fehler der Prüfmappen Zeilen verdeckt hatte.

Die Ergebnisse stehen hier:
- `offen_kritisch.csv`: nachgeführt, mit stabilen K-Nummern, neu sind K114–K182. Nach den Entscheiden der Hauptsession
  (siehe Nachtrag am Schluss) hat sie 81 Zeilen;
- `funde_nachpruefung12.csv`: 390 Zeilen;
- Rohdaten in `roh/np12_*`, darunter die Vorabliste `roh/np12_vorab_kritisch.csv` am Endstand;
- Methode in `methode/ANLEITUNG_NACHPRUEFUNG12.md` und `methode/np12_*`.

## Kurz

- **Runde 9 wirkt.** Von den 58 K-Zeilen in den 78 geänderten Dateien sind 51 erledigt, also behoben oder nur noch mit
  mittlerem Rest.
  - Kritisch bleiben 5: K38 D149622, K77 D1726, K98 D3026, K99 D2759 und K100 D149867. Dazu kommen die bewusst offenen K39
    und K41.
  - Am PDF beurteilt sind 422 geänderte Einheiten: 256 besser, 151 teilweise besser, 6 gleich, 9 schlechter.
  - Neu kritisch durch Runde 9 ist nur D3530 3.: Regel 3 schiebt dort drei von vier Inventaren ins Blatt Info.
  - In D2759, D3026 und D149867 hat der schon bekannte kritische Fehler durch die neuen Einheiten nur die Form gewechselt
    (K98–K100).
- **Fehlgriffe der Regeln 1, 3 und 31** (wie gewünscht besonders geprüft):
  - **Regel 3:** D3530 ist kritisch.
  - **Regeln 1 und 5:** In D149622 stehen die Anmerkungen zu Einträgen von Schachtel 1 jetzt im Info. Damit ist der Text weg,
    statt bei der falschen Einheit zu stehen. K38 bleibt kritisch.
  - **Regel 4:** D2589 ist unvollständig (mittel).
  - **Regel 31:** sauber. Neue Bestandszeilen gibt es nur in den 8 angekündigten Dateien, und keine echte Einheit ist
    hineingeraten. Nur in D1726 (K77) hat die Bestandszeile kein Darin; der Satz geht weiter ins Info.
- **Der Durchgang findet viel.**
  - **54 von 207 Dateien (26 %, 95%-KI 21–32 %) haben einen kritischen Fehler.** Bei 7 davon ist er bewusst offen.
  - Es gibt **69 neue kritische Zeilen in 49 Dateien**. Alle ausser D3530 bestanden schon vor Runde 9.
  - **Häufigste Muster:**
    - Überschriften oder Titelblätter ohne Signatur stehen bei der vorigen Einheit (18).
    - Schlusstext steht im Darin der letzten Einheit (11).
    - Tippfehler in Dezimalsignaturen hängen Einheiten unter fremde Gruppen (9).
  - Die Rate ist höher als in der Erstprüfung der NP11 (10 %). Die Dateien sind aber im Mittel fast siebenmal so gross (153
    statt 23 Einheiten).
- **Die Prüfmappen hatten einen Fehler.** Der Kopf/Fuss-Filter hat Inhaltszeilen verdeckt. Er ist behoben, und alle Pakete
  haben ihre betroffenen Dateien nachgesehen. R1 hat die 41 übrigen NP11-Dateien nachgeprüft: kein kritischer Fund.
- **Offene kritische Fehler** (`offen_kritisch.csv`, Stand 66c0fb74, nach den Entscheiden der Hauptsession): 81 Zeilen in 62
  Dateien.
  - 67 Zeilen sind neu aus dieser Nachprüfung, 14 stammen aus früheren.
  - 11 Zeilen sind bewusst offen. Konventionsfragen sind keine mehr offen.
  - Nicht bewusst offen sind damit 70 Zeilen in 53 Dateien. In Arbeit ist keine.
- **Abdeckung:** Jede der 715 Dateien ist jetzt mindestens einmal ganz auf kritische Fehler geprüft (507 in NP10/NP11, 207 in
  NP12, D151210 in NP6). «Keine kritischen Fehler» gilt aber erst, wenn die 70 offenen Zeilen behoben und gegengeprüft sind.

## Stände und Nachrechnung

| Stand | Lauf zellgleich | geändert gegenüber bb4c9588 | Einheiten | Fallsets |
|---|---|---|---:|---|
| 66c0fb74 (Runde 9) | ja, auch Testdaten und D151210 | 78 Dateien (D151210 unverändert) | 51'170 (+235) | A 11/12, B 33/38, C 9/12, F 5/7, Runde 2 31/34, Punkt 2 38/38 |

**Soll-Zeilen der Fallsets nach den Konventionen der Runde 9 nachgeführt:**
- **B:** Die «Überformate» in D2940 stehen seit Runde 9 im Darin von 1. (K104), vorher waren sie die erfundene Einheit 2.
- **C:** D3170 ID 328 (K107) und D2940 ID 6 (K104).
- **Runde 2:** Der «Messingpokal» in D149825 steht seit Regel 31 im Darin der Bestandszeile VII.10.

## Gegenprüfung der Runde 9 (Pakete G1–G3, 78 Dateien)

| Paket | Regeln | Dateien | beurteilte Einheiten | schlechter | K-Zeilen erledigt |
|---|---|---:|---|---|---|
| G1 | 1–7 (Schlusstext) | 32 | 45: 43 besser, 1 gleich, 1 schlechter | D3530 3. (kritisch) | 20 von 21 (Rest K38) |
| G2 | 8–20 | 23 | 307: 151 besser, 151 teilweise besser, 5 schlechter | D185 0.3./0.5., D2614 :1–:3 (mittel) | 15 von 20 (Rest K98, K99, K100; K39, K41 bewusst offen) |
| G3 | 21–31 | 23 | 70: 62 besser, 5 gleich, 3 schlechter | D4175 1.A.1., 1.D.2., 2.A. (mittel) | 16 von 17 (Rest K77) |

### Regeln 1–7 (G1)

In 29 Dateien greifen sie richtig: Literatur, Verweise, Bemerkungen, «Biografisches», Bestandsgeschichte, Lagerung und Vermerke
sind echter Schlusstext. Fehlgriffe:
- **D3530 3. «Inventare» (Regel 3, kritisch):** Drei von vier Inventaren stehen nur noch im Info. Die Einträge sind nicht
  eingerückt (x 85 wie die Signatur), darum greift die Ausnahme nicht.
- **D149622 (Regeln 1 und 5, K38):** «Anmerkung zu 1757 …» und «Anmerkung zu 1795 …» beschreiben Einträge von Schachtel 1.
  Sie stehen jetzt im Info statt im Darin von Sch. 3.
- **D2589 19. (Regel 4, mittel):** Die Überschrift «Gedruckte Exemplare (Lichtdruck):» bleibt das einzige Darin.
- **D3542 29. (Regel 7, mittel):** Der Zeitraum kommt aus den Abbruchjahren in den übernommenen Anmerkungen.

### Regeln 8–20 (G2)

- **Ohne Befund:**
  - Regeln 8 (D1261, D1263, D1686, D432) und 9 (D2123: alle 382 Einträge in der richtigen Schachtel);
  - Regeln 13, 14, 16, 17, 18 und 20.
- **Die neuen Einheiten nehmen Text nach dem Verzeichnis oder ohne Nummer mit** (Rest kritisch):
  - **D2759 (Regel 10, K99):** Die Notiz S. 3 steht als Darin 9–13 bei :11 «Publikationen», Zeitraum 1798–1970.
  - **D149867 (Regel 15, K100):** Drei «Drucksache …» ohne Nummer stehen im Darin von :15-25. Ihr Zeitraum gilt für :15-25 und I.
  - **D3026 (Regel 11, K98):** Das Geschäftsbuch (1754–1829) steht nur noch im Info, vorher im Darin der Bestandszeile. Das
    widerspricht Regel 31.
- **D176868 (Regel 12, K72):** Nur «KOMMENTAR FEHLT NOCH» fehlt noch. Das ist ein Bearbeitungsvermerk und kein Archivinhalt,
  darum habe ich die Zeile auf mittel gesetzt.
- **Regel 19 in D2614 (mittel):** Nach «Schachtel 1/2/3» folgt eine nummerierte Liste. Der Titel ist jetzt «(1) …», und der
  Zeitraum kommt nur aus (1).
- **D185 0.3./0.5. (mittel):** geerbter Titel «Grundlagen», eine Folge von Regel 17.

### Regeln 21–31 (G3)

- **Ohne Fehlgriff:** Regeln 21–25, 27 und 30.
- **Regel 31:** G3 hat alle 716 Ausgaben durchsucht. Neue Bestandszeilen gibt es nur in den 8 angekündigten Dateien. Keine
  echte Einheit ist hineingeraten, und die vorige Einheit hat überall den richtigen Zeitraum.
  - **Rest kritisch, D1726 (K77):** Die Bestandszeile hat kein Darin. «Drei Archivschachteln …» steht nur im Hinweis und im
    Info. `stueck_ohne_nummer()` legt die Zeile an, die Textzeile läuft danach trotzdem in die Schlussvermerke.
  - **Mittel und gering:**
    - Titel mit dem Datumsteil des Katalogs: D260, D3826, D3943.
    - Verweis bzw. Legende mitgenommen: D3826, D3943.
    - Der Erwerbungsvermerk des Pokals steht im Info: D149825.
- **Regel 26 (D403, K85):** Die Gliederung stimmt. Die Kinder heissen aber weiter «:a.»/«:b.» statt «:1.a.»/«:1.b.» (mittel).
- **Regel 28, nicht angekündigte Nebenwirkung in D4175 (mittel):** Eine Zeile ohne Datum nach einer datierten wird an den
  vorigen Eintrag gehängt. Betroffen sind 1.A.1., 1.D.2. und 2.A.
- **Regel 29 (D4058 19.13., mittel):** Die Beschreibung des Bereichs steht nur bei der ersten Einheit, wie beim angekündigten
  Rest von K63.

## Durchgang über die 208 nur teilweise geprüften Dateien

**Umfang:** 207 Dateien mit 31'760 Einheiten.
- **P1–P7:** 155 Dateien bis 200 Einheiten. Jede Datei ist ganz über die Prüfmappe geprüft, ab 60 Einheiten über die
  Kompaktmappe.
- **L1–L2:** 26 Dateien über 200 Einheiten.
  - Strukturbericht und Kompaktmappe;
  - mindestens 5 Seiten Zeile für Zeile;
  - eigene Abgleiche: jede Signaturzeile gegen die Einheiten, Folge der PDF-Zeilen.
- **G:** die 26 Dateien mit VOLLPRÜFUNG aus der Gegenprüfung.

| Paket | Dateien | Einheiten | mit kritischem Fehler |
|---|---:|---:|---|
| P1 | 21 | 632 | 3: D2901, D406, D4173 |
| P2 | 22 | 781 | 3: D3063, D150296, D3684 |
| P3 | 23 | 1'066 | 6: D3208 (b), D3528, D9978, D2979, D3808, D3021 |
| P4 | 22 | 802 | 5: D3709, D3628, D3271, D140969, D176824 |
| P5 | 23 | 1'079 | 6: D2735, D3828, D512 (b), D176795, D3231, D1858 (b) |
| P6 | 22 | 929 | 8: D3774, D175994, D1874 (b), D3533, D2894, D2872, D10744, D414 |
| P7 | 22 | 1'257 | 2: D2850, D1880 |
| L1 | 12 | 11'700 | 6: D149628, D3672, D176060, D2857, D32837, D3589 |
| L2 | 14 | 11'379 | 5: D3472, D175996, D4054, D151150, D10585 |
| G1 (Vollprüfung) | 15 | 702 | 4: D149622 (b), D2710, D3530, D3204 |
| G2 (Vollprüfung) | 3 | 182 | 2: D2614 (b), D1739 (b) |
| G3 (Vollprüfung) | 8 | 1'251 | 4: D4175, D3943, D3316, D9983 |
| **zusammen** | **207** | **31'760** | **54 (26 %), davon 7 nur bewusst offen** |

(b) = nur eine bewusst offene Zeile.

### Muster der 69 neuen kritischen Zeilen

1. **Überschrift oder Titelblatt bei der vorigen Einheit** (18; Gruppen-, Orts- und Zwischenüberschriften ohne Signatur):
   - nicht fett, sondern kursiv oder in Normalschrift: D2850 63./64., D3204 11., D176795, D10585 (fünf Orte), D4173, D3628,
     D175994, D3774 6.3.;
   - nach einem Seitenwechsel: D9978 28.4.24.;
   - Schachtelangabe am Gruppenanfang: D2872, D3021;
   - Vorbemerkungen zu Schachteln: D2710 (zweimal);
   - Titelblatt einer neuen Serie oder eines zweiten Nachlasses: D1880 R., D4175 1.F.;
   - Vermerk, der für die folgenden Einheiten gilt: D406 55.;
   - weitere: D149628 5.4.3.3., D3589 2.
2. **Schlusstext im Darin der letzten Einheit** (11), oft mit falschem Zeitraum:
   - Überschriften, die Regel 1 nicht kennt: D3316 («Geschichte der …:», «Zu diesem Bestand:»), D3271 7. («Anhang zum …»;
     Regel 1 nimmt «Anhang» aus), D4054 21.5.3. («Der Bestand umfasst:» mit Folgezeilen).
   - Regel 3 greift nicht:
     - sie gilt nur auf den letzten zwei Seiten: D3063 (S. 19 von 21);
     - zu kleiner Abstand: D3709;
     - kein Stichwort: D3533;
     - über 12 Zeilen: D2979;
     - nur die erste Zeile erkannt: D3628 8.
   - Bearbeitungsvermerke und Bestandsgeschichte: D3774 6.4., D2901 11., D32837 4.4.4.
3. **Text weg** (12):
   - **Schlussblock-Regeln nehmen echten Inhalt ins Info:**
     - D3530 (Regel 3) und D176824;
     - D3684 («Dem Bestand liegen bei:»), D3808 (Beilagenliste);
     - D3563 («Anmerkungen:» mit Stücken des Bestands).
   - **Stück oder Bestandsangabe nur im Vorspann:** D3774, D2894, D3828. Nach dem Entscheid der Hauptsession bleibt nur D3828
     kritisch; D3774 und D2894 sind mittel.
   - **Weitere:**
     - D3271 4.2.22.: die Gruppenbeschreibung steht nur im Hinweis;
     - D3231 2.8.: eine fette Zeile gilt als Zwischenüberschrift;
     - D176060 3.6.3.3.–3.6.3.7.: «(Enthält Patientendaten!)» fehlt;
     - D1874: bewusst offen.
4. **Eltern oder Ebene falsch** (16):
   - **Tippfehler in Dezimalsignaturen** (Muster 10): D4054 10.8.2.10. und 10.8.4., D149628 20.1.2.19., 28.1.1.3. und 29.2.9.,
     D32837 1.1.2.1.1., D2857 1.224.3., D176060 7.4.1.26., D150296 3.3.7.
     - Die Einheit hängt unter einer fremden Gruppe.
     - Verräterisch sind die Hinweise «Übergeordnete Signatur fehlt» und «Nummerierung beginnt bei n» mitten in einer
       anderen Reihe.
   - **«n.a» als Kind statt als Geschwister:** D9983 (28 Journale), D9978 28.6.12., D175996 1.a) und 460.a)/b).
   - **Zählung je Schachtel als Signatur:** D2735. **Zweite Schachtelfolge als Teile:** D2710 (Konventionsfrage).
   - **Registraturplan:** In D10744 werden die Segmente gezählt statt der Hunderter- und Zehnergruppen.
   - **D414:** Die römischen Gruppen nach der Schachtel werden oberste Stufe.
5. **Einheit fehlt oder steht im Darin** (9):
   - **Signaturformen werden nicht erkannt:**
     - «7. 2.3.» mit Leerzeichen (D10585);
     - «28.3.25:1–2» ohne Punkt vor «:» (D9978);
     - «X.» und «X.1.» (D3672, ganzer Abschnitt X.);
     - Unternummern «X.G.93.:1» eingerückt am Zeilenanfang oder in Klammern am Zeilenende (D3943);
     - «Mappe 8» mit anders geschriebenem Bestand (D32837 4.4.1.).
   - **Erste Signaturzeile:** Steht sie direkt nach «Detailverzeichnis», wird sie als Vorspann verworfen (D3528 4.). In
     D32837 fehlt die Gruppe 1.
   - **Nummer nur in einer eingeschobenen Übersicht:** D140969 57.
   - **Nr.-Spalte über Schachteln (Muster 8):** D151150 9. mit 293 Dossiers.
6. **Einheit erfunden** (2):
   - D3472 1966.19: die Aufzählung a)–c) in der Textspalte wird zu Unterstufen;
   - D2894 7.4.: eine allein stehende «Schachtel n» erzeugt einen Teil.

Dazu kommt D2850: Ein Stück ohne Nummer ist eingerückt und steht darum im Darin der letzten Einheit; Regel 31 greift dort nicht.

### Vom Prüfer gemeldet, von mir herabgestuft (mittel)

- **Eltern in einer anderen Datei:** D9978 28.1./28.2. und D9985 27.2.1. (Eltern in D149628), D4058 19.1.–19.13. (Eltern in
  D4054). Innerhalb der Datei ist das nicht lösbar, und jede Einheit hat den Hinweis «erwartet …». Gleich sieht wohl D4057 aus.
- **D3951 X.T.2.:8:** Es fehlt nur das Wort «(Band)» aus einer als Kopf verworfenen Zeile.
- **D3657:** NP6 hatte «Teil 2» für die doppelten 5./6. als Soll zugelassen.
- **D3271 4.2.9.:** Registerzeile im Titel, Grenzfall wie in NP11.
- **D140969 87.:** Das PDF widerspricht sich («82 – 87» in der Übersicht, «82 – 86» im Detail).
- **D152390 :6:** ein Überleitungssatz, kein Textverlust.
- **D150296 6.8.:** wiederholte Signatur = Teil nach Konvention.
- **Rest von K-Zeilen nur noch mittel:** K63, K67, K72, K74, K85, K101.
- **Entfällt:** D3208 VII.222.:2 ist dasselbe wie K42 (bewusst offen).

### Mittlere Funde

177 mittlere und 30 geringe Funde, meist zu Zeitraum und Titel:
- Elterntitel statt eigenem Titel (D149888: 23 Einheiten);
- Zeitraum aus Jubiläumsjahren, Literaturangaben oder Erwerbsdaten;
- die Schachtel steht nur in der Übersicht (D3324, D175454);
- dieselben Signaturen V.B.c.9.:1–:23 in zwei Dateien (D537, D539).

## Fehler in den Prüfmappen und Nachprüfung R1

- **Fehler:** Der Kopf/Fuss-Filter von `np11_pruefmappe.py` zeigte jede Zeile, die bis auf Ziffern auf 3 oder mehr Seiten
  gleich lautet, nur einmal, auch mitten auf der Seite.
  - Verdeckt waren damit Inhaltszeilen wie «Schachtel 5», «2 Exemplare», «Fotos» oder «Siegel des Grundbuchamtes …».
  - Betroffen: 25'764 Zeilen in 117 NP12-Dateien und 6'095 Zeilen in 59 NP11-Dateien.
- **Behoben** in `np12_pruefmappe.py`: Verdichtet werden nur noch Zeilen am Seitenrand. Alle Mappen sind neu erzeugt.
- **Nachkontrolle:**
  - Alle NP12-Pakete haben ihre betroffenen Dateien an den neuen Mappen nachgesehen. Ein neuer kritischer Fund kam daraus nicht
    (G2: ein mittlerer).
  - 18 der 59 NP11-Dateien waren ohnehin in NP12-Paketen.
  - **R1** hat die übrigen 41 Dateien geprüft, mit allen 2'360 verdeckten Zeilen am Zeilen-Cache gegen die Excel.
    - Ergebnis: 0 kritisch, 5 mittel, 2 gering.
    - Alle 384 verdeckten Signaturzeilen sind als Einheit da, mit richtigen Eltern.
- **Rest:** Die im Durchgang benutzten Mappen verdichten weiter 183 Zeilen am Rand (y 60–80 und 780–800, in 27 Dateien). Ein
  automatischer Abgleich zeigt alle an der richtigen Stelle. Die Fassung in `methode/` verdichtet nur noch unter y 60 und über
  y 800.

## Restlücken

- **D2510 (G1):** Die Prüfmappe ordnet nur 6 von 107 Einheiten eine Startzeile zu, eine Schwäche des Werkzeugs. Geprüft sind
  diff, Schluss und Info. Die Datei war schon in NP10/NP11 ganz geprüft.
- **Gegenprüfung ohne Vollprüfung:** 52 der 78 geänderten Dateien sind nur im Umfang diff, Schlussbereich und Altzeilen
  geprüft. Sie waren schon vorher ganz geprüft.
- **Warnzeichen der Mappen:** Sie finden die kritischen Fehler kaum. Gefunden haben sie die Prüfer am Inhalt und mit eigenen
  Abgleichen: PDF-Folge, Signaturzeilen gegen Einheiten, Text nach der letzten Einheit.

## Konventionsfragen (inzwischen entschieden, siehe Nachtrag)

1. **Gilt Regel 31 auch für Stücke, die nur im Vorspann oder in der Übersicht stehen?**
   - K166 D3828: «Summarisches …» vor 1.;
   - K171 D3774 und K176 D2894: Bestandszeile fehlt.
2. **K162 D3271 4.2.22.–4.2.50.:** Die K8-Konvention (Gruppenzeile als Hinweis bei der folgenden Einheit) deckt nur die
   Überschrift. Die Beschreibung darunter steht in keinem importierten Feld.
3. **K117 D2710:** In einem Findmittel ohne Signaturen beginnt die Schachtelzählung neu (Jahresdokumentation). Sind das eigene
   Behälter oder Teile?

**Nach bestehender Konvention kritisch gewertet** (falls anders gewollt, nur mittel):
- **K144 D151150 9.:** Muster 8 der NP11 (Nr.-Spalte über Schachteln = Signaturen, wie D1391). NP5/NP6 hatten dort nur den
  Zeitraum beanstandet.
- **K123 D9983, K154 D9978, K143 D175996:** «n.a» neben «n.» in derselben Spalte ist Geschwister, wie in D3816.
- **K142 D3472 1966.19:** a)–c) in der Textspalte sind eine Aufzählung (Darin), keine Unterstufen.
- **K119 D3563 und K98 D3026:** Sätze über Stücke in einem Schlussabschnitt («Beim Bestand befinden sich ferner 4
  Ausstellungstafeln …», das Geschäftsbuch) gehören wie bei K77 nach Regel 31 in die Bestandszeile.

### Nachtrag: Entscheide der Hauptsession (22.11.2026)

Eingetragen mit `methode/np12_entscheide_hauptsession.py` in `offen_kritisch.csv` (Spalte `entscheid`),
`funde_nachpruefung12.csv` und `roh/np12_vorab_kritisch.csv`. Die K-Nummern bleiben. Die Liste davor liegt in
`roh/np12_offen_kritisch_vor_entscheid.csv`.

1. **Regel 31 und Vorspann:**
   - **K166 D3828: ja.** Eine eigene Eintragszeile (Werktitel, Datierung) direkt vor der ersten Signatur ist ein Stück ohne
     Nummer und kommt in die Bestandszeile. Bleibt kritisch, Umsetzung in Runde 10.
   - **K171 D3774 und K176 D2894: nein.** Text in Einleitung, Übersicht oder einer Vorbemerkung in Prosa bleibt Vorspann im
     Blatt Info. Das Info ist die Quelle für die Bestandsebene und wird dort von Hand übernommen. Beide Zeilen sind jetzt
     mittel und nicht mehr in `offen_kritisch.csv`.
2. **K162 D3271:** Ein beschreibender Satz unter einer Gruppenzeile ohne Signatur (in Klammern oder «Vgl. …») kommt ins Darin
   jeder Einheit der Gruppe, bis zur nächsten Gruppenzeile bzw. zum Ende der Elterneinheit. Die Gruppenzeile selbst bleibt
   Hinweis (K8). Das Soll ist danach gefasst; Umsetzung in Runde 10.
3. **K117 D2710: bewusst offen**, wie D2681 in Runde 7.
   - Die zweite Schachtelfolge zählt dieselben Nummern; eine Trennung bräuchte einen erfundenen Signaturteil.
   - Die Teile tragen den Hinweis «Signatur taucht erneut auf …».
   - K115 und K116 (Vorbemerkungen zu Schachteln) bleiben kritisch.
4. **Bestätigt kritisch:** K144, K123, K154, K143, K142, K119 und K98. Umsetzung in Runde 10.

## Vorschläge für Runde 10

1. **Überschriften ohne Signatur zur folgenden Einheit** (Regel 28 erweitern), auch wenn sie nicht fett sind:
   - kursive Zeilen oder Zeilen in Normalschrift mit eigener Zeile direkt vor einer Signaturzeile;
   - grössere Schrift (Titelblätter);
   - nach einem Seitenwechsel.

   Fälle: Muster 1 oben (18 Zeilen).
2. **Schlussblock:**
   - **Regel 1** um diese Überschriften erweitern:
     - «Geschichte der …:», «Zu diesem Bestand:»;
     - «Der Bestand umfasst:» mit den Folgezeilen;
     - «Anhang …», wenn danach keine Signatur der Folge mehr kommt.
   - **Regel 3** auch so anwenden:
     - nicht nur auf den letzten zwei Seiten;
     - bei kleinem Abstand und ohne Stichwort;
     - über 12 Zeilen;
     - für den ganzen Block statt nur die erste Zeile.
   - **Gegen Fehlgriffe (D3530):** Kündigt der Titel der letzten Einheit eine Liste an («Inventare», «Verzeichnisse») und
     hätte sie sonst kein Darin, bleibt der Block ihr Darin.
   - **Stücke im Schlussabschnitt** gehören in die Bestandszeile (Regel 31), nicht ins Info:
     - «Dem Bestand liegen bei:», «Beim Bestand befinden sich ferner …», das Geschäftsbuch, Beilagenlisten;
     - Fälle: D3684, D3563, D3026, D3808, D176824.
     - In D1726 muss die Textzeile selbst ins Darin der Bestandszeile: `stueck_ohne_nummer()` vor `ist_schlussvermerk()`.
3. **Tippfehler in Dezimalsignaturen** wie die Regeln 23/24 behandeln:
   - **Bedingung:** Die Signatur gehört nach ihrem Präfix zu einer fremden Gruppe. Ihre PDF-Nachbarn sind aber Geschwister in
     einer anderen Gruppe derselben Tiefe, und dort fehlt genau diese Nummer.
   - **Dann:** bei den Nachbarn einordnen, mit Hinweis.
   - Vorher lohnt sich ein Suchlauf über alle Dateien nach den Hinweisen «Übergeordnete Signatur fehlt» und «Nummerierung
     beginnt bei n».
4. **Regel 25 verallgemeinern:** «n.a», «n.a.» und «n.a)» direkt nach «n.» in derselben Spalte sind Geschwister. Das gilt
   auch für Dezimalsignaturen (D9983, D9978) und bei anderem Titel (D175996), ausser die Zeile ist eingerückt.
5. **Signaturformen und Startzeilen:**
   - «7. 2.3.» (mit Leerzeichen), «28.3.25:1–2» (ohne Punkt vor «:»), «X.»/«X.1.»;
   - Unternummern «X.G.93.:1» am Zeilenanfang oder in Klammern am Zeilenende;
   - die erste Signaturzeile direkt nach «Detailverzeichnis»;
   - Nummern nur in einer eingeschobenen Übersicht (D140969).
6. **Schachtelfolgen:**
   - Regel 14 (Nr.-Spalte über Schachteln) auch für D151150 9.;
   - Zählung je Schachtel (D2735) und eine zweite Schachtelfolge (D2710) als eigene Folge.
7. **Keine Einheiten aus Aufzählungen:**
   - a)–c) in der Textspalte sind Darin (D3472);
   - eine allein stehende «Schachtel n» unter einer Vollsignatur ist kein Teil (D2894).
8. **Reste der Runde 9:**
   - Regel 10, D2759: Die Notiz nach dem Seitenwechsel, links vom Inhalt, gehört ins Info.
   - Regel 15, D149867: «Drucksache …» ohne Nummer gehört in die Bestandszeile.
   - Regel 11, D3026: das Geschäftsbuch ebenso.
   - Regel 19, D2614: Ausnahme, wenn die Folgezeile mit «(1)» beginnt.
   - Regel 28, D4175: Eine Zeile ohne Datum nicht an den vorigen Eintrag hängen.
   - Regel 26, D403: «:1.a.».
   - D149622: Die Anmerkungen zu Einträgen von Sch. 1 gehören ins Darin von Sch. 1.
9. **Einzelfälle:**
   - D3672: Abschnitt X.;
   - D176060: «(Enthält Patientendaten!)»;
   - D10744: Registraturplan;
   - D414: römische Gruppen nach der Schachtel.

## Nächste Nachprüfung (NP13)

- **Gegenprüfung der Runde 10** mit den neuen Prüfmappen, besonders auf Fehlgriffe der erweiterten Schlussblock- und
  Überschriftenregeln. Diese Regeln greifen in vielen Dateien.
- **Suchlauf** «Tippfehler in Dezimalsignaturen» über alle 715 Dateien.
- **Zufallsstichprobe** von etwa 60 Dateien aus allen 715, ganz geprüft, um die Restrate nach Runde 10 zu schätzen.

## Dateien

- `offen_kritisch.csv`: 81 Zeilen.
  - Die K-Nummern bleiben; neu sind K114–K182.
  - 51 erledigte Zeilen sind entfernt. Die Liste davor liegt in `roh/np11_offen_kritisch.csv`.
  - Nach den Entscheiden der Hauptsession sind K171 und K176 mittel und entfernt. Die Fassung mit 83 Zeilen liegt in
    `roh/np12_offen_kritisch_vor_entscheid.csv`.
  - Die Spalte `entscheid` nennt Herabstufungen, Entscheide und Begründungen.
- `funde_nachpruefung12.csv`: alle Funde aus G1–G3, P1–P7, L1–L2 und R1, mit `paket`, `k_alt` und `entscheid`.
- `roh/np12_dateien_urteil.csv`: Urteil je Datei, Spalte `urteil_jetzt`.
- `roh/np12_vorab_kritisch.csv`: die Vorabliste am Endstand, nach den Entscheiden 74 kritische Zeilen der Pakete.
- `roh/np12_<Paket>_*`: die Ausgaben der Pakete.
- `roh/np12_vgl/` und `roh/np12_geaendert_runde9.txt`: der Vergleich je geänderte Datei (78).
- `roh/np12_struktur/`: Strukturberichte der 26 grossen Dateien.
- `roh/np12_verdeckt_np11.txt`, `roh/np12_verdeckt_np12.txt`, `roh/np12_r1_dateien.txt`, `roh/np12_randzeilen.txt`.
- Die Prüfmappen (rund 35 MB) liegen nur im Scratchpad. Mit `methode/np12_pruefmappe.py` und
  `methode/np12_mappe_kompakt.py` lassen sie sich neu erzeugen.
