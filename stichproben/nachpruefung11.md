# Nachprüfung 11: Nachträge 1 und 2 der Runde 8 und die 430 nie angesehenen Dateien (22.11.2026)

Geprüft sind zwei Stände:
- **Nachtrag 1:** Skript `efe92c5f…`, gegen 7fa7e161.
- **Nachtrag 2:** Skript `bb4c958822bb50a3…`, gegen efe92c5f. Das ist der Stand jetzt im Projekt.

Dazu kommt die **erste Prüfung aller 430 Dateien, die noch niemand am PDF angesehen hatte**.

Die Ergebnisse stehen hier:
- `offen_kritisch.csv`: nachgeführt, 65 Zeilen mit stabilen K-Nummern;
- `funde_nachpruefung11.csv`: 375 Zeilen;
- Rohdaten in `roh/np11_*`;
- Methode in `methode/ANLEITUNG_NACHPRUEFUNG11.md` und `methode/np11_*.py`.

## Kurz

- **Die Nachträge wirken.** Von den 52 Zeilen, die beide Nachträge beheben sollten (24 «in Arbeit», 28 offen), sind 48
  erledigt: behoben oder nur noch mit mittlerem Rest.
  - Kritisch bleiben 4:
    - K8 D177460: «I.1:3» und «P2:10» fehlen.
    - K29 D3898: «Ledermesse Zürich …» im Darin von 110.
    - K3/K4 D149825: Stücke ohne Nummer im Darin fremder Einheiten.
  - Durch die Nachträge schlechter sind nur mittlere und geringe Dinge, z. B. Zeiträume in D177460 F und 11 unnötig
    umgeschriebene Signaturen in D3470 durch Regel 45.
- **Die Erstprüfung der 430 Dateien findet viel.**
  - **43 Dateien (10 %, 95%-KI 8–13 %) haben einen kritischen Fehler**, alle schon vor Runde 8.
  - Am häufigsten:
    - Schlusstext nach der letzten Einheit im Darin der letzten Einheit;
    - eine einzige Bestandszeile, die die Einheiten verschluckt;
    - Signaturen, die nicht als Einheit erkannt werden.
  - Die Warnzeichen der Prüfmappen fanden fast keinen dieser Fehler; gefunden haben sie die Prüfer am Inhalt.
- **Offene kritische Fehler** (`offen_kritisch.csv`, Stand bb4c9588): 65 Zeilen in 59 Dateien.
  - 48 Zeilen sind offen und niemandem zugeteilt, darunter 46 neue aus dieser Nachprüfung.
  - 7 Zeilen warten auf einen **Konventionsentscheid «Stück ohne Nummer»** (Regel 50).
  - 10 Zeilen sind bewusst offen, darunter neu D3190 und D3894 aus `runde7/AENDERUNGEN_RUNDE7.md`.
- **Abdeckung:** Jede der 715 Dateien hat jetzt jemand angesehen.
  - Ganz auf kritische Fehler geprüft sind 507: NP10 (Stichprobe und Erstprüfungen) und NP11 (430 Dateien, D260).
  - **208 Dateien mit 34'915 Einheiten (69 % aller Einheiten) sind nur teilweise geprüft**, in früheren Runden mit
    anderem Schwerpunkt (`roh/np11_teilweise_geprueft.txt`).
  - Bevor die Aussage «keine kritischen Fehler» möglich ist, braucht es für sie noch einen Durchgang mit Prüfmappen.

## Stände und Nachrechnung

| Stand | Lauf zellgleich | geändert gegenüber vorher | Einheiten | Fallsets |
|---|---|---|---:|---|
| efe92c5f (Nachtrag 1) | ja, auch Testdaten und D151210 | 14 Dateien + Testdaten D177460 | 50'902 | gleich; B: nur ID-Verschiebung D2960 |
| bb4c9588 (Nachtrag 2) | ja, auch Testdaten und D151210 | 32 Dateien | 50'935 | Runde 2 31 → 30 (D2853) |

- Weitere Kennzahlen bei bb4c9588: «[ohne Titel]» 33, Text erfasst 100 % 695, doppelte Schlüssel 10.
- **Fallset Runde 2 angepasst:** D2853 hat jetzt 8 Einheiten statt 14, das Soll aus NP10.
  - Die Zeile in `verbesserung/runde2/werkzeug/runde2_faelle.csv` sagt jetzt «Einheiten = 8».
  - Damit stehen die Fallsets wieder bei 31/34.

## Nachtrag 1 (Paket N1, 14 Dateien)

