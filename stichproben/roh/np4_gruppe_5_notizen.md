# Vierte Nachprüfung – Gruppe 5 (Stand 11:30 gegen 08:25)

Paket: 62 Zeilen – 17 behoben, 7 teilweise, 38 offen, keine schlechter, keine entfällt. Die 38 offenen betreffen
Einheiten, die laut Diff seit 08:25 unverändert sind (kurzer Blick am PDF, Befund 08:25 bestätigt; Z226 mit Hinweis
eigens nachgesehen). 21 neue Zeilen: 2 kritisch, 16 mittel, 3 gering. Regelstichprobe: 202 Einheiten in
`np4_gruppe_5_regeln.csv`, darunter alle 42 neuen Hinweise «Steht im Findmittel unter der Zwischenüberschrift …»
der 13 Regel-b-PDFs.

## Regel b – Ergebnis
- **42 neue Hinweise, 41 richtig.** Es sind echte Zwischenüberschriften (kursiv mit Doppelpunkt in D4173, D10575, D8945,
  D149888, D3793, D176795, D3231; 16 pt in D175997; Planmappen «Mappe n:» in D9978; Abschnittsüberschrift in D152781).
  Sie stehen jeweils bei der ersten folgenden Einheit, und der Text ist vollständig (nichts abgeschnitten). Vorher
  standen sie im Darin der vorigen Einheit, meist bei einer falschen Einheit (D4173 1.7., D9978 28.1.10., D10575
  13.5., D176795 2.3.9.6.2. …).
- **1 falsch: D3253 S. 2.** «Unidentifizierter Text ("Tirilin")» ist der letzte Listeneintrag von 2. Textbücher und keine
  Überschrift. Er steht jetzt nur noch als Hinweis bei 3. Diverses, also kritisch. Ursache: `grund_groesse`
  (Z. 1788–1789) wird über alle Zeilen ermittelt. Die Einleitung S. 1 ist 10 pt, daher gilt jede normale 12-pt-Zeile
  mit Absatz davor direkt vor einer Signatur als «grössere Schrift» (Z. 2048). Das kann in jedem PDF mit klein
  gesetzter Einleitung wieder vorkommen.
- **D10585 (8 Hinweise)** kommt nicht aus dem Doppelpunkt- bzw. Schriftgrössen-Zweig, sondern aus dem Zweig für
  wiederholte Gruppensignaturen (Regel d, Z. 1884–1901). Ein Beispiel ist «2. Philhellenische Predigten» vor 2.1.
  Das Ergebnis ist richtig. Vorher stand die Überschrift im Darin der letzten Einheit des Vorabschnitts, bei 1. sogar
  im Darin von 8.
- **Nur die erste Einheit bekommt den Hinweis**, obwohl die Überschrift im PDF für mehrere gilt. Das ist kein Fund,
  aber vermerkt:
  - D4173: Intérieurs 1.8.–1.13., Kleine Fotografien 1.22.–1.28., Verschiedene Bilder 1.32.–1.34. u. a.
  - D9978: «Mappe 3» für 28.3.1.–28.3.15., «Mappe 9» für 28.6.47.–28.7.2.
  - D10575: West- und Mitteleuropa 13.2.–13.5.
  - D149888: Fritschi-Umzug 10.2.1.–10.2.4.
  - D3793: Winterthur 5.3.1.–5.3.17.
  - D8945: A 6 für 3.9.1.–3.9.8.
  - D3231: «b) Texte» für alle Teile 2.1. A–Z
  - D3271: 4.2.22.–4.2.50.

  Bei D9978 und D149888 sind es eigentlich Behälterangaben (Planmappe bzw. «in grossformatiger Schachtel»). Als
  Schachtel-Nr. bei allen betroffenen Einheiten wären sie besser.
- **Lücken der Regel b (schon 08:25, als neue Zeilen «vor 08:25» erfasst):**
  - Folgen auf die Überschrift noch Beschreibungszeilen, bleibt sie im Darin der vorigen Einheit: D4173 S. 3
    «Porträts von August Benziger (1857 – 1955): …» bei 1.13.; D9978 S. 16 «Mappe 6:» und die Notiz bei 28.4.24.
    (dort zusätzlich Zeitraum 1891–1984).
  - Doppelpunkt-Zeilen mit mehr als 8 Wörtern bleiben Darin: D3204 S. 2 «Officielles Notizenblatt … (3 Bände,
    1807 – 1829):» bei 11. (Z. 2061).
  - Die erste Überschrift vor der ersten Signatur bekommt keinen Hinweis, weil `aktuell` noch None ist: D9978
    «Mappe 1:» steht nur im Blatt Vollständigkeit. Das wird nur vermerkt.
