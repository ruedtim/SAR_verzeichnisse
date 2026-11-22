# Nachprüfung 13: Gegenprüfung der Runde 10, Suchläufe und Zufallsstichprobe (22.11.2026)

Geprüft sind:
- **Runde 10:** Skript `424a9976…` gegen 66c0fb74 (Runde 9), an den 66 geänderten Dateien und den geänderten Testdaten. Das
  ist der Stand jetzt im Projekt.
- **Suchläufe über alle 715 Dateien:** Tippfehler in Dezimalsignaturen, Stück ohne Nummer im Blatt Info, «n.a» als Kind.
- **Zufallsstichprobe:** 60 Dateien, die Runde 10 nicht geändert hat und die keine Zeile in `offen_kritisch.csv` haben, je
  ganz geprüft. Sie schätzt, wie viele kritische Fehler die früheren Vollprüfungen übersehen haben.

Die Ergebnisse stehen hier:
- `offen_kritisch.csv`: nachgeführt, mit stabilen K-Nummern. Nach den Entscheiden der Hauptsession (siehe Nachtrag am
  Schluss) hat sie 33 Zeilen, neu sind K183–K202;
- `funde_nachpruefung13.csv`: 159 Zeilen;
- Rohdaten in `roh/np13_*`;
- Methode in `methode/ANLEITUNG_NACHPRUEFUNG13.md` und `methode/np13_*`.

## Kurz

- **Runde 10 wirkt.** Von den 74 K-Zeilen in den geänderten Dateien sind 68 erledigt: 61 behoben, 7 mit nur mittlerem Rest.
  - Kritisch bleiben K144 (D151150), K156 (D3808) und K178 (D10744). Dazu kommen die bewusst offenen K44, K78 und K117.
  - Am PDF beurteilt sind 413 geänderte Einheiten: 374 besser, 27 gleich, 5 teilweise besser, 7 schlechter.
- **Fehlgriffe der breit wirkenden Regeln** (wie gewünscht besonders geprüft):
  - **Regeln 6–8 (Überschriften):** keiner. Alle 17 neuen Überschrift-Hinweise sind echte Überschriften.
  - **Regel 12 (Übersicht, Inhaltsverzeichnis):** keiner. Nichts ist doppelt oder erfunden.
  - **Regeln 1–5 (Schlusstext):** einer. Regel 4 nimmt in D3808 den Schlussvermerk «chr Stand: 02.09.1992» mit in die
    Bestandszeile (K156, kritisch).
  - **Regel 9 (Tippfehler-Nachbarregel):** 10 von 12 Fällen richtig. In D3470 schreibt sie «40.430» und «41.436» um, obwohl
    die erste Nummer dort laut Vorspann frei gewählt ist (mittel).
  - **Regel 10 (Buchstaben-Geschwister):** keine falschen Geschwister, aber Lücken (siehe unten).
- **Ein Rückschritt mit Textverlust:** In D151150 fehlt die erste Nennung von 9.501. «Mietauto für Fleischschau» jetzt ganz
  (K189). In Runde 9 stand sie noch im Darin von 9. Die Vollständigkeit zeigt trotzdem 100 %. Im Textabgleich der
  Hauptsession war der Verlust nicht zu sehen, weil die Wortliste für D151150 nach den häufigen Zahlen abbricht.
- **Lücken der Regeln:**
  - Regel 14 lässt in D151150 105 Dossiers 9.1208.–9.2024. im Darin von 9.1194., weil die Nummern wie Jahreszahlen aussehen
    (K144).
  - Regel 16 macht in D10744 710 zur Zehnergruppe über 711–718 (K178).
  - Regel 10 fasst «n.a» nicht, wenn «n.» eigene Bände hat, wenn die Liste weder Umfang noch Datum hat oder wenn das Datum
    nur im Titel steht (7 Zeilen).
- **Suchlauf «Tippfehler in Dezimalsignaturen»:** In Runde 10 hängt keine Einheit mehr wegen eines Tippfehlers unter fremden
  Eltern. Neu bleibt D3472: «1952.8» und «1952.14» stehen je zweimal, 1952.9 und 1952.15 fehlen. Regel 17 macht daraus nur
  Teile mit Hinweis (K183, K184).