- **Urteile:** Fast alle der 664 geänderten Einheiten sind besser. Schlechter sind nur:
  - D177460 F 2 und F: Zeitraum «bis 2014» wird zu 1965 bzw. 1993, weil das Jahr in Klammern nicht gelesen wird (mittel).
  - D175827: von 8 geänderten Darin-Verbindungen sind 4 schlechter (gering).
  - D3170 7.2.2.: Hinweis «Nummerierung beginnt bei 2.» (gering).
- **24 Zeilen «in Arbeit»:** 22 behoben.
  - **K8 D177460:** Im PDF stehen 431 Zeilen «X n:m», das sind 430 Signaturen, weil «E 1:2» doppelt steht. In der Excel sind
    es 429 Einheiten. Es fehlen «I.1:3» (im Darin von I 1:2) und «P2:10» (im Darin von P 2:9). Die Eltern aller 429 stimmen.
  - **K15 D2828:** Das Mindest-Soll ist erfüllt: Der Anhang steht ganz im Blatt Info, 30. ist leer, 32. ist Einheit. Die
    Regesten «in 17.6.»/«in 18.» zusätzlich ins Darin dieser Einheiten wäre besser (mittel).
- **D260 (Erstprüfung):** Alle 120 Einheiten stimmen. «Schachtel II.» mit Inhalt steht seit Nachtrag 2 mit Hinweis im Darin
  von :120; das ist ein Fall für den Konventionsentscheid (K106).
- **D3472 «1967.18» S. 41:** Seit Nachtrag 2 ist das die eigene Einheit 1969.18 mit Hinweis; erledigt.
- **Neu kritisch:** D3170 (K107). «6.1.3.4.» steht auf S. 16 zweimal. Die erste Zeile («1974/75») geht als Übersichtszeile
  verloren, die zweite (eigentlich 6.1.4.4.) hängt unter 6.1.3.

## Nachtrag 2 (Paket N2, 32 Dateien)

- **Urteile:** Die Regeln 37–44 und 46–49 sind durchweg besser.
  - D2853 hat 8 von 8 Einheiten wie die Soll-Liste.
  - D175949 hat alle 25 Unternummern A.1–Q.1.
  - Regel 45 (Jahr-Tippfehler) ist in D3468 und D3472 besser. In D3470 schreibt sie aber 11 Signaturen um, obwohl die
    Laufnummern durchlaufen und nichts kollidiert (mittel; Vorschlag: nur bei Kollision).
  - Regel 50 setzt den Hinweis «Nach der letzten Einheit … ein Absatz ohne Signatur» in 13 Dateien. 12 Hinweise sind
    berechtigt, D109666 ist ein Fehlalarm. Der Hinweis selbst behebt nichts: In D2931, D175454 und D1759 bleibt der Fund
    kritisch (K108–K110).
- **28 offene K-Zeilen:** 22 behoben, bei K7, K10 und K23 ist der Rest nur noch mittel. Kritisch bleiben K3, K4 (D149825)
  und K29: D3898 «Ledermesse Zürich, Stempel für die Lederballen» steht noch im Darin von 110.
- **Deine zwei Entscheide:**
  - **D149825 K3/K4 ist so nicht vertretbar.** Der Hinweis steht nur in einer Hilfsspalte, importiert wird fremder Inhalt:
    der Protokollband 1872–1886 bei Nr. 1, der Pokal beim Neujahrsblatt 1985. Ohne erfundene Signatur ginge es so: die
    Stücke ohne Nummer ins Darin einer Bestandszeile, wie bei Regel 48.
    → Konventionsentscheid, siehe unten.
  - **D8947 ist vertretbar** und entspricht dem NP10-Soll.
- **Nebenwirkungen:** D3896 (Ortsüberschriften), D4173 («ALFRED») und D49/D67 («e) Akten (keine)») sind richtig.
- **Neu kritisch, alle schon vor Nachtrag 2:**
  - D150689 9.2. (K111): Literaturverzeichnis S. 198–201 und Schlussvermerk im Darin, der Zeitraum bis 1996 wird auf 9.
    vererbt.
  - D3324 12. (K112): Anhang «Heinrich Wehrli: Biografisches».
  - D3943 X.G.219. (K113): vier Stücke «Keine Nr.».

## Erstprüfung der 430 nie angesehenen Dateien (Pakete E1–E10)

**Umfang:** 430 Dateien, 9'785 Einheiten, am Stand efe92c5f.
- Jede Datei ist ganz über ihre Prüfmappe geprüft, bei Zweifeln am PDF.
- Grosse Dateien sind zusätzlich per Skript auf Struktur geprüft (z. B. D150829 mit 518 Einheiten).
- Die 5 Dateien, die Nachtrag 2 nochmals geändert hat, hat N2 am Stand bb4c9588 nachgeprüft.

