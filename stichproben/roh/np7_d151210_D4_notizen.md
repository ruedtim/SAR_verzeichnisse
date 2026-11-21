# D151210 (VII.200., Schauspielhaus Zürich AG) – siebte Nachprüfung, Bereich D4, PDF-Seiten 246–424

Beurteilt: `$S/neu7/D151210_scope_import.xlsx` (Stand 18:11) am PDF `$P/D151210.pdf`, Vergleich mit 15:43
(`$S/neu6/…`). Skriptzeilen beziehen sich auf `$S/neu7/findmittel_zu_scope.py` (fde790ac…). Hilfsdateien in
`$S/np7/tmp_D4/`.

## Vorgehen

- Jede geänderte, neue oder weggefallene Einheit der 75 Seiten aus `D4_seiten.txt` habe ich am PDF gelesen:
  - mit der Seitendatei `np7/d151210/seiten/seite_NNN.txt`;
  - mit den pdfplumber-Zeilen samt x0/x1 (gleiche Parameter wie `lese_zeilen`, `tmp_D4/zeilen.py`).
- Automatische Hilfen:
  - Wortabgleich 15:43 ↔ 18:11 (`vgl.py`): kein Text ist zu einer anderen Einheit gewandert. Weggefallen sind nur
    Serientitel, Datumswörter (stehen jetzt in von/bis) und die angeklebten Signaturen «8.1.1.xx.».
  - Vergleich der Eintragsgrenzen ohne Satzzeichen (`segvgl3.py`): jede neue und jede verlorene Fuge am PDF nachgesehen.
  - Teil-Nummern (`nachbar.py`).
- Ursache: Ich habe die Zwischenstände Feld für Feld verglichen (`stufen.py`):
  - `verb/aus_basis` = 8e2bd7f9;
  - `aus_haupt_f3` = Hauptsession;
  - `aus_rebase_f3` = Hauptsession + Patch;
  - 18:11.
- Der Patch der Prüfsession ändert in D151210 im Bereich nichts: Kein Feld ändert sich zwischen `aus_haupt_f3` und
  `aus_rebase_f3`.

## Zahlen

**Umfang**
- 179 Seiten (246–424), davon 75 mit Änderungen.
- Einheiten: 1544 (15:43, IDs 1619–3162) bzw. 1543 (18:11, IDs 1619–3161).
- Geändert: 191. Neu: 0. Weggefallen: 1, nämlich das 7. Vorkommen von 8.1.1.44.: Der erfundene «Teil 6» ist weg.

**Urteile (192)**
- besser 138, gleich 44, schlechter 10, unklar 0.
- Nach Bereich:

| Bereich | Einheiten | besser | gleich | schlechter |
|---|---|---|---|---|
| 5.2.4.34./35. Produktionen | 18 | 18 | 0 | 0 |
| 5.2.5. Veranstaltungen | 66 | 32 | 29 | 5 |
| 5.3./5.4. Gastspiele | 27 | 13 | 11 | 3 |
| 6. Rollenbücher | 21 | 18 | 1 | 2 |
| 8.1.1. Fotos | 43 + weg | 44 | 0 | 0 |
| 8.1.7. | 13 | 12 | 1 | 0 |
| 8.3., 11. | 4 | 2 | 2 | 0 |

**Ursachen**
- 8e2bd7f9: 109 Einheiten, davon 64 besser, 37 gleich, 8 schlechter.
- 1 (Ordnungszahl nach dem Strich): 11. 2: 1. 3: 13 + weg. 4: 31. 5: 9. 6: 1. 7: 3. 8: 5. 9: 4.
- Kombiniert: «8e2bd7f9; 8» 2, «8e2bd7f9; 5» 1, «9; 5» 1.
- Änderung 1 wirkt hier vor allem dadurch, dass Teile, die mit «60. Geburtstag …» oder «25 Jahre …» beginnen, jetzt
  einen eigenen Titel bekommen.

