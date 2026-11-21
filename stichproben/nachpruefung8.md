# Achte Nachprüfung: Gliederungsrunde (Runde 7), Stand 22.11.2026, 00:05

Geprüft wurden `findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx`, erzeugt am 22.11.2026 zwischen 00:03
und 00:05.
- **Skript:** sha256 `1f98df0beaaea412…`. Das ist der Stand nach Runde 2 und Punkt 2 (`2953088e…`) plus die
  Gliederungsrunde.
- **Vergleich:** mit `runde7/vorher/`, dem Stand 2953088e. Die Dateien dort sind zellgleich mit meinem eigenen Lauf dieses
  Stands.
- **Arbeitskopien:** Das Skript liegt als Schnappschuss in `…/scratchpad/neu8/`, die Läufe liegen in `…/scratchpad/np8/`.
- **Belege:** Jedes Urteil ist am PDF belegt, mit Seite und Wortlaut in `roh/np8_paket_N_urteile.csv`. Die kritischen
  Befunde der Prüfer habe ich selbst am PDF nachgesehen.
- **Stand beim Abschluss (00:45):** Skript und Excel im Projekt sind unverändert, sha256 `1f98df0b…`, keine Excel-Datei ist
  neuer als 00:06.

## Kurzfazit

- **Urteil: Der Stand ist stabil genug für Commit und Push inklusive aller Excel.**
  - **Excel = Skript:** Die Excel im Projekt sind genau die Ausgabe von 1f98df0b.
  - **Umfang:** Geändert sind nur die 34 gemeldeten Dateien. Die übrigen 681 Dateien, alle Testdaten und D151210 sind
    zellgleich mit vorher.
  - **Urteile:** In den 34 Dateien sind alle 748 geänderten Einheiten am PDF beurteilt: 733 besser, 7 gleich, 8 schlechter.
    32 Dateien sind besser, D176772 ist gleich. Schlechter ist nur D152781: Dort sind 5.1. und 5. die einzigen Änderungen,
    und beide haben jetzt einen zu engen Zeitraum.
  - **Textverlust:** Es geht kein Text verloren, bis auf ein Endjahr (D3828 3.17. Nr. 33, «1939 –» / «1946»). Was jetzt im
    Vorspann oder im Blatt Info steht, gehört nach Konvention dorthin.
  - **Hierarchie:** Eltern, Ebenen und Teile sind in allen 715 Dateien in sich stimmig.
- **Neue Fehler durch Runde 7:** 22 Zeilen, davon 3 kritisch, 13 mittel und 6 gering. Meist geht es um Zeitraum oder Titel
  neu entstandener Einheiten.
  - **Kritisch ist nur D2850:** Die Daten «2.1939» und «12.1961» sind weiter Einheiten. Dazu kommen die erfundene Einheit
    65.A. «Engelhardt» und die vertauschten Inhalte von 55 und 56.
- **Ältere kritische Gliederungsfehler, die Runde 7 nicht behebt:** 12 Zeilen in 10 Dateien.
  - D3810: 14 erfundene Einheiten.
  - D3313: 42 erfundene Einheiten.
  - D152817: Abschnitte als Eltern von Schachteln.
  - D140969, D1874, D845: fehlende Einheiten.
  - D134644, D151730, D2850, D3826: falsch eingehängter Inhalt.
- **D2850 ist viel besser, aber nicht fertig.** Die Einheiten 49–66 sind da, die erfundenen «A.», «B.» und «B.5.» sind weg.
  AENDERUNGEN_RUNDE7.md verspricht aber mehr, als die Ausgabe hält (siehe unten).
- **Empfehlung:**
  - Push ja.
  - Die beiden kleinen D2850-Korrekturen (Datums-Signaturen, «Künstler: 1929» / «A. Engelhardt») vor oder direkt nach dem
    Push.
  - Die übrigen Punkte in einer nächsten Runde (Vorschläge am Ende).

## Methode