| Paket | Dateien | kritisch |
|---|---:|---|
| E1 | 40 | 1: D175561 |
| E2 | 42 | 5: D1473, D3190 (bewusst offen), D176868, D1686, D151194 |
| E3 | 42 | 2: D144909, D152398 |
| E4 | 43 | 3: D1726, D3894 (bewusst offen), D3816 |
| E5 | 43 | 3: D2931, D185, D1479 (D3896 durch Nachtrag 2 behoben) |
| E6 | 44 | 4: D2733, D3503, D3343, D403 |
| E7 | 44 | 4: D2848, D3542, D1263, D2372 |
| E8 | 43 | 9: D1391, D3277, D3557, D150536, D175454, D3677, D3026, D2759, D149867 |
| E9 | 44 | 5: D2947, D1759, D2923, D2940, D3563 |
| E10 | 45 | 7: D1261, D2123, D2127, D3702, D3390, D3186, D2643 |

**Muster der kritischen Funde:**
1. **Schlusstext im Darin der letzten Einheit** (rund 17 Fälle).
   - Literatur, Verweise auf andere Bestände, Bemerkungen zum Bestand, Bestandsgeschichte und Kopier- oder Druckvermerke
     ohne Überschrift «Anhang» landen im Darin der letzten Einheit. Oft erbt diese dadurch einen falschen Zeitraum.
   - Beispiele: D2947, D3702, D150536, D150689, D3677, D3324, D175454, D3390, D2733, D3503, D144909, D2848, D3542, D1759,
     D3563.
   - Eine einzelne Schlussnotiz mit Datum oder Kürzel gilt nur als mittel.
2. **Eine einzige Bestandszeile verschluckt die Einheiten** (Findmittel fälschlich «ohne Signaturen»).
   - Die Signaturen sind leicht anders geschrieben: D1261, D1263, D1686, z. B. «V.F. b.13.c:1» ohne Punkt vor «:».
   - Oder die Tabelle hat eine Spalte, die das Skript nicht erkennt:
     - «Schachtel-Nummer»: D2123 (36 Schachteln), D2127, D2372;
     - «Mappe»: D2759;
     - «Schachtel(n)»: D3026, 258 Einträge auf 70 Schachteln;
     - «Nummer Jahrgang Titel»: D176868 (26 Einheiten).
3. **Signaturen werden nicht als Einheit erkannt:**
   - In der Signaturspalte steht nur der Bestand: D175561 (1.–22.), D151194 (a)–f)), D2931 («VII. 138. Fotografien»).
   - Die Nr.-Spalte läuft über die Schachteln durch: D1391 (1.–14.). Laut Suchlauf ist das im Korpus nur diese Datei.
   - Die Einheiten stehen nur im Darin ihrer Gruppen: D149867 (1–164 unter I.–XIII.).
   - Die eigentlichen Einheiten stehen im Darin, weil Beschreibungsabschnitte zu Einheiten werden: D2923 (Schachteln 1–4
     im Darin von 3.).
4. **Eltern oder Ebene falsch:**
   - D403: a)/b) gehören unter 1.
   - D3816: 18.a ist Kind von 18. statt Geschwister.
   - D185: «0. Grundlagen» fehlt.
   - D1473, D1479: Tippfehler in Bandfolgen machen eine Einheit zum Teil einer anderen.
5. **Erfundene Einheiten:**
   - D152398: aus der Vorbemerkung «1.»/«2.».
   - D2940: aus der Anzahl «2 Handwerkskundschaften».
   - D3343: die alphabetische Zweitfassung derselben Liste als Teil 2.
6. **Weitere:**
   - D3542: Spalte Assekuranznummern, «I - LXV» fehlt, «I - XIX» bei 11. statt 12.
   - D3702: Beschreibung der Gruppe 2.8.–9. im Darin von 2.7.
   - D3186: wiederholte «10. Varia» im Darin statt als Teil.
   - D2643: Inhaltsangaben stehen nur in der Übersicht.

**Vom Prüfer gemeldet, von mir herabgestuft (mittel):**
- D2516: Nummern im Fliesstext, Konventionsfrage.
- D3767 37.: Die Beilagen gehören zum Album.
- D3271 4.2.9.: Registerzeile im Titel, Grenzfall.

## Konventionsentscheid «Stück ohne Nummer» (Regel 50)

