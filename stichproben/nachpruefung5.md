# Fünfte Nachprüfung am Excel-Stand 20.11.2026, 13:15

Geprüft wurde `findmittel_excel/` vom 20.11.2026, 13:15, dazu `testdaten_excel/` und `D151210_scope_import.xlsx`. Das Skript
hat sha256 `68ad815eb4d61cf5…` und 5076 Zeilen.
- **Schnappschuss «neu5»:** `/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/neu5/`.
  Alle Zeilennummern beziehen sich auf das Skript dort. Beim Abschluss waren das Projektskript, `findmittel_excel/`,
  `testdaten_excel/` und `D151210_scope_import.xlsx` noch identisch mit dem Schnappschuss (sha256 verglichen).
- **Vergleich:** mit dem Stand 11:30 der vierten Nachprüfung (`…/scratchpad/neu4/`).
- **Geänderte Dateien:** Inhaltlich geändert sind 234 Dateien in `findmittel_excel/`, genau die Liste in
  `zellvergleich_1130_1315.txt`. Die «235» der Nachricht sind diese 234 plus `uebersicht_scope_import.xlsx`. Dazu kommen
  10 Testdateien. In allen übrigen Dateien hat sich nur die Zeile «Erzeugt» im Blatt Info geändert.
- **Belege:** Jedes Urteil ist am PDF belegt. Am Skript und an den Excel-Dateien habe ich nichts geändert.

## Kurzfazit

- **271 nachgeprüfte Zeilen** (alle aus `funde_nachpruefung4.csv` mit Status ≠ behoben): 30 behoben, 63 teilweise,
  175 offen, 3 schlechter.
  - 73 Zeilen liegen in PDFs, die seit 11:30 inhaltlich unverändert sind. Dort gilt der Befund von 11:30 weiter.
  - Die offenen Zeilen in geänderten PDFs sind fast alle laut Diff unverändert.
- **Kritische Zeilen: 11 von 33 behoben**, 18 teilweise, 4 offen, keine schlechter.
  - 11 der 22 nicht behobenen sind die bewusst offenen Punkte (Auftrag 4), bestätigt.
  - Echte Restfehler sind 11 Zeilen, alle teilweise:
    - D3060: Porträtbilder S. 8;
    - D3089: Rollen- und Textbücherliste im Darin von X.;
    - D3105 «Band 1»;
    - D150689 1.2.4.;
    - D1880: Unterabschnitte a.–i.;
    - D3018: Rest von S. 78;
    - D3271 4.2.22.: Bereich jetzt Zwischenüberschrift, Behälterangabe nur im Hinweis;
    - D3774: Abteilungen richtig, aber 5.3./6.4. und viele Unternummern fehlen;
    - D65, D67, D69: Kategorie-Gruppen tragen die Signatur ihrer einzigen Einheit.
  - Von den 15 kritischen Fehlern der Runde 4 sind 10 behoben, 5 teilweise (D3271, D3774, D65, D67, D69). Behoben sind z. B.:
    - D9983 5.6.: 54 Darin-Einträge wieder an der richtigen Stelle (h);
    - D3089: XI. nicht mehr erfunden (f);
    - D3253 2. (g);
    - D1880: «f. Heizamt» als Hauptabteilung, D.III./G.III. der 3. Serie (d);
    - D3018 02.3.l. (e);
    - D2534: Schachtel 7–13 nicht mehr erfunden (r);
    - D2558 3. (p);
    - D3466 168. (o);
    - D49 (s).
  - Von den 14 kritischen Zeilen, die um 11:30 teilweise behoben waren, ist nur D3099 1.2.5. jetzt ganz behoben: Die zweite
    Nennung ist Teil 2 (c).
- **Die 3 «schlechter» aus Runde 4 sind jetzt teilweise behoben:**
  - Z49 D2951 1.22.: Der eigene Titel ist wieder da.
  - Z147 D4054: Die Teile tragen meist den richtigen Zeitraum.
  - Z227 D3067: Schachtel 302 hat 1943–1958. V./V.B. beginnen aber bei 1401 aus «seit 1401».
- **Mittel/gering in geänderten PDFs (168 Zeilen):** 19 behoben, 34 teilweise, 112 offen, 3 schlechter:
  - Z121 D3018: Weitere Plannummern gelten als Jahre, bis 2028.
  - Z221 D3018: Regel n lässt «ca.1890-1964» und «1920. - 1963» ganz im Titel.
  - Z316 D3466: Regel j hängt die Folgezeile an, dadurch steht der nicht erkannte Datumsrest bei 16 weiteren Titeln mitten im
    Titel.
- **Neue Fehler: 102**, davon 11 kritisch, 82 mittel und 9 gering.
  - Aus den Regeln a–u stammen 59, davon 1 kritisch (D3774 5.3./6.4., Regel t).
  - Allein aus Regel a stammen 34 (30 mittel, 4 gering), aus b 8.
  - Nicht angekündigte Änderungen ohne passende Regel habe ich keine gefunden.
  - Schon um 11:30 vorhanden, jetzt erst erfasst: 43, davon 10 kritisch:
    - D141: 26 Einheiten fehlen;
    - D140969: 3 Einheiten fehlen;
    - D151150: «10.5..2.» fehlt;
    - D442: das zweite «26.» fehlt;
    - D631: «B 998» ist erfunden;
    - D1858: die Zählung beginnt je Schachtel neu;
    - D3808, D3874, D4057, D8949: Signaturen sind aus Zahlen im Text erfunden.
- **Regelstichprobe:** Am PDF geprüft wurden 773 Einheiten in 150 PDFs. 542 sind besser, 93 gleich, 124 schlechter und
  14 unklar.
  - Ohne neuen Fehler oder fast ohne: d, e, f, g, h, l, o, p, q, r, s.
  - Überwiegend gut, mit einzelnen Folgefehlern: n, k, i, c, t.
  - Mit erheblichen Nebenwirkungen: **a** (55 von 352 schlechter), **b** (22 von 48 schlechter) und **u** (13 von 38
    schlechter).
