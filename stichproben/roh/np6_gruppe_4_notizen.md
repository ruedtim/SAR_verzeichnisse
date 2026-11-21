# Nachprüfung 6 – Gruppe 4 (Regeln I, J, K, L, M), Stand 15:43

Geprüft am PDF (pdftotext -layout, woerter.py) gegen `neu6/alle_excel` bzw. `neu6/testdaten_excel` (D149628, D9983, D3515),
Vergleich mit `neu5`. Eigene Hilfsskripte in `np6/tmp_g4/` (u. a. Abgleich aller Titeländerungen 13:15 → 15:43 über
Signatur + Vorkommen, Wortbilanz je Einheit, Spaltendaten D438 gegen PDF-Text).

Hinweis zur Zeilennummer: Die im Auftrag genannte «Z316 (D3466, schlechter)» ist in diesem Paket **Z246** (Zeile 246 in
`funde_nachpruefung5.csv`; Z316 war die Nummer aus Runde 5). Sie wurde zuerst geprüft.

## Paket-PDFs

**D3466** – Regel I wirkt stark: «JJJJ / JJ» ist jetzt Datumsspalte, der Datumsrest steckt nur noch in 19 statt 210 Titeln
(18 × «1921 & / 1922» bei :131., 1 Tippfehler im PDF «1940 / 14»), alle 191 entfernten Daten = von/bis (Z246 teilweise).
Nebenwirkung: diese Einheiten bekommen den schmalen Spaltenrand – ~25 falsch getrennte Umbrüche sind repariert, aber 14
Einheiten verschmelzen jetzt getrennte Inhaltszeilen (neue Zeile), «Rohrkanal» rutscht in den Titel von :249., und bei
4 Ortsnamen über zwei Zeilen («Court-» / «St.Etienne») wird der zweite Teil eigener Darin-Eintrag (Muster schon vor 13:15).
Regel L: 18 «dito» jetzt im Darin (Z336 behoben), nur Teil 19 nach Seitenwechsel bleibt; Regel F behebt Z335; Wortbilanz:
in keiner der 233 geänderten Einheiten fehlt ein Wort.

**D438** – Alle 125 Spaltendaten «Monat – Monat Jahr» S. 4–9 stimmen jetzt mit von/bis (per Skript gegen den PDF-Text),
die Titel sind sauber, auch die mehrzeiligen (6.2.39., 6.2.61., 6.2.86., 6.2.97.) und 6.4.1. «Zürich um 1900». Einzige
Ausnahme 6.2.1.: «16. bis 19.» (Jahrhunderte) wird als Tagesbereich zur Spalte gezogen, Titel «… vom Jahrhundert» (Z359
teilweise, neue Zeile).

**D1180** – Alle 27 «vom N. / M. Monat Jahr» haben jetzt beide Tage im Zeitraum, Titel bleiben (Datum nach «vom»), «13 – 15.
September» ebenso (Z192 behoben, Z274 behoben über Regel A). 11.3. und 11.96. mit Folgezeile «– 17./18. …» unverändert
(Z126, Z275 offen).

**D150589** – Regel I richtig in 2.2.x/2.3.13. (Tagesbereiche; 2.2.9.6. bleibt wegen «Städtetag 1964» = 1964), Regel J verwirft 12
Bibliothekssignaturen (Db 1322 …) und das historische «1354»; zwei Signaturen «(Bb 1686)», «(Db 1805)» liegen nicht weit
genug vor 1811 und zählen weiter (neue Zeile). Regel M entfernt 8 falsche Sprung-Hinweise (2.2.1.–2.2.9. fehlen im PDF).
16.2.10. verliert durch Regel A jeden Zeitraum (Jubiläumsteller 1959, neue Zeile); Z196, Z197, Z287 offen.

**D149628** (Testdatei) – Regel K: die 12 Werklisten aus `titel_angehaengt.csv` sind jetzt ganze Titel (Z284 behoben;
743. mit Kopf «Aufführungen …:» vertretbar). Regel I: Saisonspalte wird bei zweitägigen Aufführungen durch die Tage
ersetzt (Einzeltermine behalten die Saison – uneinheitlich, aber kein Widerspruch); falsch sind 23.1.1.280. «1./ 5./ 7.
Juni 1946» (Beginn 5. statt 1.) und 26.2.4. (Heft 1938 fällt aus dem Zeitraum). 7.2.1.12. «/ 21.» erfasst Gruppe 0; kein
weiterer Fall des Musters (Scan Titel, Anm, Darin aller Dateien). 26.2.5. Text doppelt (PDF-Doppelschicht, vor 13:15).
Teile 23.2.1. jetzt in PDF-Reihenfolge (Z285 behoben).

