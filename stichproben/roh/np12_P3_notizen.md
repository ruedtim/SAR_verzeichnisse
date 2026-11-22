# P3 – Notizen (Nachprüfung 12, Paketart P, 23 Dateien, Stand 66c0fb74)

## Bilanz
- 23 Dateien ganz gelesen (17 volle Prüfmappe, 5 Kompaktmappe plus PDF-Stellen). Keine der Dateien wurde in Runde 8/9 geändert; alle Ursachen «vor Runde 9».
- 17 Dateien ohne kritischen Fehler, 6 mit: D3208 (bekannt K42), D3528, D9978 (4), D2979, D3808, D3021.
- 9 kritische Funde: 8 neu bzw. neu als kritisch eingestuft, 1 bekannt (K42). Dazu 16 mittlere Funde in `P3_funde.csv`; weitere bekannte mittlere stehen nur in `P3_dateien_urteil.csv`.
- Nach der Korrektur der Prüfmappen sind alle vorher verdeckten Zeilen der 10 betroffenen Dateien nachgesehen (Diff `mappen_alt` → `mappen`). Das ergab keine neuen Funde. Verdeckt waren Masse, Massstäbe, «2 Exemplare», Schachtel-Teilzeilen, «Mappe n:» und «Schachtel n:».

## Wichtigste kritische Funde
1. **D3528:** Die Einheit VII.327.:4. «Bilder, Zeichnungen und Skizzen … (Grossformate)» fehlt; ihre Zeile steht nur als «Text vor der ersten Signatur» im Blatt Vollständigkeit. 4.1.–4.3. stehen auf E1 mit dem Hinweis «erwartet 4.». Das ist dasselbe Muster wie K81 (D185).
2. **D9978:**
   - 28.3.25. («28.3.25:1–2», ohne Punkt vor «:») steht im Darin von 28.3.24.
   - Die Notiz zu Knell/Dürr für 28.4.25.–29. und «Mappe 6:» stehen im Darin von 28.4.24. (Seitenwechsel; Zeitraum dadurch bis 1984).
   - 28.6.12.a ist Kind statt Geschwister (Regel 25 greift nicht).
   - 28.1.–28.7. hängen am Bestand statt an VII.12.B.:28. (Einheit im Hauptverzeichnis D149628).
3. **D2979:** Sieben Absätze Bestandsgeschichte (S. 29) stehen im Darin der letzten Einheit 14.10. Regel 3 greift nicht, vermutlich weil der Block länger als 12 Zeilen ist.
4. **D3808:** Die «Beilagen:» (Polizeirapport 1945, zwei Schreiben 1946, BRB-Verweis) stehen nur im Blatt Info. Nach Regel 31 gehören sie in eine Bestandszeile. Früher standen sie fälschlich bei 1. bzw. 4.; jetzt sind sie verschoben statt richtig eingeordnet.
5. **D3021:** Die Schachtelmarken «… Schachtel 6» und «… Schachtel 8» am Zeilenende werden nicht erkannt. Die Reclam-Bände 42)–70) und die Typoskripte 71)–78) stehen deshalb im Teil «Schachtel 5» von C).
6. **D3208:** K42 ist unverändert (Abzeichensammlung 1–172 und Bibliotheksverweise bei «Publikationen»). Nach der neuen Konvention gehört die Sammlung in eine Bestandszeile.

## Muster (für die Hauptsession)
- **Obereinheit nur als Kopfzeile** (D3528 «4.», D9978 «28.»): Der Hinweis «erwartet n.» wird erzeugt, die Einheit aber nicht gebildet. Wahrscheinlich gleich bei D9985 (27.2.1. ff. unter VII.12.B. statt unter :27.2.; nicht geprüft).
- **Regeln 8 und 25 nur für Vollsignaturen:** «28.3.25:1–2» und «28.6.12.a» in Dezimalverzeichnissen bleiben unerkannt.
- **Regel 3 mit Zeilengrenze 12:** Längere Abschlussberichte zur Geschichte bleiben im Darin (D2979).
- **Gegenstück zu Regel 31:** Der Schlussblock-Fang nimmt echte Stücke («Beilagen») mit ins Blatt Info (D3808).
- **Behälter aus Überschriften oder Übersichten fehlen (mittel, häufig):**
  - nur bei der ersten Einheit: D176551 «Schachtel 2:»–«4:», D3021 B);
  - gar nicht: D9978 Mappen 1–9, D3505 und D152781 (Schachtelübersicht), D2630 9. (Schachtel 1 statt 2).
- **Zeitraum aus Familien- oder Lebensjahren (mittel):**
  - D3528 «Meier 1302»;
  - D3764 3.3. ab Geburtsdatum 1806;
  - D3505 2.1. (1752) und 2.2. (2000 = Geldbetrag).

## Unsicherheiten
- **D9978 Eltern 28.:** Das ist ein Teilverzeichnis, die Elterneinheit steht in D149628. Kritisch eingeordnet wie K81; die Behebung ist eher die Übergeordnete Signatur als eine neue Einheit.
- **D9978 28.4.24:** In NP4–NP6 war der Fall mittel. Nach den Schweregraden von NP12 ist er kritisch (Inhalt bei falscher Einheit).
- **D3021:** Die Schachtelnummer steht im Darin-Text, ist für den Benutzer also sichtbar. Bei milderer Lesart wäre der Fall mittel.
- **D3808:** Die Beilagen könnten auch als Erwerbsdokumentation gelten (dann Blatt Info). Ich lese sie als Stücke des Bestands, wegen der Stückzahl «1» und der Überschrift «Beilagen».
- **D10575:** Die Platzhalter «[nicht belegte Signatur]» (6.13., 10.28.) sind behalten. Die Konvention dazu ist seit Runde 7 offen, deshalb nicht gemeldet.
- **Nebenbefund D149628** (nicht in P3, ungeprüft): Unter VII.12.B.:28. hängt eine Einheit «28.1.1.3. Gebundene Aufführungsplakate …».