- **Zufallsstichprobe: 4 von 60 Dateien haben einen kritischen Fehler (6,7 %, 95%-KI 2,6–15,9 %).**
  - Mitgezählt ist D177470 nach dem Entscheid der Hauptsession zu Buchstaben in der Titelspalte. Vor dem Entscheid waren es
    3 von 60.
  - Hochgerechnet auf die 642 Dateien ohne bekannte kritische Zeile sind das etwa 43 Dateien (KI 17–102).
  - Alle vier Fehler sind älter als Runde 10 und wurden in früheren Vollprüfungen übersehen oder anders gewertet (D2620,
    D3067, D151759, D177470).
  - Die Suchläufe finden nach denselben Mustern 7 weitere kritische Zeilen in sechs Dateien ausserhalb der Stichprobe:
    D151756, D152383, D150589, D3012, D3038, D3089.
- **Offene kritische Fehler** (`offen_kritisch.csv`, Stand 424a9976, nach den Entscheiden): 33 Zeilen in 28 Dateien.
  - 20 Zeilen sind neu (K183–K202), 13 stammen aus früheren Nachprüfungen.
  - 10 sind bewusst offen. Nicht bewusst offen sind 23 Zeilen in 18 Dateien; zwei davon betreffen nur die Testdatei D152810.
- **Konventionsfragen:** Die drei Fragen (K135/Regel 17, Buchstaben in der Titelspalte, Zehnergruppe in D10744) hat die
  Hauptsession entschieden (Nachtrag). Offen ist nur, ob der Entscheid zu den Buchstaben auch für Untergruppen mit eigener
  Schachtel und Bandliste gilt (D3038, D3089).

## Stände und Nachrechnung

| Stand | Lauf zellgleich | geändert gegenüber 66c0fb74 | Einheiten | Fallsets |
|---|---|---|---:|---|
| 424a9976 (Runde 10) | ja, auch Testdaten und D151210 | 66 Dateien (= `runde10/geaenderte_dateien.txt`), 5 Testdateien, D151210 an einer Stelle | 51'508 (+338) | A 11/12, B 33/38, C 9/12, F 5/7, Runde 2 31/34, Punkt 2 38/38 |

- `runde10/vorher/` ist zellgleich mit meinem Lauf der Runde 9.
- **Soll-Zeilen der Fallsets nachgeführt.** Vorher standen sie bei A 10/12, B 32/38 und Runde 2 30/34; nach Signatur war
  alles unverändert richtig.
  - **A:** D2962 VII.150.:11.2.2. ist jetzt ID 69.
  - **B:** D3063 VII.190.:40.1. ist jetzt ID 68.
  - **Runde 2:** D3808 «Beilagen:» steht seit K156 im Darin der Bestandszeile VII.65. statt im Blatt Info.

## Gegenprüfung der Runde 10 (G1–G5, 66 Dateien und 2 Testdateien)

| Paket | Regeln | Dateien | Einheiten beurteilt | K-Zeilen erledigt | neu kritisch | kritische Dateien |
|---|---|---:|---|---|---:|---|
| G1 | 1–5 Schlusstext, Stück ohne Nummer | 22 | 61: 53 besser, 5 gleich, 3 schlechter | 25 von 28 | 0 | D3808 (K156); bewusst offen D2710 (K117), D3828 (K44) |
| G2 | 6–8 Überschriften, Gruppenbeschreibung | 16 | 204 besser | 20 von 21 | 0 | bewusst offen D3894 (K78) |
| G3 | 9, 10, 11, 17 | 13 + 2 Testdateien | 59: 38 besser, 17 gleich, 4 schlechter | 8 von 8 | 6 | D3470, D3472, D152817, Testdatei D152810 |
| G4 | 12–16 | 9 | 47: 40 besser, 2 gleich, 5 teilweise | 6 von 8 | 3 | D151150 (K144), D3412, D10744 (K178) |
| G5 | 11–13 in grossen Dateien | 6 | 42: 39 besser, 3 gleich | 9 von 9 | 0 | – |

Mit nur mittlerem Rest gelten als erledigt: K99, K100, K114, K121, K135, K161, K163.

### Regeln 1–5 (G1)

