# Stichproben: Findmittel-PDF ↔ scope-Import-Excel

Stand 19.11.2026. Geprüft wurde der Lauf von `findmittel_zu_scope.py` vom 19.11.2026, 21:02 (SHA-256 `cd62721dd64e814b…`), also die Excel-Dateien vom 21:03. Dieser Bericht ändert nichts am Skript und an den Excel-Dateien. Alle Fundstellen sind am PDF belegt, die Zeilennummern beziehen sich auf diesen Skriptstand.

## Kurzfazit

- **Keines der 50 Stichproben-PDFs ist fehlerfrei.** 26 haben grobe Fehler, das heisst mindestens eine Einheit fehlt, ist erfunden oder hängt falsch. 24 haben nur kleine Fehler, davon 7 mit einem systematischen Fehler, der mindestens ein Fünftel der Einheiten betrifft. Gezählt sind 897 Fundzeilen mit rund 2'697 betroffenen Stellen, davon 194 kritische Fundzeilen.
- **«Text erfasst» und «Status OK» sagen über die Struktur nichts aus.** Die Wortprüfung findet ein verschobenes Wort bei der falschen Einheit trotzdem «wieder». Vorspann, «Text vor der ersten Signatur» und Schlussvermerke zählt sie gar nicht mit. 5 Stichproben-PDFs mit Status OK und 100 % haben grobe Fehler (D3484, D2323, D442, D3672, D140955). Nur 131 von 897 (15 %) der Fundzeilen hat das Skript selbst in den Prüfhinweisen gemeldet.
- **Der schwerste Fehler kommt in der Stichprobe nur siebenmal vor:** Ganze Verzeichnisteile werden als «Vorspann», «Text vor der ersten Signatur» oder Schlussvermerk verworfen. Der Gesamtscan zeigt ihn bei mindestens 19 weiteren PDFs, 9 davon mit Status OK. Bei VII.277. fehlen die Seiten 1–141 von 201, bei V.F.c.28. die Seiten 1–21 von 22, bei VII.481. bleibt von 7 Abschnitten nur eine Einheit übrig («1 Filmrolle»; Abschnitt 6).
- **Am häufigsten** sind Fremdtext im Darin (30 PDFs), eine nicht abgetrennte rechte Spalte mit Datum oder Zahl im Titel (23) und mehrzeilige Datumsspalten, bei denen nur die erste Zeile zählt (22).
- **Am folgenreichsten ist die Signaturerkennung** (Abschnitt 4, Muster 6, 8, 9).
  - Echte Signaturen werden übersehen: «IV.B.41.:12.–14.», «V J. c.5.:3.», «1.1.1000.», «30. “Swissair”», «16. 2 Fotografien».
  - Zufällige Zahlen werden zu Signaturen: «1 Verzeichnis», «25 Jahre …», «B 1 bis B 23», «a) I 27 Asper».
  - Gliederungsebenen werden nicht erkannt: «II. KORRESPONDENZ», «I)», eingerückte Unterzählung, neu beginnende Zählung je Abschnitt.
- **Nach Gliederung:** Am schlechtesten schneidet «römisch/Buchstaben» ab (7 von 8 grob). Bei 3 von 9 Dateien der Gruppe 5 ist schon der Gliederungstyp falsch erkannt. 1-seitige PDFs sind meist brauchbar (8 von 9 nur kleine Fehler).
- **Vorschlag für die Reihenfolge der Korrekturen:**
  1. Beginn des Detailverzeichnisses bestimmen (`finde_detailbeginn`) und den Vorspann mitprüfen.
  2. Plausibilität der Signaturen prüfen: Einrückung, Folge, Mengenangaben, Zeichen nach der Nummer.
  3. Datumsspalte über ihre x-Position statt über die 18-pt-Lücke erkennen, auch über mehrere Zeilen.
  4. `SCHLUSS_RE` und `TABELLENKOPF_RE` erweitern.
  5. Zeilenumbruch-Regeln.
  6. Zeitraum-Quellen und Datumsformate.
  7. Wortfragmente in `lese_zeilen` zusammenfügen.

## 1. Stichprobe und Vorgehen

**Grundgesamtheit:** 715 PDFs laut `uebersicht_scope_import.xlsx`. Ohne die 3 Scans bleiben 712 verarbeitete PDFs.

**Ziehung:** Fester Startwert `20261119`, Skript `methode/stichprobe.py`. Die Stichprobe umfasst 50 PDFs in drei Schichten:
- **A – alle 32 PDFs mit «Text erfasst» unter 100 %.** Das war Vorgabe. Diese Schicht ist dadurch übervertreten: Häufigkeiten unten gelten für die Stichprobe, nicht für alle 712.
- **B – Firmenarchiv Locher VII.308.:** je ein zufälliges PDF ab 50 Seiten und eines darunter (D3472 F.a., D3484 D.a.).
- **C – 16 zufällige PDFs mit 100 %**, geschichtet nach Gliederung × Grösse (1 Seite / 2–49 / ab 50). Für «Vollsignatur ab 50 S.» gab es ausser D175996 (Schicht A) keinen Kandidaten.

**Abdeckung der Stichprobe:**
- alle 7 Gliederungsarten;
- 9 einseitige, 34 mittlere und 7 grosse PDFs (bis 152 S.);
- 21 × Status OK, 29 × Prüfen.

**Prüfumfang** (`methode/pruefseiten.csv`, Seiten ebenfalls mit festem Startwert gezogen):
- PDFs bis 4 Seiten und «ohne Signaturen» bis 10 Seiten: vollständig.
- Sonst: 3 Zufallsseiten vollständig.
- Immer dazu: alle Zeilen mit «Fehlt im Import» aus dem Blatt «Vollständigkeit», die Gesamtstruktur und die Grenze Vorspann ↔ Detailverzeichnis.

Funde ausserhalb der Prüfseiten sind als Sammelzeilen mit geschätzter Anzahl erfasst.

**Durchführung:** 6 Subagenten, je eine Gliederungsart, nach der gemeinsamen Anleitung `methode/ANLEITUNG.md`. Sie arbeiteten auf einem Schnappschuss der Excel-Dateien (Werkzeuge in `methode/`: `dump_excel.py`, `woerter.py`).

**Gegenprobe:** 13 Funde in 8 PDFs aus allen 6 Gruppen habe ich selbst am PDF nachgeprüft, alle bestätigt: D2323 :3, D71 III.S.1., D3589 Expl.-Zahl und geerbtes «= 1916», D3672 1.1.1000., D442 30., D4039 Schachteln, D3533 1.3./1.4./3.6., D3432 4.1./12.1. Meine eigenen Vorab-Funde zu D3533 und D3432 hat Gruppe 2 unabhängig vollständig gefunden.

**Schwere und Zählung:** Die Schwere folgt dem Auftrag.
- kritisch = Einheit fehlt oder ist erfunden, falsche Signatur oder Hierarchie, Text verloren oder bei einer fremden Einheit;
- mittel = falscher Titel, Zeitraum, falsche Schachtel, Umfang oder Darin-Trennung;
- gering = kosmetisch.

Beim Zusammenführen habe ich die Schwere über die Gruppen angeglichen (21 Fundzeilen, in `funde.csv` vermerkt):
- Ein verlorenes Datum zählt als mittel (falscher Zeitraum), denn der Text bleibt erhalten.
- Eine Bemerkung im Titel zählt als mittel.
- Signatur-Tippfehler im PDF, durch die eine Einheit verloren geht, zählen als kritisch (z. B. «V J. c.5.:3.», «V.B. 439.»): Das Skript verliert die Einheit dann ohne Hinweis.

Eine Zahl wie «12 (45)» heisst: 12 Fundzeilen, die zusammen rund 45 Stellen betreffen. Bei Sammelzeilen ist die Zahl der Stellen geschätzt.

**Urteil je PDF:**
- grobe Fehler = mindestens ein kritischer Fund;
- kleine Fehler = nur mittlere oder geringe Funde; «(systematisch)», wenn ein mittleres Muster mindestens 20 % der Einheiten betrifft (bei mindestens 10 Einheiten);
- gut = höchstens zwei geringe Funde.

Die Agenten hatten «viele mittlere» teils als grob gewertet. Das betrifft 9 PDFs, die jetzt «kleine Fehler (systematisch)» oder «kleine Fehler» heissen: D149634, D150296, D175994, D176367, D2641, D3589, D4054, D406 und D512. Ihre Originalurteile stehen in `roh/gruppe_*_urteile.md`.

## 2. Stichprobe und Urteil je PDF

Schicht A = Text erfasst < 100 %, B = Locher, C = Zufall. Fälle k/m/g = betroffene Stellen kritisch/mittel/gering. Die ausführlichen Begründungen stehen in `roh/gruppe_N_urteile.md`.

