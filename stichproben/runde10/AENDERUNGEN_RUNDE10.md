# Runde 10 – Änderungen und Bitte um Nachprüfung 13

Stand 22.11.2026. Skript `findmittel_zu_scope.py` sha256 `424a997636eb557a…`. Aufbau: Runde 9 (`66c0fb74adddd22d…`) plus
diese Runde.

`findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind mit diesem Skript neu erzeugt.

## Worum es ging

Behoben sind die kritischen Zeilen aus `nachpruefung12.md` bzw. `offen_kritisch.csv` (Stand 66c0fb74): alle 73 Zeilen, die
nicht bewusst offen sind. Ausnahme sind die zwei Zeilen, die nach dem Konventionsentscheid nur noch mittel sind (K171,
K176). Dazu kommen die Konventionsentscheide zu den Fragen der NP12 und einige Fälle derselben Art aus eigenen Suchläufen.

**Kennzahlen** (Runde 9 → Runde 10):

| Kennzahl | Runde 9 | Runde 10 | Bemerkung |
|---|---:|---:|---|
| Einheiten | 51'170 | 51'508 | davon +186 in D151150 (K144) und +9 in D3943 (K121) |
| «[ohne Titel]» | 30 | 29 | |
| «Text erfasst 100 %» | 695 | 694 | D3943 99,9 %, siehe unten |
| Doppelte Schlüssel | 10 | 10 | |
| Dateien mit Übersichtszeilen | 9 | 10 | D3190, siehe K71 |
| Tracebacks | 0 | 0 | |

- D3943 steht bei 99,9 %, weil zwei PDF-Zeilen über zwei Unternummern laufen: «… (X.G.209.:1); flache» und «Taschenmesser
  (X.G.209.:2); …». Der Text steht vollständig in den Nachbareinheiten.

**Geändert sind 66 Dateien** (`geaenderte_dateien.txt`).
- Ihr Stand vorher liegt in `vorher/`, dazu:
  - die sechs geänderten Testdaten als `vorher/testdaten_*.xlsx`;
  - das alte `D151210_scope_import.xlsx` aus dem Projektordner;
  - das Skript der Runde 9.
- Zellvergleich: `zellvergleich_runde9_runde10.txt`.
- Textabgleich: `werkzeug/textverlust_runde9_runde10.csv` (Wörter der importierten Felder, die fehlen bzw. neu sind, und
  die Schlussvermerke im Blatt Info). Erzeugt mit `werkzeug/textverlust.py alt neu dateiliste aus.csv`.
- Fehlende Wörter sind überall erklärt:
  - Sie stehen jetzt im Blatt Info (Schlusstext, 20 Dateien);
  - oder in den Spalten Signatur, Schachtel bzw. Zeitraum (z. B. D151150, D3412, D3943);
  - oder sie sind Überschriften, die jetzt als Hinweis bei der folgenden Einheit stehen.

**D151210 ändert sich an einer Stelle:**
- «4.1.2.38. Allgemeine Korrespondenz der künstlerischen Direktion 1990» steht im PDF (S. 115) zwischen 4.1.3.37. und
  4.1.3.39.; 4.1.2. hat sonst nur die Unternummern 1–3.
- Das ist ein Tippfehler im PDF. Neu ist es 4.1.3.38. unter 4.1.3., mit Hinweis; «Nr. im PDF» bleibt «4.1.2.38.».
- Sonst ist die Datei zellgleich.

**Weitere Änderungen in den Testdaten:**
- D149628 (K124–K127);
- D9983 (K123);
- D152810 und D3031 (Buchstaben-Geschwister, Regel 6);
- D3186 (Hinweis Regel 18).

**Fallsets:** C 9/12, F 5/7 und Punkt 2 38/38 sind unverändert. Drei Abweichungen, alle ohne Verschlechterung:
- **A 11 → 10 und B 33 → 32:** Die IDs haben sich verschoben, nach Signatur ist alles unverändert richtig.
  - D2962 VII.150.:11.2.2. ist jetzt ID 69 (vorher 70), 1821–1962.
  - D3063 VII.190.:40.1. ist jetzt ID 68 (vorher 66), 1911–1987.
- **Runde 2 31 → 30:** D3808 «Beilagen:» steht nach K156/Regel 31 in der Bestandszeile VII.65. und nicht mehr im Blatt Info.
- Bitte die drei Soll-Zeilen nachführen.

## Konventionsentscheide zu den Fragen der NP12

1. **Regel 31 und Vorspann:**
   - **K166 D3828:** Eine eigene Eintragszeile (Werktitel, Datierung) direkt vor der ersten Signatur ist ein Stück ohne
     Nummer. Sie kommt in die Bestandszeile.
   - **K171 D3774 und K176 D2894:** Text in Einleitung, Übersicht oder einer Vorbemerkung in Prosa bleibt Vorspann im Blatt
     Info. Das Info ist die Quelle für die Bestandsebene (Bestandsgeschichte, Findmittel). → mittel.
2. **K162 D3271:** Ein beschreibender Satz unter einer Gruppenzeile ohne Signatur, also ein Satz in Klammern mit mindestens
   fünf Wörtern oder «Vgl. …», kommt ins Darin der Einheiten der Gruppe.
   - So viele Einheiten, wie die Gruppenzeile nennt: «Buchhaltungsabschlüsse (29 Hefte)» → 4.2.22.–4.2.50.,
     «Notizen (2 Bände)» → 4.2.51.–4.2.52.
   - Ohne Anzahl nur die erste Einheit: D175994 IV.A.45., wie das Soll von K172.
   - Die Gruppenzeile selbst bleibt Hinweis (K8).
3. **K117 D2710:** bewusst offen, wie D2681 in Runde 7. Die zweite Schachtelfolge «Jahresdokumentation» zählt dieselben
   Nummern; eine Trennung bräuchte einen erfundenen Signaturteil. K115/K116 sind behoben.
4. **«Nach bestehender Konvention kritisch»** (K144, K123/K154/K143, K142, K119/K98): bestätigt und behoben.

## Die Regeln der Runde 10

Nummern in Klammern: K-Zeilen aus `offen_kritisch.csv`.

**Schlusstext und Stücke ohne Nummer**
1. **Schlussabsatz (Regel 3 der Runde 9):**
   - Er beginnt erst mit einem Absatz, der ein echtes Satzende hat. Listeneinträge wie «Mario von Moos, Verzeichnis …,
     Feraltorf 1979» unter «3. Inventare» bleiben Darin (K114 D3530). Abkürzungen wie «o. O. u. J.» zählen nicht.
   - Auch längere Prosa wird erkannt: 12–40 Zeilen mit mindestens drei Satzenden (K155 D2979).
   - Links vom eingerückten Darin genügt ein kleiner Abstand (K158 D3709).
   - Für Findmittel nach Schachteln gilt dasselbe (K145 D2901).
2. **Schlussköpfe:**
   - Neu erkannt: «Geschichte der …:», «Zu diesem Bestand:», «Aufteilung … nach Schachteln:» (K120 D3316). Eine
     Zuordnungsliste «Schachtel 1: Nummern 1.1. bis 1.25.» darin setzt trotzdem die Schachteln.
   - «Der Bestand umfasst:» nimmt die eingerückten Umfangszeilen und die Bearbeitungsvermerke darunter mit ins Info (K131
     D32837, K141 D4054, K159 D3628; ebenso D2962).
   - Bearbeitungsvermerke «neu umgebrochen …», «neu formatiert …», «S. 1 - 6 gelayoutet …» (K169 D3774).
3. **«Anhang»** gilt auch vor den letzten zwei Seiten und in Textgrösse, wenn danach die Signaturfolge nicht weitergeht.
   Beispiele: «Anhang:» S. 19 von 21 (K148 D3063); «Anhang zum Detailverzeichnis …» 14 pt (K161 D3271).
   - Die weggenommenen Zeilen zählen weiter für die Schätzung des rechten Spaltenrands. Sonst ändert sich das
     Zusammenfügen der Zeilen im ganzen Verzeichnis.
4. **Stück ohne Nummer im Schlussteil → Bestandszeile:** Der Satz bzw. die Liste kommt ins Darin der Bestandszeile, der
   übrige Schlussteil bleibt im Blatt Info. Fälle:
   - «Dem Bestand liegen bei:» mit Liste (K150 D3684);
   - «Beim Bestand befinden sich ferner …» und «Der Bestand enthält auch …» (K119 D3563);
   - «Drei Archivschachteln enthalten …» (K77 D1726);
   - «In Schachtel 9 befindet sich ferner …» (K164 D176824);
   - «Der Bestand enthält aus dem Nachlass … ein Geschäftsbuch» nach dem Register (K98 D3026);
   - «Drucksache …» ohne Nummer in der Nummernspalte (K100 D149867);
   - «liegt bei», «Zu diesem Bestand gehört auch …», «Beilagen:» (K174 D3533, K180 D2850, K156 D3808).
   - Die Bestandszeile steht immer als letzte Zeile.
5. **Vorbemerkung zu Schachteln:** «Vorbemerkungen zu den Schachteln 1 bis 5 …:» samt Absätzen kommt ins Darin der
   folgenden Schachtel, nicht der vorigen. Eine Abschnittsüberschrift wie «JAHRESDOKUMENTATION» kommt in den Hinweis (K115,
   K116 D2710).

**Überschriften ohne Signatur bei der folgenden Einheit**
6. **Kursive Gruppen- und Ortsüberschrift** in der Textspalte direkt vor der nächsten Signatur, nach einem Abstand:
   - Beispiele: «Zug» (K138 D10585), «Lose Protokolle» (K160 D3628), «Lose Kassarapporte / Vorstellungsrapporte» (K127
     D149628).
   - Nur wo Kursiv in der Spalte selten ist (nicht D3548), die Einheitszeile selbst nicht kursiv ist (nicht D1404) und die
     Zeile davor nicht auf ein Anschlusswort endet («… Lohnverhandlungen und» / «Gagen»).
   - Ebenso eine fett nummerierte Gliederungsüberschrift in der Textspalte: «2. Werke anderer Autoren» wie «1. …» (K133
     D3589).
7. **Weitere Überschriften:**
   - fette und kursive Überschriftenblöcke (K147 D4173, K172 D175994, K118 D3204, K167 D176795, K170 D3774);
   - kurze Gruppenzeile «Diverses» (K181 D2850);
   - Bereichskopf «Schachteln 7 bis 12 (…)» (K177 D2872);
   - Vermerk «V.B.3.:56. – 65. sind nicht vorhanden …» (K146 D406);
   - Titelblock einer weiteren Serie (K182 D1880) und ein Titelblatt in grosser Schrift oben auf einer Seite (K122 D4175).
   - **Nicht als Überschrift:**
     - zwischen dem Titel einer Einheit und ihrer ersten Unternummer bzw. ihrem ersten weiteren Teil (bleibt ihr Darin:
       D150689 6.1., D3628 «gebunden», D150296 4.3.2.);
     - ein Block mit Schachtelangabe (D176551);
     - ein ganzer Vermerk in Klammern «(Enthält Patientendaten!)»: er gehört zur Einheit davor (K134 D176060).
8. **Gruppenbeschreibung ins Darin** (Konvention K162, siehe oben).

**Signaturen und Gliederung**
9. **Tippfehler in Dezimalsignaturen nach der PDF-Folge** (Muster 10): Die Regel greift, wenn eine Nummer zwischen zwei
   Geschwistern einer anderen Gruppe steht und sich nur in einer Ziffer von der Nummer unterscheidet, die dort fehlt. Dann
   wird sie an der Stelle der fehlenden Nummer eingeordnet, mit Hinweis; «Nr. im PDF» bleibt.
   - **Fälle aus der Liste:**
     - D149628: «20.1.2.19.» → 20.1.3.19. (K124), «29.2.9.» → 29.1.9. (K126);
     - D2857: «1.224.3..» → 1.2.25.3. (K132);
     - D4054: «10.8.2.10.» → 10.3.2.10. (K139);
     - D150296: «3.3.7.» → 3.4.7. (K149).
   - **Vor dem Beginn einer Reihe** wird die Nummer deren Kopf: D149628 «28.1.1.3.» → 27.1.1.3. (K125).
   - **Mitten in einer Reihe** wird sie ein weiterer Teil: D32837 «1.1.2.1.1.» → 1.2.1.1. (K129), D4054 «10.8.4.» →
     10.3.4. (K140).
   - **Ausserhalb der Liste:** D151210 4.1.3.38. (siehe oben), D3470 «40.430» → 42.430 und «41.436» → 42.436.
10. **Buchstaben als Geschwister (Regel 25 erweitert):** «n.a», «n.b» … direkt nach «n.» in derselben Spalte sind
    Geschwister von «n.». Das gilt, wenn «n.» keine anderen Unternummern hat und beide denselben Titel (ohne Jahreszahlen) oder
    je eigenen Umfang bzw. eigenes Datum haben.
    - Auch mehrere Buchstaben und Dezimalsignaturen: D9983 5.6.13.a.–w. (K123), D175996 IV.B.1.a), 460.a)/b) (K143), D9978
      28.6.12.a (K154).
    - Ebenso D152817 VI.SB.C.18.a, D152810 VI.HO.B.13.a und VI.HO.C.73.a, D3031 I.1.a. und IV.l.2.a.
11. **Weitere Signaturformen:**
    - «7. 2.3.» mit Leerzeichen, mehrstufig (K137 D10585);
    - «28.3.25:1–2» ohne Punkt vor «:» (K152 D9978); die Blattangabe «:1–4» bleibt in «Nr. im PDF» und nicht im Titel
      (22 Einheiten in D9978);
    - römisch geschriebene erste Stelle «IV.4.1. Mappe 9» gleich der laufenden Nummer 4.4.1. (K130 D32837);
    - «Nr. 15» unter einem Kopf «Nummer» (D3412).
12. **Fehlende Einheiten aus Übersicht und Inhaltsverzeichnis:**
    - übergeordnete Position nur in der Übersicht, wenn das Detail mit ihren Unternummern beginnt (K128 D32837 «1. Archiv
      Anne-Marie Blanc»; ebenso D3063 6. und 40.); nur wo es für den Bestand nur ein Findmittel gibt (also nicht D4058 19.,
      der in D4054 steht);
    - ein ganzer Abschnitt «X.» mit X.1.–X.4. nur im Inhaltsverzeichnis (K136 D3672);
    - die erste Signaturzeile direkt nach «Detailverzeichnis» (K151 D3528);
    - eine Nummer nur in einer eingeschobenen Übersicht im Bereich (K163 D140969 57.);
    - Inhaltsangaben «[Enthält …]» nur in der Übersicht (K61 D2643).
13. **Unternummern im Text** einer Vollsignatur: eingerückt am Zeilenanfang «X.G.93.:1 …», in Klammern am Zeilenende
    «(X.G.200.:1)» oder im Fliesstext «(X.G.209.:1); flache …». Daraus werden eigene Einheiten (K121 D3943). Ohne eigenen
    Titel der Vollsignatur nimmt sie den Titel der ersten Unternummer, mit Hinweis.
14. **Nummerierte Dossiers unter einem Abschnitt** «9. Akten zum Schlachthof, nummerierte Dossiers», je mit Jahren und
    Schachtel, werden Einheiten 9.144. … 9.2501. (K144 D151150, Muster 8). Eine zweite Nummer auf der Folgezeile («412» /
    «415 Landwirtschaftswesens …») bleibt beim Dossier.
15. **Aufzählung a)–c)** in der Textspalte unter einer Jahr.Laufnummer ohne eigene Schachtel kommt ins Darin (K142 D3472).
16. **Schachteln:**
    - eine Marke, die direkt die laufende Schachtel wiederholt («Schachtel 2: Mappe 3: …»), ist keine neue Einheit (K165
      D2735);
    - Schachtelangabe am Ende einer Überschrift (K157 D3021);
    - römische Gruppen nach der Schachtel (K179 D414);
    - Registraturplan mit Hunderter- und Zehnergruppen (K178 D10744).
17. **Hinweis «zweimal hintereinander mit anderem Titel – Tippfehler?»** bei einem Teil, wenn die Signatur genau zweimal
    direkt hintereinander mit ganz anderem Titel steht (K135 D176060). Nur in Dateien, in denen Teile die Ausnahme sind
    (unter 2 % der Einheiten), also nicht in VII.200.
    - So auch D149888, D2857, D2979, D3186, D3470, D3472, D847.

**Weitere Fälle der Vorabliste** (vor dem Endstand der NP12 behoben): K99 D2759, K151 D3528, K153 D9978, K166 D3828,
K168 D3231, K175 D2894 (eine allein stehende «Schachtel n» ist kein Teil).

## Bewusst offen

- K38 D149622, K39 D1739, K40 D1858, K41 D2614, K42 D3208, K44 D3828, K45 D512, K78 D3894, K173 D1874 wie bisher.
- K117 D2710: neu bewusst offen (siehe oben).
- **K71 D3190** ist nicht mehr offen. «9. Paul Burkhard …» ist jetzt eine einzige Einheit aus dem Detail (S. 6), die
  Übersichtszeile S. 1 fällt weg.
  - Dabei fehlt der Umfang «2 Schachteln» aus der Übersicht (mittel).
  - «b) DETAILVERZEICHNIS» steht im Hinweis bei 1.1.

## Bekannte mittlere Reste

- D3530 «3. Inventare»: Zeitraum 1890–1981 wegen der Lebensdaten «1890 - 1980» im Titel eines Inventars.
- D151150 9.412.: Der Titel enthält die zweite Nummer «415» der Folgezeile.
- D3943 X.G.200. und X.G.209.: Titel der ersten Unternummer als Titel der Vollsignatur (Hinweis).
- D9978 28.3.25.: «undatiert, ungezeichnet» im Titel.
- D2735: «August - Oktober 1912» in zwei Darin-Zeilen (bekannt seit NP2).

## Bitte um Nachprüfung 13

1. **Gegenprüfung der Runde 10 an den 66 geänderten Dateien**, besonders auf Fehlgriffe der Regeln mit breiter Wirkung:
   - 1–3 (Schlusstext);
   - 6–7 (Überschriften);
   - 9 (Tippfehler-Nachbarregel: alle 15 Fälle nach Hinweis «zwischen … – als … gelesen» bzw. «mitten unter den Einträgen»);
   - 10 (Buchstaben-Geschwister);
   - 12 (Einheiten aus Übersicht und Inhaltsverzeichnis).
2. **Suchlauf «Tippfehler in Dezimalsignaturen»** über alle 715 Dateien, wie in NP12 geplant. Gesucht sind Reste, die Regel
   9 nicht fasst.
3. **Zufallsstichprobe** von etwa 60 Dateien aus allen 715, ganz geprüft, um die Restrate nach Runde 10 zu schätzen.