- **Kennzahlen** (eigene Zählung, gleich wie die Hauptsession):
  - Einheiten in `findmittel_excel/`: 49'314 → 49'311.
  - «[ohne Titel]»: 44 → 35.
  - «Text erfasst» 100 %: 694 → 694 von 715 PDFs.
  - Mehrfach vergebene Schlüssel (Signatur, Teil): 1'611 → 69. Das sind 4'327 → 80 überzählige Zeilen.
  - «Nicht übernommen» insgesamt: 2'108 → 2'089 Zeilen.
  - 18 PDFs wechseln von «Prüfen» zu «OK», meist weil die Hinweise «Zeitraum … geschätzt» wegfallen. Das ist kein
    Qualitätsmass: D867 und D4054 sind dabei und haben neue Fehler.
- **Gegenprobe:** 8 Urteile der Prüfagenten habe ich selbst am PDF nachgesehen, alle hielten:
  - D141 «V.A. c.115.: 76»;
  - D3018 3.1.21. (Plannummern);
  - D631 «B 998»;
  - D3774 5.3./6.4.;
  - D1858 (Zählung je Schachtel);
  - D442 «26. Tätigkeitsberichte»;
  - D151150 «10.5..2.»;
  - D10744 (Fussnotenzeichen 8,0 pt).

## Methode

1. **Schnappschuss «neu5».** `findmittel_excel/` (716 Dateien), `testdaten_excel/` (13), `D151210_scope_import.xlsx` und
   `findmittel_zu_scope.py` sind nach `…/scratchpad/neu5/` kopiert. Die sha256-Werte aller Dateien stimmen mit der Quelle
   überein. Geprüft wurde nur dieser Schnappschuss.
2. **Vergleich 11:30 ↔ 13:15.**
   - Inhaltsvergleich aller Blätter ohne die Zeile «Erzeugt»: 234 + 10 Dateien. D152810 und D3031 gibt es nur als
     Testdatei; die übrigen 8 geänderten Testdateien sind inhaltlich gleich wie in `findmittel_excel/`.
   - Einheitenvergleich je PDF. Weil Regel c die Teil-Nummern ändert, ordne ich die Einheiten diesmal über **(Signatur,
     n-tes Vorkommen)** zu, nicht über (Signatur, Teil).
   - Über alle 715 Dateien sind 43'253 Einheiten unverändert, 6'015 geändert, 46 entfernt und 43 neu. Bei 4'043 Einheiten hat
     sich nur die Teil-Nummer geändert.
   - Dazu ausgewertet:
     - die Familien der Änderungen;
     - die Art jeder Zeitraum-Änderung (1'496 Einheiten: 704 nur Quelle, 684 weiter, 52 enger, 31 nur Anmerkung, 16 neu,
       4 verschoben);
     - die geänderten Prüfhinweise;
     - Text aus 11:30, der nirgends mehr steht;
     - Titel, an die die erste Darin-Zeile angehängt wurde;
     - eine Prüfung der Teil-Nummern über alle Dateien.
   - Werkzeuge liegen in `…/scratchpad/np5/werkzeug/`, die Ergebnisse in `…/scratchpad/np5/`.
3. **Prüfliste** (`methode/np5_pruefliste.csv`, `np5_auswahl.py`). Ausgewählt sind alle 271 Zeilen aus
   `funde_nachpruefung4.csv` mit Status ≠ behoben:
   - 33 kritische;
   - die 3 «schlechter»;
   - 168 mittel/gering in geänderten PDFs;
   - 67 mittel/gering in unveränderten PDFs.
   In unveränderten PDFs ist der Befund von 11:30 übernommen (`roh/np5_vorbewertet.csv`, 73 Zeilen, davon 6 kritische).
4. **Prüfung am PDF.** Sechs Prüfagenten mit je einem Paket, dazu ich als Gruppe 0:
   - G0: bewusst offene Punkte, D3099, Testdatei D152810, Gesamtabgleiche;
   - G1: Regeln d–h;
   - G2: o–u;
   - G3: a (Beispiele der Hauptsession, Zufallsstichprobe);
   - G4: b, c, j, m;
   - G5: i, k, l, n und die übrigen Titeländerungen;
   - G6: a (verdächtige Fälle).
   Anleitung: `methode/ANLEITUNG_NACHPRUEFUNG5.md`; Rohdaten: `roh/np5_gruppe_N.csv`, `_regeln.csv`, `_notizen.md`.
5. **Regelstichprobe.**
   - Je Regel die Beispiele der Hauptsession und weitere betroffene Einheiten aus dem Vergleich. Urteil je Einheit: besser,
     gleich, schlechter oder unklar.
   - Bei a, b und c dazu zufällig gezogene PDFs (Startwert 20261120):
     - a: 10 PDFs mit 18 Einheiten, dazu 4 PDFs mit vielen Zeitraum-Änderungen;
     - a, verdächtige Fälle: alle 22 Einheiten in sonst nicht vergebenen PDFs, deren Zeitraum enger wurde, sich verschob oder
       neu entstand;
     - b: 5 PDFs;
     - c: 6 PDFs, dazu 6 mit vielen Teil-Änderungen und alle Dateien mit Dubletten.
6. **Zusammenführen** mit `methode/np5_zusammenfuehren.py`. Die Spalten sind wie in `funde_nachpruefung4.csv`.
   - `ist` ist der Stand 11:30, `neu_ist` der Stand 13:15.
   - Neue Zeilen tragen in der Bemerkung «Regel: a … u | nicht angekündigt | vor 11:30».
   - Fünf doppelt gemeldete neue Fehler (dieselbe Einheit aus zwei oder drei Gruppen) sind zusammengelegt; die behaltene Zeile
     nennt die anderen Gruppen. Die Bereinigung steht im Skript (`WEG`, `VERMERK`).
   - Doppelte Urteile derselben Einheit zählen einmal (38 Urteile).

## Ergebnis nach Auswahl

| Auswahl | behoben | teilweise | offen | schlechter | entfällt | Zeilen | davon PDF unverändert |
|---|---:|---:|---:|---:|---:|---:|---:|
| kritische Zeilen | 11 | 18 | 4 |  |  | 33 | 6 |
| «schlechter» aus Runde 4 |  | 3 |  |  |  | 3 |  |
| mittel/gering in geänderten PDFs | 19 | 34 | 112 | 3 |  | 168 |  |
| mittel/gering in unveränderten PDFs (übernommen) |  | 8 | 59 |  |  | 67 | 67 |
| **Summe** | **30** | **63** | **175** | **3** | **0** | **271** | **73** |