**Fundzeilen (46)**
- behoben 12: N385, N392–N400, N408, N409.
- teilweise 7: N381, N384, N402, N406, N407, N410, N419. Bei N384 und N402 sind nur die Folge-Nachbartitel behoben.
- offen 25.
- schlechter 2: N387, N401.
- 20 Zeilen sind bewusst offen. Davon teilweise: #30, #56, #65.
- Die 25 Zeilen mit `geaendert_seit_1543` = 0 habe ich am PDF bestätigt. Bei N384 (#30) und N402 sind die genannten
  Einheiten selbst unverändert, aber ihre Folgeteile haben sich geändert (Nachbartitel weg).

**Neue Zeilen (5)**
- 3 mittel:
  - Zeitraum aus falscher Quelle: 1716, 1717, 1842;
  - Listeneintrag als Teil-Titel: 1826, 1847, 1849, 2131;
  - Rollenbücher verschmolzen: 2123.
- 2 gering:
  - Zeilengrenze verloren: 1622;
  - Unterzeilen verbunden, schon vor 15:43: 1623, 1631, 1632, 1633, 1635.
- Keine kritischen.

## Z291 (in den Paketen Z261, #2) im Bereich: Titel vom Nachbarteil

- Stand 15:43: Auf S. 246–424 trugen **35 Teile** den Titel eines Nachbarteils.

| Serie | Teile | IDs |
|---|---|---|
| 5.2.4.35. | 8 | 1630–1637 |
| 5.2.5.3. | 7 | 1678–1684 |
| 5.2.5.4. | 5 | 1692–1696 |
| 6.4. | 8 | 1904–1911 |
| 6.62. | 2 | 2175, 2176 |
| 8.1.1.44. | 4 | |
| 8.3.2.14. | 1 | 2726 |

- Stand 18:11: **0**, automatisch gezählt über alle 747 Teile des Bereichs und am PDF geprüft.
  - 20 Teile haben jetzt ihren eigenen Produktions- oder Veranstaltungstitel. Bei 5 davon (1681–1684, 1692) stehen
    noch die Unterlagen im Titel (siehe unten).
  - 11 Teile haben jetzt den Serientitel: «Rollenbücher, Teil n» bzw. «Filmnegative und Blattkopien, Aufführungen,
    Teil 5».
  - 4 Teile heissen jetzt «Fotos der Aufführungen des Schauspielhauses, Teil n», mit dem richtigen Inhalt.
- Änderung 2 verhindert ausserdem 12 Nachbartitel, die 8e2bd7f9 neu erzeugt hätte. Netto sind diese Einheiten
  unverändert: 1704, 1712, 1718, 1721, 1800, 1813, 1822, 1827, 1828, 1831, 1866, 2557.
- Teil-Nummern (Z260/#1): 747 Teile, alle eindeutig und in PDF-Folge, «…, Teil n» passt zur Spalte Teil.
- Teile mit eigenem Titel: 162 → 272. Serientitel + Teil: 551 → 475.

## Verbesserungen (Hauptmuster)

1. **Produktionen 5.2.4.34./35. (8e2bd7f9, Regel 9)**
   - Titel ist jetzt die Produktionszeile, die Unterlagen stehen Zeile für Zeile im Darin.
   - Beispiel ID 1619: «Julies Game, Theaterstück von August Strindberg» • «Korrespondenz, Besetzungsliste, Mitteilungen» • «Bühnenpläne und Skizzen» • …
   - Blutspuren 2–5 (1626–1629) sind jetzt vor «: Besetzungsliste …» geteilt (N381).
2. **Veranstaltungen 5.2.5.x**
   - Jeder «- …»-Punkt ist jetzt Titel seines Teils. Der Zeitraum ist jetzt das Ereignisdatum bzw. Titeljahr statt
     des Jahrzehnts der Serie (51 Einheiten ohne 1716/1717, z. B. 1656 = 20.01.1963, 1695 = 01.02.1988).
   - Bei 25 Einheiten stehen die Unterlagen richtig im Darin, z. B. 1646, 1650, 1652, 1659, 1665, 1678–1680, 1693–1696,
     1711.
3. **Rollenbücher 6.x (Regel 5)**
   - «de Vega», «Molière:», «Euripides:», «Schönthan Paul von» und «Morgen - Ein Fenster …» sind jetzt richtig.
   - Damit behoben: N392–N400 (9 Zeilen).
4. **Fotolisten 8.1.1.x**
   - Regel 4: 29 Einheiten mit 31 reparierten Fugen.
   - Regel 3: alle 10 angeklebten Signaturen sind weg (N408).
   - 8.1.1.44. ist richtig: Teile –, 1–5, kein «Teil 6» (N409).
5. **Weitere**
   - Namenslisten (Regel 8): 1707, 1708, 1806, 1819, 1821, 1830, 2878.
   - Strich am Zeilenende (Regel 7): 1740, 1768, 1853.
   - 8.1.7.1. Teile 2–12 haben jetzt ihr eigenes Jahr statt 06.1988 (N410 teilweise).

## Verschlechterungen (mit Fundstelle)

- **Zeitraum aus falscher Quelle** (neue Zeile, mittel). Um 15:43 stimmte der Serienzeitraum.
  - ID 1717 (S. 256, 5.2.5.13. Teil 4): 1848–1900 aus dem Ausstellungstitel «… im jungen Bundesstaat 1848–1900».
    Folge: Hinweis bei 1714 «(1848–1998)».
  - ID 1716 (S. 256, Teil 3): Genau 1948, geschätzt aus dem Matinee-Titel «Die Verborgenen 1948».
  - ID 1842 (S. 281, 5.4.5.1. Teil 3): Genau 1991 aus dem Listeneintrag «Militärrapport 1991». Das Jahr ist dafür
    aus dem Titel entfernt.
- **Listeneintrag als Teil-Titel** (neue Zeile, mittel)
  - ID 2131 (S. 319, 6.53. Teil 3): «Dürrenmatt, Friedrich: Der Meteor Dürrenmatt-Lesung, diverse Texte» statt
    «Rollenbücher, Teil 3». Nach 8e2bd7f9 braucht die Listenregel mindestens zwei «Name: Werk».
  - ID 1826 (S. 278): «Projekt „Jemand …“: Projektbeschreibung, …».
  - ID 1847 (S. 282).
  - ID 1849 (S. 282): «Korrespondenz mit verschiedenen Theatern, Künstlern und Agenturen». Dafür ist das Darin jetzt
    richtig getrennt.
  - Ursache bei 1826/1847/1849: `_liste_folgt` sucht nur 4 Zeilen weit.
- **ID 2123** (S. 318, 6.51. Teil 4, Regel 5; neue Zeile, mittel): «… Solo für Carlos und Sigmund Bräker, Ulrich:
  Jauss der Liebesritter» ist jetzt ein Eintrag. Um 15:43 war es richtig repariert.
- **ID 1720** (S. 257, N387 schlechter): Es gibt eine zusätzliche Trennung «„Briefwechsel Dürrenmatt» / «Frisch“».
  Der Strich am Zeilenende in offener Anführung ist dabei weggefallen.
- **ID 1622** (S. 246; neue Zeile, gering): Die Zeilengrenze «Mitteilungen | Pressespiegel» ist verloren, gleich wie
  D3 ID 1604.

## Bewusst offene Arten – gezählt, nicht als neue Zeile gemeldet

- **Unterlagen nach «…:» im Titel, Darin leer** (Art #20/#30): **33 Einheiten**, alle neu seit 15:43 (8e2bd7f9; bei
  1657/1658/1661/1663/1674 Änderung 1).
  - IDs: 1640, 1641, 1644, 1645, 1647, 1648, 1653, 1654, 1655, 1657, 1658, 1661, 1663, 1666–1671, 1674–1676,
    1681–1684, 1686–1690, 1692, 1713.
  - Das Datum steht dabei weiter mitten im Titel.
  - Ursache: Teile laufen ohne Doppelpunkt-Regel durch `kopf_und_rumpf`. Die Unterlagen-Regel greift nur nach
    «… von X» (`UNTERLAGEN_RE`) bzw. nur mit Wörtern aus `UNTERLAGEN_DOPPELPUNKT` («Fotos», «Entwurf», «Brief»,
    «Verzeichnis», «Texte» fehlen). `teile_langen_titel` teilt nur ab 160 Zeichen.
  - Urteile:
    - gleich (26): Der Zeitraum ist besser, die Titel/Darin-Grenze schlechter.
    - schlechter (2): 1657 und 1713, kein Zeitraumgewinn.
    - besser (5): 1681–1684 und 1692, vorher Nachbartitel.
- **Inhaltliche Zeitraumfälle**, neu seit 15:43, alle mit Gewinn gegenüber 15:43: **6**.
  - Das Ereignisdatum übergeht Darin-Daten: 1646 (Artikel 1949), 1651 («Zeitungsartikel von 1962»), 1659 (29. Sept.
    1963), 1660 (Beilagen 1939/1963).
  - Biografie-Jahre der Bildlegende werden mitgezählt: 2546 (1932–1935), 2554 (1934–1938).
- **Datumsreste**, neu: **2**.
  - 2553: «„Pfingsten 1937, …“» → «„Pfingsten, …“», das Jahr ist mitten aus dem Zitat entfernt (Art #70).
  - 1749: «Wiener Junifestwochen 1995 (…)» → ohne Jahr; harmlos.
- **Bewusst offene Zeilen des Pakets**: alle 20 bestätigt. Siehe oben; #30, #56 und #65 teilweise wegen Folge- bzw.
  Nachbaränderungen.

## Angekündigt, wirkt im Bereich nicht oder nur teilweise

- **Regel 4 für «Titel (Szenenfotos …)» (8.3.x):** Keine Reparatur. N413 bleibt offen («König» / «Johann», «Meine» /
  «Schwester», «Herr» / «Puntila», «Faust» / «I»).
- **Regel 4 bei 8.1.1.x:** N406 ist teilweise behoben (20/28), N407 ebenfalls (10/14).
  - Offen bleibt es, wenn das Folgestück gross beginnt oder ein Datum davorsteht: «Santa» / «Cruz», «Don» / «Juan»,
    «Onkel» / «Vanja», «Dantons» / «Tod», «…, 27. Mai 1994 Blick zurück …».
  - Plakatlisten 8.2.3.x (N411, N412) sind nicht abgedeckt.
- **Regel 6** («Strich-Zeile in offener Anführung») hilft bei 1720 nicht (N387).
- **Regel 8** greift nicht bei «Ferruccio» / «Soleri» (N390).
- **Prüfhinweis «Verschobene Zeilenumbrüche … repariert»:** Er fehlt jetzt bei 2075, 2666 und 2695, obwohl die
  Reparatur weiter gemacht wird und richtig ist. Gering, Urteil gleich, nicht gemeldet.

## Textverlust (D4_textverlust.csv, 18 Stücke)

Kein echter Verlust, keine falsche Zuordnung.
- 3 Stücke aus 5.2.x sind jetzt nur anders getrennt (1620, 1652, 1665): Titel + Darin, Datum in von/bis.
- 14 Stücke sind die alten Nachbartitel «Shakespeare, William: König Johann, Teil n», «Gorki, Maxim: Nachtasyl,
  Teil n» und «Don Carlos von Friedrich Schiller, Teil n». Sie sind richtig ersetzt. Der Text steht weiter bei 6.4.
  Teil 4, bei 6.62. Teil 4 und im Darin von 8.1.1.44. Teil 1.
- 1 Stück (2553): Das Jahr ist aus dem Zitat entfernt, steht aber in «Fotos 1937» und im Zeitraum. Art #70, siehe oben.

## Fälle anderer Pakete auf meinen Seiten

- **N377 (#23, D3):**
  - Im Bereich behoben, 7 von 13: 1707, 1708, 1768, 1806, 1819, 1821, 1830.
  - Unverändert offen, 6: 1766 «Neue; Schaubühne», 1771, 1782 «Tourneetheater; E. Grabowsky» (Initial ohne
    Personenbezeichnung, gewollt), 1791, 1794, 1833.
- **N369 (#15, D2):** 1726 (S. 258) und 1987 (S. 300) unverändert.
- **N375 (#21, D3):** 1824 (S. 278) unverändert = 1988.
- **Gleiche Muster wie bei D3:**
  - «Unterlagen im Titel» (D3 1426, 1480 …);
  - Zeitraum aus dem Thema: D3 1589 = mein 1717;
  - Zeilengrenze verloren: D3 1604 = mein 1622.
  - Bei 1717 melde ich eine Zeile, weil es eine echte Verschlechterung gegenüber 15:43 ist. D3 hat 1589 nur in den
    Notizen.

## Ursachen im Skript (Kurzfassung)

- **8e2bd7f9:** Der Strich nach der Signatur fällt weg (Z. 2206–2213, 2443–2445). Damit wird jeder «- …»-Punkt
  Titel seines Teils.
  - Was dann im Titel bleibt, entscheiden `kopf_und_rumpf` (Z. 3059) und `teile_langen_titel` (Z. 3148). Es gibt
    keine Doppelpunkt-Regel für Teile, und `UNTERLAGEN_DOPPELPUNKT` (Z. 3019) ist knapp.
  - `_liste_folgt` (Z. 3038, 4 Zeilen) erkennt lange Listenpunkte nicht.
  - Die Listenregel verlangt ≥ 2 «Name: Werk» (Z. 3263).
  - Der Zeitraum eigener Teil-Titel kommt aus Titel/Darin statt aus der Serie.
- **Hauptsession nach 8e2bd7f9:**
  - Regel 1: Ordnungszahl → Titel.
  - Regel 2: Nachbartitel zurück auf den Serientitel.
  - Regeln 3–9 wie angekündigt.
  - Einzige Verschlechterung daraus im Bereich: Regel 5 bei 2123.
