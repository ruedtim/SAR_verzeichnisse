# D7 – Durchsicht Schluss und Info, Teil 7 (NP15)

## Bilanz
- 63 Dateien (D3575–D3894). Teil 7 ganz gelesen; jeden Verdacht an voller Prüfmappe, Excel (sig.py, Blatt Info) und PDF
  (pdftotext, rawlines) geprüft. Ein Skript über alle 63 vollen Mappen listet jede Zeile nach der letzten Einheit, die
  weder im Info noch ohne Warnzeichen im Darin/Titel steht, auch an verdichteten Stellen (`tmp_D7/schluss_rest.txt`).
- **Neu kritisch: 3 Dateien, 3 Funde (D3604, D3742, D3767).** Alle drei wurden früher als mittel gemeldet oder gesetzt
  (NP10 C3/C4, Entscheid NP11) und stehen nicht in bekannt.csv. Nach der heutigen Skala sind sie kritisch.
- Bekannt und noch da: **bekannt K44** (D3828 3.4., nicht im Schluss), **bekannt K78** (D3894: Schluss nach X.C.85. =
  Abschnitte 2.–4. als Teile). Dateien mit kritischem Fehler: 5 (3 neu, 2 nur bekannt); ohne: 58.
- Dazu 1 mittel (D3612 8.4.: «Heft 1» im Titel, Enddatum 1896 fehlt) und 2 gering (D3718, D3861: Darin-Einträge durch die
  Zeilenumbruch-Reparatur zerteilt).

## Wichtigste Funde
1. **D3604 :2:** Der Bearbeitervermerk «13. September 2002 / lic. phil. Karin Beck» ist Darin 15 der letzten Schachtel.
   Zeitraum dadurch bis 13.09.2002, Info «–», gleiche Form wie K203. Ursache: In der Schachteltabelle ohne Signaturen
   greift die Schlussvermerk-Erkennung nicht. Der Suchlauf `vermerk_im_darin_r12.csv` hat ihn nicht gefunden.
2. **D3742 22.:** «Letztes Blatt (schwarz kalligraphiert):» (⇣, x71) steht im Darin des Porträts 22. Die Inschrift
   «AUSGEFÜHRT / VON R. GANZ PHOT. / ZÜRICH» (Kapitälchen) steht nur im Blatt Vollständigkeit. Soll: Bestandszeile.
3. **D3767 37.:** «Beilagen (3 Farbbildchen)» mit 3 Bildern steht mit Hinweis im Darin von Foto 37. Laut S. 1 sind es
   die Beilagen des Albums → Bestandszeile. Die Signalwort-Regel kennt nur «Beilagen:». In NP11 hat die Hauptsession das
   vor dem Bestandszeilen-Entscheid auf mittel gesetzt: **bitte neu entscheiden.**

## Muster
- Alben/Objektlisten: Ein Absatz ohne Nummer am linken Rand nach grossem Abstand, ohne Signalwort, landet im Darin der
  letzten Einheit (D3742, D3767). Schachteltabelle ohne Signaturen: «Datum / Name» nach der letzten Tabellenzeile wird
  Darin (D3604); die Mappen-Dateien D3725 und D3776 machen es richtig.

## Info-Sätze geprüft, kein Fund
- Umfang fasst zusammen: D3581 «6 Schachteln», D3596 «45» (Summe der Übersicht), D3606, D3620, D3628, D3664, D3677,
  D3793, D3861, D3874. Verweis ausserhalb des Bestands: D3612 (Nc 43), D3727 (Planarchiv am gta), D3793 (V.L. 1001.,
  Zg, V.A. c.32.), D3826 (Nc-Liste der Bibliothek).
- Geschichte, Literatur, Übergabe: D3579 («In der Beilage die folgende Notiz» = Herkunftsnotiz), D3587, D3677, D3682,
  D3702, D3709, D3742, D3776, D3833, D3853. Bei D3828 steht die CV-Beilage schon in der Bestandszeile.

## Unsicherheiten
- D3742, Titelblatt mit Dedikation (S. 3 «Inhalt», «Text vor der ersten Signatur»): Stück wie das letzte Blatt oder
  Vorbemerkung (höchstens mittel)? Im Fund als Grenzfall genannt, nicht eigens gezählt.
- D3657: «5. Fremdenzimmer»/«6. Löschung» nach 6.3. (wohl 7./8.) bleiben Teile T2 – Konvention (NP12 mittel), kein Fund.
- D3828 und D3894 haben das Urteil «kritisch» nur wegen K44 bzw. K78; Schluss und Info ohne neuen Fund.