| Befund 11:30 | behoben | teilweise | offen | schlechter | Zeilen |
|---|---:|---:|---:|---:|---:|
| neu in Runde 4, kritisch | 10 | 5 |  |  | 15 |
| neu in Runde 4, mittel | 11 | 11 | 32 | 1 | 55 |
| neu in Runde 4, gering | 2 | 2 | 12 |  | 16 |
| teilweise, kritisch | 1 | 13 |  |  | 14 |
| teilweise, mittel |  | 20 | 1 | 1 | 22 |
| offen, kritisch |  |  | 4 |  | 4 |
| offen, mittel | 6 | 9 | 120 | 1 | 136 |
| offen, gering |  |  | 6 |  | 6 |
| schlechter, mittel |  | 3 |  |  | 3 |

## Bewusst offene Punkte (Auftrag 4) – bestätigt

Alle 11 Zeilen sind unverändert offen (4) bzw. teilweise (7).
- **D3828:**
  - Die Gliederung mit Nummern je Abschnitt ist unverändert. Neu sind nur die Teil-Nummern 2/3 der Mehrfachnennungen
    (Regel c) und Zeiträume.
  - 13. Teil 3 hat jetzt richtig 1912–1927, «o.D.» steht in der Anmerkung (Z81 behoben).
  - Neu verschlechtert: Über Regel b übernehmen die Erstnennungen auf S. 1–2 die Zeiträume der gleichnamigen Nummern späterer
    Abschnitte, z. B. :13. 1939–1945 → 1912–1945. Das ist als neue Zeile erfasst (Gruppe 4), obwohl die Ursache die bewusst
    offene Gliederung ist.
- **D3530:**
  - Nr. 3–63 stehen weiter als VII.327.:3.–:63. Die zweite «3.» ist jetzt Teil 2.
  - Neu falsch: Die Sammlung 1. hat «= 20.04.1999» aus dem Inventarvermerk (neue Zeile).
- **D141024, D149622, D3208, D2614:** Die Excel-Dateien sind inhaltlich unverändert.
- **D512:**
  - Struktur und Darin sind unverändert. Neu tragen 49 von 51 Saisons den Saison-Zeitraum aus dem Titel (Z186 behoben,
    Z157 teilweise).
  - Weiter falsch sind 1.8. und 1.19.:
    - 1.8. folgt dem PDF, das «28. Sept. 1964» in der Saison 1965/66 nennt.
    - 1.19. ist neu falsch, siehe unten.
  - Seit 13:15 stehen 8 Folgedaten der Einträge nirgends mehr im Import. Vorher steckten sie im falschen Saison-Zeitraum.
    Dadurch sinkt «Text erfasst» von 99,94 auf 99,87 %. Das gehört zu Z86 (Folgedaten fehlen im Eintrag).
- **D1739:** «Mappe mit Grossformaten» hat weiter keine eigene Einheit. Geändert hat sich nur die Zeitraum-Quelle von
  25 Schachteln; sie ist richtig.

Weitere bekannte offene Punkte:
- **Unverändert:**
  - Gruppen mit geschätzten Kinderzeiträumen: D10585 (PDF unverändert), D150589 und D2534 3.
  - «(n Schachteln)» ohne Umfang: 257 → 257 Einheiten.
  - D3466 «1924 / 25»: Der Datumsrest steht weiter in 210 Titeln.
  - D2951 1.22. «19./22. September» mitten im Titel.
  - D3672 1.1.1017.
  - D1880 a.–i.
  - D3060 S. 8.
  - D3105 «Band 1» und D150689 1.2.4. (beide PDFs unverändert).
  - D3018 S. 78.
- **Verändert:** D4175 1.C.1. hat neu 1805–1955 aus dem Jubiläumszeitraum (neue Zeile, Regel a).

## Regelstichprobe

| Regel | PDFs | besser | gleich | schlechter | unklar | geprüfte Einheiten |
|---|---:|---:|---:|---:|---:|---:|
| a | 80 | 254 | 33 | 55 | 10 | 352 |
| b | 20 | 21 | 3 | 22 | 2 | 48 |
| c | 28 | 24 | 17 | 10 |  | 51 |
| d | 1 | 13 | 4 | 1 |  | 18 |
| e | 1 | 2 | 1 |  |  | 3 |
| f | 1 | 2 |  |  |  | 2 |
| g | 3 | 3 | 1 |  |  | 4 |
| h | 2 | 2 | 1 |  |  | 3 |
| i | 18 | 21 | 3 | 6 |  | 30 |
| j | 2 | 3 | 16 | 6 |  | 25 |
| k | 14 | 25 | 1 | 3 |  | 29 |
| l | 1 | 7 |  |  |  | 7 |
| m | 3 | 1 | 1 | 1 |  | 3 |
| n | 26 | 59 | 4 | 2 |  | 65 |
| o | 1 | 2 |  |  |  | 2 |
| p | 2 | 2 | 2 |  |  | 4 |
| q | 1 | 6 |  |  |  | 6 |
| r | 1 | 23 | 2 |  |  | 25 |
| s | 4 | 11 | 3 |  |  | 14 |
| t | 1 | 37 | 1 | 5 |  | 43 |
| u | 3 | 23 |  | 13 | 2 | 38 |
| i/k | 1 | 1 |  |  |  | 1 |
| **Summe** | 150 | **542** | **93** | **124** | **14** | **773** |

### Regel a – Zeitraum aus dem Darin

**Was gut ist:**
- Die fünf Beispiele der Hauptsession stimmen:
  - D2979 8.x 1886–1928;
  - D3067 Schachtel 302 1943–1958;
  - D176060 16.2.3. 1988–2001;
  - D150589 1.6.3. nicht mehr verengt;
  - D408 5. 1860–1984.
- Rund 650 reine Quellen-Korrekturen «Darin (geschätzt)» → «Datumsspalte» sind richtig (Stichproben in D1924, D1739,
  D2901, D176151, D3828).