| Nr | PDF | Bestand | Gliederung | S. | Einh. | Status | Text erf. | Schicht | Geprüfte Seiten | Urteil | Fälle k/m/g | Kern |
|---:|---|---|---|---:|---:|---|---:|:-:|---|---|---|---|
| 1 | D10575 | VII.494. | dezimal | 38 | 201 | OK | 99,96 % | A | 24, 33, 34 + Lücken S. 19, 20, 27, 34 | **grobe Fehler** | 16/29/7 | «Detailverzeichnis» steht über dem Inhaltsverzeichnis → 15 Gruppen aus dem Inhaltsverzeichnis; Bandnummern 16/17 als Einheiten; Inhalt von 3.–7. bei 2.2.7/6.15 |
| 2 | D141005 | VII.380. | fortlaufend | 3 | 43 | Prüfen | 99,85 % | A | alle | **grobe Fehler** | 46/15/0 | Eingerückte Unterzählung nicht erkannt → Hierarchie fast ganz falsch; 5 Unterpunkte fehlen («August» als Monat) |
| 3 | D149634 | VII.3. | Vollsignatur | 8 | 157 | OK | 99,94 % | A | 1, 3, 5 + Lücken S. 5 | kleine Fehler (systematisch) | 0/103/0 | Inhalt sauber; Spalte «Ebene» bei allen 99 Kindern von Bereichssignaturen falsch (Parent-ID stimmt) |
| 4 | D150296 | VII.298. | dezimal | 35 | 153 | OK | 99,96 % | A | 5, 25, 30 + Lücken S. 7, 22 | kleine Fehler | 0/25/0 | Struktur korrekt; Zeitraum nur aus erster Datumszeile (22 Teile erben ihn); Darin-Einträge verschmolzen |
| 5 | D151217 | VII.416. | dezimal | 36 | 724 | Prüfen | 99,98 % | A | 4, 12, 18 + Lücken S. 2 | kleine Fehler | 0/15/0 | Prüfseiten 12/18 fehlerfrei; Titel an «–» bzw. im Zitat an «: » abgeschnitten; Jahre aus Beschreibungen als Zeitraum |
| 6 | D175994 | IV.A. | Vollsignatur | 6 | 65 | OK | 99,90 % | A | 1, 3, 5 + Lücken S. 4 | kleine Fehler (systematisch) | 0/24/0 | 2./3. Zeile der Datumsspalte geht verloren (19 Einheiten); Gliederungsüberschrift im Darin |
| 7 | D175996 | IV.B. | Vollsignatur | 100 | 1322 | OK | 99,99 % | A | 43, 63, 65 + Lücken S. 93 | **grobe Fehler** | 15/9/0 | Prüfseiten fehlerfrei; 15 Einheiten fehlen («IV.B.41.:12.–14.» mit Gedankenstrich, «1.a)», Tippfehler «V.B. 439.») |
| 8 | D175997 | IV.C. | Vollsignatur | 10 | 126 | OK | 99,94 % | A | 4, 5, 9 + Lücken S. 2 | **grobe Fehler** | 31/7/0 | 31 Einheiten IV.C.201.:1.–:31. ohne Elterneinheit (Gruppenüberschrift im Darin von IV.C.184.) |
| 9 | D176151 | VII.371. | dezimal | 25 | 70 | Prüfen | 99,98 % | A | 2, 3, 5 + Lücken S. 2 | **grobe Fehler** | 36/5/3 | Ab S. 13 zerstört: Zwischentitel «25/50 Jahre» werden Einheiten 25./50., 13.–16. fehlen, 27 Einheiten ohne Parent |
| 10 | D176367 | VII.215. | dezimal | 15 | 85 | OK | 99,95 % | A | 2, 5, 9 + Lücken S. 5 | kleine Fehler (systematisch) | 0/71/1 | Struktur korrekt; verschachtelte Spiegelstrich-Listen zerfallen (rund 50 Fälle); «ff.» als «Genau» |
| 11 | D2366 | V.J.c.66. | ohne Signaturen | 1 | 1 | Prüfen | 98,86 % | A | alle | kleine Fehler | 0/4/6 | Einleitung, Überschriften, Tabellenkopf im Darin (weil «D etailverzeichnis» zerrissen); zerrissene Wörter |
| 12 | D2641 | V.L.197. | Vollsignatur | 10 | 155 | OK | 99,80 % | A | 3, 6, 7 + Lücken S. 5, 7, 9 | kleine Fehler (systematisch) | 0/58/0 | Widmungszeile bei 37 von 155 Einheiten im Titel; «ca. 1960er» → «Genau 1960»; Werktitel-Jahre als Zeitraum |
| 13 | D2839 | VII.103. | dezimal | 23 | 23 | OK | 99,91 % | A | 2, 3, 6 + Lücken S. 3, 4, 7, 9 | **grobe Fehler** | 1/63/1 | Jahres-Zwischenzeilen verkleben Einträge, Daten gehen verloren; «4. NSDAP» fehlt; Tabellenkopf in jeder Mappe |
| 14 | D2872 | VII.118. | dezimal | 6 | 104 | Prüfen | 98,68 % | A | 2, 4, 6 + Lücken S. 6 | **grobe Fehler** | 1/82/0 | Schachtel ab 5. überall falsch («Schachteln 3 und 4», «Mappe» nicht erkannt); Schlussvermerk als erfundener Teil |
| 15 | D3018 | VII.174. | dezimal | 78 | 194 | Prüfen | 99,99 % | A | 17, 33, 40 + Lücken S. 17 | **grobe Fehler** | 256/16/2 | Abschnitte 01–09 (neu beginnende Zählung) vermischt; 55 Übersichtszeilen als Einheiten; ~50 Einheiten nur im Darin |
| 16 | D3038 | VII.181. | römisch/Buchstaben | 3 | 30 | Prüfen | 99,55 % | A | alle | **grobe Fehler** | 2/4/0 | Schachtel 2/3 als Teile an «I.b» gehängt; «Schachtel 400» am Ende verloren |
| 17 | D3060 | VII.189. | römisch/Buchstaben | 8 | 8 | Prüfen | 99,85 % | A | 6, 7, 8 + Lücken S. 4 | **grobe Fehler** | 14/11/0 | Schachtelliste: alle 8 Signaturen aus Listenmarken «a) b) c)» erfunden; Schachteln 3, 4, 7–10 fehlen |
| 18 | D3063 | VII.190. | dezimal | 21 | 68 | Prüfen | 99,16 % | A | 8, 9, 13 + Lücken S. 7, 10 | **grobe Fehler** | 13/57/1 | 20.–23., 30., 50., 51. nicht erkannt (Nummernsprung); MM.JJJJ nicht erkannt; Schachteln nicht weitergegeben |
| 19 | D3067 | VII.191. | römisch/Buchstaben | 31 | 91 | Prüfen | 99,88 % | A | 5, 11, 17 + Lücken S. 5, 8 | **grobe Fehler** | 117/21/0 | Ebenen «I)», «II) A)» nicht erkannt; Mengenangaben als Signaturen; Gruppen fehlen – unbrauchbar |
| 20 | D3077 | VII.194. | fortlaufend | 3 | 22 | Prüfen | 99,74 % | A | alle | **grobe Fehler** | 5/25/0 | Heftliste «1.–5. Heft» als 5 erfundene Einheiten; Schachtel nur bei erster Einheit; Lebensdaten als Zeitraum |
| 21 | D3089 | VII.197. | römisch/Buchstaben | 38 | 49 | Prüfen | 99,92 % | A | 3, 5, 6 + Lücken S. 3, 5, 11 | **grobe Fehler** | 49/64/0 | «II. KORRESPONDENZ …» u. ä. verworfen → II.–X. als Teile unter I.; erfundene Einheiten aus Initialen |
| 22 | D3398 | VII.282. | Vollsignatur | 4 | 33 | OK | 99,62 % | A | alle | **grobe Fehler** | 2/12/1 | Schachtelzeilen mit 2. Datumszeile: Teil 1 fehlt, Sitzungsdaten werden Titel; Schlussvermerke im Darin |
| 23 | D3432 | VII.296. | dezimal | 2 | 24 | Prüfen | 99,27 % | A | alle | kleine Fehler | 0/2/0 | 2. Zeitraum «1936 – 1956» verloren; «o.D.» im Titel |
| 24 | D3589 | VII.359. | fortlaufend | 11 | 262 | OK | 99,93 % | A | 3, 7, 8 + Lücken S. 8 | kleine Fehler (systematisch) | 0/323/13 | Struktur korrekt; Expl.-Zahl in allen 262 Titeln; 59 undatierte Bücher erben «= 1916» |
| 25 | D4007 | VII.435. | ohne Signaturen | 6 | 1 | Prüfen | 99,71 % | A | alle | kleine Fehler | 0/6/12 | Bestandszeile korrekt; Tabellenkopf im Darin; Zeilenpaare an Seitenwechseln verschmolzen |
| 26 | D4039 | V.F.c.119. | ohne Signaturen | 6 | 1 | Prüfen | 99,78 % | A | alle | **grobe Fehler** | 47/10/3 | Rechtsbündige «Schachtel 1 … 47» nicht erkannt → 1 Bestandszeile statt 47 Einheiten |
| 27 | D4054 | VII.151. | dezimal | 152 | 443 | Prüfen | 99,98 % | A | 20, 119, 143 + Lücken S. 29, 49, 55, 120 | kleine Fehler | 0/58/0 | Struktur korrekt; Zeitraum nur aus erstem Datumsblock (rund 55 Einheiten zu eng) |
| 28 | D406 | V.B.c.3. | Vollsignatur | 3 | 65 | Prüfen | 99,88 % | A | alle | kleine Fehler | 0/7/0 | Bemerkung «56.–65. nicht vorhanden» im Titel von :55; «August» als Monat; «Letzte Änderung» → Zeitraum 2012 |
| 29 | D414 | V.B.c.34. | römisch/Buchstaben | 2 | 16 | Prüfen | 98,87 % | A | alle | **grobe Fehler** | 6/4/1 | Schachtelliste S. 1 (Schachtel 1–5) nicht importiert; II./III. ohne Titel; Schlussnotiz als Einheit XV.2.12. |
| 30 | D512 | V.B.c.70. | dezimal | 68 | 63 | Prüfen | 99,95 % | A | 36, 62, 68 + Lücken S. 3, 27, 34, 41, 42, 58 | kleine Fehler (systematisch) | 0/88/0 | Dreispaltige Tabelle zeilenweise gelesen; 39 von 51 Saisons mit Einzeldatum aus Fortsetzungszeile |
| 31 | D537 | V.B.c.9. | Mappen/Schachteln | 132 | 27 | Prüfen | 99,98 % | A | 19, 47, 63 + Lücken S. 47, 54, 59, 60, 61 | kleine Fehler (systematisch) | 0/18/160 | ~2000 Darin-Einträge vollständig und richtig zugeordnet; Titel/Zeitraum der Schachteln 20–24 («1863 ff.») |
| 32 | D860 | V.C.c.75. | Mappen/Schachteln | 4 | 37 | Prüfen | 93,44 % | A | alle | kleine Fehler | 0/10/3 | Kurz-Endjahre «1987 - 88», «1989-96» falsch (7×); Kopfzeile in 12 pt im Darin (3×) |
| 33 | D3472 | VII.308.F.a. | römisch/Buchstaben | 70 | 1714 | Prüfen | 100,00 % | B | 53, 60, 62 + S. 1–2 | **grobe Fehler** | 6/3/0 | Prüfseiten fehlerfrei; 6 Mappen mit Zusatz («1939.37 a», «1938.46 –») fehlen; Jahr aus Nummer nicht als Zeitraum |
| 34 | D3484 | VII.308.D.a. | fortlaufend | 32 | 696 | OK | 100,00 % | B | 15, 28, 32 + S. 1–2 | **grobe Fehler** | 8/80/5 | 8 Mappen fehlen («639/640 div. O.», «622 a»); Folgezeile mit Datum → Titelrest im Darin, Zeitraum zu kurz (~70×) |
| 35 | D2323 | V.J.c.5. | Vollsignatur | 1 | 4 | OK | 100,00 % | C | alle | **grobe Fehler** | 1/1/0 | «V J. c.5.:3.» (Tippfehler im PDF) nicht erkannt → Einheit fehlt, steht im Darin von :2 |
| 36 | D1616 | V.G.b.405. | Vollsignatur | 1 | 5 | OK | 100,00 % | C | alle | kleine Fehler | 0/1/0 | Alle 5 Einheiten korrekt; nur «Letzte Änderung …» im Darin |
| 37 | D1120 | V.E.c.13. | Vollsignatur | 4 | 50 | OK | 100,00 % | C | alle | kleine Fehler | 0/3/0 | 3 Titel an hartem Zellenumbruch abgeschnitten, Rest im Darin |
| 38 | D3533 | VII.328. | dezimal | 1 | 15 | OK | 100,00 % | C | alle | kleine Fehler | 0/3/1 | Datum mitten im Titel (1.3., 1.4.; Lücke 15,6 pt); biografische Schlussnotiz im Darin von 3.6. |
| 39 | D442 | V.B.c.54. | dezimal | 7 | 117 | OK | 100,00 % | C | 2, 3, 5 | **grobe Fehler** | 15/29/9 | «30. “Swissair”» nicht erkannt → 30.1.–30.14. ohne Parent; «(n Schachteln)» im Titel |
| 40 | D3672 | VII.389. | dezimal | 50 | 1363 | OK | 100,00 % | C | 7, 24, 33 | **grobe Fehler** | 147/144/3 | 141 Einheiten 1.1.1000.–1.1.1140. fehlen (vierstellig); ~110 Spaltenjahre im Titel |
| 41 | D2677 | V.L.32. | fortlaufend | 1 | 2 | OK | 100,00 % | C | alle | kleine Fehler | 0/3/0 | Korrekt bis auf 3 verschmolzene Darin-Einträge |
| 42 | D2562 | V.L.123. | fortlaufend | 1 | 2 | OK | 100,00 % | C | alle | kleine Fehler | 0/1/0 | Korrekt bis auf 1 verschmolzenen Darin-Eintrag |
| 43 | D140955 | VII.442. | fortlaufend | 2 | 16 | OK | 100,00 % | C | alle | **grobe Fehler** | 1/14/0 | Nr. 16 («2 Fotografien …») fehlt; Schlussnotizen im Darin → Zeitraum bis 2013 |
| 44 | D2352 | V.J.c.57. | ohne Signaturen | 1 | 1 | Prüfen | 100,00 % | C | alle | kleine Fehler | 0/1/0 | Korrekt bis auf Tabellenkopf als ersten Darin-Eintrag |
| 45 | D3206 | VII.220. | ohne Signaturen | 2 | 1 | Prüfen | 100,00 % | C | alle | kleine Fehler | 0/3/1 | Titel mit Inhaltszeile; Biografie und Bearbeitungsvermerk im Darin |
| 46 | D3795 | VII.57. | römisch/Buchstaben | 1 | 10 | Prüfen | 100,00 % | C | alle | kleine Fehler | 0/1/2 | Korrekt bis auf Bearbeitungsvermerk im Darin und Jahresliste im Titel |
| 47 | D71 | III.S. | römisch/Buchstaben | 3 | 5 | Prüfen | 100,00 % | C | alle | **grobe Fehler** | 1/0/4 | Einzige echte Einheit III.S.1. fehlt (steht im Darin von III.S.:d.) |
| 48 | D2329 | V.J.c.502. | Mappen/Schachteln | 1 | 3 | Prüfen | 100,00 % | C | alle | kleine Fehler | 0/3/0 | Alle 3 Titel mit 2. Zeile des Bestandstitels («Altersrentner … 1959 – 1967, Schachtel 1») |
| 49 | D1739 | V.G.c.105. | Mappen/Schachteln | 10 | 28 | Prüfen | 100,00 % | C | 3, 8, 9 | **grobe Fehler** | 4/76/0 | Fach-/Mappen-Nr. als Jahre (21/28 Zeiträume falsch); Kopfzeile der vorigen Schachtel im Titel; 1 Mappe fehlt |
| 50 | D2990 | VII.161. | Buchstabe+Nr. | 2 | 5 | Prüfen | 100,00 % | C | alle | **grobe Fehler** | 5/1/0 | Typ «Buchstabe+Nr.» falsch; «B 1 bis B 23» als Signaturen; Fortsetzung von 2. als Schlussvermerk verloren |

