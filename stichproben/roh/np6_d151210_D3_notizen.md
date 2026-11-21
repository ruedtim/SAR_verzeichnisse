# D151210 (VII.200., Schauspielhaus Zürich AG) – Vollprüfung Bereich D3, PDF-Seiten 213–318

Geprüft: `$S/neu6/D151210_scope_import.xlsx` (Stand 15:43) gegen `$P/D151210.pdf`, Vergleich mit Stand 13:15
(`$S/neu5/…`). Skript-Zeilen beziehen sich auf `$S/neu6/findmittel_zu_scope.py`.

## Überblick

- **Umfang:** 106 Seiten, 801 Einheiten (IDs 1324–2124): 5.2.4.20. Teil 12 bis 5.2.4.35. (Produktionen je Spielzeit),
  5.2.5.x (Veranstaltungen/Matineen), 5.3.x (Gastspiele des Schauspielhauses), 5.4.x (Gastspiele/Junifestwochen),
  6.–6.52. (Rollenbücher). Alle Einheiten geprüft; die Einheit 1323 (beginnt S. 212) läuft auf S. 213 weiter und ist dort
  vollständig.
- **Vorgehen:** PDF-Zeilen mit pdfplumber (gleiche Parameter wie `lese_zeilen`), jede Signaturzeile des PDFs gegen die
  Excel-Folge (Nr. im PDF) abgeglichen; je Einheit Wortabgleich PDF ↔ Titel/Darin/Anm., Analyse jeder Zeilenfuge
  (Leerzeichen, «; », neuer Darin-Eintrag, Titelgrenze), Teil-Nummern, Parent/Ebene/Stufe/Übergeordnete Signatur,
  Zeitraum gegen die Titelzeile. Alle Auffälligkeiten am PDF nachgesehen. Hilfsdateien in `$S/np6/tmp_d3/`.
- **Ohne Befund:** Gliederung und Signaturen (801 PDF-Nummern = 801 Einheiten in gleicher Folge, keine fehlende oder
  erfundene Einheit, auch «5.2.4.25 .», «5.2.4.32» ohne Punkt, eingerücktes «5.2.5.12. -» richtig), Parent, Ebene, Stufe,
  Übergeordnete Signatur, PDF-Seite. Kein Text fehlt (Wortabgleich vollständig), kein Text bei der Nachbareinheit.
  Schachtel/Umfang: im Bereich keine Angaben im PDF, Spalten leer (richtig). Zeiträume aller Basiseinheiten stimmen mit
  der Titelzeile bzw. dem Inhaltsverzeichnis (5.2.5., 5.3., 5.4., 6.).
- **Teil-Nummern (Regel G):** in allen Serien des Bereichs jetzt lückenlos 2…n in PDF-Folge, Titel «…, Teil n» = Spalte
  Teil (13:15 noch «Teil 1» für den ersten Teil, Dubletten wie 6.4. 1/2/10/2…/9, 5.2.4.35. 1/10–13/2–9). Korrektur.
- **Fehler:** 38 Zeilen (34 mittel, 4 gering, keine kritischen), 149 betroffene Einheiten. Alle Fehler bestanden schon
  um 13:15, ausser dem seit 15:43 fehlenden Prüfhinweis bei 5.4.5.10. In `np6_d151210_D3_seiten.csv` zählt «fehler» die
  betroffenen Einheiten der Seite (nicht die CSV-Zeilen); 52 von 106 Seiten haben mindestens einen Befund, davon 17 nur
  geringe.

## Fehler nach Art

### 1. Titel vom Nachbarteil (M13, mittel) – 84 Teile in 10 Gruppen
Steht eine Produktion im PDF ohne «- » («5.2.4.21. Der Kaufmann von Venedig …»), bekommt sie einen eigenen Titel; alle
folgenden titellosen Teile («5.2.4.21. - Häuptling Abendwind …») übernehmen diesen Titel mit «, Teil n», ihre eigene
Produktion steht nur im Darin.

