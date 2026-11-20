# Zweite Nachprüfung am Excel-Stand 20.11.2026, 00:15

Geprüft wurde `findmittel_excel/` vom 20.11.2026, 00:15 (Skript sha256 `f1787679ee13b2fd…`, 3771 Zeilen). Excel und Skript sind als Schnappschuss gesichert unter `/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/neu2/`; Zeilennummern beziehen sich auf dieses Skript.
Verglichen wird mit dem Stand 23:05 der ersten Nachprüfung. Alle Urteile sind am PDF belegt. Die Änderungsliste der Hauptsession wurde nicht benutzt.

## Kurzfazit

- **267 nachgeprüfte Zeilen:** 31 behoben, 53 teilweise, 183 offen. 118 davon liegen in PDFs, die seit 23:05 völlig unverändert sind; dort gilt der vorherige Befund weiter.
- **Die schweren Regressionen der ersten Nachprüfung sind grösstenteils behoben.** Von den 22 kritischen sind 16 behoben, 3 teilweise und 3 offen:
  - Behoben: Schlussvermerk-Regel (D3089, D2992, D152817, D8943); Präfix «A./B.» (D512, D2992, D10684, D3429; die Übersicht wird nicht mehr importiert, die Signaturen stimmen); Doppelmarken «II) B)» (D3067); Präfix «D.» (D176151 15.1.–16.20.); D73; D140969.
  - Teilweise: D1924 (84 statt 1584 Einheiten, aber Schachteln wie «33-34» und «80a & 80b» gehen verloren); D512 (Datums-Folgezeilen nur zum Teil zurück); D176151 (9.a. und 12.a. sind wieder Einheiten).
- **Alte Befunde kaum bewegt:**
  - Von 72 kritischen offenen oder teilweisen Funden sind nur 5 behoben. Die Schwerpunkte sind unverändert: D3018 (20), D3067 (14), D10575 (10) und D176151 (6).
  - Von den 98 mittleren (Stichprobe) sind 2 behoben.
- **Neue Fehler am Stand 00:15: 49 Zeilen, davon 11 kritisch.**
  - 32 sind durch die Änderung 23:05 → 00:15 entstanden (4 kritisch).
  - 17 gab es schon um 23:05; sie sind jetzt erst erfasst (7 kritisch).
  - 47 stammen aus dem Gesamtvergleich, 2 aus der Nachprüfung.
- **Neu fehlende Einheiten (kritisch): D2614, D3208, D176824.** Text vor der ersten Signatur wird jetzt ganz verworfen (`verarbeite_pdf` Z. 3514–3523). Bei D176824 gilt «Übersicht» zudem jetzt in jeder Schreibung als Verzeichniswort (`ist_verzeichniswort` Z. 1127–1129).
- **Neu erfundene Einheit:** D3357 VII.270.:5. «Grf. Schachteln 0, 90 lfm» stammt aus dem Bestandsumfang am Schluss.
- **Die meisten neuen mittleren Fehler betreffen den Zeitraum (M09)** und stammen von drei neuen Regeln (Abschnitt «Neue Fehler»).
- **Korrektur der ersten Nachprüfung:** Ich hatte die Kennzeichnung «Schon im alten Stand» nur in Kleinschreibung gezählt. Richtig sind 48 Regressionen (22 kritisch), 34 Fehler im neu importierten Bereich und 15 alte Fehler (statt 53 / 38 / 6). `nachpruefung.md` ist berichtigt; die CSV war nicht betroffen.

## Methode

1. **Auswahl** (`methode/np2_auswahl.py`, Startwert 20261120, Ergebnis `methode/np2_pruefliste.csv`):
   - alle 97 Zeilen mit Status «neu»;
   - alle 72 kritischen Zeilen mit Status «offen» oder «teilweise», inklusive Zusatzfunde;
   - von den 114 mittleren offenen oder teilweisen Zeilen je PDF und Hauptmuster höchstens 3, zusammen 98.