- Die meisten «weiter»-Fälle stimmen, z. B. D176795, D4175, D175994, D3057, D3628 4.1.2., D152810 VI.HO.D.5./D.8.
- Durch Regel a behoben sind 11 Zeilen, z. B. D512 (Saisons), D3828 13., D3067 III.E., D3063 5.3., D3077 16., D3089 I.3.b.,
  D176795 5., D408 5./8.

**Nebenwirkungen, nach Ursache:**
1. **Reine Jahreszeilen zu weit gefasst** (verarbeite Z. 2864–2865 mit `ist_reiner_zeitausdruck` Z. 575–577). Die Funktion
   streift Klammern und Satzzeichen ab. Deshalb gelten als Spaltendatum:
   - die Folgezeilen umbrochener Daten: D1180 20. «1976», D176367 7.1. «2006 – 2017», D3313 4. «1896», D9983 3.3.4.
     «– 1860», D149835 2., D2710 1, D9985 27.2.1.;
   - Satzenden in Klammern: D512 1.19. «1938 - 1945)», D3530 1. «20. April 1999)», D3718 4.2.13. «20. September 2010).»;
   - Titelreste: D3067 V.B. «seit 1401»;
   - allein stehende Dossiernummern: D151150 9. «1517».
   Ab der Hälfte der Zeilen trägt so ein Datum allein (Z. 2873), bei Gruppen sogar immer (Z. 3612–3615). Das Ergebnis ist ein
   falscher Zeitraum mit Quelle «Datumsspalte» bzw. «Untereinheiten», ohne Hinweis.
2. **Die Spalte ersetzt die Schätzung, statt sie zu erweitern** (ergaenze_zeitraeume Z. 3634–3640). Einträge, deren Datum
   nicht erkannt wird («1934*», «1984+1986», «85/88», «… Sch. 64», Daten im Text), fallen weg. Das betrifft 12 Fälle, darunter
   D867 8./32./41., D2894 3.1., D3429 1.2., D3063 3.4., D3718 4.2.15./4.2.19., D1746 XIV. und D3077 17. Die Schätzung von
   11:30 war dort richtig.
3. **Keine Rahmenprüfung auf dem Spaltenweg** (Z. 3637–3639). Die 150-Jahre-Regel und «nach heute» gelten hier nicht. Deshalb
   kommen falsche Jahre in den Zeitraum:
   - Plannummern: D3018 02.3.1.21. 1274–1330, 02.3.1.19. bis 2028;
   - Verweise auf andere Bestände: D67 III.Q.4. bis 1833, D69 III.R.1. bis 1806;
   - Lebensdaten und Jubiläen: D3063 1.9. ab 1882, D4175 1.C.1. 1805–1955;
   - Daten von Einheiten, die im Darin der vorigen stehen: D140969 7./10., D141 :75/:86.
4. **Gruppen nehmen die Spaltendaten des eigenen Darin als «sicher»** (Z. 3612–3615), ohne die Hälfte-Regel und ohne
   `eigen`. Die Quelle heisst dann «Untereinheiten», auch wenn die Kinder keinen Zeitraum haben (D3530 1., D3313 4.,
   D2850 A.). Tagesdaten werden dabei zum Jahr (D1877 2./2.1.).
5. **Ausdrückliche Titelzeiträume werden ohne Plausibilitätsprüfung erweitert** (zeitraum_aus_titel Z. 3566–3570,
   verarbeite Z. 2874–2878):
   - Tippfehler im PDF wirken: D2141 bis 1995 (aus «1995-1897», Beginn nach Ende), D3087 bis 1990, D2960 bis 1993, D9983 5.6.
     bis 03.1947.
   - Das Titeldatum bleibt dann im Titel (D3018 03.7.2., 04.2.1.).
   - Die Anmerkung nennt nur den Wortlaut der Titelzeile (Z. 2878). Sie widerspricht so in rund 320 Einheiten von/bis, z. B.
     D3067 III.E. 1891–1933 mit Anm «1912 – 1933», D141020 8.2. 1949–1975 mit Anm «1949 – 1960».
   - **Bitte entscheiden:** Soll ein ausdrücklicher Titelzeitraum überhaupt erweitert werden? Und soll das Titeldatum im Titel
     bleiben?
6. **Kleinere Folgen:**
   - «ca.» und «vor» gehen auf dem Spaltenweg verloren (Z. 3639): D3063 40.4., D176060 17.1., D3718 4.2.15.
   - Die Hälfte-Regel zählt physische Zeilen statt Einträge (Z. 2873). Deshalb bleiben D2979 8.5./8.7. falsch, und rund
     20 Einheiten bleiben «Darin (geschätzt)».

### Regel b – Teile im Zeitraum der Einheit

- **Richtig** bei Sammeltiteln, deren Teile Fortsetzungen sind: D4054 4.2. 1880–1987, 11.2.; D3509; D1877; D3484 :365.
- **Falsch**, wenn dieselbe Nummer im PDF verschiedene Einheiten bezeichnet (ergaenze_zeitraeume Z. 3671–3677):
  - Bücher einer Schachtel: D3589 ID 1 1939 → 1939–1982;
  - Objekte einer Locher-Nummer: D3484 :596. 1938 → 1933–1938, D3466 :124.;
  - eine zweite Ablieferung oder Doppel mit gleicher Signatur: D1343, D152390;
  - Zählung je Abschnitt oder je Schachtel: D3828, D1858;
  - Tippfehler-Signaturen nach Entscheid 5: D152810 VI.HO.C.25.:12/:13 (Testdatei).
- Das eigene Datum der ersten Nennung geht dabei oft verloren, und `ca=gesamt.ca` setzt «ca.» auch auf genau datierte
  Einheiten (D1343).
- Die Hinweise «Zeitraum weicht vom Inhaltsverzeichnis ab» werden vor der Erweiterung gesetzt (Z. 3592–3600) und sind danach
  überholt (D4054, D3874).

### Regel c – Teil-Nummern

