# Gruppe 4 – Gliederung «fortlaufend»: Urteile

Grundlage: Excel-Schnappschuss `scratchpad/snapshot/excel/`, Skript-Schnappschuss `scratchpad/snapshot/findmittel_zu_scope.py`
(Zeilennummern unten beziehen sich darauf). Funde einzeln in `gruppe_4_funde.csv` (262 Zeilen; die Sammelzeilen
für das Überfliegen tragen in «anzahl» die geschätzte Zahl).

Zusatzprüfung Vorspann ↔ Detailverzeichnis (alle 7 PDFs): Ich habe überall die Vorspann-Zeilen und den «Text vor der ersten
Signatur» mit dem PDF verglichen. Dort stehen nur Titelblatt, Einleitung bzw. Biografie, Vorwort, Tabellenkopf und bei
D141005 die «A. ÜBERSICHT», deren 6 Gruppen im Detailverzeichnis noch einmal vorkommen. «Signaturen nur im Vorspann» ist
überall leer. Im Vorspann sind keine Einheiten verschluckt.

## D3484.pdf (VII.308.D.a., fortlaufend, 32 S.) – Urteil: grobe Fehler
Geprüft: S. 1–2 (Vorwort und Beginn), Prüfseiten 15, 28, 32. Das sind 88 PDF-Einträge; 85 davon stehen als
Excel-Einheiten im Import, dazu habe ich den Rest überflogen (`--kurz`, alle 80 Darin-Felder).
Signaturpraxis laut PDF: In der ersten Spalte stehen die Mappen-Nummern 190–640 der Firma Locher. Das Vorwort (S. 1)
verlangt die Bestellung als «VII. 308. D.a. 190., Schachtel 1». Im Excel steht `VII.308.D.a.:190.` und die Schachtel-Nr. 1
(Konvention). Eine Zählung «Jahr.Laufnummer» kommt in diesem PDF nicht vor.
Die Tabelle (Nr. | Ort | Bauherr/Objekt | Zeitraum | Schachtel) wird meist richtig gelesen. Die Teile-Logik für
wiederholte Mappen-Nummern stimmt, die Schachtel-Nummern stimmen auf allen Prüfseiten.
Kritisch: Die letzten drei Einheiten (639 ×2, 640 «div. O.»/«div. Orte», S. 32) fehlen und stehen im Darin von :638.
Beim Überfliegen fehlen fünf weitere aus demselben oder ähnlichem Grund: 229 «o. O.», die 2. Nennung von 477 (Schachtel 203),
«594 / 595» und «622 a» ×2.
Der grösste Fehlerblock: Hat die zweite Zeile eines Eintrags eine eigene Datumsangabe, wird sie ein Darin-Eintrag. Dann
fehlt der Ortsteil im Titel («Schwarzer-Weisser» + Darin «See, 1930 – 1932»), und von/bis nimmt nur die erste Zeile
(S. 28: 8 Zeiträume zu kurz; S. 15 :426. ohne «– 1929»). Über das ganze PDF sind es rund 55 weitere Fälle.
Ausserdem übernehmen Teile mit eigenem Titel den Titel des Nachbarteils, d. h. eines anderen Projekts (S. 15 «Engi …» als
«St. Moritz Haus Manin-Suot …, Teil 2»; dazu 3 weitere ausserhalb der Prüfseiten).
Hinweis «Untereinheiten reichen über den Zeitraum hinaus» (60×): Die Serie trägt den Zeitraum ihres Teils 1. Das folgt der
Teile-Konvention und ist kein Fund.

## D3589.pdf (VII.359., fortlaufend = Liste nach Schachteln, 11 S.) – Urteil: grobe Fehler
Geprüft: Prüfseiten 3, 7, 8 mit 82 Einheiten, Lückenzeile S. 8, Überfliegen aller 262 Einheiten.
Struktur korrekt: Signatur = Schachtel-Nr. (VII.359.:1.–:11.), das erste Buch einer Schachtel ist die Serie, die übrigen
sind Teile (Konvention). Auf den Prüfseiten fehlt kein Buch und keines ist erfunden.
In jedem Titel steht aber die Zahl aus der rechten Spalte «Expl.», bei einzeiligen Einträgen am Ende («… Bern 1920 1»,
dort bleibt dann auch das Jahr stehen), bei zweizeiligen mitten im Titel («… vo 2 anno dozumal. Zürich o.D.»).
Umfang ist überall leer.
59 Bücher ohne erkanntes Jahr bekommen das Jahr des ersten Buchs ihrer Schachtel. Fast alle sind «o.D.» oder
«o.O. u. J.» («= 1916» neben der Anm «undatiert»), drei haben ein zerrissenes Jahr («Aarau 19 59» → «= 1906»).
Auf S. 7–9 zerreisst die Textextraktion viele Wörter («Züri ch», «Mün chen»). Die Überschrift «2. Werke anderer Autoren»
steht im Darin des letzten Buchs von Schachtel 2.
Lücke S. 8 («o d» bei :8. «Stüssi, Herbert. Bilder der Erfüllung») ist kein Verlust: Im Excel-Titel steht «o.D.», im PDF
«o .D.».