2. **Gesamtvergleich aller 715 Dateien** 23:05 ↔ 00:15: Einheitenvergleich wie `diff_stand.py`, Prüfhinweise und Info-Kennzahlen.
   - 52 Dateien haben geänderte Einheiten, bei 3 weiteren haben sich nur die Info-Kennzahlen geändert (Schlussvermerke, Vorspann).
   - In 54 Dateien haben sich Prüfhinweise geändert.
3. **Vorbewertung, 118 Zeilen** (`roh/np2_vorbewertet.csv`): In ihren PDFs sind alle Einheiten seit 23:05 gleich, ebenso Prüfhinweise, Schlussvermerke und Vorspann. Der vorherige Befund bleibt also (offen bzw. teilweise; «neu» → offen).
4. **Drei Prüfagenten** nach `methode/ANLEITUNG_NACHPRUEFUNG2.md`:
   - zwei für die 149 übrigen Zeilen in 24 geänderten PDFs, je mit allen entfernten und neuen Einheiten ihrer Diffs am PDF;
   - einer für die 33 geänderten Dateien ausserhalb der Liste: 11 Korrekturen, 5 unbedenklich, 17 mit neuem Fehler.
   - Die Entscheide 1–7 wurden beachtet, auch der neue Entscheid 7 (Unterliste mit nur einer Gruppe im Darin der Elterneinheit).
5. **Gegenprobe:** Diese Urteile habe ich selbst am PDF nachgesehen; alle wurden bestätigt:
   - D2614: Einheiten V.L.149.:1–3 weg;
   - D512: Signaturen ohne «B.»;
   - D2992: VII.163.:3.–5. ohne Schachtel;
   - D3067: II.A.–C. mit eigenen Signaturen;
   - D1924: «Läderach 1892 33-34» im Darin von :35.

## Ergebnis nach Auswahl

| Auswahl | behoben | teilweise | offen | entfällt | Zeilen | davon unverändert (vorbewertet) |
|---|---:|---:|---:|---:|---:|---:|
| neue Fehler der 1. Nachprüfung | 24 | 8 | 65 | 0 | 97 | 44 |
| kritische, vorher offen/teilweise | 5 | 28 | 39 | 0 | 72 | 17 |
| mittlere, vorher offen/teilweise (Stichprobe) | 2 | 17 | 79 | 0 | 98 | 57 |
| **Summe** | **31** | **53** | **183** | **0** | **267** | **118** |

Status der 97 neuen Fehler der ersten Nachprüfung (in Klammern: davon kritisch):

| Art | behoben | teilweise | offen | Zeilen |
|---|---:|---:|---:|---:|
| Regression der 1. Nachprüfung | 20 (16) | 5 (3) | 23 (3) | 48 |
| im neu importierten Bereich (Zusatz-PDFs) | 2 (2) | 3 (2) | 29 (6) | 34 |
| alter Fehler, in Runde 1 übersehen | 2 (1) |  | 13 (5) | 15 |

| Neue Fehler am Stand 00:15 | kritisch | mittel | gering | Zeilen |
|---|---:|---:|---:|---:|
| neu durch die Änderung 23:05 → 00:15 | 4 | 28 | 0 | 32 |
| schon im Stand 23:05, bisher nicht erfasst | 7 | 10 | 0 | 17 |
| **Summe** | **11** | **38** | **0** | **49** |

## Nach Hauptmuster