- Gegenrichtung richtig: D2839 «4. NSDAP ¦ 27. Jan. 1965» ist wieder ein Darin-Eintrag (Z. 2039–2040), der falsche
  Hinweis ist weg (Z17 behoben).

## Je PDF
- **D460** – Korrektur: 2.5. «(2 Schachteln …)» ist aus dem Titel ins Darin gewandert (Regel a). Z134 ist offen.
- **D1933** – Korrektur: 5.5. hat jetzt 1919–1921 (Z293 behoben).
- **D2366** – Korrektur: Der Tabellenkopf steht nicht mehr im Titel (Z167 behoben).
- **D2710** – unbedenklich/unklar: Die Schachteltitel kommen jetzt aus der ersten Zeile. Der Zeitraum von V.L.5.:2
  stammt nun nur aus diesem Titel (1893–1928); um 08:25 war er 1692–2009, beides falsch. Z297 ist offen.
- **D2735** – neuer Fehler: Die Titel der Mappen kommen jetzt aus der ersten Zeile. Mappe 2 der Schachtel 3
  (V.L.72.:2) hat dadurch nur noch = 1912 statt 1912–2009, die Serie ebenso. Z240 ist offen.
- **D2839** – Korrektur: Z17 behoben. Z88 ist offen.
- **D2894** – unbedenklich, nur Quelle/Hinweis. Z298 ist offen.
- **D2935** – Korrektur: 8.11. Darin getrennt. Bei 9.5. wird das Datum nicht mehr mitten aus dem Titel geschnitten.
  Z90 und Z91 sind offen.
- **D3077** – Korrektur: 17. hat den Titel «Diverses» und 1949–1978 (Z188 behoben). Die übrigen 4 Zeilen sind offen.
- **D3204** – gemischt:
  - 12. und 13. haben keinen offenen Zeitraum mehr (Z322 behoben).
  - Die Überschrift vor 12. bleibt im Darin von 11. (neue Zeile, vor 08:25).
- **D3231** – Korrektur bzw. unbedenklich: Der Hinweis «b) Texte» ist richtig; die Zeiträume der Gruppen sind jetzt
  geschätzt. Z325 ist offen.
- **D3253** – neuer Fehler (kritisch, Regel b), siehe oben.
- **D3271** – gemischt:
  - 3.3. hat jetzt den richtigen Titel «Bauakten …».
  - 3.4.2. und 3.4.3. verlieren ihren Untertitel ins Darin (Doppelpunkt-Regel).
  - Bei 3.3. sind «(1)» … «(5)» im Darin abgetrennt (gering).
  - Der Hinweis bei 4.2.22. ist richtig. Die Schein-Serie «4.2.22. bis 4.2.67. (1 grossformatige Schachtel)» gab es
    schon vorher; sie ist kritisch und als neue Zeile «vor 08:25» erfasst. Z255 ist teilweise.
- **D3316** – gemischt: Der Titel von 1.3. ist jetzt vollständig. Die Lebensdaten in der Klammer ergeben aber
  01.10.1768–1860, und 1. erbt 1768 (neue Zeile). Z117 ist teilweise, die übrigen 4 Zeilen sind offen.
- **D3429** – Korrektur: 4.6.2. «Dias» (Z259 behoben), 1.2. Jahresliste getrennt. Z258 ist offen.
- **D3528** – Korrektur: Die 10 Stammtafeln haben wieder einen Zeitraum, 4 davon exakt. Bei 4.2.7., 4.2.20. und
  4.2.21. steht nur 1942 statt 1941–1942, bei 4.2.5. und 4.2.6. fehlt der Monat (Z329 teilweise).
- **D3718** – Korrektur:
  - 7.1. Beschreibung ins Darin.
  - 7.2. und 7.3. eigene Titel statt «Kataloge».
  - 7.6. jetzt 1921–1953.
  - 9.5. jetzt 1800–1891.

  «Sch. 87/140/148» stehen weiter im Titel (vor 08:25). Z262 ist offen.
- **D3764** – unbedenklich: 2.4. «Mappe 4» wie die Geschwister. Z331 ist offen.
- **D3793** – Korrektur: 2 Hinweise richtig, 3.2.6. Darin getrennt. Die Gruppen-Zeiträume sind geschätzt
  (unbedenklich).
- **D3861** – Korrektur: 3.2.1., 5.3. und 5.4. haben Titel ohne Liste. 7.1. hat keinen offenen Zeitraum mehr, beginnt
  aber 1911 statt 1929 (Z333 teilweise).
