# D151210 (VII.200., Schauspielhaus Zürich AG) – Vollprüfung D2, PDF-Seiten 107–212

Stand 15:43 (`$S/neu6/D151210_scope_import.xlsx`), verglichen mit 13:15 (`$S/neu5/…`). Skript `$S/neu6/findmittel_zu_scope.py`
(sha256 c7c28ce2…, 5475 Zeilen) – Zeilennummern unten beziehen sich darauf.

## Überblick
- **Umfang:** 106 Seiten, **776 Einheiten** mit PDF-Seite 107–212 (IDs 547 und 549–1323; Abschnitte 4.1.3.1. bis 5.2.4.20.,
  dazu die Fortsetzungen auf S. 213). Alle Seiten einzeln gelesen (PDF-Text gegen kompakte Excel-Sicht mit Zeilenzuordnung).
- **Hilfsprüfungen:** Wortabgleich aller 23 292 PDF-Wörter des Bereichs gegen Signatur/Titel/Zeitraum/Darin der Excel-Einheiten
  in ID-Folge (difflib). Ausser Umstellungen (Datum aus dem Titel nach von/bis) und den unten genannten Fällen ist jedes Wort
  in derselben Reihenfolge bei der richtigen Einheit. Kein Text fehlt, keiner steht bei der Nachbareinheit.
  Weiter geprüft: Hierarchie, Ebene, Stufe und übergeordnete Signatur (776 von 776 stimmig), Teil-Folgen je Signatur
  (36 Signaturen, 325 Teile), «…, Teil n» gleich der Teil-Nummer (294 von 294), alle 101 Anmerkungen gegen von/bis und Fugen im Darin («; » oder Leerzeichen an jeder Zeilengrenze).
- **13:15 → 15:43 im Bereich:** Geändert haben sich nur Teil-Nummern (273 Einheiten) und die Titelendung «, Teil n» (267).
  Regel G wirkt: Um 13:15 gab es 15 doppelte Schlüssel (Signatur, Teil) und 6 nicht aufsteigende Folgen, jetzt keine mehr.
  Die übrigen Felder sind unverändert, die Funde unten bestanden also schon um 13:15.
- **Ergebnis:** Kein kritischer Fehler. 15 Fundzeilen mit 155 Fundstellen. **Mittel: 42 Einheiten** in 12 Zeilen
  (30 × Titel vom Nachbarteil, 7 × Titel/Darin-Grenze, 2 × Datum im Titel, 1 × Darin, 2 × Zeitraum). **Gering: 113
  Fundstellen** (106 Einheiten, 7 doppelt gezählt) in 3 Zeilen, alles Darin-Fugen. Insgesamt sind 130 Einheiten betroffen. Signaturen, Gliederung, Teil-Nummern, Schachtel und
  Umfang sind fehlerfrei. Schachtel- und Umfangangaben gibt es im Bereich keine.

## Fehler nach Art
### Titel (Nachbarteil) – [M13], mittel, 30 Teile, alle in 5.2.4.x
In 5.2.4.x ist jede Produktion «5.2.4.n. - Titel (Datum)» ein Teil. Die titellosen Teile heissen «Produktionen des
Schauspielhauses und nicht realisierte Projekte, Teil n» (gewollt, Soll aus Runde 5). Fehlt im PDF der Gedankenstrich,
wird die Produktionszeile zum Titel dieses Teils. Alle folgenden titellosen Teile erben dann diesen Titel mit «, Teil n».
- 5.2.4.1. IDs 1097–1099 (T83–85, S. 186–187): «Der Selbstmörder …» für «Die Gräfin von Rathenow», «Die gelehrten Frauen»,
  «Hochzeit».
- 5.2.4.2. IDs 1108–1114 (T8–14, S. 188): «William Shakespeares „nackter“ Hamlet …» für Lumpacivagabundus … Amphitryon.
- 5.2.4.5. IDs 1142–1149 (T3–10, S. 191–192): «Emilia Galotti …» für Akrobaten … Die Mannschaft.
- 5.2.4.5. IDs 1151–1153 (T12–14, S. 192): «Der Alpenkönig und der Menschenfeind …».
- 5.2.4.6. IDs 1161–1168 (T8–15, S. 193–194): «Der Büchsenöffner …» für Der Ratenfänger … Richard III.
- 5.2.4.13. ID 1252 (T15, S. 204): «Die Verschwörung des Fiesco …» für «Projekt einer Jugend-Produktion».

Den Zeitraum erben diese Teile nicht. Sie haben wie die übrigen die Saison des Elternteils, auch nach 1150 mit = 20.09.1973.
Ausserhalb von 5.2.4.x gibt es im Bereich keine Nachbartitel. Die Teile in 4.1.6.x, 5.2.2.1. und 5.2.3.1. tragen ihren
eigenen Titel aus dem PDF («Bewerbungen mit Fotos S – Z», «Fotos mit Max Frisch» …), das stimmt.