| Hauptmuster | behoben | teilweise | offen | entfällt | neu | davon durch 00:15 |
|---|---:|---:|---:|---:|---:|---:|
| M01 Vorspann/Schlussvermerk verworfen | 5 | 9 | 3 |  | 4 (3 krit.) | 4 |
| M02 Echte Signatur nicht erkannt | 4 | 4 | 25 |  | 2 (2 krit.) |  |
| M03 Zahl/Marke als Signatur | 3 | 7 | 12 |  | 1 (1 krit.) | 1 |
| M04 Gliederungsebene nicht erkannt | 11 | 10 | 11 |  | 3 (3 krit.) |  |
| M05 Mehrzeilige Datumsspalte | 2 | 7 | 14 |  | 4 | 4 |
| M06 Rechte Spalte nicht abgetrennt |  | 3 | 23 |  | 1 |  |
| M07 Fremdtext im Darin |  | 6 | 19 |  | 3 | 1 |
| M08 Zeilenumbruch falsch |  |  | 12 |  | 2 | 1 |
| M09 Zeitraum aus falscher Quelle | 2 | 3 | 21 |  | 10 | 10 |
| M10 Darin falsch getrennt |  |  | 12 |  | 5 | 4 |
| M11 Schachtel-Nr. |  |  | 9 |  | 5 | 1 |
| M12 Datumsformat nicht erkannt |  | 2 | 15 |  |  |  |
| M14 Mappen/Schachteln: Titel aus Überschrift |  |  | 1 |  |  |  |
| M16 Zerrissene Wörter |  |  | 1 |  |  |  |
| M17 Kosmetik |  |  | 1 |  |  |  |
| M19 Sonstiges | 4 | 2 | 4 |  | 9 (2 krit.) | 6 |

## PDFs mit kritischen offenen oder neuen Fehlern

| PDF | kritisch offen/teilw. | neu kritisch | behoben | teilweise | offen | neu |
|---|---:|---:|---:|---:|---:|---:|
| D3018 | 20 | 0 | 0 | 1 | 22 | 0 |
| D3067 | 14 | 0 | 5 | 18 | 7 | 3 |
| D10575 | 10 | 0 | 1 | 0 | 15 | 0 |
| D176151 | 6 | 0 | 6 | 2 | 6 | 1 |
| D10675 | 4 | 0 | 0 | 1 | 7 | 0 |
| D1924 | 1 | 2 | 0 | 1 | 0 | 3 |
| D3060 | 3 | 0 | 0 | 1 | 6 | 0 |
| D3828 | 3 | 0 | 0 | 1 | 3 | 0 |
| D141005 | 2 | 0 | 2 | 1 | 5 | 0 |
| D150689 | 2 | 0 | 1 | 2 | 1 | 2 |
| D1739 | 2 | 0 | 0 | 2 | 1 | 0 |
| D3208 | 0 | 2 | 0 | 0 | 0 | 2 |
| D3530 | 2 | 0 | 0 | 1 | 2 | 0 |
| D3672 | 2 | 0 | 0 | 1 | 5 | 0 |

Je 1 kritischer offener oder neuer Fund:
- offen oder teilweise: D141024, D2589, D2708, D2729, D2839, D2990, D3063, D3089, D3105, D3466, D3484, D3684, D414, D512, D71;
- neu: D149622, D176551, D176824, D2614, D2992, D3357, D4175.

## Neue Fehler am Stand 00:15, nach Ursache

1. **Text vor der ersten Signatur wird ganz verworfen (M01, kritisch).**
   - Ursache: `verarbeite_pdf` Z. 3514–3523 verwirft Schachteln vor der ersten Signatur jetzt ohne Ersatz.
   - D2614 S. 1–4: Es bleiben nur V.L.162.:1–4; V.L.149.:1–3 (u. a. «Seminararbeiten») fehlen. «Nicht übernommen» steigt von 52 auf 131 Zeilen, die Wörter im Detail sinken von 1420 auf 895.
   - D3208 S. 1–2: Schachtel 1 «Manuskripte und Zeitungsausschnitte» und Schachtel 2 «Publikationen» fehlen.
   - D176824 S. 1: «A. Übersicht» mit A.a.–A.c. ist keine Einheit mehr (`ist_verzeichniswort` Z. 1127–1129, jetzt unabhängig von Gross- und Kleinschreibung).