- **D3943** – Korrektur bzw. teilweise: X.G.188 ist nicht mehr offen, aber 1780–1975 vermischt Thema und
  Erscheinungsjahr (Z334 teilweise). Die Schwester X.G.188. («1780 / – 1822») ist weiter = 1780.
- **D4173** – gemischt:
  - 9 Hinweise richtig.
  - Bei 1.32. steht der Bildinhalt jetzt im Darin statt im Titel (Doppelpunkt-Regel, neue Zeile).
  - Die Benziger-Überschrift bleibt im Darin von 1.13. (vor 08:25).
- **D4175** – neuer Fehler: 1. beginnt jetzt 1805, aus der Medaille «Escher Wyss 1805-1980» in 1.F. Z336 ist offen.
- **D8945** – Korrektur: 3.1. Satz wieder ganz (Z337 behoben), 2 Hinweise richtig.
- **D9978** – Korrektur: 7 Mappen-Hinweise richtig, 28.5. jetzt 1925–1981. «Mappe 6:» mit Notiz bleibt Darin von
  28.4.24. (vor 08:25).
- **D10575** – Korrektur:
  - 4 Hinweise richtig.
  - 11.20. «1675» (Z8 behoben).
  - 10.57. 1858–1861.
  - Tabellen bei 3. und 5. zeilenweise getrennt.

  Z140–Z142, Z269 und Z270 sind offen.
- **D10585** – gemischt: 8 Hinweise richtig; Beilagen und «Enhält:» ins Darin; 1.2.2. und 5.22. über den
  Zeilenumbruch gelesen (Z271 behoben). Neu falsch:
  - 3.16. 1798–1953, 8.4. und 8. ab 1758 (geschätzte Lebensdaten der Untereinheiten wandern nach oben).
  - Kosmetik «1821 –1829».
- **D134644** – unbedenklich. Z279 ist offen.
- **D149888** – gemischt: 3 Hinweise richtig. Bei 1.2.10. sind die Fortsetzungszeilen «1993 …,» und «1998 …» eigene
  Einträge (gering).
- **D150242** – unbedenklich bzw. Korrektur: Mappe 6 hat den Titel «Zeitungen». Z283 ist offen.
- **D150296** – Korrektur: 6.7. 1952–2003 (Z284 behoben); die Gruppen-Zeiträume sind geschätzt. Z150 ist teilweise,
  Z151 und Z226 sind offen.
- **D150589** – gemischt:
  - 1.6.3. Paare getrennt.
  - 6.1.30., 15.2.1. und 16.2.14. sind behoben.
  - 2.3.35. hat nur noch = 18.11.1954, weil die 2. Zeile jetzt Darin ist.
  - 16. und 16.2. beginnen jetzt 1664 (Medaille 16.2.35.).
- **D151217** – gemischt bzw. unklar:
  - 3.2.18. und 10.1.98. haben jetzt vollständige Titel.
  - Die Fussnoten S. 7 und 23 stehen nicht mehr bei der falschen Einheit, aber auch gar nicht mehr im Import
    (neue Zeile).

  Z152 und Z153 sind offen.
- **D152781** – gemischt:
  - Die Übersichtszeile 5. verdrängt die echte 5. nicht mehr (Regel f).
  - Die Titel 1.1., 1.2., 1.3., 2.1., 3.2. und 3.3. sind richtig.
  - Die Schachtelnummern der Übersicht fehlen bei 1.–5.
  - 1.3. hat jetzt 1919–15.04.2009 (Bearbeitungsvermerk «Ergänzt von Caroline Senn …»).
- **D175994** – Korrektur: Bei IV.A.45. und IV.A.51. steht die Beschreibung im Darin. Z81, Z155 und Z156 sind offen.
- **D175997** – Korrektur: Hinweis «Bürgerliche Stiftungen und Fonds» (Z157 behoben), IV.C.168. Titel ohne Liste.
- **D176151** – Korrektur: 16.15. 1937–1961 (Z288 behoben), 15. 1784–2003. Z158, Z159 und Z230 sind offen.
- **D176367** – Korrektur: Z160 und Z164 behoben. Z163 ist teilweise.
- **D176795** – gemischt: 2 Hinweise richtig, 1.5. Titel «Familientage». 5. hat jetzt 1746–24.03.2017, und das Ende
  ist das Übergabedatum (neue Zeile). Z289 ist offen.
- **D176824** – Korrektur bzw. unbedenklich: A. hat keinen Zeitraum mehr (Z290 behoben). Die Beschreibungen in A. und
  C.–I. sind jetzt eigene Darin-Einträge (Absatz 7,8 pt, vertretbar).