- **Fehlgriff Regel 4, D3808 (K156):** Mit den Beilagen steht auch der Schlussvermerk «chr Stand: 02.09.1992» (S. 1 y706)
  als Darin 6 in der Bestandszeile VII.65.; das Blatt Info zeigt «–». Ich werte das wie K169 (Bearbeitungsvermerke im
  Darin) als kritisch. K72 war mittel, weil dort nur ein interner Kommentar ohne Bearbeiter und Datum stand.
- **D2962:** Das Wegfallen von 6. Teil 2 ist richtig, denn «Schachtel 3» ist die dritte der «3 Schachteln» von 6. Seither
  bekommen aber 7.–10. (10 Einheiten) Schachtel 3, obwohl die Schachteln je Abschnitt zählen (mittel, Ursache nicht
  ermittelt).
- **D3063:** 6. und 40. aus der Übersicht sind echt und nicht doppelt. 51. hat Schachtel 24 verloren (gering).
- **D1237, D4054:** In D1237 steht im Blatt Info nur eine Bearbeitungsnotiz, die Schachteln stimmen. In D4054 ist K141
  behoben, und die Teile 6–16 von 10.3.4. sind nur umnummeriert.
- Mittlere Funde: D3063 8.–12. und 21.–23., D3316 1.44.–2.5., D3774 6.4., D4054 10.3.4. Teil 16, D2850 64.

### Regeln 6–8 (G2)

- Alle 17 neuen Überschrift-Hinweise sind echte Überschriften. Keiner ist Titelfortsetzung, Darin oder Vermerk der vorigen
  Einheit.
- K134 «(Enthält Patientendaten!)» steht bei der Einheit davor. K162 steht im Darin von so vielen Einheiten, wie die
  Gruppenzeilen nennen (29 bzw. 2).
- **K161:** Rest mittel, weil der Zeitraum von 7. aus einem Literaturzitat kommt (1889 statt o. J.).
- **Mittlere Funde:**
  - D10585 7.2.3.: Zeitraum 1815–1952, «fasc. 1815» ist aber eine Heftnummer;
  - D4173 1.14.–1.16.: Die Titel sind ohne die Überschrift unverständlich; der Block steht nur im Hinweis von 1.14.;
  - D176795 2.3.4.: Titel;
  - D3231 2.7.: Schachtel.
- **D406 (K146):** Der Vermerk «:56.–65. sind nicht vorhanden» steht nur im Prüfhinweis von :56. Das ist nach Soll zulässig.
  Weil es ein Fehlbestand ist, wäre er im Darin besser sichtbar.

### Regeln 9, 10, 11 und 17 (G3, Regel 9 von mir)

- **Regel 9:** Ich habe alle 12 neuen Fälle an der PDF-Folge geprüft (`roh/np13_regel9.txt`).
  - Richtig sind 10, darunter die 8 K-Zeilen und D151210 4.1.3.38. Damit ist auch der Widerspruch zwischen NP6 und NP12
    erledigt: NP6 hatte diesen Fall nach Entscheid 5 als «kein Fund» gewertet, NP12 gleich gebaute Fälle als kritisch.
  - D2992 3. → 1.3. stand schon vorher so; neu ist nur der Hinweistext.
  - **Fehlgriff D3470:** «40.430» → 42.430. und «41.436» → 42.436. Der Vorspann sagt: «Die erste Nummer ist im ersten Teil
    des Bestandes frei gewählt worden.» Auch sonst wechselt die erste Nummer ohne Ordnung (43.449–43.451, 44.448, 45.0). Die
    Datei ist flach, darum ist nur die Signatur falsch (mittel).
- **Regel 10:** Alle neuen Geschwister stehen in derselben Spalte wie «n.» und haben eigenen Gegenstand oder eigenes Datum.
  Die Regel hat aber Lücken:
  - D152817 VI.SB.C.33.a (K186) und Testdatei D152810 32.a und 75.a (K187, K188) bleiben Kinder, weil «n.» eigene Bände
    «:1–:n» hat; das Layout ist dasselbe wie bei 18.a, 13.a, 73.a;
  - D3470 11.43.a. und 11.44.a. (K185) bleiben Kinder in einer flachen Liste ohne Umfang und Datum.
- **Regel 11:** D9978 verliert durch das Entfernen der Blattangabe aus 21 Titeln keinen Text. K152 und K153 sind behoben,
  mit je einem mittleren Rest. Neu steht durch K153 die Notiz «1982/84» im Darin von 28.4.25., der Zeitraum ist deshalb
  07.1935–1984 (mittel).
