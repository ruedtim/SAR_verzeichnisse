# Nachprüfung 10: Runde 8 und erste Stichprobe der nie geprüften Dateien (22.11.2026)

Geprüft ist das Skript `findmittel_zu_scope.py` mit sha256 `7fa7e1613a528651…` (Runde 8) gegen `e896fb6c…`. Die Prüfung hat
zwei Teile:
- die **Gegenprüfung der geänderten Dateien**;
- eine **erste Stichprobe der 509 Dateien, die noch in keiner Fundliste standen** (Auftrag der Hauptsession).

Die Ergebnisse stehen hier:
- `offen_kritisch.csv`: nachgeführt, 59 Zeilen K1–K59;
- `funde_nachpruefung10.csv`: 258 Zeilen;
- Rohdaten in `roh/np10_*`;
- Methode in `methode/ANLEITUNG_NACHPRUEFUNG10.md` und `methode/np10_*.py`.

## Kurz

- **Runde 8 hält, was sie verspricht.**
  - Von 2'019 geänderten Einheiten sind am PDF 2'004 besser, 8 gleich und 7 schlechter; die 7 schlechteren sind alle mittel
    (Schachtel).
  - Von den 22 kritischen Fällen, die Runde 8 beheben sollte, sind 20 im kritischen Teil gelöst.
  - Offen bleiben K8 (eine von 11 Gruppen in D3271) und K28 (D3826, bewusst nach Regel 5).
  - D3470 hat jetzt 1'388 richtige neue Einheiten.
- **Runde 8 bringt einen neuen kritischen Fehler:** D3018 S. 78, «Cakeplatte (Keramik) 1 Mappe». Regel 14 schiebt ihn mit
  der Kurzliste ins Blatt Info, die Zusammenfassung S. 10 nennt ihn aber nicht.
- **Die Stichprobe zeigt, dass in den nie geprüften Dateien noch viele kritische Fehler stecken.**
  - Zufallsteil: 4 von 28 Dateien kritisch (14 %, 95%-KI 6–31 %).
  - Verdachtsfälle: 7 von 27.
  - Erstgeprüfte Runde-8-Dateien: 5 von 21.
  - Hochgerechnet haben **rund 60 (25–135) der 431 Dateien, die noch niemand angesehen hat**, mindestens einen kritischen
    Fehler.
  - **Die Prüfung muss also ausgeweitet werden.**
- **Offene kritische Fehler** (`offen_kritisch.csv`, Stand nach dem Nachtrag unten): 60 Zeilen in 37 Dateien.
  - 28 Zeilen in 16 Dateien sind offen und noch niemandem zugeteilt.
  - 24 Zeilen in 14 Dateien hat die Hauptsession in ihrer Arbeitskopie schon behoben. Das ist noch nicht im Projekt und
    noch nicht nachgeprüft.
  - 8 Zeilen sind bewusst offen.
  - 51 der 60 Zeilen sind neu in dieser Runde; alle bestanden schon vor Runde 8, ausser «Cakeplatte».

## Stand und Nachrechnung

- **Lauf:** Mein Gesamtlauf mit 7fa7e161 ist zellgleich mit `findmittel_excel/`, `testdaten_excel/` und
  `D151210_scope_import.xlsx`. Die Testdaten und D151210 sind gleich wie bei e896fb6c.
- **Geänderte Dateien:** **62 statt 59** gegenüber e896fb6c. D65, D69 und D71 fehlen in `geaenderte_dateien.txt`:
  - Dort ist nur das Blatt Info bzw. Vollständigkeit anders.
  - Die Übersicht S. 2 («a) Kopialbücher (keine)» …) zählt jetzt als Schlussvermerk statt als «Text vor der ersten
    Signatur». Grund ist Regel 5, die den Schlussblock in grösserer Schrift fortsetzt.
  - Im Import ändert sich nichts (gering).
- **Kennzahlen:** bestätigt.
  - Einheiten 48'920 → 50'387.
  - «[ohne Titel]» 30, Text erfasst 100 % 695, doppelte Schlüssel 10, 0 Tracebacks.
- **Fallsets:** bestätigt: A 11/12, B 36 → 34, C 9/12, F 5/7, Runde 2 33 → 31, Punkt 2 38/38. Die vier geänderten Fälle sind
  wie angekündigt ID-Verschiebungen oder beabsichtigt.
