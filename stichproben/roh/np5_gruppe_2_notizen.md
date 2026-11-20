# Fünfte Nachprüfung (Stand 13:15 gegen 11:30) – Gruppe 2

Geprüft am PDF: alle 31 Paketzeilen, jede entfernte, neue und geänderte Einheit der Diffs von D3774, D10744, D151217,
D49, D65, D67, D69, D2558 und D3271, in D10675 alle 32 geänderten Einheiten (alle 27 Fussnotenzeichen), in D2534 alle
61 Schachtelzuordnungen an der Aufteilung S. 1, in D3466 die neue Einheit 168 und 19 der 134 Titeländerungen. Für Regel p
habe ich zusätzlich alle 715 PDFs nach «Nummer allein, Titel 2,5–8 pt tiefer» abgesucht (Hilfsskript in `np5/tmp_g2/`).
Zeilennummern beziehen sich auf `$S/neu5/findmittel_zu_scope.py`.

## D3774.pdf – Regel t: Struktur richtig, aber neue Fehler bei den Unternummern
Der Detailbeginn bei der zweiten Überschrift «Detailverzeichnis Archivbestand» stimmt. Nur die Übersicht und die Einleitung
(S. 1–6: Allgemeine Hinweise 1.–7., Findmittel) sind jetzt Vorspann (54 → 189 Zeilen). Von S. 7–13 fehlt kein Wort, die
84 Treffer in `textverlust.csv` sind Einleitung oder nur umformatiert. Die sechs Abteilungen stehen jetzt auf der obersten
Ebene, dazu 25 Unternummern als Einheiten (Z322 teilweise). Es bleiben aber Fehler:
- 5.3. («5.3.Denkschrift», ohne Leerzeichen) und 6.4. («6.4. ohne Datum», klein) sind keine Einheiten. Ihr Text steht jetzt
  bei der Schwester 5.2. bzw. 6.3., nicht mehr bei der Gruppe (kritisch).
- 2.4. und 2.5. stehen weiter im Darin des Teils «2.38. Belege zu Nr. 174» (Teil 2 von 2.).
- Bei VII.47.1. (1843–1922 aus der Übersichtszeile «1. Archivregister») und bei 3. (1824–12.05.1858) ist der Zeitraum falsch.
- Bei 2.2., 4.1. und 6.1. ist die Grenze zwischen Titel und Darin falsch.
- Schachtel 1 und Schachtel 7 fehlen. Der Schlussvermerk steht im Darin von 6.3.
Die Signatur «VII. 47.1.» bleibt «VII.47.1.» (wie im PDF, ohne «:»), die Kinder heissen VII.47.:1.1.–1.5. Das ist nach
Konvention zulässig, aber es fehlt ein Hinweis auf den wahrscheinlichen Tippfehler.

## D10675.pdf – Regel u: alle Fussnoten richtig, aber Zeiträume aus dem Fussnotentext
Alle 27 Fussnoten stehen als «Fussnote n: …» bei der Einheit mit dem Zeichen, auch wenn das Zeichen auf der Folgezeile oder
über der Zeile steht (715.4, 715.8, 718.23, 742.21). Damit ist Z260 behoben. «Nicht übernommen» sinkt von 43 auf 2 (zwei
Zwischenüberschriften «712 Verträge/…»). Neu ist ein Fehler: Die Darin-Schätzung liest die Fussnoten mit. 700.5 und 715.18
bekommen «= 09.11.2010» (das Abrufdatum einer Webquelle), 701.50.9 bekommt «1898–06.1992» (die Geschichte des Standorts),
die Gruppen 700, 715 und 701.50 erben das, und die 65 Geschwister erhalten neu den Hinweis «Kein Zeitraum gefunden.».
718.23 = 1986 (ein Schreiben im Dossier) ist allenfalls vertretbar. Die übrigen Paketzeilen sind unverändert: Z28, Z29 teilweise,
Z31, Z191, Z258, Z259 offen. Bei Z30 ist der Titel durch Regel n jetzt vollständig.

## D10744.pdf – Regel u: nur 1 von 9 Fussnoten beim Zeichen
Fn. 3 (Umplatzierungsvermerk) steht richtig bei 430.1.601.9. Das Zeichen klebt dort am Wort («Zivilschutz3»). Die übrigen acht
hängen mit dem Hinweis «ohne erkennbares Zeichen» an der letzten Einheit der Seite. Ihre Zeichen sind 8 pt gross und
stehen als eigene Wörter. Das Skript erkennt aber nur Zeichen bis 7,5 pt. Bei Fn. 4 steht das Zeichen ausserdem auf der
Vorseite. Die 12 übrigen Zeilen «Nicht übernommen» sind die Einleitung auf S. 1 und damit korrekt.

