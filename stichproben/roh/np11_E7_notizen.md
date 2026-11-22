# E7 – Notizen (Nachprüfung 11, Paketart E, Stand efe92c5f)

## Bilanz
- 44 Dateien, alle ganz über die Prüfmappe geprüft. Bei mehr als 60 Einheiten Struktur über alle EINHEIT-Zeilen; bei D150306 (447) zusätzlich maschinell Eltern/Ebene/Nummernfolge, alle Nicht-Signaturzeilen und S. 3, 6, 9, 12, 22 Zeile für Zeile. PDF/Rohzeilen nur bei Zweifeln (D3945, D141058, D150306, D3542, D1263, D2372).
- 40 Dateien ohne kritischen Fehler, 4 kritisch: D2848, D3542, D1263, D2372.
- 22 Funde: 7 kritisch, 14 mittel, 1 gering.

## Wichtigste Funde (kritisch)
1. D1263: sechs Signaturen «V.F. b.13.c:1» … «:6» stehen nur im Darin einer Bestandszeile (Gliederung «ohne Signaturen»). Die Form mit Buchstabe vor «:» ohne Punkt wird nicht erkannt. Kein Warnzeichen, Wortprüfung 100 %.
2. D2372: Liste «Akte / Dossier | Schachtel-Nr.» (1–3) als Bestandszeile statt drei Schachtel-Einheiten (Konvention für Dossierlisten mit Schachtelspalte). Kein Warnzeichen.
3. D3542 (Tabelle Schachtel | Stadtteil | Assekuranznummern | Signatur StAZ): Zellen der Assekuranzspalte beginnen 3 pt über der Signaturzeile. Darum fehlt «I - LXV» (gilt als Text vor der ersten Signatur), und «I - XIX» steht bei 11. statt bei 12. Dazu stehen «Anmerkungen zu Schachtel 29» und die Bestandsgeschichte im Darin von 30. (Zeitraum 1905–07.1999).
4. D2848: zwei Absätze Bestandsgeschichte nach der letzten Einheit im Darin von 8.; Zeitraum dadurch 1930 statt 1939.

## Muster
- Neu gegenüber der NP10-Liste: «Bestandszeile verschluckt Einheiten». Suchlauf über alle 716 Excel (tmp_E7/suche_bestandszeile.py → suche_bestandszeile.txt), NICHT am PDF geprüft, andere Pakete:
  D1261 (V.F.b.13.b., 5 Signaturzeilen «V.F. b.13.b:n», E10), D1686 (V.G.b.58.h., 11 Zeilen «V.G. b.58.h:n», E2),
  D2123 (V.H.c.107., Kopf «Akte / Dossier Schachtel-Nummer», Schachteln 1–36 in 375 Darin-Zeilen, E10), D2127 (V.H.c.112., Schachteln 1–2, E10).
  Die Prüfmappen zeigen für diese Fälle kein Warnzeichen ([SIG?] kennt die Form nicht).
- Schlussnotiz/Bestandsgeschichte nach der letzten Einheit im Darin: D2848, D3542; Bearbeitungsvermerk «chr Stand: 27.08.1993» im Darin und als Zeitraum (D3781, mittel).
- Zeitraum (mittel): mehrzeilige Datumsspalte M05 (D3515 17 Einheiten, D2953, D1347), Lebensdaten/Sachjahre (D3008, D150306 ID 323), Spaltenausreisser 1931 ohne Hinweis (D2953), zweites Spaltendatum in Darin-Liste ignoriert (D141058).
- Tabellenkopf der Folgeseite in Titel/Darin der letzten Einheit der Vorseite (D3945 ID 13, 28).
- Architektenzeile mal Titel, mal Darin (D1584, 32 von 105). Bereichssignaturen «:4:1-3», «:2-3» je eine Einheit (richtig), aber falsche Hinweise «Nummerierung springt» (D3355, D1584).

## Signale
- [SIG?] und [NACH] bei D446/D448 sind Rauschen: Die Mappe ordnet die Einheiten 1.–4. den Inhaltsverzeichniszeilen mit gleichem Wortlaut zu, die Excel ist richtig. [VOR] fast immer gleichlautende Zeilen («1 Band», «4 Stück», «Mauerkrone», Datumszeilen).
- Von den 4 kritischen Dateien zeigte nur D3542 ein passendes Zeichen ([NICHT] bei «I - LXV»). D1263 und D2372 hatten keines.
- Hinweis des Koordinators zu D1922 bestätigt: «V.G. c.67.:1.» mit Liste 1.–6. im Darin ist kein Fehler. Den kritischen Fall «nur Bestand in der Signaturspalte, dann 1.–n.» (wie D175561) gibt es in E7 nicht; alle 44 Mappen wurden danach durchsucht.

## Unsicherheiten
- Schwere der Schlussnotizen im Darin (D2848, D3542 4. Zeile): kritisch (Grenzfall) gewertet, weil es mehrere Sätze Bestandsgeschichte sind und der Zeitraum falsch wird. NP10 wertete einzeilige Notizen (D2508, D3727) mittel. Bei Herabstufung ist D2848 ohne kritischen Fehler, D3542 bleibt kritisch.
- D1696: Signaturen V.G.b.608.:1–5 im Bestand V.G.b.609. stehen so im PDF, Hinweis vorhanden, Entscheid beim Archiv.
- D3542: Signatur aus der Schachtelnummer mit Schlusspunkt (VII.330.:1.); die Konvention für Schachtel-Einheiten lautet «Bestand:Nummer». Zu prüfen.
- Platzhalter «[nicht belegte Signaturen]» (D141058) bleiben Einheiten; die Konvention ist offen, nicht gewertet.
