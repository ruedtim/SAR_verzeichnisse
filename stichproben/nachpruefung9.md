# Neunte Nachprüfung: Nachtrag e896fb6c und offene kritische Fehler, 22.11.2026

Diese Runde hatte zwei Aufträge der Hauptsession:
1. die 14 Dateien gegenprüfen, die der Nachtrag nach der Nachprüfung 8 gegenüber 1f98df0b geändert hat;
2. alle noch offenen kritischen Fehler aus den Nachprüfungen 1–8 auflisten, am aktuellen Excel nachgesehen.

Das Ergebnis der Liste steht in `offen_kritisch.csv`, alle Funde der Runde in `funde_nachpruefung9.csv`.

- **Skript:** sha256 `e896fb6c54b4e64a…`, gepusht als 844ccb6. Schnappschuss in `…/scratchpad/neu9/`, Läufe in
  `…/scratchpad/np9/`.
- **Projekt:** Skript, `findmittel_excel/`, `testdaten_excel/` und D151210 habe ich nicht angefasst. Die Korrekturen, die die
  Hauptsession in ihrer Arbeitskopie macht (D152404 VIII./VIIIa., D1874 Reg. unter 1.), sind hier noch nicht enthalten.

## Kurzfazit

- **Der Nachtrag hält, was er verspricht, und bringt keinen neuen kritischen Fehler.**
  - Die Excel im Projekt sind genau die Ausgabe von e896fb6c.
  - Geändert sind genau die 14 genannten Dateien mit 134 Einheiten.
  - D151210 und die Testdaten sind zellgleich mit vorher.
  - Die Hierarchie ist in allen 715 Dateien in sich stimmig, und es geht kein Text verloren.
  - Gliederung am PDF: 119 Einheiten besser, 15 gleich (D1874, nur der Hinweis «Kein Zeitraum» ist gewandert), 0 schlechter.
  - Schlechter sind nur 3 Zeiträume (D3313 1. und 3., D3566 1.), siehe unten.
- **Kritisch behoben, am PDF bestätigt:**
  - D2850: Datums-Signaturen, 65.A., Schlussblock «Stadtarchiv Zürich», Titel von 66;
  - D3810: erfundene 8.–21., fehlende «8. Nachträge»;
  - D3313: 42 erfundene Einheiten aus der Porträtliste.
  - Bestätigt behoben aus früheren Runden: D3612 3.A./3.E., D3861 7.1. und D3031 V.2.–V.4.
  - Nur noch mittel oder gering: D3808, D3505 7.3., D3271 4.2.22., D141024, D150689 und D2850 65 (Zeitraum).
- **Offen sind noch 29 kritische Fehler in 26 Dateien** (`offen_kritisch.csv`).
  - 11 bearbeitet die Hauptsession gerade (2 davon sind in ihrer Arbeitskopie schon behoben).
  - 7 sind von der Hauptsession bewusst offen gelassen.
  - 11 sind noch niemandem zugeteilt.
  - 7 der 29 sind in dieser Runde neu gefunden, alle schon älter als der Nachtrag.
- **Wichtige Einschränkung:** Die Liste deckt nur die 208 Dateien ab, die je in einer Fundliste standen. Für die übrigen 509
  gibt es nur automatische Suchläufe.
  - Ein solcher Suchlauf hat in dieser Runde mit D3727 einen neuen schweren Fall gefunden.
  - «Keine kritischen Fehler mehr» lässt sich deshalb erst sagen, wenn auch diese Dateien geprüft sind (Vorschlag am Ende).

## Teil 1: Gegenprüfung des Nachtrags

**Methode:**
- Eigener Gesamtlauf mit e896fb6c. Er ist zellgleich mit `findmittel_excel/`, `testdaten_excel/` und D151210.
- Vergleich mit 1f98df0b je Datei über die Signatur ohne «:» plus n-tes Vorkommen (`roh/np9_vgl/`).
- Gegenproben wie in Nachprüfung 8: Hierarchie, Textverlust gegen die PDF-Wortzahl, Einheit gegen PDF-Zeile und die
  Strukturprüfung.
- Drei Prüfer am PDF: Q1 D2850, D1874, D152404; Q2 D3810, D3842, D3313, D3566; Q3 D3828, D512, D3484, D3018, D3530,
  D152781, D176795.

**Kennzahlen:**