- **Regel 17:**
  - Nur in D3472 fehlt die Nachbarnummer (K183, K184).
  - In D2857 (5 Teile), D2979 (3), D149888 (2), D847 (2), D3186 und D3470 (7) sind die Nachbarnummern da: kein Fund.
  - In D149888 13.1. ist der Hinweis falsch (gering): Der Teil kommt aus «Schachtel 2:», die Signatur steht nur einmal im
    PDF.

### Regeln 12–16 (G4)

- **D2735 (K165) ist richtig.** Die 20 weggefallenen Einheiten waren Mappen. Ihr Inhalt steht vollständig bei der richtigen
  Schachtel.
- **D3412:** 143 der 146 neuen Einheiten sind echt. Zwei Fehler:
  - 19 Einträge ohne Nummer («Nr. K.V.», «Nr. -») stehen im Darin von 312., dessen Zeitraum dadurch 1945–1983 statt 1983 ist
    (K190);
  - der zweizeilige Eintrag «Nr. 146/ … / Nr. 148 Stäfa» ist zerrissen: Sein Text steht bei 144., und 148. heisst nur
    «Stäfa» (K191).
- **D151150, Rest von K144:** 186 Dossiers sind jetzt Einheiten. Regel 14 greift aber nicht für die Nummern 1208–2024,
  vermutlich weil sie wie Jahreszahlen aussehen. 105 Dossiers stehen deshalb im Darin von 9.1194., dessen Schachtel und
  Zeitraum falsch sind.
- **D151150, K189 (Rückschritt):** Die erste Nennung von 9.501. «Mietauto für Fleischschau» (S. 7) fehlt ganz. Sie ist als
  Übersichtszeile verworfen, und die Vollständigkeit zeigt trotzdem 100 %. In Runde 9 stand die Zeile noch im Darin von 9.
  Mein Textabgleich (`roh/np13_textverlust_r9_r10.csv`) zeigt die drei Wörter als verloren.
- **D10744, Rest von K178:** 020, 600 und 700 sind jetzt Gruppen. Regel 16 macht aber 710 zur Zehnergruppe über 711–718.
  Damit liegen 46 Einheiten eine Ebene zu tief. Das widerspricht der Schrift im PDF (710 steht wie 711–718 und 610/611 in
  12 pt fett, die Gruppen in 14 pt) und dem Soll.
- D3528 (K151), D414 (K179), D3021 (K157), D2759 (K99) und D2894 (K175) sind behoben.

### Regeln 11–13 in grossen Dateien (G5)

- **D32837:** Die Gliederung ist ganz per Skript geprüft (Eltern, Ebenen, Folge, Teile) und sauber. Die Folge aller 267
  PDF-Signaturzeilen deckt sich mit der Excel. K128–K131 sind behoben.
- **Regel 12** hat nichts doppelt oder erfunden:
  - D32837 1., D3672 X. mit X.1.–X.4. und D140969 57. stehen nur in Übersicht bzw. Inhaltsverzeichnis;
  - in D2643 sind die sieben «[Enthält …]» richtig zugeordnet;
  - D3190 9. ist jetzt eine einzige Einheit aus dem Detail.
- **Regel 13, D3943:** Die 9 Unternummern haben richtige Titel, Jahre und Eltern. Der Zeilenübergang bei X.G.209. verliert
  keinen Text.

## Suchläufe über alle 715 Dateien

### Tippfehler in Dezimalsignaturen

- **Werkzeug:** `methode/np13_suchlauf_tippfehler.py`. Es ordnet jede Einheit über den Zeilen-Cache in die PDF-Folge ein
  (verankert: 50'434 von 51'508) und meldet:
  - eine Signatur, die nur in 1–2 Zeichen von der Signatur abweicht, die die PDF-Nachbarn erwarten lassen, und die dadurch
    unter anderen Eltern hängt;
  - eine Lücke in einer Folge, an deren Stelle im PDF eine Zeile mit Nummer in der Signaturspalte steht, die keine Einheit
    ist;
  - eine Signatur, die genau zweimal mit anderem Titel vorkommt, während die Nachbarnummer fehlt.