1. **Stand nachgerechnet.** Eigener Gesamtlauf mit dem Skript aus dem Projekt:
   - zellgleich mit `findmittel_excel/` (715 Dateien, alle Blätter ohne die Zeile «Erzeugt») und mit `testdaten_excel/`
     (11 Dateien);
   - zellgleich mit `D151210_scope_import.xlsx`; die Datei in der Projektwurzel ist byteweise gleich mit der in
     `testdaten_excel/`;
   - die Übersicht hat 715 Zeilen, und die Einheitenzahlen stimmen mit den Einzeldateien überein.
2. **Gegen 2953088e** ändern sich genau die 34 Dateien aus `runde7/geaenderte_dateien.txt`.
3. **Vergleich je Datei** über die Signatur ohne «:» plus n-tes Vorkommen (`methode/np8_vgl.py`, Ergebnis in
   `roh/np8_vgl/`): 354 Einheiten weggefallen, 92 neu und 302 geändert, zusammen 748.
4. **Sechs Prüfer** mit gemeinsamem Auftrag (`methode/ANLEITUNG_NACHPRUEFUNG8.md`).
   - Jede der 748 Einheiten ist am PDF beurteilt.
   - Die Gliederung der stark geänderten Dateien ist ganz geprüft, Seite für Seite und Signatur für Signatur.
   - Dazu kommen die 41 offenen Altzeilen aus den Nachprüfungen 6 und 7 zu diesen Dateien.

   | Paket | Dateien |
   |---|---|
   | 1 | D1874, D448, D2620, D3810 |
   | 2 | D3828, D3530 |
   | 3 | D140969, D152817, D2737, D2745, D2687 |
   | 4 | D2850, D3774, D3698, D3776 |
   | 5 | D151730, D152400, D149835, D3256, D3826 |
   | 6 | Regel 13 (6 Dateien), Regel 11 (7 Dateien), D176772 |
5. **Eigene Gegenproben:**
   - Kennzahlen und Fallsets.
   - Hierarchie (`np8_konsistenz.py`).
   - Textverlust über alle Spalten und das Blatt Info, abgeglichen mit der Häufigkeit im PDF (`np8_textverlust2.py`).
   - Einheit gegen PDF-Zeile (`np8_sigcheck.py`): keine neue Einheit ohne Zeilenanfang im PDF.
   - Umbrochene Datumsspannen (`np8_datumsumbruch.py`) und eingerückte Geschwisterfolgen (`np8_einzug.py`) im ganzen
     Korpus.
   - Die Strukturprüfung der Hauptsession, nachgerechnet mit dem gleichen Ergebnis.
6. **Selbst am PDF nachgesehen:**
   - D3810 S. 1–2;
   - D2850 S. 12–13, 20–24;
   - D3313 S. 1–3;
   - D152781 S. 4;
   - D3826 S. 1–4;
   - D3256 S. 1–2;
   - D3828 S. 12 und 15–17.

## Ergebnis je Datei

Die Spalten «neu durch Runde 7» und «neu, schon vorher» zählen kritisch / mittel / gering.