## D141005.pdf (VII.380., fortlaufend mit Unterzählung, 3 S.) – Urteil: grobe Fehler
Geprüft: alle Seiten. Das PDF hat 48 Einträge: 6 Hauptgruppen (x 71) mit eingerückten, je neu gezählten Unterpunkten
(x 110). Das Excel hat 43 Zeilen.
Das Skript liest alle Nummern als eine flache Folge. Nur VII.380.:1. steht richtig. Die Unterpunkte 1.2–1.23 werden
Hauptsignaturen :2.–:23., die Hauptgruppen 2–5 hängen als Kinder unter diesen falschen Einheiten, die Unterpunkte von 2 und 3
verteilen sich auf fremde Eltern (40 Hierarchie-Funde). Hauptgruppe 6 («Akten betr. Übergabe …», 2003–2011) ist nur Darin
eines «Teil 2» von Unterpunkt 1.6.
Ausserdem fehlen 1.20./21., 3.2, 3.10 und 3.13 («10. August Hoffmeister …»: der Vorname August gilt als Monat). Der Anfang
von 2.2 steht nur im Blatt Info als «Schlussvermerk» und damit nirgends im Import.
Dazu kommen abgeschnittene Titel bei Zeilen mit eigener Datumsangabe, dabei gehen zweite Daten verloren. Der Ziffernstrich
«‒» erzeugt Datumsreste («Fotografien 1936‒»), und die Schlussnotiz steht im Darin.
Lücke S. 2 ist echt: Bei 1.9 fehlt der Vorname «August» im Titel.

## D3077.pdf (VII.194., fortlaufend, 3 S.) – Urteil: grobe Fehler
Geprüft: alle Seiten. Das PDF hat 17 Einheiten, das Excel 22 Zeilen.
Erfunden: Die eingerückte Liste «Originalhefte: 1. Heft … 5. Heft» unter Nr. 12 wird zu fünf Untereinheiten «Heft:
Zeitspanne» unter :1.–:5. Diese werden dadurch zu Serien, und bei :12. fehlt die Liste. Das Skript meldet die Wiederholung.
«Schachtel 1» bzw. «Schachtel 2» steht nur bei :1. bzw. :12. 15 Einheiten haben keine Schachtel-Nr.
Falsche Zeiträume: :10. 1809–1889 (Lebensdaten, die Datumsspalte sagt «ohne Datum»), :12. = 27.05.1789 (Geburtsdatum statt
1860–1862). Bei :16. und :17. fehlen die Daten der Darin-Zeilen.
Titel/Darin: :1. ist nach «von Herrn» abgeschnitten, :3. falsch am «:» geteilt, :17. ohne Titel («Diverses:» steht im
Darin, zwei Einträge sind verschmolzen).
Lücke S. 2 («Sept.» bei «3. Heft … 1836 – Sept. 1836») liegt in einer erfundenen Einheit.

## D140955.pdf (VII.442., fortlaufend, 2 S.) – Urteil: grobe Fehler
Geprüft: alle Seiten. Das PDF hat 17 Mäppchen, das Excel 16 Zeilen.
Kritisch: Nr. 16 «2 Fotografien vom Juni 1988 und Visitenkarte» fehlt und steht als Darin «16. 2 Fotografien …» bei :15.
Der Titel beginnt mit einer Ziffer.
Die Schlussnotizen «12. Juni 2007 / Dr. Robert Dünki» und «Letzter Nachtrag: 15. Juli 2013 / …» stehen im Darin von :17.
Der aus dem Darin geschätzte Zeitraum reicht dadurch bis 15.07.2013.
Sieben Titel enden auf einen Datumsrest («…, dat.», «… bzw.»).
Zeiträume: «(1950/71)» und «(1962/68)» werden nicht erkannt. Die Amtszeit «1966 bis 1970» wird Laufzeit von :12. Bei :11.
und :13. fehlen die späteren bzw. früheren Daten der Darin-Zeilen.
Gut: «12. Juni 2007» wird nicht als Signatur gelesen, und die Einleitung ist nicht importiert.