| Serie | Quelle (ID, Titel) | betroffene Teile | Seiten |
|---|---|---|---|
| 5.2.4.21. | 1332 «Der Kaufmann von Venedig … (14.09.1985)» | 1333–1344 (Teil 6–17) | 214–215 |
| 5.2.4.22. | 1350 «Die Insel … Bühnenpläne und Skizzen Aufführungsvertrag, Besetzungsliste» | 1351–1365 (Teil 7–21) | 216–217 |
| 5.2.4.23. | 1370 «Harry Buckwitz zur Erinnerung, Matinee» | 1371–1383 (Teil 6–18) | 218–219 |
| 5.2.4.24. | 1398 «Onkel Wanja … Bühnenpläne und Skizzen» | 1399 (Teil 16) | 221 |
| 5.2.4.25. | 1412 «Tell gegen Hitler …: Informationsblatt, Gesprächsnotizen» | 1413–1420 (Teil 14–21) | 223–224 |
| 5.2.4.26. | 1432 «Prinz Friedrich von Homburg … Bühnenpläne und Skizzen» | 1433–1439 (Teil 13–19) | 225–226 |
| 5.2.4.35. | 1629 «Blutspuren 5: Richard III.: Besetzungsliste, … Schauspielhausaufführung» | 1630–1637 (Teil 7–14) | 247–248 |
| 5.2.5.3. | 1677 «In Memoriam Therese Giehse … vom 16. März 1975» | 1678–1684 (Teil 7–13) | 251–252 |
| 5.2.5.4. | 1691 «Pepys Show … 3. / 16. Juni 1985: Besetzungsliste, Texte» | 1692–1696 (Teil 8–12) | 252–253 |
| 6.4. | 1903 «Shakespeare, William: König Johann» | 1904–1911 (Teil 5–12) | 290–291 |

Beispiel: ID 1904 (6.4. Teil 5) «Shakespeare, William: König Johann, Teil 5», Darin «Schiller, Friedrich von: Die Braut
von Messina • …». Soll «Rollenbücher, Teil 5» bzw. «Produktionen des Schauspielhauses und nicht realisierte Projekte,
Teil n». Bekannt aus Runde 5 (funde_nachpruefung5.csv Z292, dort «ca. 120 in D151210»); seit 15:43 nur die Nummern neu.

### 2. Darin-Text im Titel / Titel abgeschnitten (M08/M19, mittel) – 12 Einheiten
- Folgezeilen hängen am Titel, Darin oft leer: ID 1350 (S. 216), 1398 (S. 221, «Bühnenpläne und Skizzen»), 1412 (S. 223,
  Zeile nach «…:»), 1432 (S. 225), 1626–1629 (S. 246–247, «Blutspuren 2–5: … Besetzungsliste, Bühnenpläne … (Blutspuren
  1-5) Informationsmaterial …», 173–203 Zeichen), 1691 (S. 252, «…16. Juni 1985: Besetzungsliste, Texte»), 1763 (S. 264,
  «…Karsenty-Herbert 1967–1970 Vereinbarungen, Abrechnungen» – Datum dadurch mitten im Titel).
- Titel abgeschnitten: ID 1757 (S. 263) «Goethe-Abend zur Zürcher Erstaufführung seines Schauspiels», Rest «„Die
  natürliche Tochter“ vom 21. Mai 1954» als erster Darin-Eintrag; Zeitraum deshalb «Darin (geschätzt)».
- Erstes Rollenbuch als Titel: ID 1962 (6.12. Teil 5, S. 296) «de Vega, Lope: Die Launen der Donna Belisa» statt
  «Rolenbücher, Teil 5».

