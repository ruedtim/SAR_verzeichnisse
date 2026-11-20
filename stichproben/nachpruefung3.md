# Dritte Nachprüfung am Excel-Stand 20.11.2026, 08:25

Geprüft wurde `findmittel_excel/` vom 20.11.2026, 08:25. Das Skript hat sha256 `356032fdf36f72f9…` und 4363 Zeilen.
- **Schnappschuss:** Excel und Skript sind gesichert unter `/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/neu3/`. Alle Zeilennummern beziehen sich auf dieses Skript. Das Projektskript hat sich seither schon wieder geändert (sha256 `41d90d89…` beim Abschluss); die Excel-Dateien sind noch die von 08:25.
- **Vergleich:** mit dem Stand 00:15 der zweiten Nachprüfung. Der Zwischenstand 01:45 ist ungeprüft, eine Kopie davon gibt es nicht.
- **Runde eines Fehlers:** Ob ein neuer Fehler aus der Runde 01:45 oder 08:25 stammt, ist aus der Änderungsliste der Hauptsession abgeleitet. Diese Liste diente nur als Hinweis, wo zu suchen ist.
- **Belege:** Jedes Urteil ist am PDF belegt.

## Kurzfazit

- **268 nachgeprüfte Zeilen:** 82 behoben, 46 teilweise, 140 offen, keine schlechter.
  - 93 davon liegen in PDFs, die seit 00:15 völlig unverändert sind; dort gilt der Befund von 00:15 weiter.
- **Kritische Zeilen: 54 von 97 behoben**, 26 teilweise, 17 offen.
  - In den geänderten PDFs (81 Zeilen) sind es 54 behoben, 17 teilweise und 10 offen.
  - Die übrigen 16 liegen in unveränderten PDFs.
- **Die Schwerpunkte der zweiten Nachprüfung sind grösstenteils gelöst:**
  - D3018: 19 von 20 kritischen behoben. Die Abschnitte 01–08 sind jetzt Teil der Signatur.
  - D10575: 9 von 10 behoben. Das Inhaltsverzeichnis wird nicht mehr als Gliederung gelesen.
  - D176151: 6 von 6 behoben.
  - D3067: 8 von 14 behoben, 3 teilweise, 3 offen.
- **Die 49 neuen Fehler der zweiten Nachprüfung:** 24 behoben, 5 teilweise, 20 offen.
  - Alle 11 kritischen sind behoben oder teilweise behoben:
    - D2614: die Schachteln jetzt bei V.L.156.;
    - D3208: Schachtel 1/2;
    - D176824: «A. Übersicht»;
    - D3357: VII.270.:5. ist weg;
    - D1924: «33-34» und «80a & 80b»;
    - D2992 3.;
    - D4175: zwei Nachlässe;
    - D176551 2.1.–2.3.
  - Ebenfalls behoben sind die Fehler des Nr.-Filters (D3063 1.4., D150296 2.2., D141020 3.2., D3170 6.3.0., D3271 4.1.1.), «2005 bis» (D2519, D2710) und die Übersichts-Zeiträume (D3057, D3067 III.D.).
- **Mittlere Stichprobe:** 12 von 133 behoben, 18 teilweise. Die Muster M05, M06, M07, M09 und M12 sind praktisch unverändert.
- **Neue Fehler am Stand 08:25: 69 Zeilen, davon 15 kritisch.**
  - Runde 01:45: 19 (1 kritisch).
  - Runde 08:25: 27 (8 kritisch).
  - Runde unklar: 2.
  - 21 waren schon um 00:15 vorhanden und sind jetzt erst erfasst (6 kritisch).
- **Die schwersten neuen Fehler:**
  - **D10675, Registraturplan-Modus (08:25):** 69 Einheiten haben eine verkürzte Signatur oder eine falsche Hierarchie, 19 frühere Einheiten stehen jetzt im Darin.
  - **D3018 (08:25):** «09 NACHTRÄGE» und 08.9. sind durch die neue Vorspann-Grenze ganz verloren.
  - **D3099 (08:25):** die zweite «1.2.5.».
  - **D8945 (01:45):** Ein Satz mitten im Verzeichnis gilt als Schlussvermerk.
