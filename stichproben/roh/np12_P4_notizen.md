# P4 – Notizen (Nachprüfung 12, Paketart P, Stand 66c0fb74)

## Bilanz
- 22 Dateien ganz geprüft: volle bzw. Kompaktmappe, Excel aller Einheiten, PDF an allen Zweifelsstellen.
- 6 Dateien mit kritischem Fehler: D3709, D3628, D3271, D140969, D176824, D9985 (Grenzfall). 16 ohne.
- 34 Funde: 10 kritisch, 21 mittel, 3 gering, alle «neu». Ausnahme: D3271 «c. Register» ist ein alter, unveränderter
  NP11b-Fund (N2), der nicht in offen_kritisch.csv steht.
- Neu erzeugte Mappen (D9985, D3067, D2937, D3271, D3225, D140969, D2992) nachgesehen: Die früher verdeckten Zeilen
  stehen alle bei der richtigen Einheit. Daraus nur bei D3067 ein mittlerer Fund (Schachtel VI.D.).
- Gegenprobe mit eigenem Skript (tmp_P4/ortcheck.py, 21 Dateien): Jede Darin-Zeile wurde im PDF zwischen ihrer
  Signaturzeile und der nächsten gesucht. Keine weitere Verschiebung gefunden.

## Wichtigste kritische Funde
1. **Schlusstext im Darin der letzten Einheit (Muster 6):**
   - D3709: Vereinsgeschichte im Darin von 2.3. Regel 3 greift nicht (Abstand nur 17 pt); Zeitraum bekommt 1959.
   - D3628: Bestandsumfang im Darin von 8.; nur «Der Bestand umfasst:» steht im Info.
   - D3271: Anhang-Tabelle im Darin von 7.; Zeitraum 1873–1898 aus der Summenzeile.
2. **D176824:** Der Inhaltssatz «In Schachtel 9 befindet sich ferner ein Schachtelregister …» steht nur als Schlussvermerk
   im Info. Soll: wie Regel 7 bei Schachtel 9 bzw. nach Regel 31 in der Bestandszeile.
3. **D140969:**
   - Schachtel 57 «Zeitungsausschnitte (1)» fehlt als Einheit; sie steht nur in der Übersicht im Darin von 50-58.
   - 87. steht auf Ebene 1, obwohl die Übersicht «82 – 87» nennt (Detailkopf «82 – 86»).
4. **D3628:** Die Zwischenüberschriften «Lose Protokolle» stehen bei den vorigen Bänden 2.1.7. bzw. 2.2.9. (Muster 2).
   Geringe Tragweite.

## Grenzfälle (bitte entscheiden)
- **D9985:** 27.2.1.–27.2.4. hängen am Bestand. Elternteil 27.2. steht in D149628 (ID 5094, «Siehe separates
  Verzeichnis»). Bisher nur Hinweis; kritisch nur, wenn Teilverzeichnisse unter ihren Elternteil gehören sollen.
- **D3271, Gruppenbeschreibungen:** «(Die Bände enthalten Notizen …)» und «Vgl. die vollständige Serie …» stehen nur
  im Prüfhinweis. Das NP11-Soll (B1/K1) liess die Gruppenzeile als Hinweis zu, die Beschreibung ist aber Verzeichnistext.
- **D3271 «c. Register»:** In NP11b schon als Grenzfall kritisch/mittel eingestuft.
- **Locher (D176824):** VII.308.A.:B.–:I. folgen der bisherigen Konvention, die übrigen Locher-Dateien haben aber
  VII.308.C.a. usw. als Bestand. Nicht gemeldet; vor dem Gesamtimport abstimmen.

## Mittlere Muster
- Zeitraum aus Eingangs-, Abgabe-, Lebens- oder Buchtiteldaten: D140969, D3067, D3628, D2937, D3225, D3275.
- Zeitraum nur aus der ersten Zeile der Schachtel: D4039.
- Schachtelmarken falsch weitergegeben: D2992, D1746, D3067, D3271.
- Titel mit «Mappe», «Teilw. undatiert» oder erster Listenzeile: D3647, D3225, D1746, D140969, D1120; «Bd. 1:» in D3271.