- **Automatische Gegenproben:** einzug, konsistenz und datumsumbruch sind unverändert.
  - sigcheck: nur kleine Verschiebungen in D140969, D1746, D3566 und D3727.
  - textverlust2 meldet Wörter in 22 Dateien. Die Prüfer haben jede Meldung am PDF nachgesehen: Es ist nirgends
    Verzeichnistext weg, ausser «Cakeplatte». Die übrigen Meldungen sind Schachtelwörter, Wiederholungszeilen, Benutzerhinweise
    und Zahlen im Blatt Info.

## Gegenprüfung der Runde 8 (Pakete A1–A5)

| Paket | Dateien | Einheiten am PDF | besser | gleich | schlechter |
|---|---:|---:|---:|---:|---:|
| A1 Gliederung (K1–K3, K5, K7, Schachtel-Bereiche) | 15 | 149 | 146 | 0 | 3 (Schachtel) |
| A2 Detailverzeichnisse, Gruppenzeilen, Schlussblock (K4, K6, K8, K23, K28) | 10 | 63 | 58 | 5 | 0 |
| A3 Signaturerkennung, Zeiträume (K9–K11, D3470, Regel 25) | 7 | 1'413 | 1'413 | 0 | 0 |
| A4 ältere kritische Fälle (K19–K29) | 9 | 66 | 63 | 3 | 0 |
| A5 Schachtel bei flacher Nummerierung (Regel 23/24) | 21 | 328 | 324 | 0 | 4 (Schachtel) |
| **Summe** | **62** | **2'019** | **2'004** | **8** | **7** |

**Die K-Fälle aus Nachprüfung 9:**
- **Ganz behoben (14):** K1, K2, K3, K5, K6, K7, K9, K10, K11, K20, K23, K24, K25, K26.
- **Kritischer Teil behoben, mittlerer Rest (6):**
  - K4 D3018: Rest «Cakeplatte», siehe unten.
  - K19 D134644: 1.2. ohne Schachtel 1.
  - K21 D140969: Titel und Zeitraum von 50a. aus dem Eingangsvermerk («bis 2010»).
  - K22 D140969: 88. Zeitraum 17.08.2006 aus dem Vermerk.
  - K27 D2850: 55. 1877–1939 aus «Jahrgängerverein 1877» und «Landesausstellung 1939»; 56. ebenso aus
    «Doktor-Jubiläum 1951».
  - K29 D845: 1.2 1938–1950 statt offenes Ende.
- **Offen (2):**
  - **K8 D3271:** 10 von 11 Gruppen sind richtig. «Buchhaltungsjournal (2 Bände)» hat keinen Absatz davor und steht weiter
    im Darin von 4.2.16. Dazu: 18 Bandtitel «Bd. n: …» sind ohne den Gruppennamen nicht verständlich (mittel).
  - **K28 D3826:** Das Porträt bleibt nach Regel 5 im Darin von 20. Das Soll verlangt eine eigene Einheit; das entscheidet
    der Nutzer (geführt als bewusst offen).
- **Bewusst offen:**
  - K14 D1858: Alle 92 Schachtel-Nr. stimmen jetzt, aber weiterhin 92 Positionen statt 20 Schachteln.
  - K12, K13, K15–K18: Die Dateien sind in Runde 8 unverändert.

**D3470 (Regel 21):** Per Skript sind 1'950 Signaturzeilen gegen die Einheiten geprüft, dazu S. 1, 12, 23, 40, 56, 71 und
80 Einheit für Einheit.
- 1'388 neue Einheiten stimmen in Titel, Schachtel und Zeitraum.
- 45.0. hat nur noch die eigene Zeile. Sein leerer Zeitraum ist richtig, «45» ist kein Jahr.
- Die zweistelligen Signaturen stehen zu Recht auf E1; der Hinweis «Keine übergeordnete Signatur» ist Rauschen.
- **Noch fehlen 8 Einheiten** im Darin der Vorgängerin:
  - 12.53a, 1937.524a/b, 1938.583a/b: in der Arbeitskopie der Hauptsession behoben;
  - 1953.1419, 1954.1514, 1961.1813: Zeilen nur mit Signatur und Schachtel; Soll «[ohne Titel]» mit Signaturjahr; offen.