Die Fälle: D149825 K3/K4, D3943 K113, D260 K106, D3277 K93 («Grossformate»), D3557 K95 («Reproduktionen (Beilage)»), D1726 K77
(nur im Blatt Info) und D3826 K43 (bewusst offen).

Es gibt drei Möglichkeiten:
- (a) eigene Einheit mit einer Signatur nach Konvention;
- (b) Darin einer Bestandszeile (wie Regel 48);
- (c) Darin der Nachbareinheit mit Hinweis.

(c) ist heute umgesetzt, importiert aber fremden Inhalt bei einer fremden Einheit. Nach der Schwere-Regel ist das kritisch.
**Das sollte der Nutzer entscheiden.** Bis dahin bleiben die Fälle kritisch.

## Vorschläge für Runde 9

1. **Schlussblock ohne «Anhang»:** Nach der letzten Signatur der Folge ist ein abgesetzter Block Schlussblock (Blatt Info),
   wenn er durch eine Überschrift oder einen grossen Abstand abgetrennt ist. Überschriften sind fett, grösser oder mit
   Doppelpunkt: «Literatur», «Bemerkungen», «Verweise», «Quellen», «Beilage», «Anmerkungen».
   - Gilt auch für Kopier- oder Druckvermerke.
   - Den Zeitraum der letzten Einheit nicht aus diesem Block schätzen.
2. **Vor «ohne Signaturen» prüfen:**
   - ob Signaturen der Form «Bestand:n» ohne Punkt vor «:» vorkommen;
   - ob der Tabellenkopf eine Spalte «Schachtel(-Nr./-Nummer)», «Mappe», «Nummer» oder «Nr.» hat. Dann Einheiten je Zeile
     bzw. je Schachtel.
3. **Signaturspalte mit blossem Bestand:** Die Nummern oder Buchstaben in der Inhaltsspalte sind die Einheiten. Durchlaufende
   Nr. über Schachteln sind Signaturen.
4. **Tippfehler in Bandfolgen** wie bei Jahr.Laufnummer: Kommt die gleiche Signatur zweimal und passen die Nachbarn zur Folge,
   ist das eine eigene Einheit mit Hinweis (D1473, D1479). Regel 45 nur bei Kollision anwenden (D3470).
5. **Einzelfälle:**
   - K8: Formen «I.1:3», «P2:10».
   - K29: «Ledermesse».
   - D3170: doppelte «6.1.3.4.»; die Übersichtszeilen-Regel verwirft hier eine echte Zeile.
   - D3186: «10. Varia» als Teil.
   - D403, D3816, D185, D149867, D2923, D152398, D2940, D3343: siehe Soll in `offen_kritisch.csv`.

## Nächste Nachprüfung (NP12)

- Gegenprüfung der Runde 9.
- Danach der **Durchgang über die 208 nur teilweise geprüften Dateien** mit Prüfmappen (`methode/np11_pruefmappe.py`), am
  besten in etwa 10 Paketen.
  - Grosse Dateien zusätzlich per Strukturskript.
  - Die Rate der Erstprüfung (10 %) spricht dafür, dass auch dort noch kritische Fehler stecken.

## Dateien

- `offen_kritisch.csv`: 65 Zeilen.
  - K-Nummern wie bisher; neu sind K61–K113.
  - Erledigt und deshalb entfernt sind 48 Zeilen; die Liste davor liegt in `roh/np10_offen_kritisch_mit_nachtrag.csv`.
  - Die Spalte `entscheid` nennt Herabstufungen und Konventionsfälle.
- `funde_nachpruefung11.csv`: alle Funde aus N1, N2 und E1–E10, mit `paket`, `k_alt` und `entscheid`. Der Status «ersetzt»
  heisst, dass N2 den E-Fund am neuen Stand nachgeprüft hat.
- `roh/np11_dateien_urteil.csv`: Urteil je Datei.
- `roh/np11_<Paket>_*`: die Ausgaben der Pakete.
- `roh/np11_vgl_nachtrag1/`, `roh/np11_vgl_nachtrag2/`: die Vergleiche je Datei.
- `roh/np11_folge_scan.csv`, `roh/np11_nrspalte_scan.csv`: Suchläufe.
- `roh/np11_erstpruefung_430.csv`, `roh/np11_teilweise_geprueft.txt`.
- `roh/np10_soll/D2123_soll_schachteln.csv`: Soll je Schachtel für D2123.
- Die Prüfmappen selbst (rund 7 MB) liegen nur im Scratchpad. Mit `methode/np11_pruefmappe.py` lassen sie sich neu erzeugen.
