# Nachprüfung der Stichproben-Funde am neuen Excel-Stand

Stand der Nachprüfung: `findmittel_excel/` vom 19.11.2026, 23:05. Die Excel-Dateien und das Skript sind als Schnappschuss gesichert (Skript sha256 `22ab56f8…`, 3681 Zeilen; Kopie unter `/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/neu/findmittel_zu_scope.py`). Zeilennummern beziehen sich auf diesen Stand; das Skript im Projekt hat sich seither schon wieder geändert.
Verglichen wird mit dem Stand der ersten Runde (21:02). Alle Urteile sind am PDF belegt. Die Änderungsliste der Hauptsession wurde nicht benutzt.

## Kurzfazit

- **Von 464 nachgeprüften Fundzeilen sind 277 behoben (60 %),** 54 teilweise, 132 offen und 1 entfällt.
- **Kritische Funde:** 131 von 194 behoben (68 %), 26 teilweise, 37 offen. Fast alles Offene steckt in vier PDFs:
  - D3018: 20 offen;
  - D3067: 11 offen oder teilweise;
  - D10575: 10 offen;
  - D176151: 7 offen oder teilweise.
- **Zusatzfunde (Vorspann-Verluste):** In 21 von 22 Fällen ist der verlorene Teil jetzt importiert. 13 davon sind ganz richtig, bei 8 stimmen Signatur, Hierarchie oder Titel noch nicht. Offen bleibt D2589.
- **Mittlere Muster (Stichprobe, 248 Zeilen):** 133 behoben, 94 offen. Am wenigsten hat sich bei M06 (Spaltendatum im Titel), M09 (Zeitraumquelle), M11 (Schachtel) und M12 (Datumsformat) getan; dort ist rund die Hälfte offen.
- **Neue Fehler: 97 Zeilen, davon 38 kritisch.**
  - 48 sind Regressionen in Einheiten, die im alten Stand richtig waren (22 kritisch).
  - 34 liegen in den neu importierten Teilen der Zusatz-PDFs.
  - 15 sind alte Fehler, die in Runde 1 übersehen wurden.
  - Berichtigt am 20.11.2026: Zuerst standen hier 53 / 38 / 6, weil die Kennzeichnung «Schon im alten Stand» nur in Kleinschreibung gezählt wurde.
- **Die Regressionen gehen vor allem auf fünf neue Regeln zurück** (Abschnitt «Neue Fehler»). Wichtig: Die Schlussvermerk-Regel verschluckt jetzt Verzeichnistext, und die Buchstaben «A. Übersicht / B. Detailverzeichnis» machen alle Signaturen eines PDFs falsch. Die Selbstprüfung des Skripts zeigt beides nicht an, weil Schlussvermerke nicht in «Text erfasst» zählen und eine falsche Signatur kein Wort verliert.

## Methode

1. **Auswahl** (`methode/np_auswahl.py`, Startwert 20261119, Ergebnis `methode/np_pruefliste.csv`):
   - alle 194 kritischen Zeilen aus `funde.csv` und alle 22 Zusatzfunde;
   - aus den mittleren Mustern M05, M06, M07, M09, M11, M12 und M14 je PDF und Muster höchstens 5 Zeilen, zuerst solche auf den Prüfseiten aus `methode/pruefseiten.csv`. Ergebnis: 248 Zeilen, davon 207 auf Prüfseiten.
2. **Prüfung** durch vier Agenten nach `methode/ANLEITUNG_NACHPRUEFUNG.md`. Es gelten die Konventionen aus `ANLEITUNG.md` und die sechs Entscheide der Hauptsession; die Entscheide wurden nicht als Fund gewertet. Status je Zeile:
   - **behoben**, **teilweise** oder **offen**;
   - **entfällt**, wenn ein Entscheid den Fund zur Konvention macht oder der Fund falsch war. Das kam einmal vor: F842, D3206, Entscheid 6.