## D151217.pdf – Regel u: beide Fussnoten bei falscher Einheit
Fn. 1 gehört zu 7. und Fn. 2 zu 8., beide Zeichen sind 9,1 pt gross und stehen hinter «1969)» bzw. «1968)». Sie stehen jetzt
mit Hinweis bei 7.2.2. und 8.1.12. Z274 bleibt offen. Die Quellenwechsel aus Regel a (2.3., 2.3.1., 2.3.2., 3.3., 3.3.1., 4.2.)
stimmen mit den Spaltendaten überein. Z102 und Z103 sind unverändert offen.

## D2534.pdf – Regel r: Korrektur
Die sieben erfundenen Einheiten «Schachtel 7–13» sind weg (Z287 behoben). Alle 61 übernommenen Schachtel-Nr. stimmen mit der
Aufteilung S. 1 überein, auch an allen Bereichsgrenzen und bei 1.4. = «3-4». Ohne Schachtel bleiben nur die Unter-Einheiten
2.3.1.–2.3.3. und 2.4.1.–2.4.4. (in Schachtel 5) sowie 4.3.1.–4.3.3. (in Schachtel 10), deshalb ist Z289 teilweise behoben.
Z288 und Z290 sind unverändert offen, Z290 ist bekannt.

## D49.pdf, D65.pdf, D67.pdf, D69.pdf – Regel s: Korrektur; Regel a verschlechtert D67/D69
Entfernt wurden nur die 11 leeren Doppel-Kategorien ohne Darin und ohne Kinder, deren Buchstabe schon als Bereichseinheit
aus der Übersicht besteht. Sonst ist nichts weggefallen: Der Wortrückgang (−9/−4/−7/−7) entspricht diesen Titeln samt Buchstabenmarke, und die Titel stehen
weiter in den Bereichseinheiten. Z334 ist damit behoben. Z335, Z336 und Z338 sind teilweise behoben: Bei Kategorien mit nur einer
Signatur (e) III.P.21., a) III.Q.1., b) III.R.1., e) III.R.36.) trägt die Gruppe weiter die Signatur ihrer einzigen Einheit,
und diese heisst jetzt «Teil 2». Schon länger bestehend und neu erfasst: Die Übersichtszeilen der leeren Kategorien «… (keine)»
stehen im Darin der vorangehenden Gruppe und zusätzlich als eigene Einheit III.x.:b. usw. (D49, D67, D69). Neu durch Regel a:
In D67 und D69 kommen Jahre aus Verweisen auf andere Bestände in den Zeitraum. Das betrifft III.Q.4. bis 1833,
III.Q.33. 1773–1831, III.R.1. bis 1806 und III.R.36. bis 1797 (Titeldatum bleibt stehen), alles über den Bestandszeitraum hinaus.

## D2558.pdf – Regel p: Korrektur
V.L.121.:3. «Werbematerial» ist jetzt eine eigene Einheit mit vier Darin-Einträgen, Z291 ist behoben. Die Suche über alle
715 PDFs fand nur noch D1759 4.1.1./4.1.2.: Diese Stellen waren schon um 11:30 richtig und sind unverändert. Die Regel wirkt
also nirgends sonst.

## D3271.pdf – Regel q: Korrektur, auch bei 6.2. und 6.6.
Die Bereichsüberschriften «4.2.22. bis 4.2.67.», «6.2. bis 6.5.» und «6.6. bis 6.9.» (alle «(1 grossformatige Schachtel)»)
sind jetzt Zwischenüberschriften. Die echten 4.2.22., 6.2. und 6.6. stehen auf ihrer Ebene. Dass auch 6.2. und 6.6. wegfielen,
war nicht angekündigt, folgt aber aus derselben Regel und ist am PDF richtig. Die drei entfernten Einheiten sind die alten
Kinder; ihr Inhalt steht jetzt in den bisherigen Schein-Serien.
- «Nicht übernommen» 1 → 7 und Wörter −37 entsprechen genau den 7 Zeilen, die nur noch im Prüfhinweis stehen: drei
  Bereichszeilen, «Buchhaltungsabschlüsse (29 Hefte)», die zwei Zeilen «Vgl. …» und «1. bis 29. Rechnung …».
- Davon sind «(1 grossformatige Schachtel)» und die Bemerkung «Vgl. …» Inhalt, kein Titel (gering).
- Z309 teilweise, Z311 behoben (Regel i), Z178 und Z310 unverändert.
Ausserdem neu erfasst: Bei 7. steht der Anhang S. 26 im Darin. Seine Baujahre gelten jetzt als Zeitraum mit Quelle
«Datumsspalte», obwohl die Übersicht «[o. J.]» angibt (Regel a). Ebenfalls neu erfasst und schon um 11:30 vorhanden: Der
Titel von 6.6. ist am «:» mitten im Satz geteilt, und bei 6.2. sind die Punkte a.–h. ein einziger Darin-Eintrag.