- **Neue Regeln mit breiter Nebenwirkung (mittel):**
  - Bricht das Endjahr auf die nächste Zeile um, wird ein offenes Ende daraus (12 Fälle).
  - Die 150-Jahre-Regel verwirft ganze Datumsangaben samt gültigem Jahr (13 Einheiten).
  - Gruppen nehmen den Zeitraum nur aus «zuverlässigen» Kindern.
  - Die Schachtellisten sind meist richtig, haben aber einzelne Fehler, darunter die rohe Liste mit rund 170 Werten in D1880.
- **Alte, jetzt erst gefundene kritische Fehler:**
  - D1880: Die ganze Gliederung ist falsch.
  - D3275, D3778 und D4098: Die Bestandssignatur enthält Initialen («VII.241.J.H.»).
  - D2534 6.3. und D3405 6.5./6.6. fehlen.
- **Die Kennzahlen der Hauptsession stimmen:** 715 Dateien, 49'191 Einheiten, 48 «[ohne Titel]», 693 Dateien mit «Text erfasst» 100 %.
  - Die Testdaten-Excel sind gleich wie die gleichnamigen Dateien des Gesamtlaufs.
  - D3031 und D152810 gibt es nur als Testdaten.

## Methode

1. **Schnappschuss** `$S/neu3/`: `alle_excel/` als Kopie von `findmittel_excel/`, dazu `testdaten_excel/`, `D151210_scope_import.xlsx` und das Skript. Die Prüfsummen der Kopien stimmen mit den Originalen überein.
2. **Auswahl** (`methode/np3_auswahl.py`, Startwert 20261121, Ergebnis `methode/np3_pruefliste.csv`). Aus `funde_nachpruefung2.csv` kommen alle Zeilen mit Status «offen», «teilweise» oder «neu» in Frage. Ausgewählt sind:
   - alle 97 kritischen;
   - alle 38 mittleren neuen Fehler der zweiten Nachprüfung;
   - von den 150 älteren mittleren oder geringen Zeilen höchstens 2 je PDF und Hauptmuster, zusammen 133.
   - Die Zeilennummer `Z<n>` bezeichnet die n-te Datenzeile von `funde_nachpruefung2.csv`.
3. **Gesamtvergleich aller 715 Dateien**, 00:15 ↔ 08:25:
   - 175 Dateien haben geänderte Einheiten: 670 geändert, 990 entfernt, 997 neu.
   - Bei einer Datei haben sich nur die Info-Kennzahlen geändert, bei einer nur die Prüfhinweise. Geänderte Prüfhinweise gibt es insgesamt in 64 Dateien.
   - Die 698 geänderten Einheiten sind feldgenau eingeordnet: 225 nur Schachtel, 217 nur Zeitraum, 147 Titel/Darin, 51 Bestandszeilen, 45 Struktur, 13 gemischt.
   - Zusätzliche Abgleiche:
     - Text aus Titel und Darin von 00:15, der um 08:25 in keinem Blatt mehr vorkommt;
     - alle Bestandszeilen;
     - alle Einheiten mit dem Hinweis der 150-Jahre-Regel;
     - alle langen Schachtellisten;
     - Einheiten ohne Zeitraum bzw. ohne Schachtel je Datei.
4. **Vorbewertung, 93 Zeilen** (`roh/np3_vorbewertet.csv`). Ihre PDFs sind seit 00:15 unverändert: Einheiten, Prüfhinweise, Schlussvermerke, Vorspann und Info-Kennzahlen. Der Befund bleibt also; «neu» wird «offen».
5. **Drei Prüfagenten** nach `methode/ANLEITUNG_NACHPRUEFUNG3.md`. Jeder prüfte alle entfernten und neuen Einheiten seiner Diffs am PDF, von den geänderten eine Stichprobe.
   - **Gruppe 1, Umbauten von 08:25:** D3018, D10675, D3099, D4175, D3208, D149622 und D2933, mit 35 Zeilen.
   - **Gruppe 2, Korrekturen von 01:45 und D3067:** 14 PDFs mit 80 Zeilen.
   - **Gruppe 3, allgemeine Regeln:** 25 PDFs mit 60 Zeilen, dazu Stichproben in 28 weiteren Dateien zu Schachteln, Titel/Darin, offenem Ende und Schlussvermerken, einschliesslich der Testdatei D3031.
   - **Hauptprüfung (ich):** 150-Jahre-Regel, Bestandszeilen und Schachtellisten über alle Dateien (`roh/np3_gruppe_0.csv`, 9 Zeilen).
   - Die Entscheide 1–7 wurden beachtet. Die bekannten offenen Punkte der Hauptsession wurden nur bestätigt, nicht neu gemeldet.