| Datei | Einheiten | besser | gleich | schlechter | neu durch Runde 7 | neu, schon vorher | Altzeilen |
|---|---|---:|---:|---:|---|---|---|
| D1874 | 303 → 105 | 267 | 0 | 0 | 0/1/0 | 1/1/2 | – |
| D140969 | 86 → 93 | 92 | 0 | 0 | 0/1/0 | 2/0/0 | 1 behoben, 1 teilweise, 1 offen |
| D3828 | 99 → 31 | 81 | 0 | 0 | 0/1/0 | 0/1/0 | 3 behoben |
| D3530 | 69 → 8 | 64 | 0 | 0 | 0/1/0 | 0/0/0 | 2 behoben, 1 offen |
| D152817 | 704 → 704 | 36 | 2 | 0 | 0/0/1 | 1/0/1 | – |
| D3774 | 34 → 59 | 36 | 0 | 1 | 0/3/0 | 0/0/0 | 1 behoben, 1 teilweise, 7 offen |
| D151730 | 20 → 42 | 32 | 0 | 1 | 0/2/0 | 1/3/1 | – |
| D2850 | 54 → 71 | 28 | 3 | 4 | 3/2/2 | 1/2/0 | 1 offen |
| D149835 | 26 → 19 | 15 | 0 | 0 | 0/0/0 | 0/0/2 | – |
| D3776 | 18 → 20 | 13 | 0 | 0 | 0/0/0 | 0/1/0 | – |
| D3256 | 10 → 5 | 10 | 0 | 0 | 0/0/0 | 0/1/2 | – |
| D3816 | 125 → 125 | 8 | 0 | 0 | 0/0/0 | 0/0/0 | – |
| D2737 | 5 → 8 | 7 | 0 | 0 | 0/0/0 | 0/0/0 | 1 behoben |
| D3826 | 23 → 20 | 6 | 0 | 0 | 0/0/1 | 1/1/0 | – |
| D152400 | 7 → 11 | 5 | 0 | 0 | 0/1/0 | 0/0/1 | 1 offen |
| D3698 | 24 → 25 | 5 | 0 | 0 | 0/0/0 | 0/0/0 | – |
| D176721 | 191 → 191 | 4 | 0 | 0 | 0/0/0 | 0/2/0 | – |
| D448 | 14 → 13 | 4 | 0 | 0 | 0/0/0 | 0/0/0 | – |
| D2687 | 2 → 2 | 3 | 0 | 0 | 0/0/0 | 0/1/0 | – |
| D2745 | 2 → 2 | 3 | 0 | 0 | 0/0/0 | 0/0/0 | – |
| D150689 | 299 → 299 | 2 | 1 | 0 | 0/0/0 | 0/1/0 | 1 behoben, 2 teilweise, 6 offen |
| D845 | 202 → 202 | 2 | 0 | 0 | 0/0/0 | 1/0/0 | – |
| D152781 | 17 → 17 | 0 | 0 | 2 | 0/1/0 | 0/1/1 | 1 teilweise, 2 offen, 1 schlechter |
| D134644 | 89 → 89 | 1 | 0 | 0 | 0/0/0 | 1/1/0 | 1 behoben |
| D3313 | 50 → 50 | 1 | 0 | 0 | 0/0/0 | 1/1/0 | 1 offen |
| D3810 | 21 → 21 | 1 | 0 | 0 | 0/0/0 | 2/0/0 | – |
| D141 | 254 → 254 | 1 | 0 | 0 | 0/0/0 | 0/0/0 | 4 offen |
| D2620 | 139 → 139 | 1 | 0 | 0 | 0/0/0 | 0/0/1 | 1 offen |
| D3677, D3951, D2270 | unverändert | je 1 | 0 | 0 | 0/0/0 | D3951 0/0/1, D2270 0/1/0 | – |
| D151761, D152390 | unverändert | je 1 | 0 | 0 | je 0/0/1 | 0/0/0 | – |
| D176772 | 22 → 22 | 0 | 1 | 0 | 0/0/0 | 0/0/0 | – |
| **Summe** | **3'047 → 2'785** | **733** | **7** | **8** | **3/13/6** | **12/18/12** | **10 behoben, 5 teilweise, 25 offen, 1 schlechter** |

## Die Regeln