**Ursache:** `ergaenze_titel`: Nach jedem Teil mit eigenem Titel gilt `quelle = t` (Z. 4155). Folgende titellose Teile
erhalten `quelle.titel` plus «, Teil n» (Z. 4157). `_ist_fortsetzung` (Z. 4119) wird dabei nicht gefragt. Für Listen wie
5.2.4.x, deren betitelte Teile keine Fortsetzung sind, müsste der Titel von `k` kommen und nicht vom letzten betitelten Teil.

### Titel/Darin – mittel, 7 Einheiten
- **Unterzeile im Titel betitelter Produktions-Teile (5 Fälle):** IDs 1096 (5.2.4.1. T82, S. 186), 1107 (5.2.4.2. T7, S. 187),
  1141 (5.2.4.5. T2, S. 191), 1160 (5.2.4.6. T7, S. 193), 1251 (5.2.4.13. T14, S. 204). Ein Beispiel ist «Der Büchsenöffner,
  Schauspiel von Victor Lanoux (25.01.1975) Bühnenpläne und Skizzen Besetzungsliste» mit leerem Darin. Das Premierendatum
  steht dann mitten im Titel, und der Zeitraum kommt nur vom Elternteil. Diese Titel werden zusätzlich vererbt (M13).
  **Ursache:** `kopf_und_rumpf` (Z. 2798 ff.) hängt die Folgezeile als weichen Umbruch an, weil der Breitentest von
  `ist_umbruch` (Z. 2534) sagt, dass das erste Wort nicht mehr auf die lange Zeile gepasst hätte. Eine Zeile, die auf
  «(TT.MM.JJJJ)» endet, müsste den Titel abschliessen.
- **Titelfortsetzung im Darin (2 Fälle):** 4.1.4.35. (ID 631, S. 125): Der Titel endet auf «… Aktennotizen von Achim», das
  Darin beginnt mit «Benning» • «1990–1991». 5.2.4.10. (ID 1205, S. 199): Das Darin beginnt mit «1977–1980, diverse Akten zu
  Aufführungen». In beiden Fällen steht der Zeitraum mit Quelle «Darin (geschätzt)» und Hinweis statt «Titel» (die Werte
  stimmen). **Ursache:** `verarbeite` – nach hartem Umbruch wird jede weitere logische Titelzeile Darin (Z. 2972). Die
  «kurzer Rest»-Regel (Z. 2961) wirkt nur bei genau zwei logischen Zeilen und nicht, wenn die Folgezeile mit einer Ziffer
  beginnt.
- **Datum am Titelende (2 Fälle, mittel nach Anleitung «Datumsrest»):** ID 1100 «Torquato Tasso … (undatiert)» und ID 1150
  «Der Alpenkönig … (20.09.1973)». Zeitraum und Anmerkung sind richtig gesetzt, nur die Klammer bleibt im Titel.
  **Ursache:** `zeitraum_aus_titel` Z. 3839–3854. Bei «(Datum)» bleibt «)» hinter dem Datum, Z. 3848 passt nicht, und der
  Titel wird nicht gekürzt.

### Darin
- **mittel, 4.2.6.8. (ID 779, S. 147):** Der Werktitel «"Frankenstein - Entstehung, Vorläufer und anderen Monstern"» ist am
  « - » in zwei Einträge zerlegt. **Ursache:** `teile_inline` (Z. 2650, Muster Z. 2655) beachtet keine offenen
  Anführungszeichen.
- **gering, 89 Teile in 5.2.4.x:** Die erste Unterzeile nach einer langen Produktionszeile ist mit Leerzeichen statt «; »
  angehängt («… (02.10.1969) Notizen, Besetzungsliste …»). **Ursache:** `baue_eintraege` fragt `ist_umbruch` (Z. 2633) vor
  der Unterzeilen-Regel (Z. 2636).
- **gering, 23 Teile in 5.2.4.x:** Unterzeilen werden eigene Darin-Einträge (z. B. ID 1016 «Streng geheim …» • «Bühnenpläne und
  Skizzen»), sonst sind sie mit «; » angehängt. **Ursache:** Z. 2636 verlangt mehr als 4 pt Einzug gegenüber dem
  Eintragsbeginn. Der Gedankenstrich steht in diesem PDF bei x ≈ 129–141 pt, die Unterzeilen bei 141–143 pt. Ob «; », ein
  Leerzeichen oder ein neuer Eintrag entsteht, hängt deshalb an etwa 1 pt.
- **gering, 5.2.3.5. (ID 1001, S. 176):** «im Schauspielhaus; Zürich:» hat «; » mitten im Satz (gleiche Stelle, Z. 2636).

### Zeitraum – mittel (Grenzfall), 2 Einheiten
4.3.2. «Dramenwettbewerb von 1958» (ID 806) hat = 1958, das Darin nennt «Korrespondenz … 1957–1959» und «Protokoll … vom
14. März 1959». 4.3.3. «Dramenwettbewerb von 1984» (ID 807) hat = 1984, das Darin nennt «Korrespondenz … 1984–1985». Das
Titeljahr ist hier das Ereignisjahr, nicht die Laufzeit. Nach Regel B/E bleibt es so; wenn der Zeitraum genau sein soll, ist
er zu eng.