- **D10744** (nicht im Paket, auf Wunsch angesehen) – unklar bzw. Textverlust: Die 9 Fussnoten stehen nicht mehr im
  Darin der letzten Einheit der Seite, aber auch nicht im Import. Fussnote 3 enthält den Umplatzierungsvermerk zu
  430.1.601.9. (neue Zeile).

## Wichtigste Punkte
1. **Regel b mit falscher Grundschrift (kritisch).** D3253 S. 2: Der Listeneintrag «Unidentifizierter Text
   ("Tirilin")» wird Hinweis bei 3. statt Darin von 2.
   - Ursache: `baue_vorkommen`, `grund_groesse` Z. 1788–1789 zählt die 10-pt-Einleitung mit. Der Test «grössere
     Schrift» in Z. 2048 trifft dann jede 12-pt-Zeile.
   - Vorschlag: `grund_groesse` nur aus dem Detailverzeichnis bestimmen, oder für die Schriftgrösse zusätzlich
     verlangen, dass sie grösser ist als die Folgezeilen bzw. die folgende Signaturzeile.
2. **Neue Doppelpunkt-Regel in `kopf_und_rumpf` (Z. 2557–2567, nicht angekündigt).** Ein Untertitel bzw. der
   Bildinhalt wandert aus dem Titel ins Darin, sobald die Folgezeile «, » enthält. Beispiele:
   - D4173 1.32. «Fotografie (oben rechts und links abgerundet)» + Darin «Villa Diana Thalwil, untere grosse Grotte»,
     während 1.33. (9 Wörter) den Inhalt im Titel behält.
   - D3271 3.4.2. und 3.4.3. «Akten zu Liegenschaften (2)/(3)», während 3.4.1. den Untertitel behält.

   In anderen Fällen ist die Regel richtig: «Bücher:», «Ehrungen:» (D152781), «Akten 1960 – 1999:» (D3861),
   «Dias:» (D3429).
3. **Elterneinheiten übernehmen geschätzte Zeiträume der Untereinheiten** (`ergaenze_zeitraeume` Z. 3466–3477, Quelle
   «Untereinheiten (geschätzt)» mit Hinweis). Das ist oft besser, z. B. D9978 28.5. und D3718 9.5. Falsche Schätzungen
   aus Lebensdaten oder Jubiläumsmedaillen wandern aber nach oben:
   - D10585 3.16. 1827–1828 → 1798–1953 und 8. → 1758–2008
   - D4175 1. → 1805–1991
   - D150589 16./16.2. → 1664–1966
4. **Zeitraum nach dem Titel/Darin-Umbau aus falscher Quelle** (Regel f bzw. Titel aus der ersten Zeile, Datumsspalte →
   Darin):
   - Steht im neuen Titel ein Datum, zählen die Darin-Daten nicht mehr: D2735 Mappe 2 = 1912 statt 1912–2009;
     D150589 2.3.35. = 18.11.1954 statt 07.04.–18.11.1954 (Regel a).
   - Wird aus allen Darin-Jahren geschätzt, zählen Notizdaten mit: D176795 5. bis 24.03.2017 (Übergabe); D152781 1.3.
     bis 15.04.2009 (Bearbeitungsvermerk).
5. **Fussnoten werden verworfen** (`baue_vorkommen` Z. 1809–1818, neu). Sie stehen nicht mehr bei der falschen
   Einheit, gehen aber dem Import ganz verloren, nur das Blatt Vollständigkeit «Fussnote» behält sie:
   - D10744 S. 2–6: 9 Fussnoten, u. a. der Umplatzierungsvermerk zu 430.1.601.9.
   - D151217 S. 7 und 23: Fussnoten zu 7. und 8.

   Besser wäre: Darin der Einheit mit dem Fussnotenzeichen, das im Titel klebt («Zivilschutz3»).
6. Kleinere Punkte:
   - **Regel-b-Lücken** (vor 08:25): D4173 1.13., D9978 28.4.24., D3204 11. (≤ 8 Wörter, Z. 2061).
   - **D3271 4.2.22.**: Die Bereichszeile «4.2.22. bis 4.2.67. (1 grossformatige Schachtel)» wird Serie (kritisch,
     vor 08:25).
   - `verbinde` Z. 2302–2303 klebt «1821 –» + «1829» ohne Leerzeichen (gering, viele PDFs).
   - `ist_umbruch` Z. 2266–2270 trennt Jahreslisten auch nach Komma (D149888 1.2.10.).