| Prüfung | 1f98df0b | e896fb6c |
|---|---:|---:|
| Einheiten | 48'980 | 48'920 |
| «[ohne Titel]» | 31 | 30 |
| Text erfasst 100 % | 695 | 695 |
| doppelte Schlüssel | 10 | 10 |
| Signal J (Jahr in der Signatur) | 2 | 0 |
| Signal Z (viele Schlussvermerke) | 4 | 3 |

Die Fallsets sind unverändert, nachgerechnet: A 11/12, B 36/38 und C 9/12 nach ID (nach Signatur 37/38 und 10/12), F 5/7,
Runde 2 33/34, Punkt 2 38/38.

**Ergebnis je Regel des Nachtrags (Einheiten am PDF):**

| Nachtrag | Wirkung | Urteil |
|---|---|---|
| 1 D2850 | 2.1939/12.1961 weg, 53 vollständig; 65.A. weg; die 73 Namen ab «Stadtarchiv Zürich» wieder im Darin von 56; Blatt Info nur noch S. 24; 66 mit Titel | 9 besser |
| 2 Masse, Wortkürzel | D1874 3. ohne «1260», Reg./Reg. 1–5 sind Einheiten; D152404 Va./Vb. sind Einheiten | 12 besser, 15 gleich |
| 3 offene Spannen | D3828 3.17. Nr. 33, 6., 7.; D512 14 Spannen in 12 Saisons; D3484 489./490.; D3018 05.7.2. (Teil 2 ohne Datum ist richtig) | 19 besser |
| 4 Bibliografie | D3530 2.3. = 1922–1975 | 1 besser |
| 5 Titel mit «:» | D152781 5.1. «Persönliche Dokumente» 1923–1937, 5. 1921–1937; D176795 1.3., 1.4. | 4 besser |
| 6 Liste in der Textspalte | D3810 8. «Nachträge» mit Schachtel IV; D3842 ohne erfundene 3./4. | 18 besser |
| 7 Liste in kleiner Schrift | D3313 Porträtliste im Darin von 4.; D3566 Beschlusspunkte im Darin | 56 besser, 3 gleich, 3 schlechter (Zeitraum) |

Durch die Regeln 6 und 7 verschwindet keine echte Einheit im Darin. Q2 hat das in allen vier Dateien Zeile für Zeile geprüft.

**Schlechter durch den Nachtrag, beides mittel:**
- **D3566 1. «Originale»:** 1519–1953. Die Jahre stammen aus der Literaturangabe «Zürcher Pfarrbuch, 1519-1952, Zürich 1953».
  Soll: 11.02.1798–13.09.1805, die Druckdaten von Nummer 1 bis Nummer 10.
- **D3313 1. und 3.:** jetzt nur noch der Jahrgang (Genau 1786 bzw. 1810), ohne Prüfhinweis. Soll: 1834–1863 bzw. 1885–1887
  aus der Titelklammer, die als Lebensdaten verworfen wird. 2. hat 1804–1854, soll 12.05.1854.
  - Damit trifft der Punkt «Jahrgangsjahr gilt als Beginn» im Nachtrag nicht mehr zu.

**Weitere Funde:** 11 mittel und 4 gering, alle schon vor dem Nachtrag:
- D3566 2.: Zeitraum 1336–1962 aus Zitaten.
- D3566 S.3.: «max / 28. März 2000» steht im Darin statt im Blatt Info.
- D3810 3.–6.: Schachtel II fehlt; die Titel von 1. und 7. sind abgeschnitten.
- D3842 1.: Die Schachtel «1» steht im Titel.
- D176795 1.2. und 2.3.10.3. ff.: Inhalt steht im Titel.
- D1874 1.10. und 1.30.: Titel.

## Teil 2: Offene kritische Fehler

**Sammlung:**
- Grundlage sind alle Fundzeilen mit Schwere «kritisch», jeweils im letzten Stand aus den Nachprüfungen 6–8. Die
  Nachprüfung 6 hat alle offenen Zeilen der Runden 1–5 übernommen; ich habe nachgezählt, dass keine kritische Zeile unterwegs
  verloren ging.
- Das ergab 36 Zeilen.
- Davon lagen 10 in den Nachtrag-Dateien (Q1–Q3). Die übrigen 26 haben zwei Prüfer am Stand e896fb6c und am PDF nachgesehen
  (Q4, Q5), mit genauem Soll.
- Hinzu kommen die neuen kritischen Funde aus Teil 1 und mein Fund D3727.