**Urteile nach Schicht und Merkmal:**

| Merkmal | Wert | grob | klein |
|---|---|---:|---:|
| Schicht | A (Text < 100 %) | 17 | 15 |
| Schicht | B (Locher) | 2 | 0 |
| Schicht | C (Zufall, 100 %) | 7 | 9 |
| Gliederung | dezimal | 8 | 7 |
| Gliederung | Vollsignatur | 4 | 6 |
| Gliederung | fortlaufend | 4 | 3 |
| Gliederung | römisch/Buchstaben | 7 | 1 |
| Gliederung | ohne Signaturen | 1 | 4 |
| Gliederung | Mappen/Schachteln | 1 | 3 |
| Gliederung | Buchstabe+Nr. | 1 | 0 |
| Status | OK | 10 | 11 |
| Status | Prüfen | 16 | 13 |
| Grösse | 1 Seite | 1 | 8 |
| Grösse | 2–49 Seiten | 21 | 13 |
| Grösse | ab 50 Seiten | 4 | 3 |

## 3. Fehler nach Feld und Schwere

Zellen: Fundzeilen (betroffene Stellen). Alle Fundzeilen stehen in `funde.csv`.

| Feld | kritisch | mittel | gering | zusammen |
|---|---:|---:|---:|---:|
| Einheit | 90 (452) | – | – | 90 (452) |
| Signatur | 27 (190) | – | – | 27 (190) |
| Hierarchie | 62 (184) | 4 (99) | – | 66 (283) |
| Titel | 1 (1) | 228 (630) | 23 (25) | 252 (656) |
| Zeitraum | – | 145 (375) | – | 145 (375) |
| Anmerkung | – | – | 4 (4) | 4 (4) |
| Darin | 14 (18) | 171 (364) | 43 (210) | 228 (592) |
| Schachtel | – | 71 (125) | – | 71 (125) |
| Umfang | – | 14 (20) | – | 14 (20) |
| **Summe** | **194 (845)** | **633 (1613)** | **70 (239)** | **897 (2697)** |