- Explizite Nummern sind unverändert, es gibt keine Lücken. Die Mehrfach-Schlüssel sinken von 1'611 auf 69.
- **Rest:** 69 Dubletten und 33 Folgen, die nicht der PDF-Reihenfolge entsprechen:
  - Dubletten: D151210 49, D2681 10 (PDF unverändert, schon vor 11:30), D3357 4, D3231 2, D4054 2, D32837 1, D4057 1.
  - Ursache: `ergaenze_titel` beginnt die Zählung nach jedem Teil mit eigenem Titel wieder bei 2 (Z. 3749), Regel c
    (Z. 3759–3763) nummeriert nur die übrigen.
  - D151210 ist keine Nummerierung je Produktion. Rund 120 Produktionen tragen dort den Titel eines Nachbarteils, z. B. «Der
    Selbstmörder …, Teil 2» für «Die Gräfin von Rathenow». Das war schon vor 11:30 so; dieselbe Stelle betrifft D3231 und
    D3357.
  - D149628 23.2.1.: A ist Teil 3, die Fortsetzung Z ist Teil 2.

### Regeln d–h

Alle wirken nur dort, wo angekündigt, und korrigieren wie angekündigt:
- **d** D1880: «f. Heizamt» und f.I.–IV. als Hauptabteilung, D.III./G.III. der 3. Serie als Teil 3. Einzige Nebenwirkung:
  Serien ohne eigenes Datum bekommen nur den Zeitraum ihrer späteren Teile (D.III. 1938–1948, neue Zeile).
- **e** D3018 02.3.l.
- **f** D3089 XI.
- **g** D3253; nur 3 Zwischenüberschrift-Hinweise fielen weg, alle zu Recht.
- **h** D9983 5.6.; VII.191. ist unverändert.

### Regeln i–n

- **i (Doppelpunkt-Titelregel enger):** 21 besser, 6 schlechter. Die geprüften neuen Titel statt «[ohne Titel]» stimmen
  (5 der 9). Schlechter:
  - Listenköpfe mit Doppelpunkt, deren Einträge ein Spaltendatum haben: Die Ausnahme «Datum erst in der Folgezeile»
    (kopf_und_rumpf Z. 2659–2660) hängt den ersten Eintrag an den Titel. Das betrifft D3581 1.1. samt «Schachtel 1» und
    D867 5. Bei Untertiteln (D3271 3.4.2./3.4.3., D1237 2) ist es richtig.
  - D152781 3.3.: Die Ausnahme «Jahresbereich am Zeilenende» (Z. 2662) greift bei einem Buchtitel mit Lebensdaten.
  - D149628 23.1.1.836./907.: Der volle Werklisten-Titel ist länger als 160 Zeichen. `teile_langen_titel` (Z. 2686–2694) lässt
    nur den Komponisten stehen, und NAMENSGRENZE_RE (Z. 2516) trennt das Darin mitten im Ausdruck. Derselbe 160-Zeichen-Schnitt
    erklärt die übrigen Titel «…, in» (Z77, Z280).
- **j (kurze zweite Tabellenzeile):**
  - D3484 «Wasserkraftanlage» und rund 130 Titel in D3466 sind richtig.
  - In D3466 steht dadurch bei 16 Titeln der nicht erkannte Datumsrest mitten im Titel (Z316 schlechter), und 18 Titel enden
    auf «dito».
- **k (Namensliste mit mindestens 2 Einträgen):** 25 besser, 3 schlechter. D2951 1.22. hat wieder den eigenen Titel.
  Folgefehler:
  - D3647 5.4.: Mit dem jetzt richtigen Titel wird das Ereignis «1. Mai 1351» zum Zeitraum statt 1851. Die Rahmenprüfung
    gilt nur für das Darin.
  - D1395 15.1. Teil 5 erbt «Seeuntersuchungen: Zürichsee», im PDF steht Walensee (Z. 3754–3755).
- **l (Spaltenkopf «Sch.»):** sauber. Die 37 neuen Zeilen «Nicht übernommen» in D151150 sind genau die 37 allein stehenden «Sch.».
- **m (Hinweis «Nummer N kommt zweimal vor»):** D3484 595. stimmt. Falsch sind D2857 1.3. (gezählt wird nur `pfad[-1]`,
  Z. 3321–3342) und D408 1.2.1.
- **n (Titeldatum nach «19. /» bleibt im Titel):**
  - 66 von 76 Rest-Titeln sind jetzt vollständig.
  - Der Zeitraum enthält weiter nur das zweite Datum («19. / 20. April 1959» → 20.04.1959). In D438 stehen 77 Spaltendaten
    «Juni – August 1943» jetzt ganz im Titel, der Zeitraum ist nur der Endmonat (vor 11:30).
  - Das Muster greift zu weit: «ca.1890-1964» und «1920. - 1963» bleiben ganz im Titel (Z221 schlechter). Vorschlag:
    `(?<!\d)\d{1,2}\.\s?[/–-]`, ohne die blosse Alternative `[/–-]`.

### Regeln o–u

- **o** D3466 168., **p** D2558 3.: richtig. p wirkt sonst nirgends; alle 715 PDFs sind abgesucht.
- **q** D3271: 4.2.22., 6.2. und 6.6. sind Bereichsüberschriften. 6.2. und 6.6. waren nicht angekündigt, folgen aber aus
  derselben Regel und stimmen. «Nicht übernommen» 1 → 7 sind genau die 7 Zeilen, die jetzt nur im Prüfhinweis stehen. Die
  Behälterangabe «(1 grossformatige Schachtel)» steht nur dort.
- **r** D2534: 61 von 61 Schachteln stimmen, auch an allen Bereichsgrenzen. Ohne Schachtel bleiben nur die Unter-Einheiten
  2.3.1.–2.3.3. und 2.4.1.–2.4.4. (Z. 4780).
- **s** D49, D65, D67, D69: Nur die 11 leeren Doppel-Kategorien sind weg. Die Kategorie-Gruppen mit der Signatur ihrer
  einzigen Einheit bleiben (Z335, Z336, Z338 teilweise).