3. **Neue Fehler** auf den Prüfseiten: Grundlage ist ein Einheitenvergleich alt ↔ neu (`methode/diff_stand.py`). Jede geänderte, entfernte oder neue Einheit wurde am PDF geprüft; unveränderte Einheiten waren schon in Runde 1 geprüft. Bei den Zusatz-PDFs kam je eine Zufallsseite im neu importierten Bereich dazu.
4. **Gesamtvergleich aller 715 Excel** (automatisch): Einheitenzahl, Signaturmengen und Info-Kennzahlen (Schlussvermerke, Vorspann, Wörter). Auffällige Fälle habe ich am PDF geprüft. 8 Regressionen ausserhalb der Stichprobe stehen als eigene Zeilen in der CSV (`roh/np_gruppe_0.csv`).
5. **Gegenprobe:** Rund 24 Agenten-Urteile habe ich selbst am PDF nachgesehen (u. a. D141005 S. 2, D3472 1938.46, D442 :30., D3018 02.5., D3067 II.B., D512 S. 62, D3684 S. 1). Alle wurden bestätigt, keines widerlegt.

## Ergebnis nach Auswahl

| Auswahl | behoben | teilweise | offen | entfällt | Zeilen |
|---|---:|---:|---:|---:|---:|
| kritische Funde (funde.csv) | 131 | 26 | 37 | 0 | 194 |
| Zusatzfunde Gesamtscan | 13 | 8 | 1 | 0 | 22 |
| mittlere Funde, Stichprobe | 133 | 20 | 94 | 1 | 248 |
| **Summe** | **277** | **54** | **132** | **1** | **464** |

| Neue Fehler | kritisch | mittel | gering | Zeilen |
|---|---:|---:|---:|---:|
| Regression (Einheit war im alten Stand richtig) | 22 | 25 | 1 | 48 |
| im neu importierten Bereich der Zusatz-PDFs | 10 | 23 | 1 | 34 |
| alter Fehler, in Runde 1 übersehen | 6 | 6 | 3 | 15 |
| **Summe** | **38** | **54** | **5** | **97** |

## Nach Hauptmuster

M08 und M10 waren nicht Teil der Stichprobe; sie kommen nur bei den neuen Fehlern vor.

| Hauptmuster | behoben | teilweise | offen | entfällt | neu | davon Regression |
|---|---:|---:|---:|---:|---:|---:|
| M01 Vorspann/Schlussvermerk verworfen | 16 | 10 | 2 |  | 5 (4 krit.) | 3 |
| M02 Echte Signatur nicht erkannt | 24 | 6 | 22 |  | 5 (5 krit.) | 1 |
| M03 Zahl/Marke als Signatur | 41 | 7 | 6 |  | 9 (9 krit.) | 3 |
| M04 Gliederungsebene nicht erkannt | 61 | 11 | 8 |  | 13 (13 krit.) | 10 |
| M05 Mehrzeilige Datumsspalte | 41 | 7 | 14 |  | 3 (1 krit.) | 2 |
| M06 Rechte Spalte nicht abgetrennt | 20 | 2 | 23 |  | 4 | 2 |
| M07 Fremdtext im Darin | 29 | 8 | 12 | 1 | 7 | 1 |
| M08 Zeilenumbruch falsch |  |  |  |  | 12 (1 krit.) | 6 |
| M09 Zeitraum aus falscher Quelle | 16 | 2 | 22 |  | 7 | 6 |
| M10 Darin falsch getrennt |  |  |  |  | 12 | 5 |
| M11 Schachtel-Nr. | 8 |  | 10 |  | 2 | 1 |
| M12 Datumsformat nicht erkannt | 12 | 1 | 13 |  | 5 | 1 |
| M13 Teile: Titel vom Nachbarteil | 1 |  |  |  |  |  |
| M14 Mappen/Schachteln: Titel aus Überschrift | 8 |  |  |  | 1 | 1 |
| M16 Zerrissene Wörter |  |  |  |  | 1 | 1 |
| M17 Kosmetik |  |  |  |  | 1 |  |
| M19 Sonstiges |  |  |  |  | 10 (5 krit.) | 5 |

## Nach PDF

Herkunft: Stichprobe = 50 PDFs der ersten Runde; Zusatz = Zusatzfunde des Gesamtscans; Gesamtvergleich = beim Vergleich alt ↔ neu gefunden.
Ganz behoben (alle Zeilen behoben): D1616, D175996, D2329, D2743 (Zusatz), D3038, D3398, D3432, D3472, D3482 (Zusatz), D819 (Zusatz), D860.