### 3. Darin falsch getrennt (M10) – 13 Einheiten mittel, 48 gering
- **Rollenbücher verschmolzen (mittel, 5):** ID 1910 «… Emil und die Detektive de Vega,Lope; Carpio, Felix: Der Ritter vom
  Mirakel» (S. 291), 1968 «… der liebe Gott Molière: Tartuffe» (S. 297), 1971 «… Das Leben ein Traum Molière: Der Geizige»
  (S. 297), 2057 «… Der Raub der Sabinerinnen Shakespeare, William: Timon von Athen» (S. 310), 2085 «… (II) Euripides:
  Medea (I)» (S. 313).
- **Eintrag zerstückelt (mittel, 8):** 6.x: ID 1926 «Wallenstein de» / «Vega, Lope; Carpio, Felix: …» (S. 292), 2006
  «Hamlet de» / «Vega, Lope: …» (S. 302), 2034 «Grumberg, Jean-Claude: Morgen» / «Ein Fenster zur Strasse» (S. 306);
  5.2.4/5.2.5/5.4: ID 1562 (S. 239, Titel mit « - » vor dem kursiven Untertitel), 1646 (S. 249, «Zeitungsartikel» /
  «„Theater als lebendige Anstalt …“»), 1711 (S. 256, «Hannah» / «Arendt, Manuskript: …»), 1720 (S. 257, «„Hans Sahl» /
  «Ein Narr der Aufrichtigkeit“», Strich weg), 1781 (S. 268, «Ferruccio» / «Soleri u. a.»).
- **«; » mitten im Namen/Satz (gering, 14):** z. B. ID 1707 «Gert; Westphal», 1708 «Peter W.; Loosli», 1766 «Neue;
  Schaubühne München», 1806 «Michael; Ende», 1830 «Heinz; Wustinger», 1833 «über Eröffnung; Junifestwochen 1989», 1435
  «Akten; 1989–1991:», 1768 «Krakow -; Protokoll …» (Strich-Rest, eigener Eintrag wäre richtig).
- **Unterzeile ohne «; » (gering, 34):** nach der Produktionszeile mit Premierendatum, z. B. ID 1366 «Das weite Land, …
  (26.03.1988) Bühnenpläne und Skizzen; Korrespondenz …» (Konvention: eingerückte Unterzeilen mit «; »).

### 4. Zeitraum (M09, mittel) – 5 Einheiten
- Teile mit übernommenem Titel bekommen den Zeitraum der Serie, obwohl die eigene Zeile einen anderen nennt: ID 1423
  «(Akten 1989–1991)» und 1435 «Akten 1989–1991» → 1990–1991; 1439 «… Schauspielhaus-Keller 1990–1992» → 1990–1991;
  1824 «Protokolle der Sitzungen über Junifestwochen 1987–1988» → = 1988.
- ID 1862 (5.4.5.10., S. 285) «Zürcher Festspiele 1997» = 1997, obwohl das eigene Darin Akten vom 6. und 21. Nov. 1996
  nennt; der Hinweis «Untereinheiten reichen über den Zeitraum hinaus (21.11.1996–1997).» ist seit 15:43 weg (einzige
  Verschlechterung im Bereich, nicht angekündigt).

### 5. Kosmetik (gering)
- Datum bleibt im Titel und steht zugleich in von/bis: ID 1332 «… (14.09.1985)», 1726 «… Mai – Juli 1955 in Paris» (Regel
  I: Zeitraum jetzt 05.1955–07.1955, Titel nicht bereinigt), 1987 «… (1955/56–1956/57)».
- ID 1717 «literarischmusikalisches» (PDF «literarisch-» / «musikalisches»).

## Änderungen 13:15 → 15:43 im Bereich (437 Einheiten)
- 433 nur Teil-Nummer und «, Teil n» im Titel (Regel G) – geprüft, überall richtig.
- ID 1691 = 16.06.1985 → 03.06.–16.06.1985 und ID 1726 = 07.1955 → 05.1955–07.1955 (Regel I) – besser; die Titel
  behalten das Datum.