**D3581** – Regel K trennt «Jahres-Abschlüsse:» richtig (Z339 behoben). Alt und bisher nicht erfasst: 2.2. Titel
«Protokolle Vorstand, Ausschuss, Generalversammlungen, 1970 - 1983, Schachtel 1» (Spaltenangaben der zweiten Titelzeile
angehängt, als Spalte gilt die dritte Zeile «1984 - 1995»; die neue Anm «1984 - 1995; Darin: 1970–1983» dreht es um) – neue
Zeile, vor 13:15.

**D152817** – Regel K: VI.SB.D.7.:1-2 «b) Lehrer» mit 5 datierten Einträgen, «Besoldungen, 1841-1932» wieder vollständig
(Z297 behoben); J: «2. Semester 1907» bleibt; M: 2 Hinweise richtig.

**D152781** – Regel K: 3.3. Titel «Manuskripte» (Z294 teilweise, Darin-Trennung «… Nichte» / «Olga Dubs-Lüssi (1989)»
bleibt); 5.1. und 3.1. unverändert (Z295 offen), ebenso Z206/Z207.

**D408 / D2857** – Regel M wirkt wie angekündigt: «zweimal»-Hinweise bei 1.2.1. bzw. 1.3. weg (Z357, Z225 behoben), die
Sprung-Hinweise vergleichen nur noch direkte Unternummern («nach 1 folgt 3» statt «nach 10 folgt 3»). In D10744 entfallen
dadurch auch zwei zutreffende Sprung-Hinweise unter eingehängten Nummern (nur Hinweise).

**D2979** – 8.5./8.7. jetzt Spannweite der Spalte (Z229 behoben), Titel «Personendossiers 1897» (Regel E); 6.x/7.x
unverändert (Z308 offen).

**D3672** – 2.3.1. «Juli / August 1930» richtig; neu falsch 1.1.59.: Inhaltsangabe «März / April 1932» ersetzt das
Briefdatum 28.2.1932. 4.31./4.32. «1937/» / «1938» (zweizeilige Spalte) seit jeher nur 1938 (neue Zeile, vor 13:15).
Z46, Z106, Z107, Z251 unverändert offen.

**D406** – 11. «2./3. April 1949» → 02.–03.04.1949, Titel sauber (Z114 behoben); Z112, Z113, Z115 unverändert.

**D2935** – 2.16., 2.23., 2.44., 5.5. mit beiden Daten (Z21 behoben); Z22 unverändert.

**D141020** – 2.23.40. richtig; 18 Titel mit Zahlenform «6./7.9.1970» bleiben bei nur dem zweiten Tag (Teil von Z193).
Z283: Anm jetzt «1949 – 1960; Darin: 1949–1975» – kein Widerspruch mehr, aber kein PDF-Wortlaut (teilweise).

**D3225** – 6.13. «9./10. Mai 1998» richtig; 9. dagegen schlechter: Zeitraum = 04.1986 statt 1899–1986 (Regel B, Z323
schlechter + neue Zeile).

**D10585** – 8.5.3. behält jetzt «den 24. Oktober 1828, in» (Regel J), sonst unverändert (Z186, Z187 offen).

## Beispiele ausserhalb des Pakets (nur meine Regeln)
- **D140969 15.**, **D10675 745.16/745.22**, **D2767 1.**, **D3515 1.1.3./1.1.40.**, **D3793 3.1.5./3.1.11./3.1.13.**,
  **D2975 1.4.1.**, **D258 12.**, **D3761 3.14.**: Regel I richtig (am PDF). D258 9. = bekannter offener Punkt.