- **t** D3774:
  - Die Einleitung ist jetzt Vorspann (54 → 189 Zeilen), von S. 7–13 fehlt nichts. Die Abteilungen stehen oben, 25
    Unternummern sind Einheiten.
  - **Neu kritisch:** «5.3.Denkschrift …» und «6.4. ohne Datum …» sind keine Einheiten, ihr Text steht bei der Schwester 5.2.
    bzw. 6.3.
  - Weiter offen:
    - 2.4./2.5. stehen im Teil «2.38.»;
    - 2.31.–2.37., 2.41.–2.55., 3.51.–3.53. und 4.51.–4.54. sind nur Darin (lies_signatur Z. 1048–1061 verlangt erstes Kind
      oder nächste Nummer);
    - falsche Zeiträume: VII.47.1. 1843–1922 aus der Übersichtszeile, :3. endet 1858;
    - bei 2.2., 4.1. und 6.1. ist die Grenze zwischen Titel und Darin falsch.
- **u** Fussnoten:
  - In D10675 stehen alle 27 Fussnoten bei der Einheit mit dem Zeichen (Z260 behoben).
  - In D10744 (8 von 9) und D151217 (2 von 2) landen sie bei der letzten Einheit der Seite. Die Zeichen sind dort 8,0 bzw.
    9,1 pt gross, `hat_zeichen` (Z. 1861–1866) erkennt nur bis 7,5 pt.
  - In D10675 liefert der Fussnotentext jetzt Zeiträume (Z. 3643–3646): 700.5 und 715.18 «= 09.11.2010» (Abrufdatum einer
    Webquelle), 701.50.9 «1898–06.1992». Die Gruppen erben das, dazu 65 neue Hinweise «Kein Zeitraum gefunden.».
  - Vorschlag: Einträge «Fussnote n:» aus der Schätzung nehmen.

## Gesamtabgleiche (Auftrag 3)

- **Bestandssignaturen:** Kein Feld «Bestand» hat sich geändert. Der Abgleich mit dem PDF-Kopf zeigt dieselben 23 bekannten
  Erkennungsartefakte wie um 11:30.
- **«Nicht übernommen»:** insgesamt 2'108 → 2'089 Zeilen.
  - Gestiegen: D151150 0 → 37 (Regel l, nur «Sch.») und D3271 1 → 7 (Regel q).
  - Gesunken: D10675 43 → 2, D10744 23 → 12, D151217 3 → 0 (Regel u), D1880 3 → 0, D3774 3 → 0, D3253 25 → 24.
  - Kein Textverlust.
- **«Text erfasst»:**
  - Gesunken nur in D512 (99,94 → 99,87 %, 8 Folgedaten, siehe oben) und D152817 (100 → 99,98 %). In D152817
    VI.SB.D.7.:1-2 löscht der erweiterte Spaltenzeitraum das Datum «1841-1932» eines Untereintrags (neue Zeile, Regel a).
  - Gestiegen in D3828 (99,96 → 100 %, «o.D.» jetzt in der Anmerkung).
- **Text, der nirgends mehr vorkommt** (`textverlust.csv`, 101 Treffer):
  - 84 in D3774, nur die Einleitung, die jetzt Vorspann ist.
  - Die übrigen sind Umbauten nach i/j/n/o/r/s; Verlust nur bei D149628 23.1.1.836./907. (Regel i, siehe oben).
- **Einheitenzahl:**
  - −3 insgesamt: entfernt 46 (D1880 11, D3774 12, D2534 7, D49/D65/D67/D69 11, D3271 3, D3018 1, D3089 1), neu 43 (D3774 25,
    D1880 16, D2558 1, D3466 1).
  - Alle Zu- und Abgänge sind am PDF geprüft und entsprechen den Regeln d, e, f, o, p, q, r, s und t.
- **«[ohne Titel]»:** 44 → 35. Die neun neuen Titel kommen aus Regel i; geprüft sind D175949 Q, D2921 3., D3587 1. und
  D8952 2/7, alle richtig.
- **Doppelte Schlüssel:** 1'611 → 69, also 4'327 → 80 überzählige Zeilen (siehe Regel c).
- **Prüfhinweise:**
  - Weggefallen: 700 × «Zeitraum aus den Jahreszahlen im Darin geschätzt» (106 PDFs) und 187 × «Untereinheiten reichen über
    den Zeitraum hinaus».
  - Neu: 72 × «Kein Zeitraum gefunden.» (65 in D10675, Regel u), 61 × «Schachtel aus der Aufteilung …» (D2534), 10 ×
    «Fussnote … ohne erkennbares Zeichen» und 3 × «Nummer N kommt zweimal vor».

## Neue Fehler am Stand 13:15, nach vermutlicher Ursache

| Vermutliche Ursache (Regel) | kritisch | mittel | gering | Zeilen |
|---|---:|---:|---:|---:|
| a |  | 30 | 4 | 34 |
| b |  | 7 | 1 | 8 |
| c |  |  | 1 | 1 |
| d |  | 1 |  | 1 |
| i |  | 3 |  | 3 |
| j |  |  | 1 | 1 |
| k |  | 2 |  | 2 |
| m |  |  | 1 | 1 |
| q |  |  | 1 | 1 |
| t | 1 | 3 |  | 4 |
| u |  | 3 |  | 3 |
| nicht angekündigt |  |  |  | 0 |
| vor 11:30 | 10 | 33 |  | 43 |
| **Summe** | **11** | **82** | **9** | **102** |

Für die Regeln e, f, g, h, l, n, o, p, r und s gibt es keine neue Zeile. Zu n sind die Folgen in Z221 erfasst, zu j in
Z316.

**Aus Regel a (34):**
- reine Jahreszeilen:
  - D512 1.19., D3530 1., D151150 9.;
  - D1180 20., D176367 7.1., D3313 4.;
  - D149835 2., D2710 1, D9985 27.2.1.;
  - D9983 3.3.4., D3718 4.2.13.;
- zu eng: D867 8./32./41. mit D2894 und D149888, D3063 3.4., D1746 XIV., D3718 4.2.15./4.2.19., D3077 17., D3429 1.2.,
  D141020 8.2./12. (Anmerkung);
- Plannummern, Verweise und fremde Jahre:
  - D3018 02.3.1.21./22., D3018 06.7.5.;
  - D67, D69;
  - D3063 1.9., D4175 1.C.1.;
  - D140969 7./10., D141 :75/:86, D3089 X. (Jahr eines Textbuchs, das im Darin von X. steht);