**Ergebnis:** 29 offene kritische Fehler in 26 Dateien.

### Nicht zugeteilt (11)

| K | Datei | Fehler | Soll (kurz) |
|---|---|---|---|
| K1 | D1746 | II.A.–II.O. und VII.1./VII.2. fehlen («A)»–«O)», «1)»/«2)» in der Signaturspalte); II.1., VII.3., VII.4. sind aus Listennummern erfunden | 14 Einheiten II.A.–II.O. unter II., VII.1./VII.2. unter VII. |
| K2 | D1880 | Die dritte Ebene fehlt: kursive «a.»–«i.» unter F.III. und H.II. (41 Einheiten bzw. Teile, rund 300 Zeilen im Darin) | eigene Einheiten unter F.III./H.II. |
| K3 | D3012 | «1)»–«8)» sind keine Signaturen; von 14 Einheiten gibt es 5, «Oberstadtgass» fehlt ganz | 1.–8. mit a.–c. darunter |
| K4 | D3018 | Rest von S. 78 (Bilder Sch. 76, Nachtrag 1/2, «Cakeplatte (Keramik)») steht im Darin von 08.8. | zu 08.9./09. |
| K5 | D3060 | Block ohne Überschrift (Porträtbild Anna Asper, grf. Schachtel) steht bei Sch. 6 statt bei Sch. 10 | Zuordnung nach Wortlaut, Einzelfall |
| K6 | D3089 | Detailverzeichnisse der Rollen- und Textbücher (S. 16–35) stehen bei X. statt bei VIII.1./VIII.2. | nach Schachtelnummer der Köpfe: 55 → VIII.1., 62 → VIII.2., 70 → X. |
| K7 | D3105 | «Band 1» ist kein Behälter, sein Inhalt steht bei Schachtel 2 | Behältermarke «Band», eigene Einheit |
| K8 | D3271 | 11 Gruppenüberschriften in 4.2. («Kassenbelege (2 Bände)» …) stehen im Darin der vorigen Einheit; die Bände heissen nur «Bd. n:» | Überschrift gilt für die folgenden Nummern (Hinweis bzw. Titelteil) |
| K9 | D3566 | «S. Vögelin, …» (Titel von Nummer 12 unter 2.) wird erfundene Einheit «:S.» | Zeile im Darin von 2. |
| K10 | D3566 | echte «3. Kopierte Briefe …» heisst :S.3. unter S. | VII.340.:3. auf E1 |
| K11 | D3727 | Datums-Tippfehler «01.12.0982», «02.08.0988», «01.09.0988» (S. 49, 60) werden erfundene Einheiten 47–49 mit rund 980 Darin-Zeilen aus 10.3. | alles im Darin von 10.3. bis vor 10.4. (S. 69) |

Hinweise zur Tabelle:
- Bei K8, K9, K10 und K11 hat ein Suchlauf über alle 715 Dateien keinen weiteren Fall gefunden. Es sind Einzelfälle mit
  klarem Merkmal.
- K3, K6 und K7 brauchen eine Konvention für Nummern oder Behälter ohne Signatur; die Prüfer haben das Nötige je Zeile
  beschrieben.

### In Arbeit bei der Hauptsession (11)

| K | Datei | Fehler |
|---|---|---|
| K19, K20 | D134644 | «2. Stammbuch» aus 1.2. ist Hauptnummer. Neu (K20): «11.1. Stadt Zürich» ist ein Tippfehler für 10.1., darum hängt der Inhalt von 10. unter 11. «Dias» und die echte 11.1. ist Teil 2. |
| K21, K22 | D140969 | 50a, 88 und 89 fehlen. |
| K23 | D151730 | Der Anhang S. 4 steht im Darin von 19.5. |
| K24 | D152404 | :VIII. und :VIIIa. fehlen. In der Arbeitskopie behoben. |
| K25 | D152817 | 5 Bereiche sind Eltern von 7 Schachteln mit 10 fremden Abschnitten. |
| K26 | D1874 | Reg. hängt oben am Bestand statt unter 1. In der Arbeitskopie behoben. |
| K27 | D2850 | 55 ist leer, die A–M-Liste steht in 56. |
| K28 | D3826 | 20.: Darin. |
| K29 | D845 | 1.2 fehlt («V.C: c.52.:1.2»). |

### Bewusst offen (7)

