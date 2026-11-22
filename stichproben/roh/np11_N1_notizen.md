# N1 – Gegenprüfung Nachtrag 1 (efe92c5f), Notizen

## Bilanz
- 14 Dateien; alle 664 Einheiten der diffs am PDF beurteilt (70 Urteilszeilen; «Σk» in Spalte n = Sammelzeile über k Einheiten, alle angesehen). Fast alles besser; schlechter nur D177460 F/F 2 (Zeitraum), D175827 3.3./4.1./7.2. und teils 5.1. (Darin-Verbindungen, gering), D3170 7.2.2. (Hinweis, gering).
- Altzeilen: 24 kritische K-Zeilen → 22 behoben, 2 teilweise mit kritischem Rest (K8 D177460, K15 D2828). Mittel/gering: B31 behoben, B35 teilweise (Rest mittel), 17 ungeprüft (Einheit laut diff unverändert).
- Ohne kritischen Fehler: D10675, D10744, D1387, D175827, D2137, D2951, D2960, D3470, D434. Mit kritischem Fehler: D177460, D2828, D260, D3170, D3472.

## Wichtigste Funde
1. D177460 (Regel 36): 431 PDF-Zeilen «X n:m» bei x 70.9 (430 Signaturen, «E 1:2» doppelt) gegen 429 Einheiten. Es fehlen genau I 1:3 («I.1:3», S. 12, im Darin von I 1:2) und P 2:10 («P2:10», S. 19, im Darin von P 2:9). Die 430 des Suchlaufs = Regex ohne die Punkt-Form. Eltern/Ebene aller 429 maschinell geprüft (alle E3 unter X n), Titel und Zeitraum je Zeile gegen den Zeilen-Cache, Prüfmappe S. 2–20 ganz gelesen. Die 17 Doppel-Darin-Zeilen sind aufgelöst.
   Mittel: Jahr in Klammern nicht als Zeitraum (F 2:15–F 2:21, P 1:17, N 4:9, M 3:7, Q 3:1, R 3:1) → F 2 bis 1965 und F bis 1993 statt 2014 (schlechter als vorher); E 2:1 1888–1897 mit Verweis im Titel; M 3:2/M 3:4 Gründungsjahr als Beginn; M 3:15 und P 1:1 Titel abgeschnitten. Gering: E 1:2 Teil 2 ohne Hinweis.
2. D260 (Erstprüfung): 120 Einheiten richtig, Hinweise und Zeiträume stimmen, nichts mehr im Darin von :25. Neu kritisch: Behälter «Schachtel II.» (S. 8, Signaturspalte, ohne Signatur) steht im Darin von :120 (vorher von :25). Mittel: :9 «V.A.v.23.:9» nicht wie :26ff. normalisiert; :1/:2 Verweis «s.Abt.…» im Titel, :60 Titel abgeschnitten, :71 Datum «20./26. Dez. / 1906» im Titel.
3. D3170 (alt): 6.1.3.4. steht auf S. 16 zweimal; die erste («1974/75») wird als «Übersichtszeile» verworfen (Blatt Info), die zweite (eigentlich 6.1.4.4., «1978/79», unter Bolliger) hängt unter 6.1.3. Übersichtszeilen-Logik im Korpus prüfen.
4. D3472 (alt): «1967.18» auf S. 41 zwischen 1969.17 und 1969.19 ist Teil 2 der fremden 1967.18 von S. 38 (Muster 3). Mittel: 1952.8/1952.14 doppelt mit Lücke (Grenzfall); 1992.25 Zeitraum 1992.
5. D2828 (K15): Mindest-Soll erfüllt (Anhang ganz im Info, 30. leer, 32. richtig). Die 5 Regesten «in 17.6.»/«in 18.» beschreiben aber Urkunden dieser Einheiten (dort «vgl. die Regesten im Anhang») → nach Muster «Liste ins Blatt Info verschoben» weiter kritisch. Einleitung und I.A. 4861.–4865. im Info vertretbar (Originale in I.A., laut 19.5. in der Urkundendatenbank). D3828 zellgleich, nur «Erzeugt» anders. Nicht angekündigt, aber besser: 19.2./24.11./27.4. jetzt mit ganzem Titel (B35 teilweise).
6. D175827 (Regel 34): Anhang richtig im Info. Die «6 Darin-Verbindungen» sind 8 Stellen in 6 Einheiten. Besser: 10. «Historischer Festzug», 5.1. «Brunner-Waser [1877 – 1941]», 5.2. zweimal. Schlechter: 3.3. «1994 - 2004 Reden am Grab» (zwei Einträge verbunden), 4.1. «[unvollständig] Einladungen», 7.2. (zwei Zeilen zu einer), 5.1. «1999 Zürich betr.». Ursache: Spaltenrand ohne Bibliografie tiefer. Alles gering, kein Textverlust.
7. D1387 (Regel 35): Zuordnung stimmt (1.–13. → Schachtel 1, 14.–30. → Schachtel 2, 31. → Mappe; 1893–1932 / 1893–1943 / 1936–1942). Mittel: Schachtel-Nr. leer; «1900 – 1901» von Pos. 1. in der Anm. der Einheit statt im Darin.
8. Regeln 27–31 (D2137, D2951, D2960, D3170, D3470, D3472, D434, D10675, D10744): alle K-Zeilen am Soll erfüllt. D2960 «1-3.» richtig, 3a. bleibt aussen. D3170 Hinweis «7.2.1. fehlt» korrekt, aber neuer Hinweis «Nummerierung beginnt bei 2.» bei 7.2.2. D10744 «nach 0 folgt 2» trotz 1a.–1c. (gering).

## Muster
- Sonderformen der Signatur (Punkt statt Leerschlag, kein Leerschlag) entgehen neuen Regeln (D177460).
- Wiederholte Signatur dreimal falsch behandelt: als Übersicht verworfen (D3170), als Teil einer fremden Einheit (D3472), als Überschrift verworfen (D10675 712, mittel).
- Eintrag ohne Nummer nach der letzten Einheit (D260 «Schachtel II.»). Zeitraum neuer Einheiten: Jahr in Klammern oder «ca.» mit Zusatz nicht erkannt.

## Unsicherheiten
- D2828: «kritisch» gilt nur, wenn Regesten zu Einheiten als Verzeichnistext zählen; das Mindest-Soll aus NP10 ist erfüllt.
- D10675 712-Köpfe und D3472 1952.8/1952.14 sind Grenzfälle (als mittel gemeldet). D3470 1947.744 zwischen 1942.743/1942.745 ist evtl. ein Zahlendreher (nur Zeitraum betroffen, nicht gemeldet).
- D260 «Schachtel II.»: Signaturform für einen Behälter ohne Signatur bitte nach eigener Konvention wählen.