2. **Erfundene Einheit (M03, kritisch).** D3357 S. 34: VII.270.:5. «Grf. Schachteln 0, 90 lfm».
   - Das ist eine Folge der richtigen Entfernung von «60.»: Danach passt «5» als nächste Hauptnummer.
   - `baue_vorkommen` prüft die Signatur (Z. 1462 ff.) vor dem Schlussvermerk (Z. 1509).
3. **D1924: Schachtelangaben ohne einfache Nummer gehen verloren (M02, kritisch, schon um 23:05).**
   - Ursache: `baue_behaelter_am_ende` Z. 2250 lässt nur `\d{1,4}[a-z]?` als Marke gelten.
   - S. 25–26: «33-34» (15 Zeilen) steht im Darin von :32 und :35. S. 24: «80a & 80b» steht im Darin von :30.
   - Eingestreute Zeilen («101», «79a») teilen :10 und :79 in Serie plus Kind (Z. 2270–2276).
4. **Nr.-Filter verschluckt echte Jahre (M09/M19).**
   - Ursache: `jahre_im_text` Z. 504–507.
   - D3063 S. 5 VII.190.:1.4. «Police-Nr. 87893, 1919 - 1945» hat keinen Zeitraum mehr.
   - D150296 S. 3 2.2. «Nr. 1-9, 12-14, 1964 – 1971» hat keinen Zeitraum mehr.
   - D141020 VII.171.:3.2.: Ende 1945 statt 1951.
   - D3170 6.3.0.: Beginn 1951 statt 1944.
   - D3271 4.1.1. und 6.4.1.
   - Korrigiert hat der Filter dagegen D10575 2.1. (jetzt 1876–1889).
5. **Darin-Jahre zählen nur noch im 10-Jahres-Fenster (M09).**
   - Ursache: `ergaenze_zeitraeume` Z. 2656–2665.
   - D4039: Bei 6 Schachteln zählt nur die erste Zeile, z. B. :39 1965–1970 statt 1949–1971.
   - «2005 bis» bzw. «2005-» wird «= 2005» (D2519 :14, D2710 :10).
   - D2735 :9: 1912 statt 1950–1967.
   - Die Regel korrigiert aber auch viele Schachteln (D539, D2519 :5/:13, D149622, D2681).
6. **Inhaltsverzeichnis liefert das letzte statt des ganzen Datums (M09).**
   - Ursache: `lese_inhaltsverzeichnis` Z. 2535/2538 (`funde[-1]`).
   - D3067 III.D. hat 1852–1942 statt 1801–1955; II. erbt den Zeitraum von II.A.
   - D3057 1.–4., z. B. 1.: 1904–1921 statt 1868–1921.
7. **Weitere neue mittlere Fehler:**
   - Schachtel gilt nur bis zur nächsten Hauptnummer (`bereich()`/`box_fuer()` Z. 1361–1376): D2992 VII.163.:3.–5. haben keine Schachtel 4/6 mehr.
   - D512 (Rückfall): 9 Saisons haben wieder ein Einzeldatum, z. B. 1.11. «Saison 1968/69» = 27.09.1968 (`baue_vorkommen` Z. 1590–1600).
   - Listen: Reicht eine Zeile bis an den rechten Rand, wird der nächste «NN.»-Eintrag angehängt (`ist_umbruch` Z. 1699). Beispiele: D3715 VII.408.:5. «53. … 54. …», D176551, D3170 6.4.
   - D150689 1.8.1., 1.2.4. und 1.6. tragen den Titel der Elterneinheit mit dem Hinweis «Kein eigener Titel» (`ergaenze_titel` Z. 2746–2748). Die Umfangsangabe von 1. ist mit S. 4 in den Vorspann gefallen.
   - D4054 10.3.4.: «Teil 2» kommt viermal vor (`ergaenze_titel` Z. 2737).
   - D8651: «STADTARCHIV ZÜRICH» in Grossbuchstaben gilt nicht mehr als Schlussvermerk und steht im Darin, weil `SCHLUSS_RE` jetzt wieder Gross- und Kleinschreibung unterscheidet.