6. **Gegenprobe:** Diese neun Urteile habe ich selbst am PDF nachgesehen; alle wurden bestätigt:
   - D2614: V.L.156.:1–3 sind richtig (es sind die Schachteln von V.L.156., nicht von V.L.149.);
   - D3067 II.A.: Das Stammbuch 1978 steht bei Schachtel 11;
   - D10575 3.: 1783–1949 statt 1882–1889;
   - D10675: «5.1 Ingenieurofferten» als `V.F.c.28.:5.1.` auf oberster Ebene;
   - D10675: 742.100–117 stehen im Darin von 742.99;
   - D3018: «09 NACHTRÄGE» fehlt;
   - D8945: «verzeichnet von Michael Kreis …» ist eine Satzmitte;
   - D10585 1.2.2.: «… bis / 31. Dezember 1823»;
   - D3405: «6. 5.» mit Leerzeichen.

## Ergebnis nach Auswahl

| Auswahl | behoben | teilweise | offen | schlechter | entfällt | Zeilen | davon PDF unverändert (vorbewertet) |
|---|---:|---:|---:|---:|---:|---:|---:|
| kritische Zeilen (offen/teilweise/neu) | 54 | 26 | 17 |  |  | 97 | 16 |
| mittlere neue Fehler der 2. Nachprüfung | 16 | 2 | 20 |  |  | 38 | 8 |
| mittlere, vorher offen/teilweise (Stichprobe) | 12 | 18 | 103 |  |  | 133 | 69 |
| **Summe** | **82** | **46** | **140** | **0** | **0** | **268** | **93** |

Herkunft der nachgeprüften Zeilen (in Klammern: davon kritisch):

| Herkunft | behoben | teilweise | offen | Zeilen |
|---|---:|---:|---:|---:|
| alte Funde (Stichprobe und Zusatzfunde), kritisch | 40 | 20 | 7 | 67 |
| neue Fehler der 1. Nachprüfung, kritisch | 6 | 3 | 10 | 19 |
| neue Fehler der 2. Nachprüfung, durch 00:15 entstanden | 15 (3) | 3 (1) | 14 | 32 |
| neue Fehler der 2. Nachprüfung, schon um 23:05 da | 9 (5) | 2 (2) | 6 | 17 |

«schlechter» kommt nicht vor. Neue Fehler an derselben Stelle sind als eigene Zeilen erfasst, z. B. Z129 (D3067 IV.E.1.): Der Zeitraumfehler bleibt offen, die neue Verschmelzung im Darin ist eine neue Zeile.

## Nach Hauptmuster

| Hauptmuster | behoben | teilweise | offen | neu | davon durch die Änderungen |
|---|---:|---:|---:|---:|---:|
| M01 Vorspann/Schlussvermerk verworfen | 4 | 9 | 3 | 4 (3 krit.) | 4 |
| M02 Echte Signatur nicht erkannt | 23 | 3 | 5 | 5 (5 krit.) | 3 |
| M03 Zahl/Marke als Signatur | 8 | 6 | 6 |  |  |
| M04 Gliederungsebene nicht erkannt | 16 | 5 | 3 | 4 (4 krit.) | 3 |
| M05 Mehrzeilige Datumsspalte | 1 | 6 | 14 | 2 | 1 |
| M06 Rechte Spalte nicht abgetrennt | 2 | 4 | 17 | 1 | 1 |
| M07 Fremdtext im Darin | 7 | 2 | 18 | 6 |  |
| M08 Zeilenumbruch falsch |  | 1 | 13 | 11 | 11 |
| M09 Zeitraum aus falscher Quelle | 8 | 3 | 19 | 12 | 12 |
| M10 Darin falsch getrennt | 5 |  | 12 | 4 | 3 |
| M11 Schachtel-Nr. | 1 | 1 | 9 | 10 | 6 |
| M12 Datumsformat nicht erkannt | 1 | 3 | 12 | 2 | 1 |
| M14 Mappen/Schachteln: Titel aus Überschrift |  |  | 1 |  |  |
| M15 Umfang |  |  |  | 1 |  |
| M16 Zerrissene Wörter |  |  | 1 |  |  |
| M17 Kosmetik |  |  | 1 | 2 | 2 |
| M19 Sonstiges | 6 | 3 | 6 | 5 (3 krit.) | 1 |