- **D3018 06.1.4.** (PDF Gruppe 2, Fundzeile Z162): «ca.1890-» mit «1964» umbrochen an den linken Rand – Zeitraum jetzt
  «1890–» offen, «ca.» nur in der Anm, «1964» wird eigener Darin-Eintrag; als Regel-I-Beispiel nicht erfüllt. 06.6.9.
  «1920. - 1963» richtig.
- **D867 5.** (K) richtig getrennt, **D3271 3.4.2.** (K) bleibt wie gefordert, **D2850 29.** (K) richtig, **D3316 1.29.** (K)
  Literaturangabe ganz.
- **D3647 5.4.**, **D2657**, **D2975** (WS/SS), **D151217 3.3.7.**, **D149628 26.2.17./26.2.25./26.2.18.** (Jg.): Regel J
  richtig. **D3793 5.8.23.**: «(vom» am Titelende (neue Zeile, gering); **D9983 5.8.1.**: «…, Zürich, den (4 Exemplare)»
  (neue Zeile, gering, gleiches Muster 9× vor 13:15).

## titelschnitt.csv (gekürzte Titel)
- 20 mit Anzeichen, alle am PDF: 18 × D3466 :525. «Darin klein» = «dito» → Darin, richtig (Regel L); D438 6.2.108.
  «… stellen aus» richtig (falsch-positiv); D3793 5.8.23. «(vom» falsch (neue Zeile).
- 20 weitere verteilt, am PDF: D3466 :143., :57., :125. T2, :229., :230., :357., :583., :274., :135., :503.; D438 6.2.2.,
  6.2.12., 6.2.39., 6.2.51., 6.2.61., 6.2.86., 6.2.97., 6.4.1., 6.2.43., 6.6.1.; dazu D10675, D140969, D150589 2.2.2.22./
  2.2.9.5., D2935 2.16./2.23./5.5., D3018 06.6.9., D258 12., D3515, D3672 2.3.1., D406 11. – alle sauber (nur Datum weg,
  Zeitraum richtig). Kaputt: D3672 1.1.59. (Inhaltsdatum entfernt, Zeitraum falsch), D9983 5.8.1. («den»), D149628 26.2.4.
  (Titel richtig, Zeitraum zu eng), D3018 06.1.4. (s. o.).
- Zusätzlich alle 325 Titel mit entfernter neuer Datumsform per Skript gegen von/bis geprüft: 323 exakt, 2 vertretbar
  (D150589 2.2.9.6. = 1964, D3031 VII.A.47. = 1935).

## textverlust.csv (20+ Fälle, ohne D151210)
Nur Datum aus dem Titel entfernt (gewollt): D438 6.2.12., 6.2.39., 6.2.61., 6.2.69., 6.2.86., 6.4.1., D3466 :143. (Wortbilanz
aller D3466-Einheiten: kein Wort verloren), D10675 745.16, D149628 23.1.1.324., D150589 17.343., D3672 2.3.1., D406 11.,
D3793 3.1.13., D3225 6.13., D2767 1., D982 6. (Anm «1937- ca.1946»). Text nur verschoben (gewollt): D152817 D.7.:1-2,
D2850 29., D3581 1.1., D867 5. (Regel K, jetzt Darin), D140969 10. und D141 :119 (Regel N, eigene Einheiten 11:1-2, 120, 121),
D8949 V.L.221.:6. (Künstlerbiografie jetzt Vorspann, die erfundene Einheit «6» fällt weg – Regel O, gewollt), D3067
VIII.B.8. (nur das doppelte Spaltendatum «um 1907 – 1908» entfällt, _mit_zusatz). Echter Verlust bzw. Fehler: **D438 6.2.1.**
(«16. bis 19.» aus dem Titel, nur noch in der Anm), **D3018 06.1.4.** (Zeitraum offen, «1964» als Darin), D258 9. (bekannt).

## Wichtigste Punkte
1. **Regel I wirkt fast überall richtig** – 323 von 325 entfernten neuen Datumsformen ergeben exakt von/bis; D438 125/125,
   D3466 191 Titel, D1180 27 Tagesbereiche. Ausnahmen mit neuem Fehler (alle mittel):
   - D438 6.2.1. (ID 88): Titeltext «16. bis 19.» wird mit der Monat–Monat-Spalte verbunden → Titel «… vom Jahrhundert».
     Ursache: neue Monat–Monat-Alternative PUNKT_RE Z. 330 zusammen mit dem «bis»-Verbinder (VERBINDER_BEREICH_RE Z. 343) in
     der Spaltentrennung (trenne_spalten Z. 732 ff.); Tageszahlen vor einem reinen Monatsbereich sollten nicht angezogen
     werden.
   - D3672 1.1.59. (ID 61) und D149628 26.2.4. (ID 4872): zeitraum_aus_titel Z. 3798 nimmt als «genauere Angabe» nur
     Bereiche (von ≠ bis) – ein jetzt erkannter Inhaltsbereich verdrängt das Briefdatum bzw. die um das Darin erweiterte
     Spalte (Z. 3764–3772 werden durch Z. 3813–3816 überschrieben). Gleiches Muster ohne Regel I bei D149628 18.1.4., D4054
     12.4. Teil 2 (dort nur Anm «…; Darin: …» im Widerspruch zu von/bis).
   - D149628 23.1.1.280.: «1./ 5./ 7. Juni 1946» → nur «5./ 7.» erkannt (PUNKT_RE Z. 327–328) → Beginn 5. statt 1. Juni.
2. **Nebenwirkung von Regel I in D3466**: Einheiten mit «JJJJ / JJ» haben jetzt eine Datumsspalte und damit den schmalen
   Rand (verarbeite Z. 2914–2915). ~25 Umbrüche sind repariert, aber 14 Einheiten verschmelzen getrennte Inhaltszeilen
   (z. B. :275. «4. Dach … Maschinenbahn Pläne Locher & Co», :261. «Hochbau: … Maschinenhaus: Pläne 1:100»), :249.
   bekommt «Rohrkanal» in den Titel, und 4 zweizeilige Ortsnamen landen halb im Darin («Court-» / «St.Etienne»). Das
   Verschmelzen gab es schon vorher bei Einheiten mit einfachem Jahr (:526. ID 1028); ist_umbruch (Z. 2500) bräuchte in
   diesen Tabellen ein Zusatzsignal (Zeile ohne Schlusskomma + Folgezeile beginnt mit «Pläne»/Ziffer «N.»).
3. **Regel J**: WS/SS/Semester/Jg., «, in», «;», «/» und frühe Titeldaten (Db-Signaturen, «1. Mai 1351», «gegründet 1805»)
   funktionieren. Reste: «(vom» (D3793 5.8.23.) – zeitraum_aus_titel Z. 3841 vergleicht `letztes` mit Klammer, ein
   `.lstrip("([")` würde reichen; «den» fehlt in der Wortliste Z. 3842–3846 (D9983 5.8.1. und 9 ältere Fälle);
   Bibliothekssignaturen «(Bb 1686)», «(Db 1805)» nach 1661 zählen weiter (D150589 17.3., 17.173., Gruppe 17.) – besser
   «(Aa 1234)»-Muster in NICHT_JAHR_VOR_RE bzw. als Klammer-Signatur ausschliessen.
4. **Regel K, L, M** ohne neue Fehler: K trennt dichte Listen (D3581, D867, D152817, D2850), lässt D3271 3.4.2. stehen,
   D152781 3.3. «Manuskripte» richtig, Werklisten ganz (D149628, D3316). L: 18/19 «dito» im Darin; der eine Rest liegt nach
   einem Seitenwechsel (dito-Prüfung kopf_und_rumpf Z. 2816–2818 nur bei Abstand auf derselben Seite). M: alle «zweimal»- und
   Sprung-Hinweise unter eingehängten Nummern weg (Z. 3564–3566); nebenbei entfallen auch zutreffende Sprung-Hinweise
   innerhalb fehlender Zwischenstufen (D10744 430.1.023.x).
5. **Nicht meine Regeln, aber in meinen PDFs**: D3225 9. verliert durch Regel B «1899» (Z323 schlechter), D150589 16.2.10.
   durch Regel A jeden Zeitraum (Jubiläumsteller, 1959 wäre richtig), D149628 26.2.5. doppelter Text (PDF-Doppelschicht,
   lese_zeilen Z. 143 ff. ohne Dublettenfilter). Kosmetik Regel F: Hinweis «Untereinheiten reichen über den Zeitraum hinaus
   (1912–1912)» (D3466 :51., :251.) statt «(1912)».
