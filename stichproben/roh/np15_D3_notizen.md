# NP15 – Paket D3 (Durchsicht Schluss und Info, teil_3.txt, 121 Dateien)

## Bilanz
- Alle 121 Blöcke gelesen. Jeden Verdacht an der vollen Prüfmappe und am Excel geprüft, die Funde zusätzlich am PDF.
- Neue Funde: 2 kritisch (D2575, D2508), 2 gering (D2534, D2346), alle in D3_funde.csv.
- D3_dateien.csv: 117 ohne kritischen Fehler, 4 kritisch (2 neu: D2575, D2508; 2 bekannt: D1858 K40, D1874 K173).
- Kein Bearbeitervermerk in Titel, Darin, Umfang oder VVE der 121 Dateien. Kein «Übersichtszeilen ignoriert», kein «fehlt:», keine
  «Signaturen nur im Vorspann».

## Wichtigste Funde
1. **D2575 V.L.13. (kritisch, Text weg):** Nach 1.44. steht «Des Weiteren enthält der Bestand vereinzelte Dokumente, die nicht ins
   „Acten-Verzeichnis“ aufgenommen wurden.» nur im Info. Soll: Bestandszeile wie bei K206, K207 und K119.
   Ursache: STUECK_SCHLUSS_RE verlangt den Satzanfang «Der (Archiv)Bestand enthält …». Ohne Menge und Behälter fehlt der Satz auch in
   info_menge_runde11 und info_stuecke_r12.
2. **D2508 V.L.1001.:16 (kritisch, Schwere bitte bestätigen):** Der Schlussvermerk «Der Bestand der Politischen Flugblätter … umfasst 16
   Archivschachteln.» steht am linken Rand und im Darin der letzten Schachtel. Ursache: SCHLUSS_RE erlaubt höchstens 3 Wörter zwischen
   «Der Bestand» und «umfasst», hier sind es 7. NP10 (C2) meldete den Fall als mittel, er war nie in offen_kritisch; nach K75 (D144909,
   gleicher Fall) ist er kritisch.
3. **Gering:** In D2534 6.10. zerlegt die Umbruch-Reparatur «Entwurf: Paul Boesch, …» und verbindet den Rest mit «Beschreibung dieser
   Scheiben …». In D2346 stehen «Neubühl ohne Angabe» ×2 und «Neubühl 1987» in einer Darin-Zeile; «ohne Angabe» gilt vermutlich nicht als Datum.

## Bekannt (nicht neu gemeldet)
- Noch offen: bekannt K40 D1858 (Schachteln 14–20 als Teile von :1.–:8., kein Text weg) und bekannt K173 D1874 (Code «-»).
- Behoben: K207 D2502 (Bestandszeile ID 20 mit Darin und Hinweis); D176824 «In Schachtel 9 …» steht in der Bestandszeile.
- Unverändert mittel: abgebrochene Titel (D1820 :18., D2270 :16.), Stückzahl im Titel (D2139, D2268), erster Listeneintrag als Titel
  (D1797, D1916, D1918), Teil-Titel (D1803, D1937), D2516 Liste 1.–16., D2508 Titel mit Tabellenkopf; D2329 «Inhalt:» ist gering.

## Geprüft, kein Fund
- Info: Umfangsangaben (D176772, D176793, D177234), Bestandsgeschichte (D2504, D2534), Überlieferungshinweise (D2009 «Ab 1990 …»,
  D2067 «Ab 1986 … zusätzlich …»; das Titelblatt nennt nur 7 bzw. 5 Bände).
- Vorspann: Diese Sätze beschreiben Verzeichnetes: D176793 (Drucksachen ab 1851), D2192, D1963, D1933, D2566. Prosa nach Konvention:
  D185, D253, D2127, D2363, D2366, D2372.
- «?», [NACH] und «→ ID x» sind Rauschen, am Excel geprüft: D1880 (3. Serie als Teile T2/T3), D1924 (79/79a richtig verteilt),
  D2510 (letzte Einheit ist eigentlich ID 107 :123), D2123, D2363, D2366, D2372, D177448, D1803.
- D177460 «C Biergerichtsentscheide» ist eine Zwischenüberschrift in C. D2519 «Siehe unter …» steht nach Konvention in VVE.

## Unsicherheiten
- Schwere von D2508: mittel nach dem Massstab von NP10, kritisch nach K75/K6/K43. Ich habe kritisch gesetzt.
- D2575 nennt keine Menge, sagt aber klar, dass es Archivgut ausserhalb der 44 verzeichneten Nummern gibt.
- Ohne Eintrag (Kosmetik): In D2510 ist «C Elternzeit-Initiative - …» in zwei Darin-Zeilen getrennt.