## D2677.pdf (V.L.32., fortlaufend, 1 S.) – Urteil: kleine Fehler
Geprüft: ganze Seite, 2 Einheiten mit 22 Darin-Einträgen.
Signaturen, Titel, Zeiträume (aus dem Darin geschätzt, 1868) und Schlussvermerk stimmen.
Im Darin von :1. sind dreimal zwei Briefe zu einem Eintrag verschmolzen («… 14. Oktober 1868 Zusammenstellung von …»).
Inhalt geht keiner verloren.

## D2562.pdf (V.L.123., fortlaufend, 1 S.) – Urteil: kleine Fehler
Geprüft: ganze Seite, 2 Einheiten mit 5 Darin-Einträgen.
Alles korrekt bis auf einen verschmolzenen Darin-Eintrag in :1. («… Sängerfest, Mai 1973 Farbreportage in: …»).
Ursache wie bei D2677.

## Muster in dieser Gruppe

1. **Echte Einheiten werden nicht als Signatur erkannt (Einheit fehlt, kritisch).** Ihr Text hängt im Darin der Einheit
   davor oder verschwindet ganz. `lies_signatur` verwirft eine einfache Nummer, wenn der Rest nicht gross beginnt
   (Z. 686–688) oder ein Monatsname folgt (Z. 683–684, trifft den Vornamen «August»). Nummern mit Zusatz passen nicht auf
   `DEZIMAL_RE` (Z. 489).
   - D140955 S. 2 VII.442.:16.: soll eigene Einheit «2 Fotografien vom Juni 1988 …», ist Darin «16. 2 Fotografien …» bei :15.
   - D3484 S. 32 VII.308.D.a.:639./:640.: soll 3 Einheiten «div. O. Strassenbeläge …» / «div. Orte Tiefbohrungen», ist Darin
     von :638.
   - D141005 S. 3 Unterpunkt 2.2: «2. August Hoffmeister an die Central Chancery …» landet über die Schluss-Heuristik
     (Z. 998–1004: >60 Zeichen nach Seitenwechsel auf der letzten Seite) im Blatt Info. Der Text fehlt im Import, die
     Vollständigkeitsprüfung zählt ihn nicht.
   - Die befürchtete Gegenrichtung (Datum links als Signatur, erfundene Einheit) kommt hier nicht vor. «12. Juni 2007» und
     «14. August 2003» werden korrekt verworfen.
2. **Eingerückte Unterzählungen werden als Signaturen der Hauptebene gelesen (Hierarchie falsch, erfundene Einheiten).**
   `lies_signatur`/`lerne_nummern` unterscheiden nicht nach Einrückung (`SIGNATUR_SPALTE_MAX` 115 deckt x 71 und x 110 ab).
   Eine wiederholte Nummer wird ein Teil bzw. ein Kind der zuletzt gesehenen gleichen Nummer (`baue_vorkommen` Z. 968).
   - D141005 S. 2 VII.380.:2.: soll Hauptgruppe «Orden Honorary Officer …» auf Ebene 1, ist «Dankesbrief an das EPD …»
     (Unterpunkt 1.2) auf Ebene 1, die Hauptgruppe hängt darunter.
   - D141005 S. 3 Hauptgruppe 6: soll Einheit «Akten betr. Übergabe …» 2003–2011, ist Darin von «Aufnahme vom Double Tenth
     Festival …, Teil 2».
   - D3077 S. 2 VII.194.:1.–:5.: soll Heftliste im Darin von :12., ist fünf erfundene Untereinheiten «Heft: Zeitspanne».
3. **Folgezeile mit eigener Datumsangabe wird ein neuer Eintrag.** Das trennt Titel, schiebt Titelreste ins Darin und
   verliert das zweite Datum. `kopf_und_rumpf` Z. 1325 trennt, sobald Titelzeile und Folgezeile je ein Spaltendatum haben,
   auch bei klein beginnender Folgezeile oder Titelende «der». Bei Teilen zerfällt der Titelblock in eine Liste
   (`verarbeite` Z. 1391), dann übernimmt `ergaenze_titel` (Z. 1904) den Nachbartitel.
   - D141005 S. 3 VII.380.:4.: soll «Brief der British Legation … Mitteilung der Ordensverleihung und Dankesbrief …»
     12.–23.01.1952, ist Titel «… mit der Mitteilung der», Zeit = 12.01.1952.
   - D3484 S. 28 VII.308.D.a.:574.: soll 1933–1936, ist 1934–1936 plus Darin «1933 – 1936». In :568. fehlt «See» im Ortsnamen.
   - D3484 S. 15 VII.308.D.a.:414.: soll Titel «Engi Vereinigte Webereien Sernftal und Azmoos …», ist «St. Moritz Haus
     Manin-Suot …, Teil 2».