- Mittel:
  - 1861.1845/1846 haben Zeitraum 1861, im PDF wohl ein Tippfehler für 1961;
  - 1961.1823 «Expo 1964» wird zu «Expo», mit Zeitraum 1964.

**Schlechter durch Runde 8:**
- **Kritisch (1): D3018 «Cakeplatte (Keramik) 1 Mappe»** (S. 78) steht in keiner Einheit mehr.
  - Regel 14 schiebt die ganze Kurzliste ins Blatt Info, auch Posten ohne Gegenstück in der Zusammenfassung.
  - Soll: Darin-Eintrag bei 09.
- **Mittel, Schachtel (7):**
  - Regel 11: D1746 V.i. 42 statt 41-42; D1880 H.II. leer statt 19-39; D10744 430.1.733.0. 16-17 statt 16.
  - Regel 23: D2630 9.; D3774 6.4. trotz «Grossformate (ausserhalb der Schachteln)»; D1387 «Mappe» und 31. Regel 23 endet
    nicht an einer Behälterzeile, die nicht genau «Schachtel n» lautet.
- **Mittel, Zeitraum:** D1746 VI. 1952–1956 statt 1951–1973; D2850 55./56. aus Namen.
- **Gering:**
  - Blatt Info von D65, D69, D71 und D3462: Übersicht bzw. Titelzeile als Schlussvermerk;
  - D2620 11.2.: neuer Hinweis «weicht vom Inhaltsverzeichnis ab» ohne Grund.

**Fragen der Hauptsession:**
- **D3774 6. «Pläne»:** Schachtel 7 stimmt für 6. und 6.1.–6.3. (S. 12 «Schachtel 7» vor 5., Übersicht S. 2). Falsch ist nur
  6.4. mit den Grossformaten.
- **D1880 «f. Heizamt», «L. Polizeiamt»:** Beide sind als E1 richtig. Laut Einleitung S. 1 ist «f.» eine Hauptabteilung; beide
  stehen in 14 pt.
- **D2853 Archivplan:** Die Konvention aus der Verbesserungsrunde 2 gilt weiter, die Tabelle bleibt im Darin von 3. Kritisch
  sind dort andere Punkte (siehe K19–K21).
  - Das Soll hat **8 Einheiten statt 14**.
  - Deshalb muss beim Umsetzen das Fallset «Runde 2 D2853 Einheiten = 14» auf 8 gehen.
- **D3089 «2a», «2b»:**
  - Gemeint ist IV.2., nicht V.2.
  - Soll: IV.2a (Sch. 44, 1869–1907) und IV.2b (Sch. 45, 1869–1957) als E3 unter IV.2.
  - Schwere: **kritisch**, nicht mittel, wie ich zuerst geschrieben hatte. Das ist dieselbe Lage wie bei D175949 «A.1» und
    D177460 «D 1:1»: Signaturen der Unterstufe stehen im Darin der richtigen Eltern-Einheit, die Einheiten selbst fehlen.

## Stichprobe der nie geprüften Dateien (Pakete C1–C4)

**Auswahl** (`roh/np10_stichprobe.csv`, Seed 20261122):
- **Grundgesamtheit:** 509 Dateien in keiner Fundliste. Davon sind 21 in Runde 8 geändert; sie stecken in der
  Gegenprüfung als ERSTPRÜFUNG.
- **Gezogen wurden 55 Dateien:**
  - alle 27 Verdachtsfälle aus `roh/np9_verdacht.csv`;
  - 27 Zufallsdateien, geschichtet nach Gliederung × Umfang, proportional mit mindestens einer je Gliederungsart;
  - D3820 als grosse Dezimaldatei mit 715 Einheiten.
- Zusammen sind das 2'778 Einheiten.

**Prüfumfang:**
- Bis 60 Einheiten ist jede Einheit am PDF geprüft.
- Bei den grossen Dateien ist die Struktur ganz per Skript geprüft (D3468 852, D3820 715, D177460 167, D3898 102, D2861 99,
  D2828 90, D814 65), dazu 5–7 Seiten Einheit für Einheit.
