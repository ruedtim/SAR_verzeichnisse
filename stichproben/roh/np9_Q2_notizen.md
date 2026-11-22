# Paket Q2 – Nachprüfung 9 (D3810, D3842, D3313, D3566), Paketart A

## Bilanz je Datei
- **D3810** (21 → 8): 15 Einheiten aus dem diff, alle besser (Regel 6). 8. «Nachträge» hat Schachtel IV, 1926–1944 und ein vollständiges Darin. Die Liste 1.–21. steht ganz im Darin von 7. Altzeilen B20, B21 behoben. Neu: 2 mittel (Schachtel II fehlt bei 3.–6.; Titel von 1. und 7. abgeschnitten), beide schon vor dem Nachtrag.
- **D3842** (4 → 2): 3 Einheiten, alle besser (Regel 6). Echte Einheiten sind nur 1. und 2. Neu: 1 mittel, schon vor dem Nachtrag: 1. hat Titel «Korrespondenz privat 1», die «1» ist die Schachtelspalte.
- **D3313** (50 → 4): Gliederung bei allen 50 Einheiten besser (Regel 7). Alle 47 Listennummern stehen im Darin von 4., ebenso Kopf und Detailinventar. Zeilenabgleich S. 2–5 ohne Fehlstelle. Zeiträume: 1. und 3. schlechter, 2. und 4. gleich (alle falsch, ohne Hinweis). B18 behoben, B17 offen, B19 schlechter.
- **D3566** (8 → 4): Gliederung der 6 Einheiten aus dem diff besser (Regel 7): Beschlusspunkte im Darin von 1., «2. Kopien» ist wieder 2. Zeitraum von 1. schlechter, 2. gleich falsch. **2 kritische Funde, schon vor dem Nachtrag und bisher nie gemeldet**, dazu 3 mittel.
- Keine echte Einheit verschwindet durch Regel 6 oder 7 im Darin. gliederung.py meldet für die vier Dateien weder vorher noch jetzt ein Signal.

## Wichtigste Funde
1. **D3566 «S.» (kritisch, vor Nachtrag).**
   - «S. Vögelin, Zürich’s ehemalige Stadtthore, … Zürich 1840» ist der Titel von «Nummer 12» unter «2. Kopien» (S. 7). Daraus wird Teilbestand VII.340.:S. (ID 3).
   - Die echte «3. Kopierte Briefe von und an Heinrich Weiss» (S. 8, 14 pt fett) hängt deshalb als VII.340.:S.3. darunter (E2). Eine Einheit VII.340.:3. fehlt.
   - Info zeigt «Gliederung: römisch/Buchstaben».
   - Vorschlag: Eine einzelne Initiale vor einem Nachnamen mit Komma («S. Vögelin,») ist ohne Buchstabenfolge A., B., … keine Signatur.
2. **D3566 1. «Originale» 1519–1953 ist falsch, nicht nur breit.**
   - 1519 und 1953 kommen aus der Literaturangabe «Zürcher Pfarrbuch, 1519-1952, Zürich 1953, S. 524» (Nummer 6, S. 3).
   - Soll: 11.02.1798–13.09.1805, nach den Druckdaten der Titelzeilen von Nummer 1 bis Nummer 10. Das passt zur Vorbemerkung «vorwiegend von 1798 bis 1805».
   - Vorher war 1. 11.02.1798–02.03.1798, zu eng, aber im richtigen Jahr.
   - Gleiche Ursache bei 2. (1336–1962 aus Bürgerbuch- und Ratslisten-Zitaten, soll etwa 1408–1840).
   - Vorschlag: Schätzung aus dem Darin auf das Ende des Online-Archiv-Zeitraums (1840) begrenzen. Literaturklammern «…, Ort Jahr, S. n» und Lebensdaten nicht zählen. Druckdaten «(Druck: …)» zuerst nehmen.
3. **D3313: Zeitraum ist nur noch der Jahrgang.**
   - Werte: 1. Genau 1786, 3. Genau 1810, 4. Genau 1818, 2. 1804–1854. Alle mit Quelle «Titel (Ereignisdatum)» und ohne Prüfhinweis.
   - Ursache 1: Als Einzeleinheit gilt jetzt das Titel-Ereignisdatum vor der Darin-Schätzung.
   - Ursache 2: Die Klammer «(1834 – 1863)» verwirft finde_zeitraeume als Lebensdaten (LEBENSDATEN_RE). PERSON_RE macht den Jahrgang zum Ereignis.
   - Vorschlag: Eine Klammer-Spanne am Titelende ist Laufzeit, wenn kein Personenname davorsteht bzw. sie im Bestandszeitraum liegt (1834–1898).
   - Der Punkt «Weiter offen: D3313 1.–3. Jahrgangsjahr gilt als Beginn» trifft nicht mehr zu.
4. **D3566 S.3.:** «max / 28. März 2000» steht im Darin, der Zeitraum reicht deshalb bis 28.03.2000 (soll 02.12.1829–28.03.1832). Im Blatt Info steht «Schlussvermerke: –».

## Unsicherheiten
- D3810 8.: 1926–1944 ist eine Schätzung aus «1943/44» und «Feuerwehrstag 1926». 1634 und 1794 sind als Bezug übergangen. Das ist plausibel, aber nicht belegt.
- D3566 2. «Kopien»: Ob scope die Daten der Originale (1408–1840) will, ist eine Konventionsfrage.
- Das Schachtel-Problem bei D3810 3.–6. und der Titel bei D3842 1. stehen als mittel (wie D151730 in NP8). D3810 1./7. waren in NP8 nur Notiz.
- D3313: Die Liste hat 47 Nummern, nicht 46. Der Kopf sagt «46 Porträtphotographien», weil Nr. 18 «Dieses Porträt fehlt.».
- Gering, nicht gemeldet: Bei D3842 2. hängen «Broschüren» und «Korrespondenz Militär» mit «; » nur am ersten Eintrag. «s. oben» und «s. Nr. 12» sind ohne «; » angehängt.