- Tippfehler im Titelzeitraum: D2141 mit D3087 und D2960, D9983 5.6.;
- Sonstiges: D152817 1-2, D1877 2.1., D3063 40.4. («ca.»), D3067 III.E. (Anmerkungen, rund 320 Fälle), D4054 12.3.4.
  («… siehe auch»).

**Aus Regel b (8):** D3589, D3484, D3466, D1343, D152390, D3828, D152810, D4054 (überholte Hinweise).

**Übrige Regeln:**
- **t (4):** D3774 5.3./6.4. (kritisch), VII.47.1., :3., 2.2./4.1./6.1.
- **u (3):** D10675 Zeiträume aus Fussnoten, D10744 und D151217 Zuordnung.
- **i (3):** D3581 1.1. mit D867 5., D152781 3.3., D149628 23.1.1.836./907.
- **k (2):** D3647 5.4., D1395 15.1. Teil 5.
- **c (1):** D149628 23.2.1., Reihenfolge.
- **d (1):** D1880 D.III.
- **j (1):** D3466 «dito».
- **m (1):** D408 1.2.1.
- **q (1):** D3271 6.2./6.6.

### Schon um 11:30 vorhanden, jetzt erst erfasst (43 Zeilen, 10 kritisch)

**Kritisch:**
- D141: 26 Einheiten fehlen («V.A. c.115.: 76» mit Leerzeichen nach dem Doppelpunkt wird nicht als Signatur gelesen). Sie
  stehen im Darin von :75 bzw. :86.
- D140969: «3:1–3», «8:1–3» und «11 : 1 – 2» fehlen.
- D151150 «10.5..2.» (doppelter Punkt) fehlt und steht im Darin von 10.5.1.
- D442: Das zweite «26. Tätigkeitsberichte» (Tippfehler für 26.2.) ist keine eigene Einheit (Entscheid 5).
- D631: «B 998 / 1942» aus einer Liste von Stadtratsbeschlüssen wird zur einzigen Einheit; 32 Zeilen sind «Nicht übernommen»,
  trotzdem zeigt «Text erfasst» 100 %.
- D1858: Die Positionen 1.–7. zählen je Schachtel neu und werden zu Signaturen mit bis zu 20 Teilen.
- D3808, D3874, D4057, D8949: Signaturen sind aus Zahlen im Text erfunden.

**Mittel, u. a.:**
- D151210, D3231, D3357: Teile tragen den Titel des Nachbarteils.
- D2681: Dubletten.
- D438: Der Zeitraum ist nur der Endmonat.
- D3089: Schlussvermerk und Daten der Bibliotheksberichte im Darin bzw. in der Anmerkung von X.
- D3774 VII.47.1. ff.
- D49, D67, D69: Kategorie-Gruppen.
- D3271 6.2./6.6./7.
- D150589 1.6.3. «= 1985».
- D176060 16.2.3.
- D2979 6.1./6.2./7.1.
- D3253 1.1.
- D3225 9., D4058 19.13.1., D3133, D32837, D8952 5, D1180 11.3., D152781 5.1./3.1., D140969 14./15./17., D176795 2.3.9.3.,
  D3429 1.1.

## Nach Hauptmuster

| Hauptmuster | behoben | teilweise | offen | schlechter | neu |
|---|---:|---:|---:|---:|---:|
| M01 Vorspann/Schlussvermerk verworfen | 1 | 6 | 3 |  |  |
| M02 Echte Signatur nicht erkannt | 4 |  | 2 |  | 6 (5 krit.) |
| M03 Zahl/Marke als Signatur | 3 | 4 |  |  | 5 (5 krit.) |
| M04 Gliederungsebene nicht erkannt | 1 | 3 | 2 |  | 1 (1 krit.) |
| M05 Mehrzeilige Datumsspalte | 4 | 7 | 12 |  | 3 |
| M06 Rechte Spalte nicht abgetrennt |  | 3 | 20 |  | 8 |
| M07 Fremdtext im Darin | 1 | 1 | 25 |  | 8 |
| M08 Zeilenumbruch falsch | 4 | 7 | 13 |  | 4 |
| M09 Zeitraum aus falscher Quelle | 5 | 11 | 32 | 1 | 41 |
| M10 Darin falsch getrennt |  | 2 | 18 |  | 1 |
| M11 Schachtel-Nr. |  | 2 | 20 |  | 1 |
| M12 Datumsformat nicht erkannt | 1 | 7 | 9 | 2 | 4 |
| M13 Teile: Titel vom Nachbarteil |  |  |  |  | 4 |
| M14 Mappen/Schachteln: Titel aus Überschrift |  |  | 2 |  | 1 |
| M15 Umfang |  |  | 2 |  | 1 |
| M16 Zerrissene Wörter |  |  | 1 |  |  |
| M17 Kosmetik | 1 |  | 8 |  | 5 |
| M19 Sonstiges | 5 | 10 | 6 |  | 9 |

## PDFs mit kritischen offenen oder neuen Fehlern

| PDF | kritisch offen/teilw./schlechter | neu kritisch | behoben | teilweise | offen | schlechter | neu |
|---|---:|---:|---:|---:|---:|---:|---:|
| D3828 | 3 | 0 | 1 | 1 | 2 |  | 1 |
| D3530 | 2 | 0 |  | 1 | 2 |  | 1 |
| D3774 | 1 | 1 |  | 2 |  |  | 6 |
| D140969 | 0 | 1 |  |  | 1 |  | 3 |
| D141 | 0 | 1 |  |  | 1 |  | 2 |
| D141024 | 1 | 0 |  | 1 |  |  |  |
| D149622 | 1 | 0 |  | 1 |  |  |  |
| D150689 | 1 | 0 |  | 2 | 7 |  |  |
| D151150 | 0 | 1 | 2 |  |  |  | 2 |
| D1739 | 1 | 0 |  |  | 1 |  |  |
| D1858 | 0 | 1 |  |  |  |  | 1 |
| D1880 | 1 | 0 | 2 | 1 | 2 |  | 1 |
| D2614 | 1 | 0 |  | 1 |  |  |  |
| D3018 | 1 | 0 | 1 | 2 | 6 | 2 | 3 |
| D3060 | 1 | 0 |  | 1 | 3 |  |  |
| D3089 | 1 | 0 | 2 | 2 | 5 |  | 3 |
| D3105 | 1 | 0 |  | 1 |  |  |  |
| D3208 | 1 | 0 |  | 2 |  |  |  |
| D3271 | 1 | 0 | 1 | 2 | 1 |  | 4 |
| D3808 | 0 | 1 |  |  |  |  | 1 |
| D3874 | 0 | 1 |  |  |  |  | 1 |
| D4057 | 0 | 1 |  |  |  |  | 1 |
| D442 | 0 | 1 |  |  | 2 |  | 1 |
| D512 | 1 | 0 | 1 | 2 | 1 |  | 1 |
| D631 | 0 | 1 |  |  |  |  | 1 |
| D65 | 1 | 0 |  | 1 |  |  |  |
| D67 | 1 | 0 |  | 1 | 1 |  | 2 |
| D69 | 1 | 0 |  | 1 |  |  | 2 |
| D8949 | 0 | 1 |  |  |  |  | 1 |