Lesehilfe:
- **Einheit/Signatur/Hierarchie** sind die kritischen Strukturfehler: fehlende, erfundene oder falsch gehängte Einheiten.
- **Titel** sind meist mittel: Datum oder Zahl im Titel, abgeschnittener Titel, Folgetext im Titel.
- **Zeitraum** ist ausschliesslich mittel, betrifft aber viele Stellen (mehrzeilige Datumsspalten, falsche Quellen).
- **Darin** ist vor allem Fremdtext und falsche Trennung.
- Von den 210 geringen Darin-Stellen sind 160 «.;»-Reste in D537.

**Nicht gezählt (Entscheidungsfrage):**
- **Locher F.a. (D3472):** 1663 von 1714 Einheiten haben keinen Zeitraum. Das Jahr steckt laut Vorwort nur in der Nummer «Jahr.Laufnummer». Soll das Skript den Zeitraum aus der Nummer übernehmen?

## 4. Die 10 häufigsten systematischen Fehlermuster

Die Agenten haben rund 170 verschiedene Musterbezeichnungen vergeben. Ich habe sie zu 18 Hauptmustern zusammengefasst (Zuordnung in `methode/muster_map.py`). Rang = Zahl der betroffenen Stichproben-PDFs. «Vom Skript gemeldet» = Anteil der Fundzeilen, zu denen schon ein Prüfhinweis im Excel steht.

| Rang | Hauptmuster | PDFs | Fundzeilen | Fälle | kritisch / mittel / gering (Zeilen) | vom Skript gemeldet |
|---:|---|---:|---:|---:|---|---:|
| 1 | M07 Fremdtext im Darin (Schlussnotiz, Tabellenkopf, Überschrift, Kopfzeile, Einleitung) | 30 | 57 | 115 | 0 / 51 / 6 | 0 % |
| 2 | M06 Rechte Spalte nicht abgetrennt – Datum/Zahl im Titel, Datumsreste | 23 | 152 | 471 | 0 / 131 / 21 | 11 % |
| 3 | M05 Mehrzeilige Datumsspalte – zweites Datum verloren, Folgezeile wird eigener Eintrag | 22 | 99 | 254 | 0 / 97 / 2 | 11 % |
| 4 | M10 Darin falsch getrennt – Einträge verschmolzen oder zerstückelt | 21 | 91 | 226 | 0 / 88 / 3 | 0 % |
| 5 | M08 Zeilenumbruch falsch beurteilt – Titel abgeschnitten oder Folgetext im Titel | 20 | 55 | 100 | 0 / 55 / 0 | 9 % |
| 6 | M02 Echte Signatur nicht erkannt – Einheit fehlt, Text im Darin der vorigen | 17 | 52 | 268 | 52 / 0 / 0 | 13 % |
| 7 | M09 Zeitraum aus falscher Quelle (Nummern, Werktitel, Lebensdaten, Notiz, geerbt) | 14 | 64 | 129 | 0 / 63 / 1 | 25 % |
| 8 | M03 Zahl/Marke am Zeilenanfang als Signatur gelesen – erfundene Einheit | 13 | 52 | 212 | 49 / 3 / 0 | 56 % |
| 9 | M04 Gliederungsebene/Überschrift nicht erkannt – Hierarchie falsch | 11 | 83 | 364 | 80 / 3 / 0 | 46 % |
| 10 | M12 Datumsformat nicht erkannt (Jahrzehnt, «1987-88», «ff.», MM.JJJJ, Vorname «August») | 10 | 34 | 50 | 0 / 34 / 0 | 21 % |
| 11 | M16 Zerrissene Wörter (Schriftwechsel bzw. Zeichenreihenfolge im PDF) | 7 | 26 | 33 | 0 / 0 / 26 | 0 % |
| 12 | M01 Verzeichnistext als Vorspann, Schlussvermerk oder Kopfzeile verworfen | 7 | 13 | 18 | 13 / 0 / 0 | 0 % |
| 13 | M17 Kosmetik (Satzzeichen, Anmerkung) | 6 | 8 | 167 | 0 / 0 / 8 | 25 % |
| 14 | M11 Schachtel-Nr. falsch oder fehlt | 5 | 70 | 125 | 0 / 70 / 0 | 0 % |
| 15 | M15 Umfang nicht erkannt (Klammer, Titel, Darin) | 4 | 14 | 20 | 0 / 14 / 0 | 0 % |
| 16 | M13 Teile: Titel vom Nachbarteil, eigener Titel im Darin | 3 | 7 | 17 | 0 / 4 / 3 | 0 % |
| 17 | M14 Mappen/Schachteln: Titel aus Überschrift vor der Marke bzw. Tabellenkopf | 2 | 16 | 29 | 0 / 16 / 0 | 0 % |
| 18 | M18 Spalte «Ebene» passt nicht zur Parent-ID | 1 | 4 | 99 | 0 / 4 / 0 | 0 % |

### 1. Fremdtext im Darin – Schlussnotiz, Tabellenkopf, Überschrift, Kopfzeile, Einleitung (30 PDFs, mittel)

Bearbeitungs- und Schlussvermerke, Spaltenköpfe, Gliederungsüberschriften ohne Signatur, Kopfzeilen der Folgeseiten und bei «ohne Signaturen» Einleitung und Biografie landen als Darin-Einträge bei der vorangehenden bzw. letzten Einheit. Folgefehler: Das Datum eines Vermerks wird als Zeitraum geschätzt.

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D140955 | 2 | VII.442.:17. | Darin ohne Schlussnotiz; Zeitraum bis 2007 | Darin «12. Juni 2007 / Dr. Robert Dünki», «Letzter Nachtrag: 15. Juli 2013 / …»; Zeitraum (aus dem Darin geschätzt) bis 15.07.2013 |
| D3533 | 1 | VII.328.:3.6. | kein Darin (biografische Notiz zum Bestand) | Darin «Alfred Jud-Frei, 9.7.1914 – 23.7.1995, von Stäfa, Bauschlosser und Berufschauffeur. Kurzbiografie liegt bei.» |
| D2366 | 1 | V.J.c.66. | Darin beginnt mit «Bewohner BS: Korrespondenz 1960-1991, A–J, Schachtel 1» | Darin beginnt mit der Einleitung («Informationen über die Tätigkeit der Verwaltungseinheit …»), dann «D etailverzeichnis», «Bürgerstube Gerechtigkeitsgasse» und der Tabellenkopf «Akte / Dossier Schachtel-Nr.» am ersten Eintrag |

Vermutete Ursache:
- `SCHLUSS_RE` (Z. 499) kennt «Letzte Änderung», «Letzter Nachtrag», «Neuarchivierung», «Stand: …» und «Datum / Kürzel» nicht. Die Ersatzregel ab Z. 998 verlangt mehr als 60 Zeichen.
- `TABELLENKOPF_RE` (Z. 501) verlangt «Signatur|Saison|Nr.» am Zeilenanfang. Nach «Nr\.» greift `\b` vor einem Leerzeichen nicht, so dass «Nr. / Titel Datum» durchfällt.
- `baue_vorkommen` (Z. 994) erkennt Überschriften nur als Tabellenkopf oder in GROSSBUCHSTABEN.
- `ist_kopf_oder_fuss` (Z. 186) verlangt ≤ 10,5 pt; die Kopfzeile in D860 hat 12 pt.
- `baue_bestandszeile` (Z. 1516) trennt die Einleitung nur über `DETAIL_RE` ab. In D2366 scheitert das an «D etailverzeichnis» (Muster 11).
- `ergaenze_zeitraeume` (Z. 1843) schätzt dann aus dem Vermerkdatum.

### 2. Rechte Spalte nicht abgetrennt – Datum oder Zahl im Titel, Datumsreste (23 PDFs, mittel)

