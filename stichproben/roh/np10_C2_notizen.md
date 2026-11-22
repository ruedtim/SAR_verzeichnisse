# C2 – Nachprüfung 10, Paketart C (13 Dateien, Stand 7fa7e161)

## Bilanz
- 11 Dateien ohne kritischen Fehler, 2 kritisch: D2363 (4 Funde), D175827 (2). Zusammen 6 kritisch, 12 mittel, 6 gering.
- Je Datei (k/m/g): D141062 0/0/2 · D175827 2/2/0 · D1918 0/1/0 · D2363 4/0/1 · D2508 0/2/0 · D3043 0/1/0 ·
  D3293 0/0/0 · D3382 0/1/0 · D3415 0/0/0 · D3561 0/1/0 · D3575 0/0/0 · D3596 0/1/0 · D3820 0/3/3.
- Bis 60 Einheiten jede Einheit am PDF, dazu Blatt Vollständigkeit und Schlussvermerke. D3820: Skript `tmp_C2/struktur.py`.
  - 716 Signaturzeilen auf S. 3–33 gegen 715 Einheiten; 0 Abweichungen bei Eltern, Ebenen, Folge und Stufen.
  - Datumsspalte aller 612 datierten Zeilen gegen von/bis (`zeitraum_check.py`): 2 Abweichungen.
  - Einheit für Einheit: S. 3, 11, 20, 22, 33 (Zufallsseiten mit Seed 20261122).

## Wichtigste Funde
1. **D2363 (Mappen/Schachteln), kritisch.** Zeilen stehen bei der falschen Schachtel (:5/:6, :7/:8, :8/:9, :9/:10).
   - `baue_behaelter_am_ende` setzt am_ende=True, weil die Tabellenzeilen gleichmässig 20 pt auseinander liegen.
   - Im PDF steht die Nummer aber in der ersten Zeile der Gruppe (Spaltenkopf «Akte / Dossier Schachtel-Nr.»).
   - Beispiel: :6 hat den Titel «Tschernobylkinder …», der zu :5 gehört.
   - Suchlauf lohnt sich: Mappen/Schachteln-Dateien mit am_ende und Spaltenkopf «Schachtel-Nr.».
2. **D175827, kritisch.** «Anhang: Darstellungen zur Zunft Hottingen …» (S. 9–10) steht im Darin von 10.
   Regel 4 prüft mit `re.fullmatch(r"Anhang\s*:?")`; «Anhang: <Text>» fällt durch (wie K23).
3. **D175827, kritisch (Grenzfall).** 2.2. «Inventare» fehlt.
   - Die Signatur steht nur in der Inventarübersicht; im Detailverzeichnis ist es ein Aufzählungspunkt unter 2.1.
     Dort hat 2.1. alle 6 Schachteln von 2.
   - Folgt man dem Detailverzeichnis, ist es nur mittel. Suchlauf über «Signaturen nur im Vorspann» im Blatt Info möglich.

## Mittlere Funde (Muster)
- Titeldatum schlägt Inhaltsverzeichnis bzw. Darin: D175827 4.2. «[1946]» und 6.4., D3596 7.
- Lebensdaten oder Literaturjahre als Laufzeit: D3561 IDs 2, 4 (1798–1992), 5; D3382 5.1.
- Fremdtext im Titel:
  - Tabellenkopf «Zeitraum Anzahl Auswahl» (D2508, 16 Titel); rechte Spalte «VII.183: n» (D3043);
  - eingebettetes Datum (D3820 IDs 474, 669); abgeschnittener Titel (ID 697).
- Weitere: erster Listeneintrag als Titel (D1918); Schlussnotiz «… umfasst 16 Archivschachteln» im Darin von :16 (D2508).

## Signale
- N war immer Titelblatt, Einleitung oder Tabellenkopf (Rauschen). V (D175827): Vorspann richtig, nur 2.2. echt.
- Z (D2363): Rauschen; die Verschiebung fand erst die Kontrolle Schachtel für Schachtel.
- sigliste «verloren?»: nur Übersichten, Kopf-/Fusszeilen, Schlussvermerke, Literatur – keine verlorene Einheit.

## Unsicherheiten
- D2363 :7: «Protokoll Haussitzung» ohne Nummer habe ich zu 7 gezählt (gleicher Abstand; Gruppenlücken auf S. 2).
- D3820: Die 17 Fälle «Überschrift + gleiche Nummer» sind als Teil 2 konventionsgemäss; nur 18. weicht ab (gering).