### Ohne Fehler
Gliederung und Signaturen (jede Nummer eine Einheit, keine erfundene, Ebene/Parent/Stufe stimmig), Teil-Nummern,
Anmerkungen, Schachtel/Umfang (im Bereich nicht vorhanden). Die Zeiträume aus Titel, Inhaltsverzeichnis und Untereinheiten
stimmen mit dem PDF bzw. dem Inhaltsverzeichnis S. 5–7 überein.

## Beobachtungen, kein Fund
- S. 115: «4.1.2.38.» ist ein Tippfehler im PDF (zwischen 4.1.3.37. und 4.1.3.39.). Er ist nach Entscheid 5 eigene Einheit
  ID 547 unter 4.1.2. mit Hinweis «Nummerierung springt: nach 4 folgt 38» und steht in ID-Folge bei 4.1.2. Bei 4.1.3.39.
  steht der Hinweis «nach 37 folgt 39». Der Text ist vollständig.
- S. 134: Bei 4.1.6.17./18. steht im PDF «Bewerbungen mit Fotos …, Teil 1–5/1–7» meist ohne Signatur. Die Einträge sind
  richtig als Teile mit den PDF-Nummern 1–5 bzw. 1–7 erfasst. Die Serie selbst zählt nach Konvention ebenfalls als «Teil 1»,
  ohne Schlüsselkonflikt, weil ihr Teil-Feld leer ist.
- 4.1.6.x: Das Datum mitten im Titel («… Personals 1966–1972 mit Beilagen, alphabetisch geordnet») bleibt stehen. Das ist
  vertretbar, aber uneinheitlich zu 4.1.3.x («…, alphabetisch geordnet» ohne Datum).
- 5.2.4.x: Titellose Teile haben den Saison-Zeitraum des Elternteils (Konvention), obwohl jede Produktion ein Premierendatum
  nennt. ID 1150 (betitelt) hat dagegen = 20.09.1973.
- Im PDF fehlt bei 1126 und 1157 die schliessende Klammer, bei 1210 und 1211 die öffnende. Bei 1126 und 1157 werden deshalb
  alle Unterzeilen mit Leerzeichen verbunden (PDF-Fehler). Bei 1118 steht im PDF «- -».
- 4.1.3.40. (ID 587): « - einzelne Programme» wird nicht geteilt, weil `teile_inline` nur vor Grossbuchstaben trennt. Im PDF
  steht ohnehin kein Aufzählungszeichen.
- 4.2.4.19./4.2.4.21. und viele Produktionen in 5.2.x: «siehe (auch) Sign. …» steht mitten in einer Darin-Zeile und
  bleibt im Darin. «Verwandte» ist im Bereich nie gefüllt.
- 5.2.1.1. ist geschätzt 1949–31.05.2004 (Wegleitung zur Ausstellung 2004) und reicht über 5.2.1. (laut Inhaltsverzeichnis
  1941–1998). Bei geschätzten Kindern gibt es keinen Hinweis «Untereinheiten reichen über den Zeitraum hinaus», ebenso bei
  5.2.2.2. (bis 1995) unter 5.2.2. (1945–1994).
- 5.2.4.11.: Die erste Produktion («Zürich, Florhofgasse 1 …») steht im PDF ohne eigene Signatur direkt unter der Überschrift
  und ist deshalb Darin der Serie (Konvention «Inhalt der ersten Nennung»).

## Wichtigste Punkte
1. **M13 Nachbartitel (30 Teile):** Ursache ist `ergaenze_titel` Z. 4152–4159. Betitelte Teile in Listen ohne Fortsetzung
   (5.2.4.x) dürfen ihren Titel nicht weitergeben. Beispiel: ID 1161 «Der Büchsenöffner …, Teil 8» = «Der Ratenfänger» (S. 193).
2. **Produktionszeile ohne «- » (5 + 2 Teile):** Die Unterzeile wird an den Titel gehängt (`ist_umbruch` Breitentest Z. 2534).
   Das ist zugleich die Quelle der Nachbartitel. Beispiel: ID 1160 mit leerem Darin.
3. **Titelfortsetzung nach hartem Umbruch im Darin (4.1.4.35., 5.2.4.10.):** `verarbeite` Z. 2961/2972.
4. **Darin-Fugen in 5.2.4.x (gering, 112 Teile):** `baue_eintraege` Z. 2633/2636. Die Folge (Umbruch, «; » oder neuer Eintrag)
   hängt an etwa 1 pt Einzug.
5. **Regel G** ist im Bereich ohne Rest umgesetzt: keine doppelten oder ungeordneten Teil-Nummern mehr, Titelnummer gleich
   Teil-Nummer.