«davon durch die Änderungen» zählt die neuen Fehler der Runden 01:45, 08:25 und «unklar».

## PDFs mit kritischen offenen oder neuen Fehlern

| PDF | kritisch offen/teilw. | neu kritisch | behoben | teilweise | offen | neu |
|---|---:|---:|---:|---:|---:|---:|
| D10675 | 1 | 5 | 3 | 3 | 2 | 7 |
| D3067 | 6 | 0 | 15 | 5 | 6 | 8 |
| D3018 | 1 | 2 | 19 | 2 | 2 | 7 |
| D3060 | 3 | 0 |  | 1 | 6 |  |
| D3828 | 3 | 0 |  | 1 | 3 |  |
| D141005 | 2 | 0 |  | 1 | 5 |  |
| D150689 | 2 | 0 |  | 2 | 3 | 1 |
| D1739 | 2 | 0 | 1 | 1 | 1 |  |
| D3530 | 2 | 0 |  | 1 | 2 |  |
| D3672 | 2 | 0 |  | 1 | 4 |  |
| D10575 | 1 | 0 | 10 |  | 4 | 2 |
| D1880 | 0 | 1 |  |  |  | 2 |
| D2534 | 0 | 1 |  |  |  | 2 |
| D3099 | 0 | 1 |  |  |  | 4 |
| D3405 | 0 | 1 |  |  |  | 2 |
| D3275, D3778, D4098 | 0 | je 1 |  |  |  | je 1 |
| D8945 | 0 | 1 |  |  |  | 1 |
| je 1 kritisch offen/teilweise: D141024, D149622, D2589, D2614, D2708, D2729, D2839, D2990, D3063, D3089, D3105, D3208, D3466, D3484, D3684, D414, D512, D71 | | | | | | |

Seit 00:15 unverändert sind davon D3060, D141005, D3672, D414, D3484, D71, D2708, D2729, D2589, D3105, D3684 und D512.

## Neue Fehler am Stand 08:25, nach Ursache

### Runde 08:25 (27 Zeilen, 8 kritisch)

1. **D10675, Registraturplan-Modus (M04/M02, kritisch, 5 Zeilen).** Die Codes 010–029 und 600–624 sind jetzt richtig Einheiten. Daneben gibt es diese Fehler:
   - 29 Unter-Unterpositionen haben eine verkürzte Signatur, stehen auf oberster Ebene und haben keinen Parent.
     - Beispiel S. 4: «5.1 Ingenieurofferten» wird ID 135 `V.F.c.28.:5.1.`; richtig wäre 702.5.1 unter 702.5.
     - Ebenso betroffen sind 712.20.x und 713.2/3/13/30.x.
     - Ursache: `lies_signatur` Z. 1080–1085 kennt im Registraturplan-Zweig nur dreistellige Codes und «n.»; «5.1» fällt in die Dezimalregel.
   - 37 Positionen 109–142 und 210.1–215 (S. 7–8) haben eine Signatur ohne «712.», obwohl Fussnote 9 «712.109» nennt. Sie hängen an der ersten Nennung von 712 (Z. 1082, 1097–1098).
   - 742.100–742.117 (18 Einheiten, S. 17) stehen jetzt im Darin von 742.99 (ID 484), 701.40.7 (S. 4) im Darin von ID 110. Um 00:15 waren das eigene Einheiten. Ursache: Z. 1084 lässt nur zweistellige Unternummern gelten.
   - Die Dubletten 440.733.3, 440.744.6 und 440.745.19 (S. 22) hängen unter 440 statt unter 802 (`baue_einheiten` Z. 2754–2762). Folge: 802 hat keine Kinder mehr, und 440 bekommt den Zeitraum 1981–1987.
   - Mittel: Bei 745.52 ist der Titel abgeschnitten.