8. **Schon um 23:05 vorhanden, erst jetzt erfasst (kritisch):**
   - D149622: Das ganze Verzeichnis steht im Darin von Schachtel 3.
   - D4175: Zwei Nachlässe sind vermischt (A.–N. als Teile).
   - D3208: Die drei Nummernfolgen sind vermischt (Abzeichen als Teile der Theaterstücke).
   - D176551: 2.1.–2.3. aus 7. hängen unter 2.
   - D2992 S. 6: «3. Filmzettel» hängt unter der Tippfehler-Einheit «3. Werbefilme».

## Wichtigste offene Punkte

1. **D3018** (20 kritische offen): Die Abschnitte 01–09 mit neu beginnender Zählung fehlen weiter. Die Überschriften stehen jetzt nur als Prüfhinweise, z. B. «03 BUCHHALTUNG UND INVENTARE» bei «Journale».
2. **D3067** (14 kritische offen oder teilweise): Die Doppelmarken sind gelöst. Offen sind:
   - die Untergruppen ohne Doppelmarke (III.A., IV.A., V.A./B., VI.A./B.);
   - Schachtelnummern, die nur im Text stehen («101 altes Urbar …»);
   - die Zwischenüberschrift «Weitere Handschriften:» im Titel von III.8.
3. **D10575** (10 kritische offen): Das Inhaltsverzeichnis S. 7 wird weiter als Gliederung gelesen (`finde_detailbeginn`).
4. **D176151:** 9.a. und 12.a. sind wieder Einheiten, die Bibliotheksliste steht bei 12.a. (`lies_signatur` Z. 1035–1036 gilt nur für einfache Nummern). 14. hat den Zeitraum 1336–1939 aus Buchtiteln.
5. **Entscheid 4** (Überschrift als Prüfhinweis) setzt den Hinweis teils an die falsche Stelle (`baue_vorkommen` Z. 1548–1552). D2839 «4. NSDAP» fehlt weiter, der Hinweis steht bei 2.16.; in D150296 geht die Titelzeile «ZBVV» von 3.5.31. verloren.
6. **Neu importierte Bereiche der Zusatz-PDFs** (29 von 34 Zeilen offen) sind seit 23:05 fast unverändert:
   - D10675: Positionen 010–029 und 600–624 stehen nur im Darin;
   - D3828 und D3530: abschnittsweise Zählung;
   - D3684: «4 Kinder:» als Einheit.
7. **Mittlere Muster M06, M07, M09 und M12** sind praktisch unverändert offen (2 von 98 Stichprobenzeilen behoben).

## Dateien

- `funde_nachpruefung2.csv`: 316 Zeilen, Spalten wie `funde_nachpruefung.csv`.
  - Die ersten 267 Zeilen sind die nachgeprüften Funde. `pdf`, `seite`, `signatur`, `feld`, `schwere`, `soll` und `bemerkung` sind unverändert und verbinden die Zeilen eindeutig mit `funde_nachpruefung.csv`.
  - `ist` = Stand 23:05 (= `neu_ist` der ersten Nachprüfung), `neu_ist` = Stand 00:15 mit Fundstelle und Begründung.
  - Es folgen 49 neue Fehler (`status` = `neu`, Herkunft in der Bemerkung).
- `roh/np2_vorbewertet.csv`, `roh/np2_gruppe_1…3.csv` und `roh/np2_gruppe_1…3_notizen.md`: Rohergebnisse und Befund je PDF. Gruppe 3 hat ein Urteil für jede der 33 Dateien.
- `methode/`: `ANLEITUNG_NACHPRUEFUNG2.md`, `np2_auswahl.py`, `np2_pruefliste.csv`, `np2_zusammenfuehren.py`.