| Regel | besser | gleich | schlechter | Bemerkung |
|---|---:|---:|---:|---|
| 1 Bereich mit Buchstabe (D3698) | 5 | 0 | 0 | 6-7a mit 6, 7, 7a stimmt am PDF S. 1. |
| 2 Liste unter fetter Hauptnummer (D3828, D3530) | 145 | 0 | 0 | Siehe unten. |
| 3 Unternummern (D3774, D151730, D152400) | 64 | 0 | 2 | Siehe unten. |
| 4 Sammelmarke als Bereich (D3776) | 13 | 0 | 0 | 2-3 und 6-9 stehen über den Mappen. Die Kapitelnummern im Titel sind richtig (Signal T). |
| 5 Gliederungsränge (D2850) | 25 | 3 | 4 | Siehe D2850 unten. |
| 6 «Signatur: …» im Inhalt (D1874) | 266 | 0 | 0 | Siehe unten. |
| 7 Übersichten (D3256, D3826, D176772) | 16 | 1 | 0 | Die Doppelungen sind weg. Die Stiftungsbeschreibung D3256 und die Gruppenübersicht D3826 stehen im Vorspann; das ist nach Konvention richtig. |
| 8 Zahl am Anfang einer Inhaltszeile (D2745, D2687, D448) | 10 | 0 | 0 | «7 Einladungen …», «3 Auszüge …» und «V.B. c.57.:10.» sind keine Einheiten mehr. |
| 9 Doppelnummern (D2737) | 7 | 0 | 0 | 3/4, 7/8 und 10/11 sind Einheiten. 9. hat 1914–1987 (Fallset B). |
| 10 Bereich als Gruppe (D140969, D152817) | 128 | 2 | 0 | Siehe unten. |
| 11 Signaturform (9 Dateien) | 28 | 0 | 0 | In den 7 Dateien von Paket 6 stehen alle 18 «:» hinter dem Bestand des Titelblatts, nirgends hinter einem Unterbestand (Quote 83–99 %). D3774 und D151730 ebenso. |
| 12 «Anmerkungen zum Bestand» (D149835, D2620) | 16 | 0 | 0 | Siehe unten. |
| 13 Klammerliste (6 Dateien) | 6 | 1 | 2 | Fünf Titel stimmen am PDF. D152781 5.1. ist schlechter, siehe unten. |
| 14 Schlussblock links einer Unternummer (D152400, D3810) | 2 | 0 | 0 | Siehe unten. |
| 15 Bearbeitungsvermerk mitten im Findmittel (D1874) | 3 | 0 | 0 | Beide «Juli 1999 / RD» stehen im Blatt Info. |
| nicht angekündigt | 3 | 0 | 0 | D2850 8., 21., 40.: Die zweite Zeile mit eigenem Datum ist jetzt Darin. |

**Bemerkungen zu einzelnen Regeln:**
- **Regel 2:**
  - D3828 hat die Abschnitte 1.–9. mit 3.1.–3.19. Alle 22 Listen stehen lückenlos im Darin der richtigen Einheit.
  - Vorher waren dort 35 Zeilen als Übersicht verworfen, obwohl «Text erfasst» 100 % zeigte.
  - In D3530 steht die Bibliografie 1–63 vollständig im Darin von 2.3.
- **Regel 3:**
  - Alle Unternummern sind Einheiten mit richtigen Eltern.
  - Schlechter sind D151730 19.5. (der Anhang S. 4 hängt jetzt daran) und der Zeitraum von D3774 2.
- **Regel 6:**
  - Alle 199 weggefallenen Einheiten waren erfunden.
  - Die Planmappen-Tabelle steht vollständig im Darin von 2.: 331 von 331 Einträgen, «X» und «fehlt» sind erhalten.
  - 3. ist neu, darunter 3.1.–3.11. und 54 Mappen.
- **Regel 10:**
  - D140969: Alle 7 Bereiche stehen so im PDF, jede Nummer hängt am engsten.
  - D152817: 8-11 liegt in 8-12; 7-15, 16-17 und 18-19 liegen in 7-19.
- **Regel 12:**
  - D149835: Die Liste 1.–7. und die Nc-Urkunden stehen im Blatt Info, davor ist nichts verrutscht.
  - D2620: Die Liste 2.–9. steht im Info-Blatt, die Überschrift «Anmerkungen zum Bestand V.L. 167.» aber weiter im Darin von
    15.3. (gering, ebenso D149835 19.).
- **Regel 14:**
  - D3810: «rpt Stand: 10.09.1992» steht im Blatt Info.
  - D152400: «Vgl. auch V.J. b.202.» stand schon vorher dort.

## Neue Fehler durch Runde 7 (22 Zeilen)