- In allen Dateien ist jede Zeile im Blatt Vollständigkeit geprüft.

| Auswahl | Dateien | mit kritischem Fehler |
|---|---:|---|
| Zufall | 28 | 4: D2834, D177460, D175949, D3898 |
| Verdacht | 27 | 7: D2363, D814, D2828, D175827, D2853, D3468, D8947 |
| Runde 8 geändert (Erstprüfung in A1–A5) | 21 | 5: D1387, D2137, D3470, D847, D149825 |
| eigene Suchläufe (ausserhalb der Stichprobe) | – | 2: D2960, D434 |

**Was das bedeutet:**
- **Hochrechnung:** 431 nie geprüfte Dateien hat noch niemand angesehen. Nimmt man den Zufallsteil (14 %), sind darunter etwa
  60 mit kritischem Fehler, mit einem Bereich von 25 bis 135.
- **Verteilung:** Die kritischen Zufallsfunde liegen in den selteneren Aufbauten:
  - eine Tabelle mit eigener Spalte «Bez.» (D2834, 2 Einheiten);
  - «X n:m» (D177460);
  - Unternummern in der Titelspalte (D175949);
  - fette Ortsüberschriften (D3898).

  Die häufigen einfachen Arten (Vollsignatur bis 50 Einheiten, dezimal, fortlaufend, ohne Signaturen) waren im Zufallsteil
  mit 0 von 24 fehlerfrei.
- **Verdachtssignale:** Sie trennen schlecht, 7 von 27 Fällen gegenüber 4 von 28 im Zufallsteil.
  - N ist meist Titelblatt, Einleitung oder Biografie; Z meist Schachtel- oder Mappen-Einheiten nach Konvention.
  - Echt waren Z bei D2853 und D2363, N bei D8947 und V bei D175827.
- **Grenzen der Gegenprobe:** `sigliste` erkennt die Formen «X n:m», «A.1» und Vollsignaturen mit falschem Bestandsteil nicht.
  Die schwersten Funde kamen erst am PDF.

## Eigene Suchläufe über alle 715 Dateien

| Suchlauf | Treffer | bestätigte kritische Fehler |
|---|---|---|
| Nummer mit Kleinbuchstabe ohne Einheit (`np10_buchstabe_scan.py`) | 34 Zeilen in 9 Dateien | D2960 3a./5a., D10675 730a, D10744 430.1.733.1a–c, D2951 1.23a., D3472 1973.9a, D3470 (5), D3089 2a/2b; D2853 ist der Archivplan, kein Fehler |
| Signaturform in Folge ohne Einheit (`np10_darin_signatur.py`) | 336 Kandidaten, gefiltert 93 in 24 Dateien | D434 2.6.1., D3170 7.2.1.c./e., D847 38/50/219, D2828 32.; D152817 S. 33 ist kein Verlust (Teile) |
| Schachtel-Titel verschoben (`np10_behaelter_scan.py`) | 7 | nur D2363 und D814, beide schon aus der Stichprobe |
| Jahr.Laufnummer, Jahr passt nicht zur Seite | 4 | D3468 1947.7 und D3472 1967.18 (Zahlendreher → Teil der ersten Nennung); D3482 zweimal echte Fortsetzung |
| Verdacht und Ausreisser neu | – | Änderungen nur in den Runde-8-Dateien |

## Offene kritische Fehler (`offen_kritisch.csv`, 60 Zeilen)

**Nachtrag nach dem Bericht:** Die Hauptsession meldet weitere Korrekturen in ihrer Arbeitskopie; das Projekt steht
weiter auf 7fa7e161.
- Neu «in Arbeit» sind diese 9 Zeilen aus der Liste unten:
  - K2 D1387;
  - K6 D175827;
  - K8 D177460: laut Hauptsession 429 Einheiten «X n:m»; der Prüfer zählte 430/431 Zeilen, das gleiche ich in NP11 ab;
  - K9 D2137;
  - K14 und K15 D2828;
  - K25–K27 D3470.
- Neu ist K60 D260, eine Nebenwirkung der neuen D2137-Regel:
  - Ab :26 steht im PDF «V.B. c.23.» statt «V.A. c.23.», darum standen die 95 Einheiten :26–:120 im Darin von :25.
  - Das ist kritisch und war bisher nicht gemeldet. In der Arbeitskopie ist es behoben, von mir aber noch nicht am PDF
    gesehen.