4. **Rechte Spalten ohne Datum gehen in den Titel oder verloren.** `trenne_spalten` (Z. 439–484) kennt nur Datum, Umfang mit
   Masseinheit und Schachtel. Eine «Schachtel n»-Zeile gilt bei flacher Zählung nur für die erste Einheit
   (`baue_vorkommen.bereich` Z. 879–882 liefert dann die Einheit selbst als Abschnitt).
   - D3589 S. 3 VII.359.:4.: soll Titel «Hesse, Hermann. Ein Luzerner Junker vor hundert Jahren. Bern» mit Umfang 1 Expl.,
     ist «… Bern 1920 1» ohne Umfang. Das betrifft alle 262 Titel.
   - D3077 S. 1–2 VII.194.:2.–:11.: soll Schachtel-Nr. 1, ist leer (ebenso :13.–:17. ohne Schachtel 2).
5. **Zeitraum aus der falschen Quelle oder nicht erkannt.**
   - Lebensdaten und Amtszeiten ohne Klammern zählen als Laufzeit (`zeitraum_aus_titel` Z. 1745 ff., `PERSON_RE` Z. 233 nur
     mit Klammern): D3077 S. 2 :10. ist 1809–1889 statt undatiert; :12. ist = 27.05.1789 statt 1860–1862; D140955 :12. ist
     1966–08.02.1971 statt = 08.02.1971.
   - Undatierte Teile erben das Jahr des ersten Buchs der Schachtel (`ergaenze_zeitraeume` Z. 1847–1848, ohne Prüfung von
     `e.undatiert`): D3589 S. 3 :4. «Sachs, Hans. Ausgewählte dramatische Werke. Leibzig o. D.» ist = 1916 neben Anm
     «undatiert».
   - Nicht erkannt werden der Ziffernstrich «‒» U+2012 (`VERBINDER_BEREICH_RE` Z. 227; D141005 «Fotografien 1936‒»),
     «1950/71» (`_punkt` Z. 311; D140955 :4.), «MM.JJJJ» (D141005 «Canton, 09.1946») und zerrissene Jahre (D3589 «19 59»).
6. **Darin-Zeilen werden falsch zusammengefügt.** In `ist_umbruch` (Z. 1090–1092) gilt eine Folgezeile als Fortsetzung, wenn
   ihr erstes Wort nicht mehr in die Vorzeile gepasst hätte, auch wenn die Vorzeile mit einem vollständigen Datum endet.
   Der Absatzabstand liegt genau bei 8,0 pt und erreicht damit `ABSATZ_ABSTAND` (Z. 69) nicht, weil Z. 1185 auf «>» prüft.
   - D2677 S. 1 V.L.32.:1.: soll «… Spenden, 14. Oktober 1868» und «Zusammenstellung von Spendenanfragen …» getrennt, ist ein
     Eintrag (3×).
   - D2562 S. 1 V.L.123.:1.: «… Mai 1973 Farbreportage in: …» verschmolzen.
   - Umgekehrt trennen kurze Zeilen ohne Anschlusswort den Titel: D3077 :1. «… von Herrn» und Darin «Dr. Max Wild, *1900,
     + 1986».
7. **Schlussnotizen landen im Darin, Datumsreste im Titel.** `SCHLUSS_RE` (Z. 499) kennt «Datum / Name», «Letzte Änderung:»
   und «Letzter Nachtrag:» nicht. Sie werden nur erkannt, wenn vorher «Stadtarchiv Zürich» steht (so bei D3589 und D3484).
   Beim Entfernen des Titeldatums bleibt «dat.» bzw. «bzw.» stehen (`zeitraum_aus_titel` Z. 1790 ff.).
   - D140955 S. 2 VII.442.:17.: Darin «12. Juni 2007 / Dr. Robert Dünki», Zeitraum bis 15.07.2013 statt 2007.
   - D141005 S. 3 VII.380.:6. (Teil 2): Darin «14. August 2003 / Mag. Halina Pichit».
   - D140955 S. 1 VII.442.:1.: soll «Fähigkeitszeugnis (Lehrabschluss) als kaufmännischer Angestellter», ist «…, dat.».