- **An Runde 9 (Probe des Werkzeugs):** 16 Zeilen.
  - Gefunden sind alle 9 bekannten K-Zeilen dieses Musters (K124–K126, K129, K132, K135, K139, K140, K149), dazu D151210
    4.1.2.38. und D3472 1952.8/1952.14.
  - Die Lückenprüfung findet genau D10585 «7. 2.3.» (K137).
  - Vier schwache Treffer stehen in Planlisten.
- **An Runde 10:**
  - Keine Einheit hängt mehr unter fremden Eltern, und es gibt keine Lücke mit Signaturzeile.
  - 7 Teil-Zeilen: D3472 zweimal kritisch (K183, K184); D176060 = K135 (Konventionsfrage).
  - Kein Fund sind D3468 1958.16 und 1983.11, D3482 1953.25 und D3484 405: In diesen Planlisten trägt oft eine Nummer mehrere
    Objekte, und die Plan-Nummer ist gleich.
  - In den Testdaten gibt es keinen Treffer.

### Stück ohne Nummer im Blatt Info

- **Werkzeug:** `methode/np13_suchlauf_info_stuecke.py`. Es sucht Sätze in den Schlussvermerken, die Archivgut ohne
  Signatur nennen. Gefunden sind 24 Sätze in 20 Dateien.
- **Kritisch:** «Die Protokolle von … bis … sind lose verschachtelt.» in D151759 (Z3, K198), D151756 (K192) und D152383
  (K193). Regel 4 erkennt diese Form nicht.
- **Kein Fund:**
  - Verweise auf Material ausserhalb des Bestands (Bibliothek, Zentralbibliothek, Institut, andere Bestände);
  - Bearbeitungsbemerkungen und Literatur;
  - D141062 «Ferner sind kleinere Aktenbestände vorhanden …»: Der Satz steht als Prosa im Vorspann, ist nach dem Entscheid
    zu K171/K176 also mittel.

### «n.a» als Kind (Suchlauf von G3)

- **Kritisch:**
  - D150589 2.2.1.8. a und 2.2.9.12. a (K194, K195): eigene Vorträge mit eigenem Datum, als Kinder fremder Vorträge;
  - D152817 33.a (K186);
  - D3067 IV.A.5.a./b. (Z3, K197).
- **Vor dem Entscheid zu Buchstaben in der Titelspalte** hatte ich D3012 1.a.–c./8.a.–c. und D3089 I.3.a. als echte
  Unterteile gewertet. D177470 27./28. a)–h) war eine Konventionsfrage. Nach dem Entscheid sind alle drei kritisch, dazu
  D3038 (K199–K202, Nachtrag).

## Zufallsstichprobe

- **Festgelegt vor Runde 10:**
  - Reihenfolge `random.Random(20261122)` über die 715 Dateien (`roh/np13_zufall_reihenfolge.txt`);
  - Stichprobe = die ersten 60 Dateien, die Runde 10 nicht geändert hat und die nicht in `offen_kritisch.csv` stehen (Rang
    1–73);
  - Grundgesamtheit: 642 Dateien.
- **Umfang:** 60 Dateien mit 1'287 Einheiten, je ganz geprüft: Z1 20 Dateien mit 600 Einheiten (darunter D438), Z2 20/344,
  Z3 20/343.
- **3 kritisch vor dem Entscheid der Hauptsession (5 %, 95%-KI 2–14 %):**
  - **D2620 (K196):** «Bibliographische und andere Notizen (1 Mäpplein)» am Ende von Gruppe 1 steht im Darin von 1.22.
    Inhaltsverzeichnis und Gruppenkopf kündigen die Notizen für die ganze Gruppe 1 an («einschliesslich bibliographische
    Notizen»).
  - **D3067 (K197):** IV.A.5.a. und 5.b. hängen als Kinder unter 5. Es sind eigene Schriftstücke anderer Absender mit eigenem
    Datum in derselben Spalte, also Geschwister. 5. wird dadurch Serie mit falschem Zeitraum.
  - **D151759 (K198):** «Die Protokolle von 1964 bis 1981 sind lose verschachtelt.» steht nur im Blatt Info.
- **Hochrechnung:** 5 % von 642 sind etwa 32 Dateien (KI 11–88). Davon sind jetzt 6 bekannt: 3 aus der Stichprobe und 3 aus
  den Suchläufen.