| PDF | Herkunft | behoben | teilweise | offen | entfällt | neu | kritisch offen/teilw. | neu kritisch |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| D3018 | Stichprobe | 1 | 1 | 22 |  |  | 20 |  |
| D3067 | Stichprobe | 21 | 20 |  |  | 12 | 11 | 8 |
| D176151 | Stichprobe | 4 | 5 | 4 |  | 5 | 7 | 4 |
| D10575 | Stichprobe | 3 |  | 17 |  | 1 | 10 |  |
| D10675 | Zusatz |  | 1 |  |  | 7 | 1 | 3 |
| D3060 | Stichprobe | 9 | 1 | 1 |  | 5 | 1 | 2 |
| D512 | Stichprobe | 4 | 1 | 2 |  | 3 |  | 3 |
| D150689 | Zusatz |  | 1 |  |  | 3 | 1 | 2 |
| D3828 | Zusatz |  | 1 |  |  | 3 | 1 | 2 |
| D3089 | Stichprobe | 16 | 1 | 5 |  | 3 | 1 | 1 |
| D141005 | Stichprobe | 53 | 2 | 3 |  | 3 | 2 |  |
| D3672 | Stichprobe | 3 | 1 | 3 |  | 2 | 2 |  |
| D1739 | Stichprobe | 12 | 2 | 1 |  |  | 2 |  |
| D3530 | Zusatz |  | 1 |  |  | 2 | 1 | 1 |
| D2992 | Gesamtvergleich |  |  |  |  | 2 |  | 2 |
| D3063 | Stichprobe | 9 | 2 | 6 |  | 5 | 1 |  |
| D3484 | Stichprobe | 5 | 2 | 2 |  |  | 1 |  |
| D2589 | Zusatz |  |  | 1 |  | 2 | 1 |  |
| D414 | Stichprobe | 5 |  | 3 |  |  | 1 |  |
| D2708 | Zusatz |  | 1 |  |  | 1 | 1 |  |
| D2839 | Stichprobe | 13 |  | 1 |  | 1 | 1 |  |
| D2951 | Zusatz | 1 |  |  |  | 2 |  | 1 |
| D2990 | Stichprobe | 4 | 1 |  |  | 1 | 1 |  |
| D3684 | Zusatz | 1 |  |  |  | 2 |  | 1 |
| D10684 | Gesamtvergleich |  |  |  |  | 1 |  | 1 |
| D140969 | Gesamtvergleich |  |  |  |  | 1 |  | 1 |
| D141024 | Zusatz |  | 1 |  |  |  | 1 |  |
| D152817 | Gesamtvergleich |  |  |  |  | 1 |  | 1 |
| D1924 | Gesamtvergleich |  |  |  |  | 1 |  | 1 |
| D2323 | Stichprobe | 1 | 1 |  |  |  | 1 |  |
| D2729 | Zusatz |  | 1 |  |  |  | 1 |  |
| D3105 | Zusatz |  | 1 |  |  |  | 1 |  |
| D3429 | Gesamtvergleich |  |  |  |  | 1 |  | 1 |
| D3466 | Gesamtvergleich |  |  |  |  | 1 |  | 1 |
| D71 | Stichprobe |  | 1 |  |  |  | 1 |  |
| D73 | Gesamtvergleich |  |  |  |  | 1 |  | 1 |
| D8943 | Zusatz | 1 |  |  |  | 1 |  | 1 |
| D176367 | Stichprobe |  |  | 13 |  |  |  |  |
| D3077 | Stichprobe | 5 |  | 11 |  |  |  |  |
| D140955 | Stichprobe | 5 |  | 8 |  |  |  |  |
| D537 | Stichprobe |  | 1 | 3 |  | 3 |  |  |
| D3316 | Zusatz | 1 |  |  |  | 5 |  |  |
| D3589 | Stichprobe | 9 |  | 3 |  | 1 |  |  |
| D406 | Stichprobe | 2 |  | 4 |  |  |  |  |
| D150296 | Stichprobe | 3 | 1 | 1 |  | 1 |  |  |
| D175994 | Stichprobe | 4 |  | 2 |  | 1 |  |  |
| D2641 | Stichprobe | 5 |  | 3 |  |  |  |  |
| D2937 | Zusatz | 1 |  |  |  | 3 |  |  |
| D3021 | Zusatz | 1 |  |  |  | 3 |  |  |
| D149634 | Stichprobe | 1 |  | 1 |  | 1 |  |  |
| D151217 | Stichprobe |  |  | 2 |  |  |  |  |
| D2872 | Stichprobe | 8 |  | 2 |  |  |  |  |
| D2935 | Zusatz | 1 |  |  |  | 2 |  |  |
| D4039 | Stichprobe | 2 |  |  |  | 2 |  |  |
| D4054 | Stichprobe | 4 | 1 | 1 |  |  |  |  |
| D442 | Stichprobe | 7 |  | 2 |  |  |  |  |
| D175997 | Stichprobe | 3 | 1 |  |  |  |  |  |
| D2352 | Stichprobe |  |  | 1 |  |  |  |  |
| D2366 | Stichprobe | 2 |  | 1 |  |  |  |  |
| D2901 | Zusatz | 1 |  |  |  | 1 |  |  |
| D3206 | Stichprobe |  | 1 |  | 1 |  |  |  |
| D3533 | Stichprobe | 2 |  | 1 |  |  |  |  |
| D3795 | Stichprobe |  |  | 1 |  |  |  |  |
| D4007 | Stichprobe |  |  | 1 |  |  |  |  |
| D460 | Zusatz | 1 |  |  |  | 1 |  |  |