2. **D3018, verlorener Verzeichnistext (M01, kritisch).** Der Umbau selbst stimmt:
   - 01–08 sind Teilbestände mit Abschnittssignatur, die Eltern stimmen;
   - «5.1.», «22.01.56», 1.5.1.–1.5.4. und «2. Neubauten» sind am PDF geprüft.

   Verloren geht aber Folgendes:
   - **Vorspann:** Alles vor «DETAILVERZEICHNISSE» ist jetzt Vorspann, 274 Zeilen (`finde_detailbeginn` Z. 3813–3815).
     - 08.9. und «09 NACHTRÄGE» stehen nur in der Zusammenfassung S. 10 und fehlen jetzt ganz: Nachtrag 1–3 mit Schachtel 78/79, der Herkunftsvermerk V.J.W.c.19. und «Grossformate in Mappe».
     - Das Blatt Info nennt sie nur unter «Signaturen nur im Vorspann». Um 00:15 gab es noch eine Einheit «NACHTRÄGE».
   - **S. 67:** Die fette Zeile «alle Negative vom obigen Katalog Firmengeschichte» vor «08 FOTOGRAPHIEN» gilt als Zwischenüberschrift (`baue_vorkommen` Z. 1776–1782). Sie fehlt bei 07.3. und erscheint nur als Hinweis bei 08.
3. **D3099 (M02, kritisch):**
   - Die zweite «1.2.5.» («6. Generation», ein Tippfehler im PDF) ist ins Darin der ersten gerutscht. Ursache ist die Regel «Signatur versehentlich im Text» (`baue_vorkommen` Z. 1838–1851). Nach Entscheid 5 wäre das eine eigene Einheit mit Hinweis.
   - Mittel: 2. hat «= 1963», weil «(1988)» bei 2.4.2. nicht gelesen wird.
4. **Zeitraum einer Gruppe nur aus «zuverlässigen» Kindern (M09, mittel).** `ergaenze_zeitraeume` Z. 3005–3016 übergeht geschätzte Kinder, sobald eines eine Datumsspalte oder einen Titel hat. Beispiele:
   - D3018 07. «= 1963» (Kinder 1919–1986), 05.7. «= 01.1931», 01., 05.1., 05.2.;
   - D3099 7. 1963–1988 statt 1941–1988;
   - D3067 V. nur 1584.
5. **150-Jahre-Regel verwirft gültige Jahre (M09, mittel, 13 Einheiten).**
   - Ursache: `jahre_im_text` Z. 535–537 verwirft eine gefundene Zeitangabe ganz, sobald ein Ende vor dem Rahmen liegt. `finde_zeitraeume` liest Listen wie «ca. 1568 – 1944, Juli 1944», «1604 – 1924, 1941 – 1942» oder «1351 / 1951» aber als eine einzige Angabe. So fällt das gültige Datum mit weg.
   - Betroffen sind:
     - D3528: 10 Stammtafeln (S. 6–8, z. B. 4.2.5. ohne Zeitraum statt 07.1944);
     - D2534: 2.1. und 6.2. (1951);
     - D150589: 16.2.14. (1950).
   - Von 31 Einheiten mit dem neuen Hinweis haben 14 ein gültiges Jahr im Darin. Der 14. Fall, D3512 2.2. «Regesten von Urkunden 1391 bis 1895», ist ein Grenzfall und nicht gezählt.
   - Daneben korrigiert die Regel viele Fehler, z. B. 1291/1336/1351 in D149888, D150689, D176367, D2534 2.2. und D3612.