- **Nach dem Entscheid zu Buchstaben in der Titelspalte** (Nachtrag) ist auch D177470 kritisch (K199). Damit sind es 4 von 60
  (6,7 %, KI 2,6–15,9 %), hochgerechnet etwa 43 Dateien (KI 17–102). Bekannt sind davon 10: 4 aus der Stichprobe und 6 aus
  den Suchläufen.
- NP12 hatte D2620 mit der Kompaktmappe geprüft. Dort war genau diese Zeile als unauffällige Darin-Zeile verdichtet.
- **Mittlere Funde** (27 neu), häufigste Muster:
  - Titel und Darin sind am Zeilenumbruch falsch getrennt;
  - Zeiträume kommen aus Jahreszahlen in Werktiteln, Literatur oder Lebensdaten;
  - Schachteln werden nicht über Abschnittsgrenzen übertragen.
- **D8952 (Z1):** «Es liegen Farbfotokopien der 8 Lithographien bei.» steht in der Bestandsbeschreibung vor der ersten
  Signatur. Das ist eine Vorbemerkung in Prosa, nach dem Entscheid zu K171/K176 also mittel.

## Neue kritische Zeilen (K183–K202)

| Muster | Zeilen | Fälle |
|---|---:|---|
| Buchstaben in der Titelspalte als Einheiten (nach dem Entscheid vom 22.11., Nachtrag) | 4 | K199 D177470, K200 D3012, K201 D3038, K202 D3089 |
| «n.a» als Kind, Regel 10 greift nicht | 7 | K185 D3470, K186 D152817, K187/K188 D152810 (Testdaten), K194/K195 D150589, K197 D3067 |
| doppelte Nummer, Nachbarnummer fehlt, Regel 17 setzt nur den Hinweis | 2 | K183/K184 D3472 |
| Stück ohne Nummer nur im Blatt Info | 3 | K192 D151756, K193 D152383, K198 D151759 |
| Einträge ohne Nummer im Darin der letzten Einheit | 1 | K190 D3412 |
| zweizeiliger Eintrag zerrissen | 1 | K191 D3412 |
| Einheit fehlt, als Übersichtszeile verworfen | 1 | K189 D151150 |
| Zeile am Gruppenende bei der letzten Untereinheit | 1 | K196 D2620 |

Durch Runde 10 entstanden sind:
- **K189 (D151150):** Die Zeile stand vorher im Darin von 9., jetzt fehlt sie ganz.
- **K190 und K191 (D3412):** Vorher stand die ganze Datei in einer einzigen Einheit. Die neue Gliederung hängt die 19
  Einträge ohne Nummer an 312. und zerreisst 146/148.
- der Rest von K156 (D3808).

Die übrigen 17 Zeilen bestanden schon vorher.

## Konventionsfragen (inzwischen entschieden, siehe Nachtrag)

1. **K135 und Regel 17.** In D176060 bleibt «Pathologies somatiques …» Teil 2 einer fremden Publikation, jetzt mit dem
   Hinweis «… zweimal hintereinander mit anderem Titel – Tippfehler? Als Teil übernommen». Das Soll der NP12 verlangte nach
   Entscheid 5 eine eigene Einheit.
   - Ich habe Regel 17 als Konvention der Hauptsession übernommen, weil die Nachbarnummern 7.4.1.25. und 7.4.1.27. da sind
     und der Tippfehler nicht eindeutig ist. K135 ist deshalb mittel.
   - Bitte bestätigen. Soll stattdessen die eigene Einheit gelten, betrifft das alle Teile mit diesem Hinweis.
2. **Buchstaben in der Titelspalte.** In D177470 (27. und 28., je a)–h)) und D3826 (8. und 14., a)–c)) steht der Buchstabe
   in der Titelspalte der Gruppe, mit eigenem Datum.
   - Das Layout ist gleich, das Ergebnis nicht: D177470 macht daraus Einheiten, D3826 Darin.
   - Nach der Konvention «Listen ohne eigene Signatur stehen im Darin» und nach Regel 15 (K142) wäre D177470 falsch, nämlich
     erfundene Einheiten und damit kritisch. Die Stichprobe hätte dann 4 von 60.
   - Empfehlung: einheitlich Darin wie in D3826, ausser die Buchstaben stehen in einer eigenen Spalte. Bis zum Entscheid ist
     es nicht gezählt.