- Zu beurteilen in NP11: In D175827 ändern sich laut Hauptsession 6 Darin-Verbindungen, weil der Anhang nicht mehr die
  Textspalte mitbestimmt.
- Damit bleiben **28 Zeilen in 16 Dateien offen und nicht zugeteilt**: D149825, D152817, D175949, D2363, D2834, D2850,
  D2853, D3018, D3089, D3271, D3468, D3472 (1967.18), D3898, D814, D847, D8947.
  - D2853 (K19–K21): Nur die Archivplan-Tabelle bleibt im Darin. Das erfundene «I.», 5. unter I. und die 5 Teile aus der
    Schachtelübersicht sind zu beheben.
  - D3089 (K23) ist kritisch.

**Offen und nicht zugeteilt, Stand des Berichts (37 Zeilen in 22 Dateien), nach Muster:**

- **Einheit im Darin**, Signaturen der Unterstufe, die das Skript nicht kennt:
  - D177460 K8: 430 × «X n:m»; D175949 K7: «A.1»–«Q.1», 25 Einheiten;
  - D847 K31–K35: «1Aa»–«1E», «38 1. Legat …», «50 2. Legat …», «219 1. …», «9 Orgelfonds Enge» = 92;
  - D2834 K17: «b)»/«c)» in der Spalte «Bez.»;
  - D3089 K23: 2a/2b;
  - D2137 K9: «V.G. c.45.:10./11.», Bestandsteil im PDF falsch geschrieben;
  - D2828 K14: 32.;
  - D3470 K25–K27: Zeilen ohne Titel.
- **Inhalt bei falscher Einheit:**
  - D2363 K10–K13 und D814 K30: Schachtel-Inhalt um eine Schachtel verschoben; `baue_behaelter_am_ende` liest die Nummer
    am Gruppenende, sie steht aber vorn;
  - D3898 K29: 16 fette Ortsüberschriften im Darin der vorigen Einheit;
  - D3271 K1: «Buchhaltungsjournal»;
  - D2828 K15 und D175827 K6: Anhang im Darin der letzten Einheit. Regel 4 greift nur auf den letzten zwei Seiten und nicht
    bei «Anhang: <Text>»;
  - D149825 K4: Messingpokal ohne Nummer nach 272.
- **Eltern/Ebene falsch:**
  - D3468 K24 und D3472 K28: Zahlendreher im Jahr; eine Einheit wird Teil einer fremden Einheit;
  - D152817 K5: «VI.SB.103.» = C.103. hängt am Bestand;
  - D1387 K2: Behälterzeilen «Schachtel 1 (V.F. c.18.:1)»;
  - D2853 K20: 5. unter erfundenem I.
- **Einheit erfunden:**
  - D2853 K19 «I. Verzeichniss …» und K21: 5 Teile aus der Schachtelübersicht S. 5;
  - D8947 K36: «1. Kuvert»/«2. Kuvert».
- **Text weg:**
  - D8947 K37: Objektbeschreibung, 18 Zeilen vor der ersten «Signatur»;
  - D149825 K3: Protokollband ohne Nummer vor 1.;
  - D2850 K18: «SATUS» in der Briefliste;
  - D3018 K22: «Cakeplatte» (Runde 8).
- **Einheit fehlt:** D2834 K16: a) steht nur als «Text vor der ersten Signatur»; die Spalte «Bez.» wird nicht erkannt.

**In der Arbeitskopie der Hauptsession behoben (14 Zeilen K46–K59):** D10675, D10744, D2951, D2960 (3), D3170, D3470 (5),
D3472 1973.9a, D434. Das muss die nächste Gegenprüfung bestätigen.

**Bewusst offen (8 Zeilen K38–K45):** D149622, D1739, D1858, D2614, D3208, D3826, D3828 3.4., D512.

**Schwere herabgesetzt** (Spalte `entscheid` in `funde_nachpruefung10.csv`):
- D140969 87.: Das PDF ist widersprüchlich.
- D176772 2.5./2.6.: Das Findmittel ist mehrdeutig; ein Hinweis genügt.
- D175827 2.2.: Die Signatur steht nur in der Übersicht.
- D3462 «1.8.)»: nur ein Querverweis.

