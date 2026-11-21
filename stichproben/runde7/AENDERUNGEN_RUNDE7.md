# Gliederungsrunde (Runde 7) – Änderungen und Bitte um Nachprüfung 8

Stand 22.11.2026. Skript `findmittel_zu_scope.py` sha256 `1f98df0beaaea412…`. Aufbau: Stand nach Runde 2 und Punkt 2
(`2953088e…`) plus diese Runde.

`findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind mit diesem Skript neu erzeugt.

## Worum es ging

Eine Strukturprüfung über alle 715 Ausgaben (`werkzeug/gliederung.py`) hat Gliederungsbrüche gefunden, die weder die
Kennzahlen noch die Stichproben zeigen:

- Unternummern im Darin;
- Signaturen im Titel;
- Lücken in Nummernfolgen, deren Text im Darin steht;
- Listen, die als Hauptnummern gelesen werden;
- Signaturen ohne «:».

Die Funde wurden am PDF gesichtet; das zweite Drittel davon hat eine Hilfsprüfung triagiert. Bei den echten Fällen
ist die Ursache behoben.

| Signal | vorher | nachher | Bedeutung |
|---|---:|---:|---|
| T | 10 | 9 | Titel beginnt mit Signatur. Rest nur D3776: dort ist es die Kapitelnummer im Titel der Mappe, richtig. |
| D | 45 | 0 | Unternummern im Darin. |
| L | 36 | 20 | Nummer fehlt, ihr Text steht im Darin. Rest laut Triage legitim (Hausnummern, Daten, «Mappen beseitigt», Gruppensprünge). |
| : | 186 | 163 | Signatur ohne «:». Rest legitim: III.G./P./Q./R., X.C. schreiben nie «:». Ausnahme D151773, Sonderform. |
| E | 37 | 61 | Eltern ist kein Präfix. Legitim: D10675 (Registraturplan) und D3774 (2.31. unter 2.3.). |

Kennzahlen:

- Einheiten 49'242 → 48'980.
- «[ohne Titel]» 34 → 31.
- «Text erfasst 100 %» 695 = 695.
- Doppelte Schlüssel 10 = 10.
- Tracebacks 0.

**Geändert sind 34 Dateien** (`geaenderte_dateien.txt`). Ihr Stand vorher liegt in `vorher/`, der neue in
`findmittel_excel/`.

**D151210 und alle Testdaten sind zellgleich mit vorher.**

## Regeln (mit Beispiel und betroffenen Dateien)

1. **Bereich mit Buchstabe am Ende.** «VII.4.:6-7a Kopierbuch …» war nicht erkannt; Einheit und Bände standen falsch.
   Jetzt ist 6-7a eine Einheit mit den Kindern 6, 7, 7a. D3698.
2. **Nummerierte Liste unter einer fetten Hauptnummer** (D3828: vorher 99 Einheiten, die Abschnitte 4–9 fehlten; jetzt
   31).
   - Fall: fett «1. 1. Fortifikation von Zürich», darunter «1. Bericht …» bis «28. Schachtel …»; unter «3.1.» stehen
     «1.» bis «25.».
   - Regel: «2.» bzw. «4.» setzt die Liste fort und ist nicht die nächste Hauptnummer. Die Zählung gilt je Spalte, auch
     für die Zehnerregel.
   - Betroffen: D3828 und D3530 (63 Bibliografie-Einträge waren Hauptnummern 3–63).
   - Zusätzlich D3828: die doppelte Nummer «6. 5. Brückenbauten» wird als 5. gelesen, mit Hinweis.
3. **Unternummern.**
   - Ohne Punkt angehängt: «2.3.» / «2.31.» … «2.38.» / «2.4.» / «2.41.» ist 2.3.1. Die Signatur bleibt wie im PDF,
     die Einheit hängt unter 2.3., mit Hinweis. D3774: 34 → 59 Einheiten.
   - Rückkehr zur nächsten Nummer einer höheren Stufe.
   - Unternummern in der Titelspalte (x 170–184), wenn sie erstes Kind oder nächstes Geschwister sind. Der letzte
     Punkt darf dann fehlen («7.4», «2.54»). D151730, D152400.
   - Konvention: Unterpunkte mit eigener Signatur werden eigene Einheiten. Bloss nummerierte Listen (1., 2., …) bleiben
     im Darin.
4. **Sammelmarke als Bereich.** «Mappen 2 - 3 1. Überblick», danach «Mappe 2», «Mappe 3»: jetzt Einheit 2-3 über den
   Mappen. Vorher stand der Text im Darin von Mappe 1. Ein Kapitel mit Unterkapiteln ist Titel der Mappe
   («2. Siedlungsentwicklung»). D3776.
5. **Gliederungsränge** (D2850: 54 → 71 Einheiten).
   - Umbrochene Daten («1. Juni 1925») zählen beim Lernen der Ränge nicht mehr als Nummer. D2850 hatte dadurch «A./B.»
     über den Zahlen: 49–66 fehlten, B.12.1961. war erfunden. Jetzt gibt es 48 mit 48.A., 48.B., danach 49–66.
   - Eine fette Zwischenüberschrift, unter der eingerückt weitergeht, bleibt in der Untergruppe.
   - «A. Engelhardt» nach «Künstler:» ist ein Name.
6. **«Signatur: Stadtarchiv Zürich V.G. c.42.:2» im Inhalt.** Die Tabelle darunter (192 Planmappen, Codes «X», «-»)
   ist Inhalt von 2. Sie gilt bis zur nächsten Nummer derselben Stufe. Vorher waren «X» und die Mappennummern
   erfundene Einheiten. D1874: 303 → 105.
7. **Übersichten.**
   - Auch nach einer Überschrift «Verzeichnis» wird eine Übersicht übersprungen, wenn ihre Einträge mit gleichem Titel
     wiederkommen. Beispiel D3256: «1. Kopie der Gründungsakten» … «5.» / fett «1. … Schachtel 1»; vorher war jede
     Einheit doppelt.
   - Nach einer schwachen Überschrift gilt nur eine echte Wiederholung, keine Bände-Spalte als Seitenzahl (D3808 bleibt
     richtig).
   - Eine kurze Liste direkt unter «Übersicht», deren Zählung im Verzeichnis neu beginnt, gilt als Übersicht nach
     Gruppen. Beispiel D3826: «1. Amtliches / 2. Privates / 3. Gratulationsdiplome». Ihre Zeiträume werden nicht
     übernommen.
   - Nicht bei Vollsignaturen: III.Q./III.R. bleiben wie bisher.
8. **Zahl am Anfang einer Inhaltszeile** in der Textspalte, die nicht die nächste Nummer ist, ist keine Signatur. Fälle:
   «7 Einladungen …» unter «1. Akten» (D2745), «3 Auszüge …» (D2687).
   - Die Fortsetzungszeile eines Verweises «… und Passiver Luftschutz» / «V.B. c.57.:10.» ist keine Einheit (D448).
9. **Doppelnummern «3/4», «7/8», «10/11».** Sie gelten als Einheit, wenn sie die Folge fortsetzen; danach wird ab der
   zweiten Nummer weitergezählt. Ein Datum mit Leerzeichen «11. 2. 1987 / Hb» ist keine Signatur. D2737: 5 → 8.
10. **Bereich als Gruppe.**
    - «13 – 34 Akten 1925 – 1940», «57 – 58 Zeitungsausschnitte» werden Bereichseinheiten über den Nummern, wenn sie
      mit der nächsten Nummer beginnen (D140969).
    - Eltern ist der engste Bereich: 57-58 liegt in 50-58 (D140969), 8 in 8-11 in 8-12 (D152817).
    - Die Zeiträume der Gruppen werden nach der Tiefe im Baum berechnet.
11. **Signaturform.**
    - Schreibt ein Findmittel mindestens 75 % seiner Vollsignaturen «Bestand:Nummer», bekommen die übrigen das «:» mit
      Hinweis. Beispiele: «VII. 47.1.» → VII.47.:1., «V.J. c.402.16.» → V.J.c.402.:16.
    - Betroffen: D3774, D151730, D3816, D176721, D151761, D152390, D845, D141, D2270.
    - Nicht bei Beständen, die nie «:» schreiben (III.x, X.C.).
12. **«Anmerkungen zum Bestand …» auf den letzten Seiten.** Alles danach kommt ins Info-Blatt.
    - D149835: die Liste 1.–7. dort war zu Teilen von 1.–7. geworden. Auch die Nc-Urkunden stehen jetzt im Info-Blatt.
    - D2620: die Anmerkungszeilen sind aus dem Darin von 15.3. heraus.
13. **Klammerliste.** Bei einer Einheit mit eigener Signatur wird der Titel erst ab drei Klammereinträgen als erster
    Listeneintrag behandelt; bei Teilen wie bisher ab zwei. Dadurch haben eigene Titel statt eines geerbten:
    - D134644 10.1.1. «Rechtes Limmatufer (grosse Stadt)», laut Inhaltsverzeichnis richtig;
    - D150689 1.8.1. und 6.3.2.;
    - D3313 2.;
    - D3677 1.24.;
    - D3951 :3.

    Gemischt ist D152781 5.1.
14. **Schlussblock auch links einer eingerückten Unternummer.** «Vgl. auch V.J. b.202. …» kommt ins Info-Blatt, nicht
    ins Darin von 7.4. (D152400). D3810: «10.09.1992» zählt nicht mehr zum Zeitraum von 21.
15. **Bearbeitungsvermerk mitten im Findmittel.** «29. Juli 1999 / RD» (Monatsname oder Ziffern) kommt ins Info-Blatt.
    D1874: Einheit 2 reicht nicht mehr bis 1999.

## Fallsets

| Fallset | Ergebnis | Bemerkung |
|---|---|---|
| a | 11/12 | unverändert |
| b | 36/38 | D2737 ID 5 ist verschoben; 9. ist jetzt ID 7, der Wert 1914–1987 stimmt |
| c | 9/12 | D3828 ID 20 ist verschoben; 3.16. ist jetzt ID 22, 1940–1945 stimmt |
| f | 5/7 | unverändert |
| Runde 2 | 33/34 | D149835 7.: «Nc 4-6 …» steht jetzt im Info-Blatt (Regel 12), beabsichtigt |
| Punkt 2 | 38/38 | |

Die Fallsets a–c, f arbeiten mit IDs. In den 34 geänderten Dateien verschieben sich IDs, deshalb bitte nach Signatur
vergleichen.

## Bewusst offen

- **D3894:** Die Abschnitte «1.»–«4.» (14 pt) kollidieren mit den Siegeln «X.C. 1.»–«4.». Siegel 1 ist Teil 2 von
  Abschnitt 1, die Abschnitte 2–4 sind Teile der Siegel 2–4; 8 Zeilen. Eine Trennung nach Signaturform würde anderswo
  Übersichten verdoppeln.
- **D3190:** Die Übersichtszeile «9.» bleibt als Einheit mit dem Detail als Teil 2. Im Detail fehlt die Zeile «1.».
- **D2681:** Zwei Abschnitte zählen Mappe 1–10, die Signaturen sind doppelt. Dazu müsste ein Abschnittsteil der
  Signatur erfunden werden.
- **D1343, D152390:** Das PDF vergibt Nummern doppelt.
- **D3828:** «3.4. Akten zu verminten Brücken» steht im Abschnitt 2 (Tippfehler im PDF). Diese erste Nennung wird
  Einheit 3.4., die echte «3.4. Bundesfeiern» im Abschnitt 3 dadurch Teil 2 davon.
- **D149835:** «4.2.» ohne «4.» steht so im PDF.
- **D1874:** Der Code «-» (Planmappe nicht mehr vorhanden) fällt wie bisher als Aufzählungszeichen weg; «X» bleibt.
- **D151773:** Die Form «..5/..6» wird nicht angeglichen.
- **Platzhalter-Einheiten:** «nicht belegte Signaturen», «Nicht vergeben» (34 in 11 Dateien). Die Konvention ist
  offen; heute werden sie behalten.

## Bitte um Nachprüfung 8 (kurz)

1. **Die 34 geänderten Dateien am PDF prüfen**, Schwerpunkt Gliederung:
   - Eltern, Ebenen, Teile;
   - keine verlorene oder erfundene Einheit;
   - Titel und Signatur.

   Vergleich vorher/nachher:
   `python -I stichproben/runde7/werkzeug/zelldiff.py stichproben/runde7/vorher findmittel_excel D3828 [max] [breite]`.
   `werkzeug/sig.py <xlsx> <regex|#a-b>` zeigt Einheiten.