6. **Schachtellisten aus den Einträgen (M11, mittel).**
   - Richtig sind sie in D1395, D151150, D3043, D3133, D3221, D3405, D134644, D2894 und D3089.
   - **Fehler:**
     - D1880 VI.I. (S. 23): Die Schachtel ist eine rohe Liste mit rund 170 Werten, «163-360, 163-169, 163-164, 165, …». Ursache: `schachtel_liste` Z. 2234–2252 gibt die Rohliste aus, sobald ein Bereich mehr als 50 Schachteln umfasst. Das ist der einzige solche Fall in allen Dateien.
     - D3089 X. «55-60, 68-73»: Die Schachteln 55–60 stammen aus dem falsch angehängten Detailverzeichnis.
     - D2894 15.: «2» statt «1-2».
     - D176795: unvollständig.
     - D141: Die führende Null fällt weg (gering).
     - Testdatei D3031: IV.e.5. hat «15» statt 14, IV.e.12. «16» statt 15. Die Bereichsangabe nach der Marke («Ku-Sch») gilt als Inhalt der vorigen Einheit (`inhalt_beginnt` Z. 1591–1601). «2 ¦ Schachtel 14» wird dort jetzt richtig gelesen.
   - **D3067 (Schachtelspalte):**
     - V.B.: Die allein stehenden Nummern 302–304 erzeugen drei Teile ohne Teil-Nr., mit einem Bucheintrag als Titel (`nr_box` Z. 1736, `inhalt_beginnt` Z. 1591–1611).
     - VI.D. erbt die Schachtel 400 statt 401.
     - VI.C./VI.D. haben als Zeitraum nur das Datum der ersten Zeile (`verarbeite` Z. 2273–2274).
     - Bei VI.C./VI.D. steht nach einem Doppelpunkt der Folgetext im Titel.
   - **D3208:**
     - Die Abzeichensammlung 1–172 hat im PDF keine Schachtel, steht aber im Darin von Schachtel 2. Daraus entsteht der Zeitraum 1828–1994.
     - An Seitenwechseln sind vier Einträge mit dem vorigen verschmolzen.
7. **D3067, Runde unklar (mittel):**
   - Vier Darin-Einträge sind neu verschmolzen. Am schwersten wiegt II.A.: Das Stammbuch von 1978 steht dadurch bei Schachtel 11 statt 10.
   - «Doppelgrösse» gilt als Tabellenkopf und ist verworfen (KOPFWORTE Z. 782–786).

### Runde 01:45 (19 Zeilen, 1 kritisch)

1. **Offenes Ende, wo nur das Endjahr umbricht (M08, mittel, 12 Fälle in 9 PDFs).**
   - Beispiele:
     - D10585 1.2.2.: «vom 1. August 1822 bis / 31. Dezember 1823» wird «Von 01.08.1822–», der Titel endet auf «bis».
     - D3204 12./13.: «1807 - / 1809».
     - D150589 6.1.30.: Das Endjahr steht nach dem Seitenwechsel.
     - Weitere Fälle: D150589 15.2.1., D150296 6.7., D3943 X.G.188, D1933 5.5., D149628 23.8.1.8., D3861 7.1., D10585 5.22. und D176151 16.15. («1961» steht im Darin).
   - Ursache: `finde_zeitraeume` Z. 467–472. Ein Titel, der auf «–», «-» oder «bis» endet, gilt als offen, die Folgezeile ist zu diesem Zeitpunkt schon Darin.
   - Vorher stand dort «Genau Anfangsjahr», das war ebenfalls falsch.
   - Unbedenklich ist D150536: «1897 ff.» steht so im PDF.
2. **D8945 S. 4, 3.1. (M01, kritisch).** «verzeichnet von Michael Kreis (1578 – 1661), von und in Egnach bis zur» ist die Mitte eines Satzes, gilt aber als Schlussvermerk.
   - Ursache: `SCHLUSS_RE` Z. 771–778 erkennt «verzeichnet von» auch klein geschrieben.
   - Richtig sind die übrigen neuen Schlussvermerke: D3253, D3265, D150242, D3429, D3206, D8651, D2710, D2735, D3231, D2992 «Bestand: 7 Schachteln, 1 Mappe», D3357 Bestandsumfang, D4175 und die Bestandszeilen.