**Kritisch, alle in D2850 (Regel 5):**
1. **«2.1939» und «12.1961» sind Daten, keine Signaturen.**
   - Sie stehen auf S. 12 in der Datumsspalte der Referatsliste von 53 (x 94.9, wie «17.03.1938»). Echte Signaturen stehen
     bei x 70.9.
   - Vorher standen sie als B.2.1939. und B.12.1961. unter der erfundenen «B.». Jetzt hängen sie ohne Hinweis unter den
     echten Einheiten 2 und 12, die dadurch Teilbestand werden; 12. meldet «Untereinheiten reichen über den Zeitraum hinaus».
   - In 53 fehlen deshalb die Referate von Februar 1939 bis 1962, die Nachrufe, die Festansprachen und der Hinweistext.
   - Das Signal J der Strukturprüfung zeigt beide zu Recht an.
2. **65.A. «Engelhardt» ist erfunden.** Im PDF steht S. 23 «… im Seitenprofil; Künstler: 1929» / «A. Engelhardt».
   - Die angekündigte Ausnahme greift nicht. `PERSONENBEZEICHNUNG_AM_ENDE_RE` prüft `vor.text` samt der Datumsspalte, die
     Zeile endet also auf «1929», nicht auf «Künstler:».
   - Dadurch ist 65 Teilbestand, und der Künstlername fehlt bei der Plakette.
3. **55 und 56:**
   - S. 13 nennt «55 … I A – M» und «56 … II N – Z» als Übersicht. Die Listen beginnen auf S. 14 bzw. S. 18.
   - Jetzt ist 55 leer. Die Einleitung «Briefsammlung Emil Klöti» und die A–M-Liste (204 Namen) stehen im Darin von 56, dessen
     Zeitraum 1877–1939 aus «Jahrgängerverein 1877» geschätzt ist.

**Mittel (13):**
- **D1874 3.:** Die neue Einheit erbt «Genau 1260» von 3.11. Dort ist «1260 x 891» ein Format in mm, das schon vorher als
  Jahr galt.
- **D3828 3.17. Nr. 33:** Die reine Datumszeile «1946» unter «1939 –» fällt weg. Vorher war 33. eine erfundene Einheit
  mit 1939–1946.
  - Im ganzen Korpus findet `np8_datumsumbruch.py` dieses Muster nur in D3828. Die drei übrigen Fälle (S. 15–17,
    «1953 –» / «1956» usw.) bestanden schon vorher.
- **D3530 2.3.:** 1862–1975 statt 1922–1975. Die 1862 stammt aus Lebensdaten im Titel von Nr. 22.
- **D2850:**
  - 66 hat «[ohne Titel]»; der Titel «Schweizer Armee- und Zivilschutzgasmaske …» steht im Darin.
  - 64 hat einen Doppeltitel und 1937–1951 statt 1930–1962.
- **D3774:**
  - 2. hat 1841–1951 statt 1841–1963, weil der Beginn der offenen Serie 2.5. «1951-» als Ende gilt.
  - 3.51. hat 1848–1896 statt 1848–1908.
  - Die Titel von 3.53. und 4.53. enthalten die erste Unterzeile («undatiert» / «ohne Datum»).
- **D151730:**
  - 19.5. hat den Titel «Zigarettenausgabe an die Mädchen Anhang».
  - 4. und 15. haben «Genau 1914» bzw. «Genau 1930». Die Datumsspalte nennt nur den Beginn; 15. hatte vorher richtig
    1930–1966.
- **D152400 7.3.:** Der Titel endet auf «… Stadtarchivar», «Dr. P. Guyer» steht im Darin.
- **D152781 5.1.:**
  - Im PDF steht «5.1. Persönliche Dokumente:» mit drei Einträgen (1923, 1928, 1937).
  - Jetzt lautet der Titel «Persönliche Dokumente: Kursausweis … (1923)», der Zeitraum ist = 1923 statt 1923–1937.
  - 5. hat deshalb 1921–1923 statt 1921–1937, und der Hinweis fehlt.
  - Die Ursache ist, dass das Label «…:» nicht abgetrennt wird; Regel 13 legt das nur offen.