## Neue Fehler (Regressionen), nach Ursache

1. **Schlussvermerk-Regel verschluckt Verzeichnistext (M01, kritisch).**
   - Ursache: `SCHLUSS_RE` (Z. 718–723) prüft jetzt ohne Rücksicht auf Gross- und Kleinschreibung (`re.I`). Deshalb gilt auch die Fortsetzungszeile «bearbeitet von …» als Schlussvermerk. Danach nimmt `im_schluss` (Z. 1456–1459) alle linksbündigen Zeilen bis zur nächsten Einheit mit.
   - D3089 S. 22–23 und 32–33: rund 105 Zeilen bzw. 85 Einträge der Textbücherliste stehen nur noch im Blatt Info, z. B. «"Der Biberpelz" von Gerhart Hauptmann 1931 Berlin».
   - D2992 S. 3: «… für den Film / bearbeitet von Otto Ritter.»
   - D152817 S. 1: «… bearbeitet von Dr. Claudia Caduff, in VI.SB.A.1.»
   - D8943 S. 8: Bei VII.481.:7.2. fehlen der Rest des Kochbuch-Eintrags und das Jahr 1928.
   - Kein Fund sind die neuen Schlussvermerke in D3826 (Diplomliste «Bibliothek Nc») und D152781 (Bibliografie). Das sind Anhänge ausserhalb des Bestands.
2. **«A. Übersicht» / «B. Detailverzeichnis» werden als Gliederungsebene gelesen (M04/M03, kritisch).**
   - Ursache laut Gruppe 3: `lerne_buchstabenabschnitte` (Z. 1132 ff.) zusammen mit Regel 1a in `lies_signatur` (Z. 968–973).
   - Folge: Alle Detail-Signaturen bekommen ein «B.» vorangestellt, z. B. D512 S. 62 «V.B.c.70.:B.1.42.» statt «V.B.c.70.:1.42.». Dazu kommt die Übersicht als doppelte Einheiten «:A.», «:A.1.» usw.
   - Betroffen: D512 (64 Signaturen, 6 doppelte Einheiten) sowie D2992, D10684 und D3429 aus dem Gesamtvergleich. Im alten Stand waren die Signaturen richtig.
3. **Doppelmarke «II) B)» – nur die erste Marke wird gelesen (M04, kritisch, D3067).**
   - Ursache: `lies_signatur` (Z. 1076–1084) liest nur «II)». Die wiederholte Signatur hängt danach nach der Teile-Regel unter der ersten Nennung.
   - Beispiele: «II) B) MITGLIEDERVERZEICHNISSE» ist ID 3 mit Signatur «VII.191.:II.», Parent «A) FAMILIENRÖDEL». Gleich bei III.B.–F., IV.B.–E. und IV.E.1.–3.
4. **Buchstabenabschnitte einer Bibliotheksliste werden oberste Ebene (M04/M03, kritisch, D176151).**
   - A.–D. stehen ohne Parent statt unter 14.; 67 Buchnummern sind Einheiten geworden.
   - Die Archivnummern 15.1.–16.20. heissen jetzt «VII.371.:D.15.1.» … und hängen unter D.
5. **Zweite und dritte Datumszeile geht verloren (M05, kritisch, D512).**
   - Ursache: `baue_vorkommen` (Z. 1534–1541) hängt sie als `weitere_daten` an die Einheit statt an den Darin-Eintrag.
   - Beispiel S. 62: «Schluss-Akkord 12./ 19./ 26. Okt./ 2. Nov. 1998» – «2. Nov. 1998» fehlt im ganzen Excel. Insgesamt fehlen 70 Datumsangaben in 28 Saisons.