3. **Zeiträume aus Beschreibungstext (M09, mittel).** Die Ursache ist jeweils, dass jetzt richtig zugeordneter Text in die Schätzung einfliesst:
   - D10575 3./4./5.: 1783–1949, 1876–1962 und 1882–1942 statt 1882–1889, 1880–1890 und 1882–1884. Der Einleitungstext ist jetzt richtig zugeordnet und zählt mit.
   - D176824 A.: «–1958» aus «Bis 1958 enthalten die Bände …».
   - D3067 VIII.: die Abgabedaten 2000–2002 (`lese_inhaltsverzeichnis` Z. 2908–2913).
   - D10575 8.1.4.: «1798–» aus dem Buchtitel «(1798 ff.)».
4. **Weitere Fehler aus Runde 01:45:**
   - **Nr.-Filter:** In D150689 6.9.20. zählen jetzt die Lebensdaten nach «Nr. 194,» (`NR_LISTE_RE` Z. 509–515).
   - **Fette Titel nicht mehr ins Darin:** Die Regel wirkt (D141020 mit 18 Einheiten, D3548, D3764, D134644 6.2.). Nebenwirkungen:
     - D3548 5.3.: Nur die ersten zwei Jahreszeilen zählen als Datum.
     - D3764 1.1.: Im Zitat ist das Jahr gelöscht.
   - **Listenmarken «(n)»:** Sie gelten als Fortsetzung (`ist_umbruch` Z. 1936). Dadurch sind in D2614 V.L.156.:3 und V.L.162.:4 je zwei Einträge verschmolzen.
   - **Bestandszeile = Abteilung:** richtig in 56 von 59 Bestandszeilen; leer bei D3275, D3778 und D4098 (siehe unten).
   - D3057 4.: Die Anmerkung ist unvollständig (gering).

### Schon um 00:15 vorhanden, jetzt erst erfasst (21 Zeilen, 6 kritisch)

- **D1880 (M04, kritisch):** Die Gliederung ist ganz falsch.
  - Richtig wären die Ämter A.–P. als oberste Ebene mit I.–VII. darunter (Inhaltsverzeichnis S. 2–3).
  - Stattdessen hängen die römischen Nummern aller Ämter unter den gleichnamigen von A. Die Buchstaben stehen als V.C., IV.F., VI.E., VI.H. … unter falschen Gruppen.
  - Der ganze Abschnitt «H. Hochbauamt» (S. 23–31, Schachteln 163–362) steht als 195 Zeilen im Darin von VI.I. «Personelles und Organisation [leer]».
  - Die Datei hat nur 44 Einheiten und war in keiner Stichprobe.
- **D3275, D3778, D4098 (kritisch):** Die Bestandssignatur lautet «VII.241.J.H.», «VII.49.J.A.» bzw. «VII.465.J.J.» statt VII.241., VII.49. bzw. VII.465.
  - Ursache: `finde_bestand` Z. 3738–3743 nimmt die längere Fassung aus der Kopfzeile der Folgeseite, und `BESTAND_RE` (Z. 3705) liest die Initialen als Signaturteile.
  - Der Abgleich mit dem Online-Archiv (Z. 3896) greift nicht, weil die falsche Fassung mit der richtigen beginnt.
  - Neu seit 01:45 ist dort auch die Übergeordnete Signatur leer.
- **D2534 6.3. (kritisch):** «6.3. 1351 - 1951 …» gilt als Datum (`lies_signatur` Z. 1144–1145: Folgt ein Jahr, ist es keine Signatur). Der Text steht im Darin von 6.2.
- **D3405 6.5./6.6. (kritisch):** «6. 5.» mit Leerzeichen wird nicht als Signatur erkannt.
- **Mittel:**
  - Die Schachtel zieht nicht weiter, wenn es weniger als 40 Schachtelangaben gibt und eine davon wiederholt wird (Z. 1502–1503; D3429, D3405, D176795).
  - Schlussnotizen bleiben im Darin (D150242, D3221, D2710).
  - D4175: Titelblatt und Zwischentitel stehen im Darin.
  - D10675: Fussnotentexte stehen im Darin.
  - D3018: Datumsspalte, Datumsreste und Umfang.
  - D149622: Jahreszeilen sind verschmolzen, die Anmerkungen zu 1757 und 1795 stehen bei Schachtel 3.

