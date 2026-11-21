# Punkt 2: Zeitraum der Teile mit eigenem Titel, dazu D3793 5.9.3.

Auftrag der Hauptsession (21.11.2026), Stand 15:58:
- **Punkt 2 aus Nachprüfung 7:** Jahre aus dem Werktitel und einzelne Darin-Jahre sollen die Spielzeit nicht verdrängen.
  - Regel: Mit Premierendatum gilt nur dieses, sonst die Spielzeit der Einheit vor der Darin-Schätzung.
  - Beispiele: D151210 IDs 1296, 1343, 1155, 1183, 1716, 1717, 1842 sowie 1493, 1569, 1578, 1611, 1614, 1615.
- **D3793 5.9.3.:** Ein volles Datum in einer Klammer mitten im Titel gilt als Rückfall. Lebensdaten zählen nicht.

Geändert habe ich nur `zeitraum_aus_titel`, `ergaenze_zeitraeume` und drei neue Hilfsfunktionen davor. Die Stellen, die
sich die Hauptsession vorbehalten hat, habe ich nicht angefasst. Gearbeitet habe ich nur in Kopien im Scratchpad.

## Dateien

- **`findmittel_zu_scope_punkt2.patch`:** gilt gegen «5e333035 + Runde 2» (sha256 c4b486eb…), 82 Zeilen.
  - Angewendet ergibt er genau `findmittel_zu_scope_vorschlag_punkt2.py` (sha256 2953088e…, 6250 Zeilen).
  - Er passt auch ohne Fuzz auf «fde790ac + Runde 2».
- **`findmittel_zu_scope_runde2_punkt2_auf_5e333035.patch`:** Runde 2 und Punkt 2 in einem Patch gegen den heutigen
  Projektstand 5e333035, 212 Zeilen. Er ergibt dieselbe Datei.
- **`aenderungen_korpus.csv`:** die 35 Einheiten, die sich durch Punkt 2 ändern.
- **`werkzeug/punkt2_faelle.csv`:** 38 Fälle für `../werkzeug/pruefe_runde2.py`.
  - 9 davon sind Kontrollfälle, die gleich bleiben müssen.
  - Dazu kommen 3 Werte, die schon vorher stimmten: die beiden Titel mit Werktitel-Jahren und 1578 bis 1998.

## Testergebnisse

| Prüfung | ohne Punkt 2 | mit Punkt 2 |
|---|---:|---:|
| Fallset Punkt 2 (38 Fälle) | 12 | 38 |
| Fallset Runde 2 (34 Fälle) | 34 | 34 |
| Fallsets A, B, C, F aus Runde 6 | 11, 37, 10, 5 | unverändert |
| Einheiten / «[ohne Titel]» / Text 100 % / doppelte Schlüssel | 49'242 / 34 / 695 / 10 | unverändert |

- **Gesamtlauf:** Es ändern sich 35 Einheiten in 7 Dateien, alle angesehen. Die D151210-Fälle habe ich mit dem PDF-Text
  verglichen.
- **Textverlust:** keiner. Weg sind nur die Anmerkungen «1917, 03.02.1977» und «1856, 01.04.1984». Die Werktitel-Jahre
  stehen weiter im Titel.
- **Testdaten:** unverändert.
- **Runde 2 und Punkt 2 zusammen auf 5e333035:** 223 Einheiten in 72 Dateien, also genau 188 + 35.

## Die Regeln

### 1. Premierendatum (`zeitraum_aus_titel`, neu `_ist_premierendatum`)

Hat ein Teil mit eigenem Titel am Ende ein Tagesdatum in Klammern, zählt nur dieses. Die übrigen Jahre gehören zum
Werktitel und bleiben im Titel:
- 1183 «Travesties oder Zürich 1917, Theaterstück von Tom Stoppard (03.02.1977)» ergibt = 03.02.1977, vorher
  1917–03.02.1977 mit Hinweis «Mehrere Zeitangaben».
- 1296 «Aus dem Leben der Regenwürmer. Ein Familiengemälde von 1856, … (01.04.1984)» ergibt = 01.04.1984.

### 2. Spielzeit der Serie (`ergaenze_zeitraeume`, neu `_spielzeit_fuer_teil`, `_lage_zur_spielzeit`)

**Wann die Regel gilt:**
- Es geht um einen Teil mit eigenem Titel.
- Die Serie hat einen Zeitraum aus Datumsspalte, Titel oder Inhaltsverzeichnis über genau zwei aufeinanderfolgende Jahre,
  zum Beispiel «Produktionen … 1974/75» oder «Akten über Veranstaltungen … 1997–1998».