- **D140969 87.:** Die Einheit steht neben 82-86, weil der Detailkopf «82 – 86» sagt; die Übersicht S. 1 sagt «82 – 87».

**Gering (6):**
- D151761 und D152390: Zwei sich widersprechende Hinweise («Tippfehler?» und «ohne Doppelpunkt»).
- D152817: Schachtel 12 steht vor 8-11.
- D2850: «Diverses» im Darin von 63; 48.B. beginnt mit 1901.
- D3826 1.: Der Hinweis «Schachtel 1 – Amtliches» fehlt, weil die Überschrift jetzt zum Vorspann gehört.

## Ältere kritische Gliederungsfehler (12 Zeilen, Runde 7 nicht die Ursache)

Keiner davon steht unter «Bewusst offen». Die Strukturprüfung meldet keinen davon, ausser D2850 (Signal Z).
- **D3810, 2 Zeilen:**
  - Die eingerückte Liste unter 7. (x 106.9, «1. Kiburg …» bis «21. Vereinzelte genealogische Notizen») ist ab «8.» als
    14 Hauptnummern 8.–21. gelesen.
  - Die echte «8. Nachträge» (x 70.9, Schachtel IV) fehlt; ihr Inhalt steht im Darin der erfundenen 21.
  - Regel 2 greift hier nicht, weil die Hauptnummern nicht fett sind. `np8_einzug.py` findet den Fall; die übrigen Treffer
    im Korpus sind Registraturpläne und Tabellen.
- **D3313:** Das «Detailinventar der enthaltenen Porträtphotographien» (46 Nummern, S. 3–5) ergibt 4 falsche Teile 2
  unter 1.–4. und 42 erfundene Einheiten :5.–:47.
- **D134644:** «2. Stammbuch …» aus 1.2. wird Hauptnummer 2., die echte «2. Manuskripte» nur Teil 2. Das ist seit der
  Nachprüfung 3 bekannt.
- **D140969, 2 Zeilen:** 50a, 88 und 89 fehlen.
  - Ihr Text steht bei 50. (das deshalb bis 2010 reicht) bzw. bei 87.
  - «88 Pläne» ist der Umfang von 87.
- **D152817:** Läuft ein Buchstabenabschnitt über zwei Schachteln, wird er Eltern dieser Schachteln.
  - So hängen a)–e) und g) unter «f) Arbeitslosenfürsorge»; insgesamt sind 5 Bereiche mit 10 fremden Abschnitten betroffen.
  - Neu in Runde 7 ist nur der passende Hinweis.
- **D1874:** «V.G. c.42.:Reg.» und «Reg. 1»–«Reg. 5» haben auf S. 1 eigene Vollsignaturen, fehlen aber als Einheiten. Ihr
  Text steht im Darin von 1., «5 Bände» im Umfang von 1.
- **D151730 19.5.:** Der Anhang S. 4 (Verweise auf V.J. b.301.–c.17.) steht im Darin, mit 1912–1947. Den Zeitraum erbt 19.
- **D2850:**
  - Der Schlussblock beginnt fälschlich bei «Stadtarchiv Zürich», einem Absender in der Briefliste 56 (S. 20).
  - Die 73 Namen bis «Zunftgesellschaft zum Kämbel» stehen deshalb nur im Blatt Info.
  - Die echte Bearbeitungsnotiz S. 24 («Zürich, Oktober 1976 / Dr. Paul Guyer …») steht dagegen im Darin von 66.
- **D3826 20.:** Im Darin stehen die Mappe «Mappe – Porträt (Grossformat)» mit dem Stich von 1911, der Vermerk
  «Weitere Diplome …» und der Kopf des Nc-Verzeichnisses S. 4.
- **D845:** 1.2 fehlt. Die Tippform «V.C: c.52.:1.2» wird nicht als Signatur erkannt.