3. **K178, D10744:** 710 ist Zehnergruppe über 711–718. Das widerspricht der Schrift im PDF und dem Soll, darum bleibt es
   kritisch. Will die Hauptsession Zehnergruppen als Konvention, entfällt der Rest.

### Nachtrag: Entscheide der Hauptsession (22.11.2026)

Eingetragen mit `methode/np13_entscheide_hauptsession.py`; die K-Nummern bleiben, neue Zeilen sind K199–K202. Die Liste
davor (29 Zeilen) liegt in `roh/np13_offen_kritisch_vor_entscheid.csv`.

1. **K135 / Regel 17: bestätigt.**
   - Stehen die Nachbarnummern da, bleibt die zweite Nennung ein Teil mit Hinweis «Tippfehler?». K135 ist mittel.
   - Fehlt die Nachbarnummer, wird die zweite Nennung zur fehlenden Nummer, mit Hinweis (K183, K184). Umsetzung in Runde 11.
2. **Buchstaben in der Titelspalte:** a)–h) in der Titelspalte einer Gruppe (nicht in der Signaturspalte) sind Darin-Einträge
   der Gruppe, auch mit eigenem Datum. Eigene Einheiten werden sie nur in einer eigenen Spalte.
   - Ein neuer Suchlauf (`methode/np13_suchlauf_buchstaben_titelspalte.py`) findet 27 solche Einheiten in 4 Dateien. Er
     meldet Einheiten, deren Buchstabe dort steht, wo bei der übergeordneten Einheit der Titel beginnt.
   - Die vier Dateien:
     - **K199 D177470:** 27.a.–h. und 28.a.–h., 16 Einheiten. D177470 liegt in der Stichprobe (Z2) und zählt nun dort.
     - **K200 D3012:** 1.a.–c. und 8.a.–c.
     - **K201 D3038:** I.a. und I.b.
     - **K202 D3089:** I.3.a.–c.
   - In D3038 und D3089 sind es Untergruppen mit eigener Schachtel und Bandliste («a) Vorstandsprotokolle» mit 11 Bänden).
     Bitte bestätigen, dass der Entscheid auch dafür gilt; sonst entfallen K201 und K202.
   - Die Fälle in derselben Spalte wie die Nummer bleiben Einheiten: Regel 10 (Geschwister) und D150589 «2.2.1.8. a».
3. **K178 D10744:** keine Zehnergruppen nach der Nummer allein. Gruppe wird ein Code nur nach der Schrift (14 pt gegen 12 pt);
   710 ist ein gewöhnlicher Code. Umsetzung in Runde 11.

## Vorschläge für Runde 11

1. **Regel 14 (K144):** Nummern 1208–2024 in der Nr.-Spalte sind Nummern, wenn sie die Folge fortsetzen und Titel, Jahre und
   Schachtel folgen.
2. **Übersichtszeilen (K189):** Eine Zeile mitten im Detail mit eigenem Titel, Jahr und Schachtel nie als Übersichtszeile
   verwerfen. Eine doppelte Nummer wird Teil mit Hinweis.
3. **Regel 4:**
   - auch «Die … von … bis … sind lose verschachtelt.» erkennen (K192, K193, K198);
   - Einträge ohne Nummer in der Nummernspalte («Nr. K.V.», «Nr. -») nach der letzten Einheit in die Bestandszeile (K190);
   - den Schlussvermerk («Stand: …», Kürzel und Datum) nie in die Bestandszeile (K156).
4. **Regel 10 erweitern** (K185–K188, K194, K195, K197): «n.a» direkt nach «n.» in derselben Spalte ist Geschwister auch dann,
   - wenn «n.» eigene Bände «:1–:n» hat;
   - wenn die Liste flach ist, ohne Umfang und Datum;
   - wenn das Datum nur im Titeltext steht.

   Buchstaben in der Titelspalte einer Gruppe sind nach dem Entscheid vom 22.11. keine Einheiten, sondern Darin der Gruppe
   (K199–K202).
5. **Doppelte Nummer, die Nummer danach fehlt (K183, K184):** wie D1473/D1479 umdeuten. Steht «n» zweimal und fehlt «n+1»,
   wird die zweite Nennung «n+1», mit Hinweis.