- ID 1983 (6.18.) 1955–1957 → 1955–1956 mit Hinweis «Untereinheiten reichen über den Zeitraum hinaus (1955–1957)»
  (Regel F, Faulkner-Teil ist keine Fortsetzung) – besser.
- ID 1862 Hinweis entfernt – schlechter (siehe 4.).

## Ursachen im Skript (`$S/neu6/findmittel_zu_scope.py`)
1. **M13:** `ergaenze_titel` Z. 4149–4159: `quelle` wird jeder Teil mit eigenem Titel (Z. 4154–4156), danach
   `basis = quelle.titel or k.titel` (Z. 4157). Titellose Teile sollten den Titel der Serie `k.titel` bekommen (oder den
   Nachbartitel nur, wenn `_ist_fortsetzung`, Z. 4119, zutrifft). Regel G (Z. 4141–4148) ist in Ordnung.
2. **Darin im Titel bei Teilen ohne «- »:** `verarbeite` Z. 2959–2963 hängt einen «kurzen Rest» (≤ 2 Wörter) nach hartem
   Umbruch an den Titel («Vereinbarungen, Abrechnungen», «Aufführungsvertrag, Besetzungsliste», «Informationsblatt,
   Gesprächsnotizen», «Besetzungsliste, Texte»); Z. 2975–2976 macht bei Teilen aus einem einzigen logischen Eintrag den
   ganzen Titel; `ist_umbruch` Z. 2522 verbindet jede Zeile nach «…:» als weichen Umbruch (Blutspuren, Tell, Pepys).
3. **Umbruchtest:** `ist_umbruch` Z. 2532–2534 vergleicht mit dem globalen rechten Rand (`rechter_rand`, 98. Perzentil,
   Z. 306–309, ≈ 554). Die Blöcke in 5.2.5/5.4 enden früher (≈ 520–545), echte Umbrüche gelten dort als harte →
   «; » (`baue_eintraege` Z. 2636–2641) oder neuer Eintrag (Z. 2643): «Gert; Westphal», «Ferruccio» / «Soleri», 1646.
   Umgekehrt gilt eine lange Zeile mit langem Folgewort als weicher Umbruch → Unterzeilen ohne «; », 2057/2085 verschmolzen.
   Abhilfe: rechten Rand je Absatz/Block bestimmen.
4. **Rollenbuchlisten:** `trenne_namenseintraege`/`NAMENSGRENZE_RE` Z. 2672–2702 trennt nur bei «Nachname, Vorname:»
   mit Grossbuchstaben – Autoren ohne Vorname («Molière:», «Euripides:») und Partikel («de Vega») fallen durch (1968, 1971,
   2085; «de» bleibt bei 1926/2006); `ist_umbruch` Z. 2528 hält eine klein beginnende Zeile («de Vega,Lope; …», 1910) für
   eine Fortsetzung. Die Listenreparatur trennt auch «Hannah» / «Arendt, Manuskript:» (1711). Ein erstes Rollenbuch mit
   Kleinbuchstaben («de Vega, Lope: …», 1962) wird nicht als Namenseintrag erkannt und Titel.
5. **Gedankenstriche:** `teile_inline` Z. 2650–2665 trennt bei « - » + Grossbuchstabe auch innerhalb eines Stücktitels
   (2034, 1562); «–» am Zeilenanfang ist Aufzählungszeichen (`AUFZAEHLUNG` Z. 880, `ist_aufzaehlung` Z. 1720) → 1720.
6. **Zeitraum der Teile:** Z. 3908–3909 setzt bei übernommenem Titel den Zeitraum der Serie, bevor eigene Daten im Darin
   (erste Zeile «Akten 1989–1991») geprüft werden.
7. **Bindestrich:** `verbinde` Z. 2543–2545 entfernt den Trennstrich vor jedem Kleinbuchstaben («literarisch-» +
   «musikalisches»).