## D3466.pdf – Regel o: Korrektur; die Titeländerungen kommen aus Regel j
Die neue Einheit 168 «div. O. Kühltürme etc.» (1925, Schachtel 71, 14 Einträge) stimmt mit dem PDF, Z315 ist behoben. Es gibt
keine weitere neue Einheit, also keinen Fehlgriff der Regel. Die 134 Einheiten «darin->titel / darin zusammengezogen» stammen aus
Regel j (kopf_und_rumpf Z. 2640–2645). Die kurze zweite Zeile der Spalte Bauherr/Objekt kommt in den Titel, ohne Trennzeichen
und nur, wenn genau eine Zeile folgt. Das ist so gewollt wie in D3484 «… Perlen Wasserkraftanlage» und meist unbedenklich
(13 von 19 geprüften Fällen gleich). Schlecht ist es in zwei Fällen:
- Bei «dito» (18 Teile von 525.) ergibt sich ein sinnloser Titel.
- Bei den Titeln mit nicht erkanntem Datum «1921 &» oder «1924 / 25» steht der Rest jetzt mitten im Titel. Das betrifft
  16 weitere Titel (27 → 43), deshalb ist Z316 jetzt schlechter.
Die 593 Änderungen nur an der Teil-Nummer stammen aus Regel c und wurden nicht einzeln geprüft. Z317 ist unverändert.

## Wichtigste Punkte
1. **Regel u wählt die Einheit mit dem Zeichen nur in D10675 richtig.** `hat_zeichen` (Z. 1861–1866) verlangt für das
   Zeichen ≤ 7,5 pt oder ein am Wort klebendes Zeichen. In D10744 sind die Zeichen 8 pt, in D151217 9,1 pt gross. Deshalb
   landen 8 von 9 bzw. 2 von 2 Fussnoten bei der letzten Einheit der Seite (Z. 1869–1871). Vorschlag: die Grösse relativ zu
   den Nachbarwörtern prüfen (z. B. ≤ 0,75 ×) und auch die Vorseite durchsuchen (D10744 Fn. 4).
2. **Fussnoten verfälschen die Zeitraum-Schätzung (D10675).** Die angehängten Fussnoten (Z. 1874–1883) zählen in der Darin-Schätzung
   mit (`ergaenze_zeitraeume` Z. 3643–3646, `jahre_im_text`). Folgen: 700.5 und 715.18 «= 09.11.2010», 701.50.9 «1898–06.1992»,
   die Gruppen 700, 715 und 701.50 erben das, und es gibt 65 neue Hinweise. Einträge «Fussnote n:» sollten aus der Schätzung
   ausgeschlossen werden.
3. **Regel t ist nur halb umgesetzt (D3774).**
   - `lies_signatur` Z. 1048–1061 nimmt eine Unternummer der Textspalte nur als erstes Kind oder nächste Nummer an, und nur
     mit grossem Folgewort. Daran scheitern 2.31./2.41./3.51./4.51. (Sprung) sowie «5.3.Denkschrift» und «6.4. ohne Datum».
   - Nach dem Teil «2.38.» ist `kind_von` leer (Z. 1888–1890, `not aktuell.ist_teil`), deshalb fehlen 2.4. und 2.5.
   - Neu landet Text bei der falschen Schwester (5.2., 6.3.).
   - Der Zeitraum von VII.47.1. kommt aus der falschen «1.»-Zeile der Übersicht (Z. 3593–3598).
4. **Regel a holt Jahre aus Verweisen (D67, D69, D3271 7.).** Betroffen sind Fortsetzungsnotizen «Fortsetzung im Bestand …»,
   «… siehe V.H. b.4.» und Vermerke wie «… sind in den Bestand Schulamt, V.H. b.2., eingegliedert» (Z. 2862, 2864–2865,
   2874–2879). Dazu kommt ein Anhang im Darin (D3271 7., Quelle jetzt «Datumsspalte», Z. 2873/3634–3640). Die Zeiträume reichen
   über den Bestand hinaus (bis 1806/1831/1833). Vorschlag: Zeilen mit «siehe», «vgl.», «Fortsetzung» oder «eingegliedert»
   nicht mitzählen.
5. **Regeln mit eindeutiger Korrektur:** r (61/61 Schachteln richtig, 7 erfundene Einheiten weg), s (11 leere Doppel-Kategorien weg,
   sonst nichts verloren), q (3 Bereichsüberschriften), o (168.) und p (V.L.121.:3.). Offen bleiben:
   - die Unter-Einheiten ohne Schachtel bei Regel r (Z. 4780, `len(v.pfad) != len(von_p)`);
   - Kategorie-Gruppen mit der Signatur ihrer einzigen Einheit, jetzt als «Teil 2» (D65, D67, D69);
   - die Behälterangabe «(1 grossformatige Schachtel)», die nur im Prüfhinweis steht (D3271).