Das Spaltendatum bleibt mitten im Titel oder Darin-Eintrag stehen. Spalten ausser Datum, Umfang und Schachtel (Expl., Anzahl, Fach/Mappe) hängen am Titel. Beim Entfernen eines Titeldatums bleiben Reste.

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D3533 | 1 | VII.328.:1.3. | «Mitgliedbüchlein der Schweizerischen Grütlikrankenkasse, 2 Führerausweise, Schiessbüchlein …», 1947–1993 | «… 2 Führerausweise, 1947 – 1993 Schiessbüchlein und Dienstbüchlein, …» (Lücke zur Datumsspalte 15,7 pt) |
| D3589 | 3 | VII.359.:4. | «Hesse, Hermann. Ein Luzerner Junker vor hundert Jahren. Bern», = 1920, Umfang 1 Expl. | Titel «… Bern 1920 1» ohne Umfang – die Expl.-Zahl steht in allen 262 Titeln |
| D3672 | 33 | VII.389.:1.1.934. | Spaltenjahr 1942 in von/bis | «… krankes 1942 Kind» (rund 110 Fälle im PDF) |

Vermutete Ursache:
- `trenne_spalten` (Z. 439) trennt die rechte Spalte nur bei einer Lücke ≥ `SPALTEN_LUECKE` = 18 pt (Z. 70). Gemessen: D3533 «Führerausweise,» x1 = 477,0 → «1947» x0 = 492,7, also 15,7 pt. Das Datum steht exakt in der Datumsspalte (x0 = 492,7 wie bei allen anderen Daten).
  - Vorschlag: die x-Position der Datumsspalte aus den übrigen Zeilen lernen und dort ab etwa 6 pt Lücke trennen.
- `trenne_spalten` kennt nur Datum, Umfang mit Masseinheit und Schachtel.
- `zeitraum_aus_titel` (Z. 1745 ff.) entfernt nur ein Datum am Titelende. Dabei bleiben «dat.», «bzw.», «Frühjahr», «o.D.» und «1938‒» stehen; der Ziffernstrich U+2012 fehlt in `VERBINDER_BEREICH_RE` (Z. 227).

### 3. Mehrzeilige Datumsspalte – zweites Datum verloren, Folgezeile wird eigener Eintrag (22 PDFs, mittel)

Hat eine Einheit mehrere Datumszeilen, gilt nur die erste als Zeitraum. Die übrigen werden Darin-Einträge oder gehen verloren. Folgezeilen mit eigenem Datum werden ein neuer Eintrag, so dass Titelreste im Darin landen.

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D175994 | 5 | IV.A.53. | 1893–1985 (Datumszeilen 1893–1955 und 1961–1985) | 1893–1955; «1961–1985» als Darin (19 Einheiten in IV.A.) |
| D3432 | 1 | VII.296.:4.1. | 1912–1956 bzw. Anm. «1912 – 1920, 1936 – 1956» | 1912–1920; die Zeile «2 Bände ¦ 1936 – 1956» wird nur als Umfang gelesen, das Datum fehlt ganz |
| D4054 | 143 | VII.151.:17.1. | 1873–1986 | «= 1873» (rund 55 Einheiten im PDF) |

Vermutete Ursache:
- `kopf_und_rumpf` (Z. 1325): Eine Folgezeile mit eigenem Datum gilt als neue Tabellenzeile und kommt ins Darin.
- `baue_vorkommen` (Z. 1024): Eine reine Datumszeile wird nur Datum, solange die Einheit noch keines hat.
- `baue_vorkommen` (Z. 1028–1031): Das Datum einer Umfangszeile wird verworfen.
- `verarbeite` (Z. 1410 ff.) nimmt nur die erste Datumszeile.
- `_mit_zusatz` (Z. 1148) wirft ein Spaltendatum weg, wenn dasselbe Jahr schon im Text steht. Beispiel D512 S. 3, 34, 41, 58.
- Bei Schachtelzeilen fehlt so ein ganzer Teil: D3398 VII.282.:4./:5., Teil 1 fehlt, die Sitzungsdaten werden Titel.

### 4. Darin falsch getrennt – Einträge verschmolzen oder zerstückelt (21 PDFs, mittel)

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D2677 | 1 | V.L.32.:1. | «… Spenden, 14. Oktober 1868» und «Zusammenstellung von Spendenanfragen …» getrennt | ein Eintrag (3×) |
| D2839 | 2 | VII.103.:2.1. | «22. Zeitleichen - Strassen aufgerissen, 29. Mai 1947» | «… 8. Aug. 1946; 1947 22. Zeitleichen» + eigener Eintrag «Strassen aufgerissen»; das Datum fehlt |
| D176367 | 5 | VII.215.:1.2.2. | «Oberstrass; Satzungen 1944, 1952, 1969 (3); Zünfterverzeichnisse …» | zwei Einträge, der zweite beginnt mit «; Zünfterverzeichnisse …» |

Vermutete Ursache:
- `ist_umbruch` (Z. 1090–1092): Endet eine Zeile an der rechten Spalte bzw. ist sie lang, gilt sie als «voll», und die nächste Zeile wird angehängt. Bei einem Seitenwechsel (Abstand None) entscheidet nur diese Regel, deshalb wird dort fast immer verbunden (D4007, D537).
- `ABSATZ_ABSTAND` = 8,0 pt wird mit «>» geprüft (Z. 1185). Ein Absatzabstand von genau 8,0 pt zählt deshalb nicht (D2677).
- `teile_inline` (Z. 1204) trennt an « - » vor einem Grossbuchstaben.
- Unterstriche, die 3 pt tiefer liegen, werden eigene Zeilen (`lese_zeilen` Z. 150, Toleranz 2,5 pt).
- Mehrzeilige Tabellenzellen werden zeilenweise gelesen (D512, D1739).

