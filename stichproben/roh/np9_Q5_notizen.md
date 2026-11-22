# Q5 – offene kritische Funde am Stand e896fb6c (Nachprüfung 9, Paketart B)

**Grundlage:** Excel aus `$NP9/aus_neu`. Für alle 12 Dateien ist das Blatt scope-Import zellgleich mit `findmittel_excel` und
mit 1f98df0b; der Nachtrag ändert keine davon. D3031 ist eine Testdatei und ist an `$NP9/test_neu9` (= `testdaten_excel`)
geprüft. Jede Zeile ist am PDF nachgesehen (pdftotext, Zeilen-Cache mit x und Schrift).

**CSV:** `ist` = Stand der Vorrunde (altes `neu_ist`). `soll` ist präzisiert (Einheiten, Eltern, Titel, Zeitraum, Schachtel).
Bei «behoben» bleibt die Schwere des Funds stehen, wie in `funde_nachpruefung8.csv`.

## Bilanz: 13 Altzeilen, 2 neue Zeilen
| Status | Anzahl | Zeilen |
|---|---:|---|
| behoben | 3 | D3031 V.2.–V.4. (seit 18:11); D3612 3.A./3.E. (seit 2953088e, bestätigt); D3861 7.1. (seit 5e333035) |
| teilweise | 6 | D3060, D3089, D3105 (weiter kritisch); D3271 4.2.22. (jetzt gering); D3808 (jetzt mittel, 1. bestätigt); D3505 7.3. (jetzt mittel) |
| offen | 4 | alle kritisch: D3012; D3208 (bewusst offen); D3826 20. und D845 1.2 (beide in Arbeit, unverändert) |
| schlechter | 0 | – |
| neu | 2 | D3271 4.2. (kritisch); D3612 «Mappe 6» (mittel) |

## Je Datei
- **D3012:** Die Gliederung 1)–8) ist nicht erkannt. Soll sind 14 Einheiten, jetzt 5: 1.–8. fehlen, 8.a/8.c sind Teile von c., «Oberstadtgass» fehlt im Import. Merkmal: «n)» fett bei x 70.9 über eingerücktem «a)».
- **D3089:** Das Detail der Rollen- und Textbücher (S. 16–35) steht bei X. statt bei VIII.1./VIII.2. Zuordnung über die Schachtelnummer der Köpfe (55 → VIII.1., 62 → VIII.2., 70 → X.); X. dann 1866–1956 und Schachtel 68–73; «Bestand geordnet … Caduff» ins Blatt Info.
- **D3105:** «Band 1» fehlt als Einheit, weil `BEHAELTER_RE` kein «Band» kennt. Die Signaturform ist zu entscheiden.
- **D3060:** Das Porträtbild (S. 8, ohne Überschrift) steht in :6 statt in :10. Einzelfall.
- **D3208 (bewusst offen):** Nötig wären die Abzeichensammlung als eigene Einheit (Signatur bilden, 1909–1963), die Verweise S. 4 als «Verwandte Verzeichnungseinheiten» und für :2 der Zeitraum 1902–1964.
- **D3826 und D845:** in Arbeit (Hauptsession). Der Stand jetzt ist unverändert, das genaue Soll steht in der CSV.
- **D3271:** 4.2.22. ist erledigt, die Schachtelangabe steht nur im Hinweis (gering). **Neu:** 11 Gruppenüberschriften in 4.2. (x 127.7, z. B. «Kassenbelege (2 Bände)», «Notizen (2 Bände) (Die Bände …)») stehen im Darin der vorigen Einheit; die Bände heissen nur «Bd. n:».
- **D3808:** Beilagen und «chr Stand» stehen im Blatt Info, 4. hat 1906–1907. Rest: Titel «Protokoll 1» usw. mit der Bandzahl (mittel).
- **D3505:** 7.3. ist richtig. Die Schachteln 1 und 2 aus dem Schlussblock sind nicht zugeordnet (mittel).
- **D3612:** behoben. **Neu:** «Mappe 6» fehlt in 6. und steht als Hinweis bei 7.; Nebenwirkung von Runde 2 Änderung A.
- **D3861:** behoben; die Zeiträume aus Amtszeiten bleiben mittel (Z177). **D3031:** behoben; bei V.3. fehlt Schachtel 315 (gering).

## Nebenbei, nicht in der CSV
- **D3089 VII.1.:** «Plakate (1934-1960)» hat keinen Zeitraum; das Blatt Vollständigkeit meldet «1934 1960» als fehlend (mittel). **D845 1.:** steht zweimal, S. 1 «Theater. Verzeichnis» und als Detailkopf S. 5 «Stadttheater» (Teil 2, ID 2); wie D3190, dort bewusst offen.

## Unsicherheiten
- **Schwere der neuen Funde, beides Grenzfälle:** D3271 als kritisch (Gruppenbeschreibung in fremder Einheit, aber kein Textverlust); D3612 als mittel (die Mappenmarke steht nur im Prüfhinweis).
- **Signaturen ohne Nummer im PDF** (D3105 Band, D3826 Mappe, D3208 Abzeichen) sind eine Konventionsfrage.
- **D3060 und D3208** lassen sich nur mit Einzelregeln lösen; «bewusst offen» ist vertretbar.
- **D3826 und D845** sind am Projektstand 22.11. 01:01 geprüft; spätere Änderungen der Hauptsession sind nicht berücksichtigt.