Alle vier sind jetzt mittel.

## Vorschläge für Runde 9

1. **Signaturspalte allgemein:** Jede Zeile wird eine Einheit, deren erstes Wort in der Signaturspalte der Datei steht (gleiches
   x, gleiche Schrift) und eine Signaturform der Datei hat, auch eine erweiterte.
   - Erweiterungen sind z. B. Buchstabenzusatz «3a.»/«1Aa», «:m» nach «X n», «.m» ohne Schlusspunkt nach «A», «a)» in eigener
     Spalte.
   - Das gilt auch ohne Titel (nur Datum oder Schachtel) und trotz einer Ordnungszahl danach («38 1. Legat»).
   - Die Eltern folgen aus der Form:
     - «n» → «na»: Geschwister;
     - «X n» → «X n:m» und «A» → «A.1»: Kind.

   Das würde den grössten Teil der Muster «Einheit im Darin» lösen.
2. **Anhang:** Regel 4 auch für «Anhang: <Text>» und auf früheren Seiten anwenden, wenn danach keine Signatur der
   Verzeichnisfolge mehr kommt (D2828, D175827).
3. **Behälter vorn oder hinten:** `baue_behaelter_am_ende` am Zeilenabstand in der Gruppe entscheiden. Eine Folgezeile dicht
   unter einer Nummernzeile gehört zu ihr (D2363, D814).
4. **Jahr.Laufnummer:** Eine wiederkehrende Signatur, deren Jahr nicht zu den Nachbarn passt, ist eine eigene Einheit mit
   Hinweis und kein Teil der ersten Nennung (D3468, D3472).
5. **Regel 14:** Posten der Kurzliste ohne Gegenstück in der Zusammenfassung bleiben im Darin der letzten Einheit (D3018).
6. **Gruppen- und Ortsüberschriften** wie in Regel 18 der folgenden Einheit zuordnen, auch ohne Bandzahl (D3898) und ohne
   Absatz davor (D3271).
7. **Bei der Umsetzung anpassen:** das Fallset Runde 2 für D2853 (14 → 8). D177460 liegt auch in `testdaten/`; der
   Regressionssatz ändert sich also.

**Danach:**
- Gegenprüfung der Runde 9.
- Die **ausgeweitete Prüfung der 431 Dateien**, die noch niemand angesehen hat. Am besten in Paketen zu rund 25 Dateien, die
  selteneren Aufbauten und Dateien über 50 Einheiten zuerst.
- Vorher ein Suchlauf «Signaturzeilen ↔ Einheiten» mit dateieigenen Signaturformen; `sigliste` reicht dafür nicht.

## Dateien

- `offen_kritisch.csv`: 59 Zeilen K1–K59.
  - Spalten: nr, datei, signatur_id, seite, feld, befund_jetzt, soll, ursache, status, erstmeldung, bewusst_offen,
    in_arbeit_hauptsession, k_alt, paket, muster, entscheid, bemerkung.
  - `k_alt` ist die Nummer aus Nachprüfung 9; die alte Liste liegt in `roh/np9_offen_kritisch.csv`.
- `funde_nachpruefung10.csv`: alle 258 Fundzeilen der Pakete A1–A5, C1–C4 und S (eigene Suchläufe), mit `paket`, `k_alt`,
  `entscheid` und `in_arbeit`.
- `roh/np10_dateien_urteil.csv`: Urteil je Datei der Stichprobe und der Erstprüfungen in A5.
- `roh/np10_<Paket>_{urteile,funde,notizen,dateien_urteil,altzeilen,dateien}.*`, `roh/np10_vgl/` (62 Vergleiche), `roh/np10_soll/`
  (Soll-Listen D2853 und D175949).
- Suchläufe: `roh/np10_stichprobe.csv`, `roh/np10_population.csv`, `roh/np10_buchstabe_scan.csv`,
  `roh/np10_darin_signatur*.{csv,txt}`, `roh/np10_behaelter_scan.csv`, `roh/np10_verdacht.csv`, `roh/np10_textverlust2.csv`,
  `roh/np10_sigcheck.txt`, `roh/np10_sigliste_stichprobe.txt`.