- Der Teil setzt die Einheit nicht fort (`_ist_fortsetzung`), und er trägt keinen Hinweis «Signatur taucht erneut auf».

**Was mit dem Titeldatum geschieht:**
- Ein Jahr ausserhalb der Spielzeit oder ein einzelnes Jahr innerhalb wird zur Spielzeit. Die Jahre bleiben im Titel.
  Das betrifft 1155, 1343, 1589, 1717, 3081 sowie 1564, 1702 und 1842.
- Es bleiben:
  - ein Tages- oder Monatsdatum;
  - die Spielzeit selbst;
  - eine Spanne, die die Spielzeit schneidet und über sie hinausreicht. Beispiele: 1423 «(Akten 1989–1991)», 1439
    «Produktionen im Schauspielhaus-Keller 1990–1992», 1987 «(1955/56–1956/57)».

**Was mit der Darin-Schätzung geschieht:**
- Ein einzelnes Datum oder eines ausserhalb wird zur Spielzeit. Das betrifft 1493, 1569, 1611, 1614, 1615 und 1716.
- Eine Spanne innerhalb der Spielzeit bleibt, weil sie genauer ist: 1281 «(16.10./01.12.1982)» sowie 1812, 2684 und 2698.
- Eine Spanne, die über die Spielzeit hinausreicht, wird mit ihr vereinigt: 1578 «Gastspiele 1997/98» ergibt 1996–1998,
  wie im Soll von Nachprüfung 7.

**Folge für die Serien:** Ihre falschen Hinweise «Untereinheiten reichen über den Zeitraum hinaus (1856–1984)» und
ähnliche fallen weg (1154, 1180, 1295, 1328, 1585, 1714, 3071).

**Warum so eng:** Eine erste Fassung mit «Serie bis zwei Kalenderjahre» änderte 280 Einheiten.
- In D3589, D3943, D1880 und D3231 sind Teile eigene Stücke mit eigenen Jahren: Bücher, Ausgaben, spätere Schachteln.
  Ein Beispiel ist «Gemeindegesetz ¦ 1938–1940» nach «Gemeindegesetz ¦ 1934–1935».
- Der Strich nach der Signatur wäre das bessere Merkmal. Er fällt aber schon in der Hauptschleife weg, also im Bereich der
  Hauptsession.

### 3. Volles Datum in einer Titelklammer (`zeitraum_aus_titel`)

**Regel:** Gibt es sonst kein Titeldatum und keine Datumsspalte, zählt ein volles Datum aus einer Klammer mitten im Titel.
- Es muss Tag, Monat und Jahr haben und höchstens ein Jahr umfassen. Lebensdaten wie «(16. Oktober 1718 – 17. März 1767)»
  fallen damit weg.
- Nahe Jahre im Darin zählen mit, höchstens 10 Jahre entfernt.

**Wirkung:**
- **D3793 5.9.3.:** = 14.08.1938, die Serie 5.9. reicht jetzt bis 14.08.1938.
- **Vorher ohne Zeitraum, jetzt richtig:**
  - D10675 742.68: 14.01.1987 aus «Postulat … (14. Januar 1987)»;
  - D141020 9.4.: 16.05.1971 aus «Hans-Reinhart-Ring (Zürich, 16.5.1971)»;
  - D150589 15.1.47.: 10.10.1956;
  - D151399 12./12.1.: 16.01.2019–28.07.2019, die Ausstellungsdaten;
  - D3437 4.3.: 31.10.1980 aus «Auflösung … (auf den 31. Oktober 1980)».
- **D10675 745.52:** 03.04.1992–08.03.1993, das erste Seminar im Titel, das zweite im Darin. Vorher galt nur 08.03.1993.
- **D151210 1435:** bleibt 1989–1991 aus «(02.10.1990), Akten» und «1989–1991: Besetzungsliste …».

## Offen und Grenzfälle

- **1569 «Korrespondenz ab 1982»:** jetzt die Spielzeit 1996–1997, wie die Regel der Hauptsession es will. Das Soll aus
  Nachprüfung 7 nannte auch «1982–1997».
- **1564 und 1702:** Hier steht ein einzelnes Jahr in der Spielzeit, «Theater – Labor – Tage 1997» und «Kultursymposium
  1990». Die Einheiten haben jetzt die Spielzeit, das Jahr steht wieder im Titel.
- **3081:** Im Darin steht «Premiere: 10. Februar 1989», das zählt nicht als Premierendatum im Titel. Es gilt die Spielzeit
  1988–1989.