6. **Weitere Regressionen (mittel):**
   - **Zeilen verschmolzen.** Der rechte Rand wird für Einheiten mit Datums- oder Umfangsspalte auf die Textspalte verengt (`verarbeite` Z. 1932–1933, `rand_der_textspalte` Z. 2293). Getrennte Zeilen laufen dadurch zusammen: D2839 S. 2 VII.103.:1.1. (Beschreibung im Titel), D175994 S. 5 IV.A.65., D141005 VII.380.:6., D3063 VII.190.:51.
   - **Titeldatum statt Spaltendatum.** Ein Datum im Titel ersetzt den Zeitraum der Datumsspalte (`zeitraum_aus_titel` Z. 2513–2514). Beispiel D141005 S. 3 VII.380.:2.5.: Genau 31.01.1952 statt 22.–23.01.1952.
   - **Schachtel-Zeitraum aus Titel und Darin geschätzt** (`ergaenze_zeitraeume` Z. 2592–2600). Beispiel D537 V.B.c.9.:15: 1831–1946 statt 1843–1846. Betroffen sind 21 Schachteln; bei 15 steht das Datum wieder im Titel.
   - **Fehlende Teil-Nr.** Teile mit eigenem Titel bekommen keine Teil-Nr. mehr (`ergaenze_titel` Z. 2668–2670). Beispiel D150296: 22 Einheiten «VII.298.:3.1.2.» ohne Teil.
   - **Nummer als Jahr.** «o. J.» lässt jetzt die Schätzung aus dem Darin zu (`ergaenze_zeitraeume` Z. 2583–2590), und `NICHT_JAHR_VOR_RE` (Z. 320) schützt nur die erste Zahl nach «Nr.». Beispiel D10575 S. 8 VII.494.:2.1.: 1461–1889 aus «Nr. 1453 (…), 1461 (…)».
7. **Einzelfälle aus dem Gesamtvergleich (kritisch):**
   - D1924: Ab Schachtel 10 (zweistellig) wird jede Schachtel eine Serie mit dem Titel der ersten Zeile, und jede weitere Zeile wird ein eigenes Dossier (1513 erfundene Einheiten). Schachtel 1–9 sind richtig nach Entscheid 3 aufgebaut.
   - D73 S. 2: Die Lagerungsangabe «Schachtel 1 Filme Nummern 448 bis 463» … wird zu drei Schachtel-Einheiten, und die Gemeinden 1.–3. hängen falsch darunter.
   - D140969 S. 4: Die Einheit VII.80.:44. «Pläne Landgasthof» ist weggefallen; der Text steht im Darin von 35.

**Fehler in den neu importierten Bereichen der Zusatz-PDFs** (34 Zeilen, 10 kritisch):
- Übersichtszeilen werden erfundene Serie-Ebenen (D150689, etwa 20 Fälle; `baue_einheiten` Z. 2307).
- Abschnittsweise neu beginnende Zählung wird ohne Abschnitt gelesen (D3828 S. 15, D3530 S. 31–34).
- Zahlen und Mengen werden zu Signaturen: D3684 «4 Kinder:», D2951 Tageszahlen, D10675 Fussnote «1», D150689 «1 Kartonmappe».
- D10675: Rund 70 Positionen (010–029, 600–624) stehen nur im Darin.

## Wichtigste offene Punkte (unverändert seit Runde 1)

1. **D3018:** Die Abschnitte 01–09 mit je neu beginnender Zählung werden nicht erkannt. Alle 20 kritischen Funde sind offen. Beispiel S. 33: «5.1. Imago AG» hängt unter «5. Patente»; der Teilbestand 03 fehlt, sein Inhalt steht im Darin von «Imago AG».
2. **D10575:** Das Inhaltsverzeichnis S. 7 wird weiter als Gliederung gelesen (`finde_detailbeginn` Z. 3293 ff.). Die echten Abschnitte 3.–15. stehen im Darin der jeweils vorigen Einheit; 10 kritische Funde sind offen.
3. **Entscheid 4** (Überschrift ohne Signatur als Prüfhinweis bei der folgenden Einheit) ist nur für fette Zwischentitel umgesetzt.
   - Überschriften in Grossbuchstaben werden ohne Hinweis verworfen oder bleiben im Darin der vorigen Einheit (`baue_vorkommen` Z. 1495–1497).
   - Beispiele: D3063 S. 12 «VERBANDSTAETIGKEIT/MILITÄRDIENST/ETC.» als erfundener Teil, D175994 S. 4, D175997 S. 3, D3589 S. 2.
   - Kritisch in D2839 S. 19: «4. NSDAP ¦ 27. Jan. 1965» fehlt weiter (F251).