## Wichtigste offene Punkte

1. **D10675:** Der Registraturplan-Modus braucht Codes mit mehr als einer Unterstufe («702.5.1», «742.100», «712.109») und Unternummern ohne Punkt. Dazu 2 offene und 3 teilweise behobene alte Zeilen.
2. **D3067**, 6 kritische Zeilen offen oder teilweise, dazu 8 neue mittlere:
   - VI.D.1./VI.D.2. sind aus Listenmarken erfunden;
   - die Nachträge VIII. sind Einheiten mit der Signatur der Elterneinheit;
   - im Titel von III.A.8. steht die Zwischenüberschrift «Weitere Handschriften:»;
   - IV.A.d.18. hat den falschen Parent.
3. **D3018:** «09 NACHTRÄGE» fehlt; das ist neu und kritisch. Ein möglicher Weg: Signaturen, die nur im Vorspann stehen, als Einheiten übernehmen. Die Plannummern 2008–2022 zählen weiter als Jahre; das ist ein bekannter Punkt.
4. **Unveränderte PDFs mit kritischen alten Funden:** D3060 (3), D141005 (2), D3672 (2) sowie je 1 in D414, D3484, D71, D2708, D2729, D2589, D3105, D3684 und D512.
5. **Bekannte offene Punkte, bestätigt:**
   - D3828/D3530: Zählung je Abschnitt;
   - D512, D4054 und D4039;
   - D1395: «, Teil 2»;
   - D134644 1.2.;
   - D10675: Schachtelnummer am Titel;
   - D3018: Plannummern.
6. **Regeln, die als Nächstes zu prüfen wären:**
   - Endjahr auf der Folgezeile (Abschnitt Runde 01:45, Punkt 1);
   - 150-Jahre-Regel nur auf das einzelne Datum statt auf die ganze Angabe anwenden;
   - Gruppen-Zeitraum auch aus geschätzten Kindern;
   - `schachtel_liste` bei grossen Bereichen;
   - Weiterziehen der Schachtel bei kurzen Listen.
7. **Mittlere Muster M05, M06, M07, M09 und M12:** praktisch unverändert offen (12 von 133 Stichprobenzeilen behoben).
8. **Nicht abgedeckt:** Dateien, die nie in einer Stichprobe waren. D1880 zeigt, dass dort schwere Gliederungsfehler unbemerkt bleiben können. Eine Strukturprüfung über alle Dateien könnte weitere finden, etwa nach vielen wiederholten Signaturen oder Buchstaben unter römischen Nummern.

## Dateien

- `funde_nachpruefung3.csv`: 337 Zeilen, Spalten wie `funde_nachpruefung2.csv`.
  - Die ersten 268 Zeilen sind die nachgeprüften Funde. `pdf`, `seite`, `signatur`, `feld`, `schwere`, `soll` und `bemerkung` sind unverändert und verbinden die Zeilen eindeutig mit `funde_nachpruefung2.csv`.
  - `ist` = Stand 00:15 (= `neu_ist` der zweiten Nachprüfung), `neu_ist` = Stand 08:25 mit Fundstelle und Begründung.
  - Es folgen 69 neue Fehler (`status` = `neu`). In der Bemerkung stehen Herkunft und Runde: «Runde: 01:45», «08:25», «unklar» oder «vor 00:15».
- `roh/np3_vorbewertet.csv`, `roh/np3_gruppe_0…3.csv` (0 = Hauptprüfung), `roh/np3_gruppe_1…3_notizen.md`: Rohergebnisse und Befund je PDF bzw. Stichprobendatei.
- `methode/`: `ANLEITUNG_NACHPRUEFUNG3.md`, `np3_auswahl.py`, `np3_pruefliste.csv`, `np3_zusammenfuehren.py`.
- Hilfsdaten im Scratchpad `…/scratchpad/np3/`:
  - `gesamt.json`, `klassen.json` und `familien.csv`: Gesamtvergleich und feldgenaue Änderungen;
  - `diff/D<id>.txt`: Diffs je Datei;
  - `textverlust.csv` und `regel150_verluste.csv`: die Abgleiche zu verlorenem Text und zur 150-Jahre-Regel.
