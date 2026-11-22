# NP13 – Vorbereitung (22.11.2026, vor der Installation von Runde 10)

## Ablauf nach «Runde 10 installiert»

1. `bash start13.sh`:
   - Skript und Projektstand (findmittel_excel, testdaten_excel, D151210) als Kopie;
   - Gesamtlauf, Testdaten, D151210;
   - Zellvergleiche: Projekt gegen eigenen Lauf, Runde 9 gegen Runde 10;
   - Fallsets A, B, C, F, Runde 2, Punkt 2;
   - Suchlauf Tippfehler.
2. `stichproben/runde10/` lesen (AENDERUNGEN_RUNDE10.md, geänderte Dateien). Die vorher/-Kopie der Hauptsession gegen
   `np12/aus_neu` vergleichen; sie muss zellgleich sein.
3. **G-Pakete:**
   - von Runde 10 geänderte Dateien, je Regelgruppe;
   - mit den K-Zeilen aus `offen_kritisch.csv` (81 Zeilen) als Altzeilen;
   - besonders auf Fehlgriffe der erweiterten Schlussblock- und Überschriftenregeln achten.
   - Werkzeuge: Prüfmappen `np12/pruefmappe.py`, Kompaktmappe `np12/mappe_kompakt.py`, Strukturbericht `np12/strukturbericht.py`.
4. **Suchlauf Tippfehler:** `tipp_r10.csv` gegen `tipp_r9.csv` (unten). Die Kandidaten sehe ich selbst am PDF nach.
5. **Zufallsstichprobe:**
   - die ersten 60 Dateien aus `zufall_reihenfolge.txt`, die weder in `offen_kritisch.csv` stehen noch von Runde 10 geändert
     sind;
   - festgelegt vor Runde 10 mit `random.Random(20261122)`;
   - ganz geprüft wie die Pakete P/L der NP12;
   - Restrate = Anteil kritischer Dateien unter den geprüften und unveränderten Dateien ohne bekannte K-Zeile.

## Suchlauf «Tippfehler in Dezimalsignaturen» an Runde 9 (Basis)

- **Werkzeug:** `suchlauf_tippfehler.py`. Es ordnet jede Einheit über den Zeilen-Cache in die PDF-Folge ein; verankert sind
  50'425 von 51'170 Einheiten.
- **Arten:**
  - **AEHNLICH:** Die Signatur weicht in 1–2 Zeichen von der Signatur ab, die die PDF-Nachbarn erwarten lassen, und die
    Einheit hängt dadurch unter anderen Eltern.
  - **AEHNLICH_DA:** dasselbe, die erwartete Signatur gibt es aber schon.
  - **TEIL:** Eine Signatur kommt genau zweimal vor, mit anderem Titel, und die Nachbarnummer fehlt.
- **Ergebnis an Runde 9:** 16 Zeilen.
  - **Bekannt (9):**
    - D149628: K124 20.1.2.19., K125 28.1.1.3., K126 29.2.9.;
    - D150296: K149 3.3.7.;
    - D2857: K132 1.224.3.;
    - D32837: K129 1.1.2.1.1.;
    - D4054: K139 10.8.2.10., K140 10.8.4.;
    - D176060: K135 7.4.1.26. Teil 2.
  - **D151210 4.1.2.38. (S. 115):**
    - steht zwischen 4.1.3.37. und 4.1.3.39.;
    - NP6 hat den Fall nach Entscheid 5 als «kein Fund» gewertet: eigene Einheit, Signatur wie im PDF;
    - NP12 hat gleich gebaute Fälle (K124, K139, K149) kritisch gewertet;
    - das ist widersprüchlich; in NP13 einheitlich werten und die Frage der Hauptsession melden.
  - **D3472, stark:**
    - 1952.8 zweimal (Hochwald / Horgen); 1952.9 fehlt;
    - 1952.14 zweimal (Locarno / Mauvoisin); 1952.15 fehlt;
    - der zweite Eintrag wird Teil 2 des ersten;
    - gleich wie D1473/D1479 (K70/K80, kritisch).
  - **Schwach (Planlisten mit oft mehrfach vergebenen Nummern und Lücken):**
    - D3468 1958.16: Plan-Nr. 559 zweimal, wohl echt;
    - D3468 1983.11 (1983.10 fehlt);
    - D3482 1953.25;
    - D3484 405 (404 fehlt).
- **Fehlalarme**, inzwischen ausgeschlossen:
  - führende Nullen (D10675 011);
  - Buchstabenzusatz (D2960 3a);
  - mehrere Bestände in einer Datei (D152817);
  - Ziffern angehängt (D3774 2.4. → 2.41.);
  - Verankerung an «1+2 (…)» (D10675 762.1).

## Ablauf am 22.11.2026 (nach «Runde 10 installiert»)

1. `np13_start13.sh`: Stand sichern (Skript, findmittel_excel, testdaten_excel, D151210), Gesamtlauf, Testdaten, D151210,
   Zellvergleiche, Fallsets, Suchlauf Tippfehler. Ergebnis: zellgleich, 66 Dateien geändert (= Liste der Hauptsession),
   `runde10/vorher/` zellgleich mit dem eigenen Lauf der Runde 9.
2. Fallsets: Soll-Zeilen A (D2962 ID 69), B (D3063 ID 68) und Runde 2 (D3808 «Beilagen:» in der Bestandszeile VII.65.)
   nachgeführt; Sicherung im Scratchpad `np13/fallsets_vorher/`.
3. `np13_mappen13.sh`: Vergleiche Runde 9 → 10 (66 Dateien, dazu Testdaten D152810/D3031), Prüfmappen, Kompaktmappen,
   Strukturberichte für die 66 Dateien und die 60 Stichprobendateien.
4. Regel 9 selbst an der PDF-Folge geprüft (`roh/np13_regel9.txt`).
5. Pakete nach `roh/np13_AUFTRAG13.md`: G1 (Regeln 1–5, 22 Dateien), G2 (6–8, 16), G3 (9, 10, 11, 17; 13 + 2 Testdateien),
   G4 (12–16, 9), G5 (11–13 in sechs grossen Dateien), Z1–Z3 (Zufallsstichprobe, je 20 Dateien ganz geprüft).
6. Suchläufe über alle 715 Dateien:
   - `np13_suchlauf_tippfehler.py` (Runde 9 und 10, dazu Testdaten);
   - `np13_suchlauf_info_stuecke.py` (Stück ohne Nummer im Blatt Info, nach dem Fund D151759 von Z3);
   - Suchlauf «n.a als Kind» von G3 (`roh/np13_G3_*`, Skript in tmp_G3), Treffer von der Prüfsession nachgesehen.
7. `np13_zusammen13.py <pakete> <offen_kritisch_alt.csv> <aus>`: K-Nummern stabil, neue ab K183. Die Entscheide der
   Prüfsession stehen im Skript (HERAB: kritischer Teil behoben, Rest mittel; NOTIZ: Begründung, Schwere bleibt).