**Weitere ältere Funde (mittel/gering)** stehen in der Fundliste, unter anderem:
- Schachtel-Nr. fehlt: D3826 alle 20, D151730 31 von 42, D3256 3. «2» statt «2-5»;
- D3313 1.–3. haben den Jahrgang als Beginn;
- D150689 5.4.3./6.4.6. erben den Titel;
- D2270 hat die Stückzahl im Titel;
- D176721 3. hat einen abgeschnittenen Titel.

## Altzeilen aus den Nachprüfungen 6 und 7 (41)

- **behoben, 10:**
  - D3828 ganz (3);
  - D3530 Gliederung (2);
  - D3774 Hierarchie;
  - D140969 Bereiche;
  - D2737 Doppelnummern;
  - D150689 1.8.1.;
  - D134644 10.1.1.
- **teilweise, 5:**
  - D150689 Übersicht als Einheit und Titelumbruch;
  - D3774 Darin-Trennung;
  - D140969 14./17.;
  - D152781 3.3.
- **offen, 25:** vor allem Zeiträume und Titel in D3774 (7), D150689 (6) und D141 (4).
- **schlechter, 1:** D152781 5.1. (A37, siehe oben).

## D151210

`D151210_scope_import.xlsx` ist sauber:
- zellgleich mit dem Stand nach Punkt 2 (2953088e);
- byteweise gleich mit der Kopie in `testdaten_excel/`;
- identisch mit meinem Lauf.

Damit gelten die Prüfungen aus der Nachprüfung 7 und aus Punkt 2 unverändert, auch die 13 Soll-Fälle mit dem Fallset Punkt 2
38/38.

## Kennzahlen, Fallsets, Testdaten, Textverlust

| Prüfung | vorher (2953088e) | nachher (1f98df0b) |
|---|---:|---:|
| Einheiten | 49'242 | 48'980 |
| «[ohne Titel]» | 34 | 31 |
| Text erfasst 100 % | 695 | 695 |
| doppelte Schlüssel (überzählig) | 10 | 10 |
| Dateien mit Übersichtszeilen | 12 | 10 |
| Fallset A / F | 11/12, 5/7 | unverändert |
| Fallset B / C nach Signatur | 37/38, 10/12 | unverändert |
| Fallset Runde 2 | 34/34 | 33/34 |
| Fallset Punkt 2 | 38/38 | 38/38 |
| Testdaten (11 Dateien) | – | zellgleich |

Zu den Fallsets:
- **B und C:** Nach ID zeigen sie 36/38 und 9/12, weil sich in D2737 und D3828 die IDs verschoben haben. Nach Signatur bleibt
  9. = 1914–1987 und 3.16. = 1940–1945.
- **Runde 2:** «Nc 4-6 …» bei D149835 7. steht jetzt im Blatt Info (Regel 12). Das ist richtig, der Fall wird angepasst.

**Textverlust:** `np8_textverlust2.py` vergleicht alle Textspalten und das Blatt Info und gleicht mit der Häufigkeit im PDF
ab. Er findet ausser «1946» nur:
- Titel, die vorher von den Eltern geerbt und jetzt durch den eigenen ersetzt sind;
- den Vorspann von D3256 und D3826;
- Nummern, die vom Darin in die Signatur gewandert sind.

**Strukturprüfung der Hauptsession, nachgerechnet:**

| Signal | vorher | nachher |
|---|---:|---:|
| T | 10 | 9 |
| D | 45 | 0 |
| E | 37 | 61 |
| F | 45 | 41 |
| L | 36 | 20 |
| : | 186 | 163 |
| J | 2 | 2 |
| Z | 3 | 4 |

Das sind dieselben Zahlen wie in `runde7/gliederung_nachher.txt`. J und Z betreffen D2850 und sind echte Fehler (siehe oben).

## Hinweise zu AENDERUNGEN_RUNDE7.md

- **D2850:**
  - «Jetzt gibt es 48 mit 48.A., 48.B., danach 49–66» stimmt.
  - «B.12.1961. war erfunden» ist nur halb behoben: Die Daten 2.1939 und 12.1961 sind weiter Einheiten.
  - «A. Engelhardt nach Künstler: ist ein Name» wirkt in der Ausgabe nicht.