### 5. Zeilenumbruch falsch beurteilt – Titel abgeschnitten oder Folgetext im Titel (20 PDFs, mittel)

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D2641 | 3 | V.L.197.:35 | Titel «Haas, Rudi, Ottawa – Our Nation`s Capital, Toronto», Zeitraum 1980, Darin «Widmung des Bürgermeisters an Thomas Wagner.» | Widmung samt Jahr im Titel (37 von 155 Einheiten) |
| D151217 | 4 | VII.416.:3.2.18. | «Meister, Peter Marcel. Schweizer Uniformen und Fahnen von 1800 – 1852», = 12.01.1968 | Titel endet «… von 1800», Darin «1852, 12. Januar 1968» |
| D406 | 3 | V.B.c.3.:53 | Titel «… Expertenbericht Weiss in St. Gallen» | Titel abgeschnitten, Darin «Weiss in St. Gallen» |

Vermutete Ursache:
- `ist_umbruch` (Z. 1069–1092) prüft gegen den Seitenrand («hätte das erste Wort der Folgezeile noch Platz gehabt?»). Bei Word-Tabellen mit schmaler Textspalte und harten Umbrüchen versagt das in beide Richtungen.
- `rand_spalte` (Z. 1350) gilt nur für Einheiten mit Datumsspalte.
- Die Kurzrest-Regel (Z. 1374) greift nur bis 2 Wörter.
- «–» am Zeilenende gilt als Listenbeginn (`kopf_und_rumpf` Z. 1320).
- `teile_langen_titel` (Z. 1333) teilt Titel über 160 Zeichen am ersten «: », auch mitten im Zitat (D151217 10.1.62). Bibliografien enden so auf «…, in» (Gesamtscan: D10585, D176060).

### 6. Echte Signatur nicht erkannt – Einheit fehlt, Text im Darin der vorigen (17 PDFs, kritisch)

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D2323 | 1 | V.J.c.5.:3. | eigene Einheit «Brotrechnungen für die Stadtarmenpflege», 1850-1861 | fehlt; Darin von :2 «V J. c.5.:3. Brotrechnungen …, 1850-1861» (Punkt fehlt im PDF) |
| D3672 | 35–39 | VII.389.:1.1.1000.–1.1.1140. | 141 Einheiten | fehlen; 138 Darin-Einträge bei 1.1.999. (Status OK, 100 %) |
| D442 | 6 | V.B.c.54.:30. | Einheit «30. “Swissair” Schweizerische Luftverkehrs AG» mit 30.1.–30.14. | fehlt; Darin von 29.3.; 30.1.–30.14. hängen ohne Parent am Bestand |

Weitere Fälle:
- D175996: 15 Einheiten fehlen, z. B. «IV.B.41.:12.–14.» mit Gedankenstrich, «IV.B.1.a)».
- D140955: :16. «2 Fotografien …».
- D3484: «639/640 div. O.», «622 a».
- D3472: «1939.37 a», «1938.46 – …».
- D71: III.S.1.
- D10575: 11.25. «Aug. A. Lemaître».

Vermutete Ursache in `lies_signatur` (Z. 625 ff.):
- Vollsignaturen werden nur zusammengesetzt, wenn das erste Wort auf `[IVX]{1,4}\.` passt (Z. 638). «V J.» fällt durch, und «III.S. 1.» scheitert, weil das erste Wort schon der Bestand ist.
- Bereiche werden nur mit «-» erkannt, nicht mit «–»; Formen «a)» gibt es nicht (Z. 645).
- `DEZIMAL_RE` (Z. 489) erlaubt höchstens 3 Ziffern je Stufe.
- Der Rest nach der Nummer muss gross beginnen oder mit „«"( (Z. 686). Das typografische “, eine Ziffer, «div.» oder ein Kleinbuchstabe fallen durch.
- Folgt ein Monatsname, wird die Nummer verworfen (Z. 683). Das trifft den Vornamen «August».
- Im Modus dezimal gilt eine einteilige, nicht fette Nummer nur als hauptnr+1 (Z. 695). Sprünge 12→20 fallen durch (D3063).
- «Jahr.Nummer» mit Zusatz wird nicht erkannt (Z. 657).

Es gibt keinen Prüfhinweis dafür. Vorschlag: Einen Darin-Eintrag, der mit einer Signatur beginnt, als «mögliche übersehene Einheit» melden.

### 7. Zeitraum aus falscher Quelle (14 PDFs, mittel)

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D1739 | 3 | V.G.c.105.:10 | 1872–1932 (Spalte «Jahr») | «= 1492» (Allg. Nr.); 21 von 28 Zeiträumen falsch |
| D2641 | 3 | V.L.197.:40 | = 1971 (Erscheinungsjahr) | 1971–2000 (Jahr aus dem Werktitel) |
| D3589 | 3 | VII.359.:4. (Sachs, Ausgewählte dramatische Werke) | undatiert | «= 1916» (vom ersten Buch der Schachtel geerbt) neben Anm. «undatiert» (59×) |

Weitere Fälle:
- Lebensdaten als Laufzeit: D3077 :10. 1809–1889.
- Schlussvermerk als Datum: D406 bis 29.11.2012, D140955 bis 15.07.2013.
- Inhaltsjahre als Zeitraum: D10575 11.32. 1830–1851, D176367 1.1.1. 1798–2021.

Vermutete Ursache:
- `zeitraum_aus_titel` (Z. 1745 ff., Z. 1785) vereinigt alle Titeljahre; `jahre_im_text` (Z. 404) nimmt alle Jahreszahlen.
- `PERSON_RE` (Z. 233) erkennt Lebensdaten nur in Klammern.
- `JAHR` (Z. 215, 1200–2049) nimmt blosse Nummern in der rechten Spalte als Jahr.
- `ergaenze_zeitraeume` (Z. 1847) vererbt den Zeitraum, ohne `e.undatiert` zu prüfen.
- Gesamtscan: In Locher C.a. (D3482) werden vierstellige Schachtelnummern ≥ 1200 als Jahr gelesen. 353 Einheiten haben dort «von = 1348» o. Ä. und keine Schachtel. Ursache: `trenne_spalten` akzeptiert als Schachtel nur `\d{1,3}`.

### 8. Zahl oder Marke am Zeilenanfang als Signatur gelesen – erfundene Einheit (13 PDFs, kritisch)

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D176151 | 13 | VII.371.:25. | keine Einheit: Zwischenüberschrift «25 Jahre der Zunft Oberstrass 1925 – 1950» unter 12. | Einheit :25. «Jahre der Zunft Oberstrass»; danach werden 13.–16. verworfen, 27 Einheiten hängen ohne Parent |
| D3067 | 5 | VII.191.:1. | Darin-Eintrag «1 Verzeichnis 1780» | Signatur VII.191.:1. (Mengenangabe); insgesamt 30 solche Signaturen |
| D2990 | 1 | VII.161.:B 1 | Fortsetzungszeile «B 1 bis B 23 …» von Nr. 1 | Einheit «B 1» (zweimal); die echte Nr. 2. wird «VII.161.:B.1.2.» |

Weitere Fälle:
- D3060: Listenmarken «a) I 27 Asper Johannes» werden zu allen 8 Signaturen.
- D3077: «1.–5. Heft» werden 5 Einheiten.
- D10575: Bandnummern «16», «17».
- D2872: Schlussvermerk als Teil.
- Gesamtscan: D2743 «2 Listen …», D2901 «2 Schreiben …», D141024 «2 Tonbandkassetten», D2589 «9 Stadträte».

Vermutete Ursache:
- `_folgt` (Z. 562) akzeptiert jede Zahl bis «letzte + 6».
- Mehrteilige Nummern und «Buchstabe + Nr.» werden ohne Folge- oder Einrückungsprüfung übernommen (Z. 685 ff., Z. 714).
- `KLEIN_RE` (Z. 739) gilt auch für Listenmarken im Darin.
- Fett genügt für eine Hauptnummer (Z. 695).
- Alles links von 115 bzw. 130 pt zählt als Signaturspalte (Z. 67 f.).

Vorschlag: Die x-Position der echten Signaturen lernen und Zeilen verwerfen, die eingerückt sind, eine Mengeneinheit tragen («1 Verzeichnis», «2 Bände», «1 Filmrolle») oder die Folge sprengen.

### 9. Gliederungsebene oder Überschrift nicht erkannt – Hierarchie falsch (11 PDFs, kritisch)

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D3089 | 5 | VII.197.:I.1. | VII.197.:II.1. «ALLGEMEINE KORRESPONDENZ» | Teil von VII.197.:I.1. «STATUTEN»; die Gruppen II.–X. fehlen ganz |
| D141005 | 2 | VII.380.:2. | Hauptgruppe 2 «Orden Honorary Officer …» auf Ebene 1 | Unterpunkt 1.2 «Dankesbrief an das EPD …» als :2.; die Hauptgruppe hängt darunter (40 Hierarchie-Funde) |
| D175997 | 8 | IV.C.201.:1.–:31. | unter der Gruppe «Privatrechtliche Stiftungen (IV.C.201.)» | 31 Einheiten ohne Parent am Bestand; die Überschrift steht im Darin von IV.C.184. |

Weitere Fälle:
- D3018: Abschnitte 01–09 mit neu beginnender Zählung werden zu «Teilen» derselben Signatur; 55 Übersichtszeilen werden Knoten.
- D3038, D3060: Ein Schachtel-Teil hängt an der zuletzt offenen Untereinheit.
- D149634: Die Spalte «Ebene» ist bei Bereichssignaturen 1 statt 2; die Parent-ID stimmt (Muster M18).

Vermutete Ursache:
- `lies_signatur` (Z. 726) verwirft eine römische Zahl vor einem GROSSWORT («II. KORRESPONDENZ»); `baue_vorkommen` (Z. 994) sortiert die Zeile dann als Überschrift aus.
- «I)», «A)» passen nicht auf `ROEMISCH_RE`/`GROSS_RE` (Z. 491 f.).
- Die Einrückung (x 71 / x 110) wird nicht ausgewertet.
- Überschriften ohne Signatur werden nicht zu Elterneinheiten.
- `inhalt_beginnt` (Z. 947) nimmt immer den zuletzt offenen Pfad.
- `Einheit.tiefe` (Z. 1303) = Länge des Signaturpfads, unabhängig vom Parent aus `bereiche`.

### 10. Datumsformat nicht erkannt (10 PDFs, mittel)

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D2641 | 6 | V.L.197.:81 | ca. 1960er Jahre (Anm.) | «Genau 1960», Anm. «ca. 1960; undatiert» (14×) |
| D860 | 2 | V.C.c.75.:106 | 1987–1988 («Jahrgang 1987 - 88») | «= 1987» (7 Endjahre falsch) |
| D3063 | 8 | VII.190.:3.6. | 02.1934–09.1936 | kein Zeitraum (MM.JJJJ nicht erkannt), Einträge verschmolzen |

Weitere Fälle:
- «1966 ff.» → «Genau» ohne Anmerkung (D176367, D537).
- «um 1817» → «Genau 1817», «um» bleibt im Titel (D2872).
- «o.J. (1889)» → nur «undatiert» (D10575).
- Vorname «August»/«Aug.» als Monat gelesen (D141005, D406, D10575).

Vermutete Ursache:
- `PUNKT_RE`/`finde_zeitraeume` (Z. 216 ff., 329 ff.) kennen weder Jahrzehnte noch «-NN» noch «ff.» noch «MM.JJJJ-MM.JJJJ».
- `MONAT_WORT_RE` (Z. 214) wird ohne Kontext angewandt (`trenne_spalten` Z. 462 ff., `lies_signatur` Z. 683).
- Steht der Vorsatz «um»/«nach» am Titelende und das Jahr in der Datumsspalte, findet `finde_zeitraeume` (Vorsatzprüfung mit `VORSATZ_RE`, Z. 229/360) ihn nicht. «um» bleibt dann im Titel, und der Zeitraum wird «Genau» ohne «ca.».

### Sondermuster (Rang 12, aber am folgenreichsten): Verzeichnistext als Vorspann, Schlussvermerk oder Kopfzeile verworfen (7 PDFs, kritisch)

Text des Verzeichnisses wird als nicht zu importierend eingestuft. Er steht dann nur im Blatt «Vollständigkeit», und «Text erfasst» zählt ihn nicht.

| PDF | Seite | Signatur | Soll | Ist |
|---|---|---|---|---|
| D414 | 1 | V.B.c.34.:1–:5 | Schachtelliste «Schachtel 1: Generalverkehrsplan Zürich / Gutachten Pitath/Feuchtinger 1954 …» bis Schachtel 5 | fehlt ganz («Text vor der ersten Signatur»); nur Nr. 5 hängt als Schachtel an I. |
| D3067 | 4 | VII.191.:I. | «I) URKUNDEN – Ordnung über die Verwaltung … Anno 1758 …, Schachtel 1» | fehlt |
| D2990 | 2 | VII.161.:2. | Fortsetzung von 2. (4 Einträge) im Darin | als Schlussvermerk nur im Blatt «Info» |

Weitere Fälle:
- D141005 2.2 «2. August Hoffmeister …»: als Schlussvermerk verloren.
- D10575 «1675»: als Fusszeile verworfen.
- D1739: Zwischenüberschriften verworfen.
- D3018 «3.1. Neubau Tonwarenfabrik»: als Übersichtszeile gelöscht.
- Gesamtscan: Abschnitt 6.

Vermutete Ursache:
- `finde_detailbeginn` (Z. 2491–2512) beginnt ohne Überschrift «Detailverzeichnis» bei der **letzten** Nennung der ersten Signatur. Jede spätere «1» verschiebt den Start nach hinten: Mengenangaben «1 Filmrolle», Fortsetzungszeilen «1. März“, Zürich 1927» oder «1 Uhr aufgeboten …», neu beginnende Zählungen.
- Steht «Detailverzeichnis» über dem Inhaltsverzeichnis, wird das Inhaltsverzeichnis importiert (D10575: 15 Gruppen mit Seitenzahl im Titel).
- `baue_vorkommen` (Z. 991): Alles vor der ersten erkannten Signatur ist «Vorlauf». Der Rückfall auf eine Schachtelliste greift erst bei über 50 % Vorlauf (Z. 2573).
- Die Schlussregel (Z. 998 ff.) wertet langen Text nach einem Seitenwechsel als Schlussvermerk.
- `pruefe_vollstaendigkeit` zählt Vorspann, «Text vor der ersten Signatur» und Schlussvermerke nicht mit.

Vorschläge:
- Start bei der *ersten* Nennung der ersten Signatur nach dem Inhaltsverzeichnis, bzw. bei der Nennung mit der längsten geordneten Folge danach.
- Status «Prüfen», wenn der Vorspann mehr als 2 Seiten oder 20 % der Seiten umfasst oder wenn «Signaturen nur im Vorspann» nicht leer ist.
- Den Vorspann im Wortabgleich ausweisen.

## 5. Weitere Muster

- **M16 Zerrissene Wörter** (7 PDFs, gering; Gesamtscan: mindestens 565 Stellen in 37 PDFs), z. B. «Liegenschaftenverwaltu ng», «D etailverzeichnis», «1960-1 991» (D2366), «S iehe» (D176151), «Züri ch» (D3589). Es gibt zwei belegte Ursachen:
  - (a) Schriftwechsel mitten im Wort. `extract_words(extra_attrs=["fontname","size"])` (Z. 146) trennt dort, z. B. «S» normal / «iehe» kursiv.
  - (b) Die Zeichen stehen im PDF-Inhaltsstrom nicht in Leserichtung. In D2366 stehen «ng,» an Stromposition 61–64, «…altu» an 834–836, bei gleicher Schrift, gleicher Höhe und 0,0 pt Abstand.
  - Fix für beide: In `lese_zeilen` Wörter mit Abstand < 0,5 pt zu einem Wort verschmelzen. Schon heute folgt daraus ein Strukturfehler, weil `DETAIL_RE` «D etailverzeichnis» nicht erkennt.
- **M11 Schachtel-Nr. falsch oder fehlt** (5 PDFs, 125 Stellen):
  - «Schachteln 3 und 4», «Schachteln 7 bis 12», «Mappe» und «Schachtel 20l» passen nicht auf `SCHACHTEL_RE` (Z. 495). Die alte Nummer läuft weiter (D2872: ab 5. alles «2»).
  - Eine Schachtel in der rechten Spalte einer Einheitszeile wird nicht an die folgenden Einheiten weitergegeben (D3063).
  - Bei flacher Zählung gilt «Schachtel n» nur für die erste Einheit (D3077, `bereich` Z. 879).
  - Die letzte Schachtelmarke am Dateiende geht verloren (D3038 «Schachtel 400»).
  - Die Schachtel-Zuordnungsliste am Schluss wird nicht angewandt (D2872 S. 6).
- **M15 Umfang nicht erkannt** (4 PDFs): «(2 Schachteln)», «(1 Band)» in Klammern stehen im Titel. Grund: `UMFANG_RE` (Z. 432) verlangt die Zahl am Zeilenanfang (D442 14×, D3398, D175997). Umgekehrt wird «1 Mäppchen» eines Darin-Eintrags zum Umfang der Einheit (D176367).
- **M13 Teile: Titel vom Nachbarteil, eigener Titel im Darin** (3 PDFs; Gesamtscan: bis zu 1816 Teile in 46 PDFs, davon 590 in D3482, 426 in D3466, 103 in D3468, 322 in D151210).
  - Ein Teil mit mehrzeiligem Kopf gilt als «Liste» (`verarbeite` Z. 1391). Sein eigener Titel kommt ins Darin, und `ergaenze_titel` (Z. 1904) setzt «<Titel des ersten Teils>, Teil n».
  - Beispiele: D3482 1946.2 «Zürich Stampfenbachstrasse 114 / Umbau» heisst «Zürich Kirchgemeinde Aussersihl, Teil 2». D3484 S. 15 VII.308.D.a.:414. «Engi Vereinigte Webereien …» heisst «St. Moritz Haus Manin-Suot …, Teil 2».
  - Bei Locher ist jede Zeile ein eigenes Objekt.
- **M14 Mappen/Schachteln: Titel aus der Überschrift vor der Marke** (D1739, D2329):
  - `baue_behaelter` (Z. 1465 ff.) nimmt die letzte Überschrift *vor* der Marke. Gilt die Kopfzeile aber für die folgende Schachtel, trägt jede Schachtel die Sachgruppe der vorigen samt Tabellenkopf («Flüsse und Bäche Jahr Fach Mappe Allg. Nr., Schachtel 17» statt «Friedhöfe»).
  - In D2329 zählt die zweite Zeile des Bestandstitels als Überschrift.
- **Gliederungstyp falsch erkannt** (Gruppe 5):
  - D3060 ist eine Schachtelliste, D3472 eine flache Jahr.Nummer-Liste («römisch/Buchstaben»), D2990 eine Liste 1./2. («Buchstabe+Nr.»).
  - D4039 ist eine Liste nach 47 rechtsbündigen Schachteln. `baue_behaelter` sucht Marken nur bei x0 ≤ 160 (Z. 1457) und macht daraus «ohne Signaturen».
- **M18 Spalte «Ebene»** (D149634, 99 Einheiten): Bei Bereichssignaturen («VII.3.:6-16» > «VII.3.:6») passt die Spalte «Ebene» nicht zur Parent-ID.

## 6. Zusatzfunde aus dem Gesamtscan (ausserhalb der Stichprobe)

Parallel zur Stichprobe habe ich alle 712 Excel-Dateien automatisch gegen den PDF-Text abgeglichen (Skripte im Scratchpad, Heuristiken). Die Verdachtsfälle habe ich am PDF von Hand bestätigt. Die einzelnen Funde stehen in `zusatzfunde_gesamtscan.csv`; sie sind nicht in `funde.csv` und nicht in den Zählungen oben enthalten. Alle betroffenen PDFs zeigen «Text erfasst 100 %».

**Verzeichnisteile verworfen bzw. Mengenangabe als Signatur (kritisch):**

| PDF | Bestand | Status | Befund |
|---|---|---|---|
| D150689 | VII.277. | Prüfen | 4933 Zeilen auf S. 1–141 (von 201) als Vorspann verworfen; Import beginnt bei «VII.277.:1. Photographie (6) …» |
| D10675 | V.F.c.28. | Prüfen | S. 1–21 (von 22) verworfen; Registraturplan-Codes 010, 020 … nicht als Signatur erkannt |
| D3530 | VII.327. | Prüfen | S. 1–31 (von 35) verworfen; Import beginnt bei der neu beginnenden Zählung «1 Herren von Dietikon.» |
| D2937 | VII.140. | Prüfen | S. 1–18 (von 30) verworfen; Abschnitte A.–N. mit je neu beginnender Zählung → falsche Teile |
| D3828 | VII.76. | OK | S. 1–17 (von 18) verworfen; von 12+ Einheiten bleiben 4 |
| D3316 | VII.255. | OK | S. 1–12 verworfen; einzige Einheit aus «1 Schachtel Grossformat: …» |
| D8943 | VII.481. | OK | Abschnitte 1.–7. verworfen; einzige Einheit aus «1 Filmrolle (Durchmesser 7 cm)» |
| D3021 | VII.175. | OK | A)–E) verworfen; einzige Einheit aus «1 Karikatur Kopf Gretlers von Naef» |
| D2951 | VII.146. | Prüfen | Briefe 1.1. ff. (S. 1–11) verworfen; Start bei Fortsetzungszeile «1 Uhr aufgeboten worden …» |
| D2935 | VII.14. | Prüfen | Abschnitte 1.–3. (S. 3–12) verworfen; Start bei «1 Faszikel je Sitzung).» |
| D460 | V.B.c.63. | OK | 1.1.–1.5. verworfen; Start bei Fortsetzungszeile «1. März“, Zürich 1927» (Einheit 1. heisst «März“, Zürich») |
| D3684 | VII.394. | OK | Einheiten 1.–3. verworfen, nur 4. und 5. im Excel |
| D2708 | V.L.45. | Prüfen | erste Gruppe ohne «1.» (rund 25 Einträge) nicht importiert; Excel beginnt mit 2. |
| D2729 | V.L.68. | Prüfen | wie D2708 (rund 22 Einträge) |
| D819 | V.C.c.26. | OK | «V.C. c.25.:1», «V.C. c.25.:2.» (Tippfehler im PDF) verworfen; nur 1 von 3 Einheiten |
| D2743 | V.L.8. | OK | «2 Listen mit diversen Einträgen» als Einheit :2.; die übrigen 4 Einträge fehlen |
| D2901 | VII.124. | Prüfen | «2 Schreiben von Reichstags-Abgeordneter A. Bebel …» als Einheit :2.; rund 60 Zeilen davor verworfen |
| D3105 | VII.2. | OK | Unterpunkte «2. Entwürfe …, 3. Zirkulare, 4. Strassennamen» als Einheiten, Schachtel-1-Inhalt davor verworfen; «Stand: 05.07.1994» als Zeitraum |
| D141024 | VII.487. | Prüfen | Tabelle Medium/Inhalt: «2 Tonbandkassetten», «1 Notizheft» als Signaturen 2, 1, 1 … |
| D2589 | V.L.136.b. | Prüfen | Überschrift «9 Stadträte» als Einheit 9 |
| D3482 | VII.308.C.a. | Prüfen | vierstellige Schachtel als Jahr (353 Einheiten); ca. 590 Teile mit fremdem Titel |

**Automatisch gezählte Muster über alle 712 Dateien** (Untergrenzen bzw. Grössenordnungen, Heuristik):

| Muster | Stellen | PDFs | Methode |
|---|---:|---:|---|
| Zerrissene Wörter | ≥ 565 | 37 | Wortpaar im Excel, das zusammen ein Wort des PDF-Texts ergibt |
| Datum der rechten Spalte mitten im Titel | 168 Bereiche + 139 Einzeljahre | ~40 | Titeljahr mit Text danach; im Layout-Text steht das Jahr nach ≥ 3 Leerzeichen am Zeilenende |
| «o. D.», «undatiert» am Titelende | 331 | 35 | Regex auf Titel |
| Datumsbereich am Titelende stehen geblieben | 284 | 42 | Regex; teils gewollt (Amtszeiten in Personentiteln, Bauzeiten IV.B.) |
| Teil mit übernommenem Titel, eigener Titel im Darin | ≤ 1816 | 46 | erster Darin-Eintrag steht im PDF auf der Signaturzeile; enthält gewollte Listen-Teile |
| Schachtelnummer ≥ 1200 als Jahr | 353 | 1 (D3482) | Einzeljahr weit vor Bestandsbeginn aus der Datumsspalte |
| Verzeichnisteile im Vorspann verworfen | – | ≥ 19 | Info «Vorspann (nicht importiert)», «Signaturen nur im Vorspann», Nummernzeilen ohne Excel-Einheit, von Hand bestätigt |

## 7. Was die eingebaute Prüfung nicht sieht

- **Der Wortabgleich ist blind für Verschiebungen.** Ein Wort gilt als gefunden, sobald es irgendwo in der Excel-Zeile der Einheit steht, der seine PDF-Zeile zugeordnet wurde. Steht eine übersehene Einheit im Darin der vorigen Einheit, ist alles «gefunden». Beispiele: D3672 mit 141 fehlenden Einheiten bei 100 %, D1739 bei 100 %.
- **Vorspann, «Text vor der ersten Signatur» und Schlussvermerke zählen nicht mit.** Gerade dort liegen die grössten Verluste (Abschnitt 6).
- **Viele «Lücken» im Blatt «Vollständigkeit» sind Fehlalarme.** Beispiele: Silbentrennung «No-vember», «Nr» aus «Schachtel Nr. 98» (37× in D860), «(ohne / Datum» über einen Umbruch (D2641, D537). Die Schicht A mit < 100 % hatte deshalb kaum mehr grobe Fehler (17 von 32) als die Zufallsschicht C (7 von 16).
- **Prüfhinweise decken nur einen kleinen Teil ab:** 131 von 897 (15 %) aller Fundzeilen, 74 von 194 (38 %) der kritischen.

Vorschläge für zusätzliche automatische Prüfungen:
- Vorspann-Anteil an den Seiten (Status «Prüfen» ab 20 %).
- Nummernzeilen im PDF, die weder Einheit noch Darin-Anfang wurden.
- Darin-Einträge, die mit einer Signatur beginnen.
- Jahre ausserhalb des Bestandszeitraums laut Katalog.
- Titel mit Jahr mitten im Text, wenn die Lücke unter 18 pt liegt.
- Mengenangaben als Signatur («1 Filmrolle»).

## 8. Offene Fragen an die Hauptsession

1. **Locher-Signaturen:** Das Vorwort von D.a. verlangt die Bestellung als «VII. 308. D.a. 190., Schachtel 1», F.a. und C.a. als «VII. 308. F.a.1933.1, Schachtel 1». Das Excel schreibt nach Konvention «VII.308.D.a.:190.» bzw. «VII.308.F.a.:1933.1». Das ist kein Fund, sollte aber bestätigt werden.
2. **Zeitraum aus «Jahr.Laufnummer»** übernehmen? D3472 hat 1663 von 1714 Einheiten ohne Zeitraum.
3. **Dossierlisten mit Spalte «Schachtel-Nr.»** «ohne Signaturen» (z. B. D2366, Schachtel 1–8): Bestandszeile wie bisher, oder Schachtel-Einheiten wie bei «Mappen/Schachteln»?
4. **Gliederungsüberschriften ohne Signatur** (z. B. «Privatrechtliche Stiftungen (IV.C.201.)», «3.» in D3432): Eigene Elterneinheit bilden, oder die Einheiten wie bisher an den Bestand hängen?
5. **Signatur-Tippfehler im PDF** («V J. c.5.:3.», «V.B. 439.», «V.C. c.25.:1» in V.C.c.26.): korrigieren, wörtlich übernehmen oder wenigstens als eigene Einheit mit Prüfhinweis führen? Heute gehen diese Einheiten verloren.
6. **Bestandszeile «ohne Signaturen»:** Die Übergeordnete Signatur ist die eigene (z. B. VII.435. unter VII.435.). Beim Import beachten.

## 9. Dateien

- `stichproben/bericht.md`: dieser Bericht.
- `stichproben/funde.csv`: 897 Fundzeilen der Stichprobe; Semikolon, UTF-8; Spalten `pdf;seite;signatur;feld;schwere;soll;ist;bemerkung`. Die Bemerkung beginnt mit dem Hauptmuster `[M01]`–`[M18]` und dem Muster der Gruppe. Am Ende stehen gegebenenfalls «betrifft n Fälle» (Sammelzeile), «Skript meldet es in den Prüfhinweisen» und eine Schwere-Anpassung.
- `stichproben/zusatzfunde_gesamtscan.csv`: 22 von Hand bestätigte Funde ausserhalb der Stichprobe, gleiches Format.
- `stichproben/roh/gruppe_1…6_funde.csv` und `…_urteile.md`: Rohergebnisse der sechs Prüfgruppen, mit den zusätzlichen Spalten `muster;anzahl;hinweis`, den ausführlichen Urteilen und den Mustern je Gruppe.
- `stichproben/methode/`:
  - `ANLEITUNG.md`: Prüfanleitung;
  - `stichprobe.py`, `seitenwahl.py`: Ziehung mit Startwert 20261119;
  - `stichprobe.csv`, `pruefseiten.csv`;
  - `dump_excel.py`, `woerter.py`: Werkzeuge;
  - `muster_map.py`: Zuordnung der Muster.