| K | Datei | Fehler |
|---|---|---|
| K12 | D149622 | Rest am Ende von Sch. 3: Anmerkungen zu 1757/1795, Signaturvermerk. |
| K13 | D1739 | «Mappe mit Grossformaten» im Darin von Sch. 28. |
| K14 | D1858 | Gliederung nach Schachteln 1–20. |
| K15 | D2614 | 12 der 14 Bestände fehlen als Zeilen. |
| K16 | D3208 | Drei Listen im Darin von Sch. 2. |
| K17 | D3828 | 3.4. «Akten zu verminten Brücken» (Tippfehler im PDF). |
| K18 | D512 | 14 Angaben der Datumsspalte fehlen noch, vorher 22. |

Je Zeile steht in der CSV, was nötig wäre. Nach der Schwere-Definition bleiben alle sieben kritisch.

## Ungeprüfte Dateien

`methode/np9_verdacht.py` sucht über alle 715 Dateien nach Signalen (Liste `roh/np9_verdacht.csv`, ungeprüft). Gesucht wird
nach:
- grossem Vorspann mit Signaturen, die nur dort stehen;
- vielen Schlussvermerken;
- vielen nicht übernommenen Zeilen;
- «Text erfasst» unter 100 %;
- Einheiten ohne Zeilenanfang im PDF.

In 33 der 509 nie geprüften Dateien gibt es solche Signale. Angesehen habe ich D814, D2363, D3727, D175827, D3742, D3593,
D3293 und D3415:
- Echt und kritisch ist nur D3727 (K11).
- Die übrigen sind Schachteltabellen («Schachtel n» als Nummer), Einleitungen und Titelblätter, also keine Fehler.
- D175827 ist eine Konventionsfrage: 2.2. «Inventare» steht nur in der Inventarübersicht, im Detail als Spiegelstrich.

Die Signale sind verrauscht und fangen Fehler wie D3566 oder D3271 nicht. Für das Ziel «keine kritischen Fehler mehr» reicht
die Suche deshalb nicht.

## Vorschlag für die nächsten Runden

1. **Zuerst die 11 nicht zugeteilten Fälle** aufteilen. K8–K11 sind Einzelfälle mit klarem Merkmal, K1–K3 und K6 grössere
   Gliederungsfälle.
2. **Nach jeder Korrektur eine Gegenprüfung** der geänderten Dateien wie in dieser Runde.
3. **Die 509 nie geprüften Dateien:** Entweder alle in Paketen am PDF prüfen, nur auf kritische Fehler, also verlorene oder
   erfundene Einheiten, falsche Eltern, Inhalt in der falschen Einheit und verlorenen Text, mit einem Prüfer je rund 25
   Dateien. Oder zuerst eine Zufallsstichprobe ziehen, zum Beispiel 50 Dateien, und daraus die Fehlerrate schätzen. Das ist
   eine Entscheidung über den Aufwand.

## Ablage

- **Berichte:** `nachpruefung9.md`, `offen_kritisch.csv` (29 Zeilen) und `funde_nachpruefung9.csv` (104 Zeilen).
- **Spalten von `offen_kritisch.csv`:**
  - nr, datei, signatur_id, seite, feld;
  - befund_jetzt, soll, ursache;
  - status (offen, teilweise oder neu) und erstmeldung (Runde der ersten Meldung, NP0 = Stichprobe vom 19.11.);
  - bewusst_offen, in_arbeit_hauptsession, paket, bemerkung.
- **Spalten von `funde_nachpruefung9.csv`:** wie in Runde 8.
  - `ist` ist der Stand der Vorrunde, `neu_ist` der Stand e896fb6c.
  - Der Status ist behoben, teilweise, offen, schlechter, neu oder «ungeprüft». Ungeprüft sind 31 mittlere und geringe
    Altzeilen, deren Einheit der Nachtrag nicht geändert hat.
- **Rohdaten:**
  - `roh/np9_Q1…Q5_funde.csv`, `_notizen.md`, `_urteile.csv` (Q1–Q3);
  - `roh/np9_Q*_altzeilen.csv` und `np9_Q*_kritisch.csv`;
  - `roh/np9_vgl/`, `roh/np9_kritisch_offen_alt.csv` (die 36 Ausgangszeilen) und `roh/np9_verdacht.csv`.
- **Methode:** `methode/ANLEITUNG_NACHPRUEFUNG9.md`, `np9_offen_kritisch.py` und `np9_verdacht.py`.
