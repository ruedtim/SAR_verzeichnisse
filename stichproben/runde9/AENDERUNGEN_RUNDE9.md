# Runde 9 – Änderungen und Bitte um Nachprüfung 12

Stand 22.11.2026. Skript `findmittel_zu_scope.py` sha256 `66c0fb74adddd22d…`. Aufbau: Stand nach Nachtrag 2 der Runde 8
(`bb4c958822bb50a3…`) plus diese Runde.

`findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind mit diesem Skript neu erzeugt.

## Worum es ging

Behoben sind die offenen kritischen Fälle aus `nachpruefung11.md` bzw. `offen_kritisch.csv` (ohne die bewusst offenen),
nach den fünf Mustern der Erstprüfung der 430 Dateien, dazu weitere Fälle derselben Art aus eigenen Suchläufen.

Kennzahlen (Runde 8 Nachtrag 2 → Runde 9):

- Einheiten 50'935 → 51'170.
- «[ohne Titel]» 33 → 30.
- «Text erfasst 100 %» 695 = 695.
- Doppelte Schlüssel 10 = 10; Dateien mit Übersichtszeilen 10 → 9 (D3170).
- Tracebacks 0.

**Geändert sind 78 Dateien** (`geaenderte_dateien.txt`, Blatt scope-Import oder Schlussvermerke im Blatt Info). Ihr Stand
vorher liegt in `vorher/`, dazu die drei geänderten Testdaten als `vorher/testdaten_*.xlsx`. Zellvergleich:
`zellvergleich_runde8_runde9.txt`.

**D151210 ist zellgleich mit vorher.** Bei den Testdaten ändern sich nur D177460 (K8), D3186 (K64) und D9983 (Schlussblock
«Bemerkungen zu diesem Teilbestand:» jetzt im Blatt Info).

**Fallsets:** A 11/12, F 5/7 und Punkt 2 38/38 unverändert. Drei Abweichungen, alle ohne Verschlechterung:
- B 33 → 32 und C 9 → 7: die IDs in D2940 (K104: der erfundene Teil 2 ist weg) und D3170 (K107: neue Einheit 6.1.4.4.) sind
  verschoben; die Soll-Zeilen zu D2940 ID 2/7 und D3170 ID 327 zeigen jetzt auf andere Einheiten. D3105 ID 2 ist wieder ok.
  Bitte die Soll-Zeilen in `b_faelle.csv`/`c_faelle.csv` nachführen.
- Runde 2 31 → 30: D149825 «Messingpokal …» steht nach der neuen Konvention (Regel 31) in der Bestandszeile, nicht mehr im
  Darin von 272. Bitte das Soll in `runde2_faelle.csv` nachführen.

## Konventionsentscheid «Stück ohne Nummer» (Regel 31)

Der Nutzer hat mir die Entscheide überlassen («entscheide selber»). Ich nehme Variante **(b)** aus `nachpruefung11.md`:

- Ein Stück ohne Nummer kommt ins Darin einer **eigenen Zeile für den Bestand**: Signatur = Bestand, Stufe «Bestand»,
  Titel aus dem Online-Archiv, als letzte Zeile der Datei, also ohne ID-Verschiebung.
- Der Prüfhinweis lautet: «Stück ohne Nummer im Findmittel («…», S. n) – hier beim Bestand übernommen (keine Signatur
  erfunden); in scope beim Bestand ergänzen oder von Hand als Einheit anlegen.»
- So entsteht weder eine erfundene Signatur noch fremder Inhalt bei einer Nachbareinheit.

## Regeln (mit Beispiel und betroffenen Dateien)

### Schlusstext im Darin der letzten Einheit (Muster 1)

1. **Überschrift eines Schlussabschnitts ohne «Anhang».** Danach folgt keine Signatur und keine Schachtel mehr. Die
   Überschrift ist fett oder mindestens 1,5 pt grösser als die Grundschrift (dann auch weiter rechts, bis x 300), oder sie
   steht in Textgrösse links vom Darin der letzten Einheit. Ab hier gilt das Blatt Info, auch für die Überschrift selbst.
   - Erkannte Wörter: «Literatur», «Literaturverzeichnis», «Quellen», «Bibliografie», «Verweise auf …», «Hinweise zu …»,
     «Bemerkungen», «Anmerkungen (zu …)», «Notizen zu …», «Bestandsgeschichte», «Verwandte/Weitere Bestände», «… in der
     Bibliothek des Stadtarchivs», «Nachweise zu/über …», «…: Biografisches», «Benützung».
   - Betroffen: D3702 (K62), D2947 (K102), D3677 (K97), D2733 (K82), D144909 (K75), D150536 (K96), D175454 (K109),
     D3277 (K94), D150689 (K111), D3324 (K112, auch fett bei x 185), D3390 (K65), D149622, D2710, D3530, D2589, D9983.
2. **«Anmerkungen zum Bestand …»**: Jetzt steht auch die Überschrift selbst im Blatt Info, nicht im Darin (D2620,
   D149835).
3. **Absatz zur Bestandsgeschichte ohne Überschrift** nach der letzten Einheit. Bedingungen:
   - Er steht in deren Signaturspalte, nach einem Abstand, auf den letzten zwei Seiten und vor dem Schlussvermerk.
   - Er hat 2 bis 12 Zeilen Prosa mit Satzende.
   - Er enthält ein Wort wie Bestand, Nachlass, Verein, gegründet, übergeben, integriert, StRB oder zugeordnet.
   - Das gilt nicht für den eingerückten Inhalt der Einheit.
   - Betroffen: D3503 (K83), D2848 (K86), D1759 (K110), D1439, D3204, D3727, D8631.
4. **Schlussnotiz in der Signaturspalte** («Der Bestand wurde … übergeben», «Die Literatur … ist verzeichnet bei:») zählt
   jetzt auch nach einem Seitenwechsel und links vom Darin (D3321, D175454).
5. **Findmittel nach Schachteln/Mappen.** Nach der letzten Schachtel beginnt der Schlussabschnitt mit einer Überschrift
   wie in Regel 1 oder mit einer Notiz links vom Inhalt («Lagerung: 1 Normschachtel»). Nach einem Schlussvermerk gehen
   weitere Zeilen in der Markenspalte («Briefwechsel …: 17. Dezember 2010 / RD») ins Blatt Info.
   - Betroffen: D2733, D144909, D149622, D2710, D3277, D3776, D144914, D150242, D2510, D537, D539.
6. **Weitere Schlussvermerke:** ein Vermerk mit «bzw.» («9. Januar bzw. 13. Oktober 2008 / RD», D3677) und «Neu erfasst am
   …» (D67).
7. **«Anmerkungen zu Schachtel 29:»** nach der letzten Einheit kommt ins Darin der Einheit mit dieser Schachtel bzw.
   Nummer, mit Hinweis (D3542 K89).

### Eine Bestandszeile verschluckt die Einheiten (Muster 2)

8. **Signatur ohne Punkt vor «:».** «V.F. b.13.b:1» bei V.F.b.13.b. ist eine Vollsignatur, ohne Tippfehler-Hinweis; ebenso
   «V.B. c.5::72.».
   - Betroffen: D1261 (K68, 5 Einheiten), D1263 (K91, 6), D1686 (K73, 11), D432 (72. war im Darin von 71.).
9. **Spaltenkopf «Schachtel-» / «Nummer»** (auf zwei Zeilen) bzw. «Akte / Dossier ¦ Schachtel-Nr.» schon bei wenigen Zeilen;
   die Zahl darf irgendwo unter dem Kopf stehen.
   - Betroffen: D2123 (K66, 36 Schachteln), D2127 (K67), D2372 (K92).
   - Nebenbei D176018 und D176186: Die Zahl steht jetzt als Schachtel-Nr. da, nicht mehr im Titel.
10. **Spaltenkopf «Mappe: Inhalt: Zeitraum:»:** Die Nummern in der ersten Spalte sind Mappen (D2759 K99, 11 Einheiten).
11. **Alphabetisches Register «Titel ¦ Schachtel(n)»:** je Schachtel eine Einheit mit den Stichworten, die auf sie
    verweisen; ein Bereich «7-10» gilt für jede Schachtel. Was nach dem Register steht, kommt ins Blatt Info (D3026 K98,
    70 Schachteln).
12. **Tabelle «Nummer ¦ Jahrgang ¦ Titel»:** «1. ¦ 1982 ¦ Das Corso-Theater …» ist Signatur 1., der Jahrgang die
    Datierung (D176868 K72, 26 Einheiten).

### Signaturen, die nicht als Einheit erkannt wurden (Muster 3)

13. **Nur der Bestand steht in der Signaturspalte:** Die Nummern bzw. Buchstaben in der Inhaltsspalte sind die
    Einheiten.
    - Betroffen: D175561 (K69, 1.–22.), D151194 (K74, a)–f)).
    - Nicht betroffen ist «V.G. c.64.:1. ¦ 1. …»: Dort steht eine eigene Signatur, und die Nummern zählen ihren Inhalt.
14. **«Schachtel ¦ Nr. ¦ Inhalt»** mit Nummern, die über die Schachteln hinweg durchzählen: Die Nummern sind Signaturen,
    die Schachtel gilt bis zur nächsten (D1391 K101, 14 Einheiten).
15. **Behälterbereiche in einer Übersicht** («Schachtel Nr. 1 – 14 ¦ …», «Bände Nr. 15 – 25», «Band Nr. 164») sind
    Bereichseinheiten unter ihrer Gruppe I.–XIII. (D149867 K100, 38 Einheiten).
16. **Nummerierte Abschnitte einer Bestandsbeschreibung** («1. Herkunft des Bestandes», «2. Hinweise», «3. Gliederung»)
    sind keine Einheiten; die Schachteln sind die Einheiten (D2923 K103).
17. **«0. Grundlagen»** vor «0.0. Adresslisten» ist Einheit 0. (D185 K81).
18. **«I.1:3», «P2:10»** (mit Punkt bzw. ohne Leerzeichen) sind I 1:3 und P 2:10 (D177460 K8, Testdaten).
19. **Vollsignatur, nach der nur «Schachtel 1» steht**, mit dem Titel auf der nächsten Zeile: Die Schachtel kommt in die
    Spalte, der Titel von der nächsten Zeile. Kommt nach einer Schachtelmarke derselbe Titel wieder, ist das ein Teil.
    - Betroffen: D152398 (Akten, Schachteln 1–7), D2614 (V.L.162.:1, :2), D152817.
    - Nicht bei einer Bemerkung wie «Mit Inventarium …» oder «Soweit datierbar …», und nicht bei einer Datumszeile.
20. **Vorbemerkung mit nummerierten Punkten** vor dem Tabellenkopf «Signatur ¦ Inhalt ¦ Jahre» ist Vorspann (D152398 K76).

### Eltern, erfundene Einheiten, Tippfehler (Muster 4 und 5)

21. **Blosse Zahl ohne Punkt**, nicht fett, vor derselben Nummer mit Punkt in Fettschrift: Das ist eine Anzahl, keine
    Signatur («2 Handwerkskundschaften …», D2940 K104).
22. **Dieselbe Liste ein zweites Mal, anders geordnet** («2. Auswahl … (alphabetisch nach Autor)»): kein Teil, sondern
    weiter Darin derselben Einheit, mit Hinweis (D3343 K84).
23. **Tippfehler in einer Folge von Vollsignaturen:** Eine Nummer fehlt, und die Nachbarnummer steht doppelt («:111»,
    «:113», «:113», «:114»). Die erste 113 wird 112, mit Hinweis; «Nr. im PDF» bleibt die Form im PDF (D1473 K70, D1479 K80).
    Das gilt nicht für blosse Nummern mit Lücken und Teilen (VII.308.C.a.).
24. **Tippfehler in der vorletzten Stelle:** «6.1.3.4.» nach 6.1.4.1.–6.1.4.3. wird 6.1.4.4., mit Hinweis. Die erste
    6.1.3.4. bleibt erhalten (D3170 K107).
25. **Vollsignatur «n.a» mit demselben Titel wie «n.»** direkt davor: Sie ist Geschwister von n., nicht Kind (D3816 K79,
    auch D1343 «:12.a Luftschutz»).
26. **Einzige Vollsignatur mit Nummer, danach nur Buchstaben:** a) und b) sind 1.a und 1.b (D403 K85). Die Kategorien
    a)–e) unter vielen Vollsignaturen in III.G., III.P. usw. bleiben, wie sie sind.
27. **Fette Hauptnummer mit derselben Nummer direkt darunter:** Steht die Nummer normal, mit anderem Titel, ohne Datum und
    ohne Schachtel, ist sie Teil 2 («10. Varia - Sachen», D3186 K64, Testdaten).
28. **Fette Überschrift in der Textspalte** vor der nächsten Signatur ist eine Zwischenüberschrift, auch mit bis zu 8
    Wörtern ohne Ziffern («Ledermesse Zürich, Stempel für die Lederballen», D3898 K29; D4175).
29. **Bereichskopf mit abgekürztem Ende** («2.8. – 9. „Jahrbüchli“ …», «19.13.1.–7. …»): Seine Beschreibung kommt ins Darin
    der ersten Einheit des Bereichs, nicht der vorigen (D3702 K63, D4058).
    - Das Ende liegt höchstens 10 über dem Anfang, und beide Nummern folgen einzeln. Nicht betroffen ist «5.2.4.31. - 85.
      Geburtstag …» in VII.200.
30. **Eintrag einer weiteren Spalte knapp über der Signaturzeile** gehört zur neuen Einheit.
    - «I - LXV» über «1 Kleine Stadt» (D3542 K87, K88).
    - Datumszeile «1916 – 2002» über «1. Jahresberichte» (D1401, D1935).

### Stücke ohne Nummer (Regel 31, siehe oben)

31. Sie kommen zur Zeile für den Bestand:
    - D149825 K3 (Protokollband vor 1.) und K4 (Messingpokal);
    - D260 K106 («Schachtel II.»);
    - D2931 K108 («VII. 138. Fotografien»);
    - D3943 K113 (vier «Keine Nr.»);
    - D3826 K43 («Mappe – Porträt (Grossformat)»);
    - D3277 K93 («Grossformate: …»);
    - D3557 K95 («Reproduktionen (Beilage):»);
    - D1726 K77 («Drei Archivschachteln enthalten Drucksachen …»).

## Weiter offen

- **K61 D2643:** Die Inhaltsangaben «[Enthält Artikel über …]» stehen nur in der Übersicht und sind nicht bearbeitet.
- **K63 Rest:** Die Beschreibung steht bei 2.8., aber nicht auch bei 2.9. (mittel).
- **K85 Rest:** Die Signatur V.B.c.12.:1 bleibt in der PDF-Form, mit dem Tippfehler-Hinweis (mittel).
- **Bewusst offen:** K38–K45, K71 (D3190), K78 (D3894).
- **Vorschlag aus NP11 nicht umgesetzt:** «Regel 45 nur bei Kollision» (D3470, mittel).

## Bitte um Nachprüfung 12

1. Gegenprüfung der Runde 9 an den 78 geänderten Dateien.
   - Vergleich mit `vorher/`.
   - Je Regel die genannten Dateien; bei Regel 1, 3 und 31 bitte auch auf Fehlgriffe achten.
2. Dann der Durchgang über die 208 nur teilweise geprüften Dateien, wie in `nachpruefung11.md` vorgeschlagen.