- **Bewusst offen, D3828 3.4.:** Die Beschreibung ist verdreht. «Akten zu verminten Brücken» (S. 5) ist die Einheit,
  «3.4. Bundesfeiern» (S. 6) ihr Teil 2.
- **Regel 14, D152400:** «Vgl. auch V.J. b.202.» stand schon vor Runde 7 im Blatt Info. Geändert hat sich dort die Gliederung
  nach Regel 3.

## Vorschläge für die nächste Runde (nach Nutzen)

1. **D2850, Datums-Signaturen.** «M.YYYY» am Anfang einer Zeile in einer Datumsliste ist keine Signatur. Merkmal: gleiche x wie
   die Zeilen «dd.mm.yyyy» davor und danach, rechts der Signaturspalte. Das Signal J findet solche Fälle.
2. **D2850, «Künstler: 1929» / «A. Engelhardt».** Die Personenbezeichnung ohne die Datumsspalte der Vorzeile prüfen.
3. **Nummerierte Liste im Inhalt, die die Hauptfolge fortsetzt (D3810, D3313).** Die Zählung je Spalte aus Regel 2 auch ohne
   fette Hauptnummer anwenden:
   - wenn die Liste gegenüber der Signaturspalte eingerückt ist (D3810);
   - wenn sie unter einem Listenkopf wie «46 Porträtphotographien folgender Personen:» steht (D3313).
4. **D2850, Rest:**
   - Schlussblock nicht mitten in einer Namensliste beginnen lassen («Stadtarchiv Zürich» als Absender);
   - die Übersicht 55/56 auf S. 13 als Übersicht erkennen;
   - Titel von 66.
5. **Zeiträume neuer Gruppen:**
   - Nennt die Datumsspalte nur den Beginn («1930–»), die Kinder nehmen (D151730 4./15.).
   - Bei offenen Serien kein Beginn als Ende (D3774 2.).
   - «1260 x 891» ist ein Format, kein Jahr (D1874 3.11.).
   - Lebensdaten in Bibliografie-Titeln zählen nicht (D3530 2.3.).
6. **D152781 5.1.:** Das Label «Persönliche Dokumente:» als Titel abtrennen, der Zeitraum dann 1923–1937.
7. **Übrige ältere kritische Fälle:**
   - D152817 Abschnitt über zwei Schachteln;
   - D140969 50a/88/89;
   - D1874 Reg.;
   - D845 «V.C:»;
   - D134644 2./1.2.;
   - D151730 Anhang;
   - D3826 20.

Auf Wunsch liefere ich für 1–3 wie bisher einen Patch in einer Kopie, mit Gesamtlauf und Abgleich gegen diesen Stand.

## Ablage

- **Berichte:** `nachpruefung8.md` (dieser Bericht) und `funde_nachpruefung8.csv`.
  - Die Fundliste hat 105 Zeilen: 64 neue, dazu die 41 Altzeilen mit Status.
  - Die Spalten sind wie in Runde 7. `ist` ist bei Altzeilen der Stand der Vorrunde, bei neuen der Stand 2953088e; `neu_ist`
    ist der Stand 1f98df0b.
  - Die Bemerkung beginnt mit «Ursache: Regel n», «Ursache: vor Runde 7» oder bei Altzeilen mit «[An]».
- **Rohdaten in `roh/`:**
  - `np8_paket_N_urteile.csv` (748 Urteile mit Beleg), `np8_paket_N.csv` (Funde) und `np8_paket_N_notizen.md`;
  - `np8_paket_N_altzeilen.csv`;
  - `np8_vgl/` (34 Vergleichsdateien);
  - `np8_sigcheck.txt`, `np8_einzug.txt` und `np8_textverlust2.csv`.
- **Methode:** `methode/ANLEITUNG_NACHPRUEFUNG8.md` und `methode/np8_*.py`.
- **Projekt unverändert:** Skript, `findmittel_excel/`, `testdaten_excel/` und D151210 habe ich nicht angefasst.