## Wichtigste offene Punkte

Die Zeilennummern beziehen sich auf `…/scratchpad/neu5/findmittel_zu_scope.py`.
1. **Regel a nachschärfen.**
   - Als reine Jahreszeile nur zählen, was in der Datumsspalte steht (x-Position) und keine Folgezeile eines Satzes oder eines
     umbrochenen Datums ist. `strip("()")` gehört nicht in `ist_reiner_zeitausdruck` (Z. 575–577). Zahlen ohne Text in
     Nummernspalten («1517») ausschliessen.
   - Den Rahmen (150 Jahre, «nach heute») auch auf den Spaltenweg anwenden (Z. 3637–3639).
   - Die Schätzung aus dem Text nicht verwerfen, sondern vereinigen oder mit Hinweis behalten (Z. 3634–3640, Z. 3612–3615).
   - Bei Gruppen die Hälfte-Regel verlangen und die Quelle nicht «Untereinheiten» nennen, wenn der Zeitraum aus dem eigenen
     Darin kommt.
   - Zeilen mit «siehe», «vgl.», «Fortsetzung», «eingegliedert» und «Fussnote n:» nicht mitzählen.
   - **Zu entscheiden:** Ausdrückliche Titelzeiträume erweitern oder nicht? Titeldatum im Titel lassen? Anmerkung mit welchem
     Wortlaut (heute oft enger als von/bis, rund 320 Fälle)?
2. **Regel b** nur bei gleichem Titel bzw. Objekt anwenden (Z. 3671–3677), nicht bei Tippfehler-Teilen, Zählung je
   Abschnitt oder Schachtel und verschiedenen Objekten derselben Nummer. Das eigene Datum gehört in die Anmerkung, «ca.» nicht
   übertragen, den Inhaltsverzeichnis-Vergleich danach machen.
3. **Regel u:** Das Zeichen relativ zur Schriftgrösse der Nachbarwörter erkennen statt fest ≤ 7,5 pt (Z. 1861–1866), auch auf
   der Vorseite suchen. Den Fussnotentext von der Zeitraum-Schätzung ausnehmen.
4. **Regel t / D3774:** Unternummern der Textspalte ohne die Bedingung «erstes Kind oder nächste Nummer» und ohne grosses
   Folgewort annehmen (Z. 1048–1061), auch nach Teilen (Z. 1888–1890). Sonst fehlen 5.3., 6.4. und die Sprünge.
5. **Regel c / Teile:** Die Zählung in `ergaenze_titel` nicht nach jedem Teil mit eigenem Titel neu beginnen (Z. 3749).
   Titel nicht vom Nachbarteil übernehmen (D151210 rund 120, D3231, D3357; vor 11:30).
6. **Regel i:** Die Ausnahme «Datum erst in der Folgezeile» nur bei einem Untertitel anwenden, nicht bei Listen mit
   Datumsspalte (D3581, D867). `teile_langen_titel` nicht bei Werklisten und «in:» anwenden.
7. **Regel n:** Das Muster einengen (Z221). Den Anfang eines Doppeldatums mit Monat und Jahr des Endes ergänzen
   («19. / 20. April 1959» → 19.–20.04.1959, D438 «Juni – August 1943»).
8. **Alte kritische Fehler:**
   - Signaturen mit Leerzeichen nach dem Doppelpunkt (D141) und mit doppeltem Punkt (D151150 «10.5..2.»).
   - Wiederholte Nummer als Tippfehler (D442).
   - Erfundene Signaturen aus Zahlen im Text (D631, D3808, D3874, D4057, D8949).
   - Zählung je Schachtel (D1858) und D140969.
9. **Bewusst offen** wie besprochen: D3828, D3530, D141024, D512, D149622, D3208, D2614, D1739.

## Dateien

- `stichproben/nachpruefung5.md` – dieser Bericht.
- `stichproben/funde_nachpruefung5.csv`:
  - 373 Zeilen: 271 nachgeprüft (in der Reihenfolge von `methode/np5_pruefliste.csv`), 102 neu.
  - Spalten `pdf;seite;signatur;feld;schwere;soll;ist;bemerkung;status;neu_ist`.
  - `ist` = Stand 11:30, `neu_ist` = Stand 13:15. Status behoben / teilweise / offen / schlechter / neu.
- `stichproben/methode/`: `ANLEITUNG_NACHPRUEFUNG5.md`, `np5_auswahl.py`, `np5_pruefliste.csv`, `np5_geaendert.txt`,
  `np5_zusammenfuehren.py`.
- `stichproben/roh/`: `np5_vorbewertet.csv`, `np5_gruppe_0.csv` … `np5_gruppe_6.csv`, je mit `_regeln.csv` (zusammen
  811 Urteile, 773 nach Zusammenlegung) und `_notizen.md`.
- Vergleichsergebnisse im Scratchpad unter `…/np5/`:
  - `diff/`, `diff_test/`, `hinweise/`;
  - `familien.csv`, `regelart.csv`, `zeitraum.csv`, `textverlust.csv`, `teile.json`, `titel_angehaengt.csv`;
  - `gesamt.json`, `zaehlung.json`, `skript.diff`.