2. **D151210:** zellgleich mit vorher. Bitte nur kurz bestätigen, dass `D151210_scope_import.xlsx` sauber ist.
3. Die unveränderten Dateien sind zellgleich mit dem Stand nach Runde 2/Punkt 2.
4. **Urteil:** stabil genug für Commit und Push inklusive aller Excel?

`werkzeug/zeige.py` und `werkzeug/rawlines.py` lesen PDF-Zeilen aus einem Zeilen-Cache. Den Cache legt das Skript mit
`--cache <ordner>` an: `<ordner>/<D>.zeilen.json`. Alternativ direkt am PDF in `findmittel_pdf/pdf/` prüfen.

## Nachtrag nach Nachprüfung 8 (22.11.2026)

Skript sha256 `e896fb6c54b4e64a…`. `findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind damit
neu erzeugt.

Gegenüber dem geprüften Stand `1f98df0b` sind 14 Dateien geändert:

- D152404, D152781, D176795, D1874, D2850, D3018, D3313;
- D3484, D3530, D3566, D3810, D3828, D3842, D512.

Unverändert gegenüber `1f98df0b`:

- D151210 und alle Testdaten (zellgleich mit dem Stand nach Punkt 2);
- die Fallsets.

Kennzahlen:

- Einheiten 48'980 → 48'920.
- «[ohne Titel]» 31 → 30.
- «Text erfasst» 695.

Behoben sind die Funde aus `nachpruefung8.md`, soweit sie die Regeln betreffen:

1. **D2850 kritisch:**
   - «2.1939», «12.1961» (Monat.Jahr in der Datumsspalte) sind keine Signaturen mehr. Das kommt im Korpus nur hier vor.
   - «A. Engelhardt» nach «Künstler: ¦ 1929» ist ein Name; die Datumsspalte am Zeilenende wird übergangen.
   - Ein «Stadtarchiv Zürich» mitten in einer Liste (Briefliste S. 20) beginnt keinen Schlussblock mehr. Dadurch stehen die
     73 Namen bis «Zunftgesellschaft zum Kämbel» wieder im Darin.
   - «Zürich, Oktober 1976 / Dr. Paul Guyer …» auf den letzten Zeilen ist ein Schlussvermerk. 66 hat damit wieder seinen
     Titel.
2. **D1874:**
   - «1260 x 891» und andere Massangaben gelten nicht als Jahr; 3. erbt nicht mehr «1260».
   - «V.G. c.42.:Reg.» und «Reg. 1»–«Reg. 5» sind Einheiten. Kurze Wortkürzel sind als Signaturteil erlaubt; ebenso
     «:Va.», «:Vb.» in D152404, die vorher fehlten.
3. **D3828 3.17. Nr. 33:**
   - Eine offene Spanne eines Listeneintrags «1939 –», deren Ende allein in der Datumsspalte darunter steht («1946»),
     wird im Eintrag geschlossen.
   - Das korrigiert auch D3828 6./7., D512 (z. B. «26. Dez. 1969 – 28. März 1970»), D3484 489./490. und D3018 05.7.2.
     D3018 05.7.2. Teil 2 erbt dadurch keinen Zeitraum mehr.
4. **D3530 2.3.:** Bei einer Bibliografie (mindestens 60 % «In: …») zählen nur die Erscheinungsjahre, also der Teil ab
   «In:» und «Ort Jahr». Ergebnis 1922–1975.
5. **D152781 5.1.:** Ein Titel mit «:» am Zeilenende vor mindestens zwei Einträgen, die mit «(Jahr)» enden, wird am
   Doppelpunkt geteilt. 5.1. heisst jetzt «Persönliche Dokumente», 1923–1937. Ebenso D176795 1.3. und 1.4.
6. **D3810:** Eine Zahl, die eine Liste in der Textspalte der laufenden Einheit fortsetzt, ist Inhalt, auch als nächste
   Hauptnummer.
   - Die erfundenen 8.–21. sind weg, «8. Nachträge» ist Einheit 8.
   - Nebenbei D3842: Aus «3. Kompagnie Bat. 11» und «4. Kompagnie Bat. 11» waren erfundene Einheiten 3. und 4. geworden.
7. **D3313:** Eine nummerierte Liste in kleinerer Schrift (12 pt statt 14 pt der Gliederungsnummern) ist Inhalt, wenn sie
   neu beginnt oder eine solche Liste fortsetzt; eine Lücke ist erlaubt.
   - Das «Detailinventar der enthaltenen Porträtphotographien» 1.–46. steht im Darin von 4.: 50 → 4 Einheiten.
   - Ebenso D3566: Die Beschlusspunkte 1.–4. in «Nummer 2» sind keine Teile und Einheiten mehr. Der geschätzte Zeitraum
     von «1. Originale» ist dadurch breit (1519–1953, als «geschätzt» markiert).

Weiter offen (für eine nächste Runde):

- **D2850 55/56:** Die Briefliste A–Z steht ganz in 56. Die Aufteilung nach Initialen ist nicht gemacht.
- **D2850 64:** Doppeltitel mit Jahr in der Mitte.
- **D3313 1.–3.:** Das Jahrgangsjahr gilt als Beginn.
- **D3566 1.:** Breiter Schätzzeitraum.
- **D140969:** 50a, 88 und 89 fehlen; 87. steht neben 82-86.
- **D152817:** Abschnitte sind Eltern von Schachteln.
- **D134644 2.:** «2. Stammbuch» aus 1.2.
- **D845:** «V.C: c.52.:1.2» wird nicht erkannt.
- **D151730 19.5.:** Der Anhang steht im Darin.
- **D3774:** Zeiträume von 2. und 3.51.
- **D151761, D152390:** doppelte Hinweise.
- **Ältere offene Punkte:** siehe oben und `nachpruefung8.md`.