6. **Regel 9** nicht anwenden, wenn die letzte Stelle über alle Gruppen durchläuft (D3470).
7. **Regel 16 (K178):** Zehnergruppen nur nach Schrift (14 pt fett) und ohne eigene Schachtel. 710 ist ein gewöhnlicher Code.
8. **Zweizeiliger Eintrag (K191):** «Nr. 146/ …» mit «Nr. 148 Stäfa» auf der Folgezeile ist eine Einheit.
9. **Gruppenende (K196):** Eine eingerückte Zeile nach der letzten Untereinheit, mit grösserem Abstand, die das
   Inhaltsverzeichnis für die Gruppe ankündigt, gehört ins Darin der Gruppe.
10. **Kleinere Fälle:** D149888 13.1. falscher Hinweis (gering), D2962 Schachtel 3 bei 7.–10. (mittel), D9978 28.4.25.
    Zeitraum (mittel), D406 Fehlbestand-Vermerk auch ins Darin.

**Für den Textabgleich der Hauptsession** (`runde10/werkzeug/textverlust.py`): Zahlen getrennt ausweisen oder weglassen.
In D151150 verdeckten 837 fehlende Zahlen die drei Wörter «Mietauto für Fleischschau» (K189).

**Für die Prüfmappen** (meine Werkzeuge): die letzte Zeile vor einem Wechsel auf eine höhere Ebene nie verdichten (D2620),
und Signaturformen wie «3:1-3» sicher verankern (D140969).

## Nächste Nachprüfung (NP14)

- **Gegenprüfung der Runde 11** an den geänderten Dateien, mit den 23 nicht bewusst offenen Zeilen als Altzeilen.
- **Suchläufe über alle 715 Dateien:**
  - Tippfehler, Stück ohne Nummer im Info und «n.a» als Kind wie in NP13;
  - neu «Gruppenende» mit den verbesserten Prüfmappen;
  - Nummern, die wie Jahreszahlen aussehen, in Nr.-Spalten.
- **Zweite Zufallsstichprobe** von 60 Dateien aus derselben festen Reihenfolge (ab Rang 74). Sie schätzt die Restrate nach
  Runde 11; zusammen mit dieser Stichprobe sind es 120 Dateien, das Konfidenzintervall wird enger.

## Dateien

- `offen_kritisch.csv`: 33 Zeilen.
  - Die K-Nummern bleiben; neu sind K183–K202.
  - 68 erledigte Zeilen sind entfernt. Die Liste vor NP13 (81 Zeilen) liegt in `roh/np13_offen_kritisch_vorher.csv`, die
    Fassung vor den Entscheiden der Hauptsession (29 Zeilen) in `roh/np13_offen_kritisch_vor_entscheid.csv`.
- `funde_nachpruefung13.csv`: 159 Zeilen, mit Paket, K-Nummer und Entscheid der Prüfsession bzw. Hauptsession.
- Suchlauf «Buchstaben in der Titelspalte»: `roh/np13_buchstaben_titelspalte_r10.csv`.
- `roh/np13_*`:
  - Pakete G1–G5, Z1–Z3 und S (Funde der Prüfsession): Funde, Urteile, Dateiurteile, Notizen;
  - `np13_dateien_urteil.csv`, Vergleiche Runde 9 → 10 in `np13_vgl/`;
  - Suchläufe `np13_tipp_r9.csv`, `np13_tipp_r10.csv`, `np13_tipp_test_r10.csv`, `np13_info_stuecke_r10.csv`,
    `np13_textverlust_r9_r10.csv`;
  - Stichprobe `np13_zufall_reihenfolge.txt`, `np13_zufall60.txt`, `np13_population_715.txt`;
  - `np13_regel9.txt`, `np13_geaendert_r10.txt`, `np13_AUFTRAG13.md`.
- `methode/ANLEITUNG_NACHPRUEFUNG13.md` und `methode/np13_*` (Suchläufe, Zusammenführen, Ablaufskripte).
- Fallsets: Soll-Zeilen nachgeführt in `verbesserung/werkzeug/faelle/a_faelle.csv`, `b_faelle.csv` und
  `verbesserung/runde2/werkzeug/runde2_faelle.csv`.
