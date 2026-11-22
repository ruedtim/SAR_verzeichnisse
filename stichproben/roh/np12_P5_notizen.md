# P5 – Notizen (Nachprüfung 12, Paketart P, 23 Dateien, Stand 66c0fb74)

## Bilanz
- 23 Dateien geprüft: 16 ohne kritischen Fehler, 7 mit kritischem Fehler.
  - Neue kritische Funde (5): D2735, D3657, D3828, D176795, D3231.
  - Nur bekannte, bewusst offene kritische (unverändert): D512 K45, D1858 K40; dazu D3828 K44.
- Dazu 7 mittlere (D3231, D408, D3077, D73, D3038, D3429 ×2) und 2 geringe Funde (D1924, D3429).
- Methode: Prüfmappe bzw. Kompaktmappe ganz; dazu ein eigenes Skript (tmp_P5/segcheck2.py). Es ordnet jede Cache-Zeile
  dem PDF-Abschnitt ihrer Einheit zu und prüft sie gegen deren Felder. D1924: alle 2009 Tabellenzeilen gegen die
  Schachtel ihrer Spalte.
- Verdeckte Zeilen: neue gegen alte Mappen verglichen (tmp_P5/neu_<D>.txt), kein neuer Fund; K45 um S. 59 ergänzt.

## Wichtigste neue Funde
1. **D2735 (Mappen/Schachteln):** Die je Schachtel neu beginnende Mappennummer wird als Signatur V.L.72.:1–:10 genommen.
   Mappen der Schachteln 2/3 werden so Teile fremder Mappen der Schachtel 1 (z. B. «Tagblatt» unter «Korrespondenzen»).
   Soll: Schachtel → Mappe zweistufig.
2. **D3231 S. 22/23:** In ganz fett gesetzten Werklisten gilt der letzte Eintrag vor der nächsten «2.8.» als
   «Zwischenüberschrift». «Das Armband …» und «Der Mörder seiner Tochter …» stehen nur im (falschen) Hinweis der
   folgenden Teile. War schon in bb4c9588 so; Runde 9 Regel 28 hat die Regel erweitert.
3. **D176795 S. 7/8:** «Kinder von …:» ist letzte Darin-Zeile der Eltern-Einheit (2.3.1., 2.3.3.) (Muster 2); bei x 138
   (S. 13/15) wird dieselbe Form richtig als Überschrift erkannt.
4. **D3657:** «5. Fremdenzimmer 1964» und «6. Löschung … 2003» (nach 6.3.) sind Teil 2 der fremden 5./6. (Muster 10).
   NP6 hatte «Teil 2» zugelassen – Entscheid Hauptsession.
5. **D3828 S. 1:** «“Summarisches Curiculum vitae in Stichworten” … Ende 1961» ist ein Stück ohne Nummer vor 1. (laut
   Schlussabsatz in Schachtel 1) und wird nicht importiert → Bestandszeile (Regel 31). Grenzfall zur Vorbemerkung.

## Muster
- Zweistufige Behälterzählung (Schachtel/Mappe, Zählung je Schachtel) bleibt die Hauptquelle falscher Gliederung
  (D2735 neu, D1858 K40).
- Die Regel «fette Zeile vor Signatur = Überschrift» braucht eine Gegenprobe: Ist die Zeile davor in derselben Spalte
  auch fett, ist es ein Listeneintrag.
- Mittlere Funde: Zeiträume aus Lebensdaten, Gründungs- oder Übergabejahren (D3077, D3038, D3231). Titel verlieren das
  Zähljahr, wenn es gleich dem Spaltendatum ist (D408, 27 Einheiten).

## Unsicherheiten / nicht als Fund gezählt
- D3099 1.2.5. Teil 2 «6. Generation …»: inhaltlich 1.2.6., aber nach Konvention «zweimal hintereinander → Teil
  mit Hinweis Tippfehler?».
- D8949: Sammlungsbeschreibung, Masse und Biografie vor 1. bleiben Einleitung (früheres Soll).
- D3231 c) im Teil b) (2.2.), d)/e) in c) (3.10.): innerhalb derselben Signatur, wie früher mittel. Bekannte mittlere
  und geringe Funde aus NP2–NP11 stehen nur in den Dateiurteilen.