4. **Entscheid 5** ist erst halb umgesetzt: In D2323 ist V.J.c.5.:3. jetzt eine eigene Einheit, aber ohne den verlangten Prüfhinweis.
5. **Datums- und Spaltenmuster M06, M09, M11 und M12 sind überwiegend offen.** Beispiele:
   - Der Vorname «August» wird als Monat gelesen (D141005 VII.380.:1.9., D406 V.B.c.3.:19.; `trenne_spalten` Z. 665 ff.).
   - «… bis» über einen Zeilenumbruch geht verloren (D176367 ist ausser VII.215.:15. ganz unverändert).
   - In D3077 und D140955 sind die meisten mittleren Funde offen (11 von 16 bzw. 8 von 13).
6. **Weitere unveränderte Einzelfälle:**
   - D414: erfundene Einheit V.B.c.34.:XV.2.12. und Schlussnotiz im Darin von XV.
   - D2589: «9 Stadträte» als Einheit.
   - D141005: «20./21.» ist weiter keine Einheit.
   - D3672 S. 50: Bereichssignaturen werden weiter zu je zwei Einheiten.

## Hinweise für die Selbstprüfung des Skripts

- **Schlussvermerke prüfen:** Viele Zeilen, kleingeschriebener Anfang oder Anführungszeichen-Einträge sollten einen Prüfhinweis auslösen. Die Verluste in D3089, D2992 und D152817 zeigt die Vollständigkeitsprüfung heute nicht.
- **Signaturpräfixe prüfen:** Ein Wechsel aller Signaturen auf ein Präfix «A.»/«B.» vor einem Grossbuchstaben-Wort wie ÜBERSICHT oder DETAILVERZEICHNIS sollte auffallen. Ebenso eine Übersicht, die als eigene Einheiten erscheint.
- **Vergleich alt ↔ neu mitlaufen lassen:** Die Fälle aus dem Gesamtvergleich zeigen, dass grosse Änderungen der Einheitenzahl oder verschwundene Signaturen ein guter Fehlerspürer sind. Nach jeder Parser-Änderung `methode/diff_stand.py` und einen Einheitenzahl-Vergleich laufen lassen.
- **Geprüfte Abnahmen ohne Fehler:** D3357 (460 → 66: nummerierte Fotohefte jetzt im Darin von VII.270.:3.), D3818 und D2921 (erfundene Teile entfernt, Inhalt im Darin).

## Grenzen

- Die mittleren Muster sind nur stichprobenweise geprüft (höchstens 5 je PDF und Muster). M08, M10, M13 und M15–M18 waren nicht Teil der Stichprobe; von ihnen ist nur ein einzelner Zusatzfund (M13) nachgeprüft.
- Neue Fehler wurden auf den Prüfseiten nur dort gesucht, wo sich etwas geändert hat. Ausserhalb der Prüfseiten stammen sie aus dem heuristischen Gesamtvergleich und sind nicht vollständig.
- Bei den Zusatz-PDFs wurde je eine Zufallsseite im neu importierten Bereich geprüft.

## Dateien

- `funde_nachpruefung.csv`: 561 Zeilen, Spalten wie `funde.csv` plus `status` und `neu_ist`.
  - Die ersten 464 Zeilen sind die nachgeprüften Funde. Ihre ersten acht Spalten stehen unverändert wie in `funde.csv` bzw. `zusatzfunde_gesamtscan.csv`, die Zeilen lassen sich also verbinden.
  - Es folgen 97 Zeilen mit `status` = `neu`.
  - `ist` ist der alte Stand (21:02). `neu_ist` ist der neue Stand (23:05) mit Fundstelle (ID, Seite) und kurzer Begründung.
- `roh/np_gruppe_1…4.csv` und `roh/np_gruppe_1…4_notizen.md`: Rohergebnisse und Befund je PDF der vier Prüfgruppen.
- `roh/np_gruppe_0.csv`: eigene Funde aus dem Gesamtvergleich.
- `methode/`: `ANLEITUNG_NACHPRUEFUNG.md`, `np_auswahl.py`, `np_pruefliste.csv`, `diff_stand.py` (Einheitenvergleich zweier Excel-Stände), `np_zusammenfuehren.py`.
