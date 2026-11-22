# Runde 12 – Änderungen und Bitte um Nachprüfung 15

Stand 22.11.2026. Skript `findmittel_zu_scope.py` sha256 `439a6fbf2f8dd78b…`. Aufbau: Runde 11 (`94ff40ba…`) plus diese Runde.

`findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind mit diesem Skript neu erzeugt.

## Worum es ging

Behoben sind alle 6 nicht bewusst offenen Zeilen aus `nachpruefung14.md` bzw. `offen_kritisch.csv` (K203–K208, Stand
94ff40ba). Dazu kommen der kleine Rückschritt der Runde 11 in D177470 und die Vorschläge 5–7 der NP14.

**Kennzahlen** (Runde 11 → Runde 12):

| Kennzahl | Runde 11 | Runde 12 | Bemerkung |
|---|---:|---:|---|
| Einheiten | 51'602 | 51'605 | +3 Bestandszeilen (D1729, D2502, D152401) |
| «[ohne Titel]» | 29 | 29 | |
| «Text erfasst 100 %» | 694 | 694 | weiter nur D3943 bei 99,9 % |
| Doppelte Schlüssel | 10 | 10 | |
| Dateien mit Übersichtszeilen | 9 | 9 | |
| Tracebacks | 0 | 0 | |

**Geändert sind 18 Dateien** (`geaenderte_dateien.txt`).
- Ihr Stand vorher liegt in `vorher/`, dazu die zwei geänderten Testdaten als `vorher/testdaten_*.xlsx` und das Skript der
  Runde 11.
- Zellvergleich: `zellvergleich_runde11_runde12.txt`.
- Textabgleich: `werkzeug/textverlust_runde11_runde12.csv`. Die fehlenden Wörter sind alle erklärt:
  - Die Lückenvermerke «[… nicht belegte Signaturen]» stehen jetzt im Prüfhinweis der nächsten Einheit (Regel 7). Das
    Werkzeug zählt den Prüfhinweis nicht mit.
  - Die zweiten Nummern 415, 1517 und 1524 in D151150 stehen jetzt in der Signatur (Regel 6).
  - «17. April 1998 béatrice wiggenhauser» in D175949 steht jetzt im Blatt Info (Regel 2).

**D151210:** Geändert ist nur K208, also 13.4. und 13.4.7. In den Testdaten ändert sich sonst nur D177470 (Regel 4).

**Fallsets:** alle unverändert: A 11/12, B 33/38, C 9/12, F 5/7, Runde 2 31/34, Punkt 2 38/38.

## Entscheide zu den Fragen der NP14

1. **K207 (Konventionsfall):** bestätigt. «Der Bestand V.L.1. … umfasst neben den Brandassekuranzbüchern … noch 5
   Schachteln Assekuranzscheine, Tabellen und Rechnungen.» ist ein Stück ohne Nummer und kommt in die Bestandszeile, wie
   K119. Ebenso D152401 «Zusätzlich 1 Schachtel Besoldungsquittungen und Lieferscheine (nach 10 Jahren kassieren!)» (NP12
   mittel): Das Findmittel zählt die Schachtel zum Total; ob sie noch da ist, zeigt erst der Bestand.
2. **K208 (Grenzfall):** Das Plakat kommt ins Darin der Gruppe 13.4., mit Hinweis. Die Regel greift nur, wenn jede
   Unternummer der Gruppe ein einziger Absatz ohne Untereinheiten ist. In 13.1.x mit den Saison-Sammelmappen greift sie
   nicht.
3. **K205 (Grenzfall):** Der Filmvermerk kommt ins Darin der Gruppe 7.3., wie vorgeschlagen.
4. **Lückenvermerke** «[VI.SB.C.11.-15. nicht belegte Signaturen]»: Sie werden ein Prüfhinweis bei der nächsten
   nummerierten Einheit («Vor dieser Einheit steht im Findmittel der Vermerk …») und stehen im Blatt «Vollständigkeit»
   unter «Nicht übernommen». Das sind 16 Vermerke in 6 Dateien: D152817 (9), D49 (2), D69 (2), D65, D67 und D3793.
5. **Jahr.Laufnummer mit durchlaufender Laufnummer** (D3470): Die Signatur bleibt wie im PDF, mit Hinweis (siehe Regel 5).

## Die Regeln der Runde 12

1. **Stück ohne Nummer im Schlussteil, neue Satzformen** (K206 D1729, K207 D2502, D152401):
   - «Der (Archiv)Bestand enthält noch …»;
   - «Der Bestand … umfasst neben …»;
   - «Zusätzlich n Schachteln/Mappen/Ordner/Bände …».
   - Über alle 715 PDFs treffen die Formen genau diese drei Zeilen.
   - **Durchsicht des Blatts Info:** Ich habe alle 1843 Sätze unter «Schlussvermerke im Findmittel» aller 715 Dateien
     nach Menge und Behälter gefiltert (`werkzeug/info_saetze.py`, Ergebnis `werkzeug/info_menge_runde11.csv`, 92 Sätze).
     Stücke ohne Nummer sind darunter nur diese drei. Die übrigen sind Umfangsangaben («Der Bestand umfasst 6 Schachteln»),
     Verweise auf andere Bestände (D149835 «Urkunden … im Bestand Nc», D3793 «V.A. c.32. …», D2620
     «Zeitungsausschnitt-Sammlung …»), Literatur und Standortangaben. D3018 «Nicht im Detail verzeichnet» ist über die
     Zusammenfassung schon importiert (08.9., 09.).
2. **Bearbeitervermerk «Datum Name» ohne Schrägstrich** (K203 D175949): «17. April 1998 béatrice wiggenhauser» kommt ins
   Blatt Info.
   - Bedingungen: in den letzten 15 Zeilen, in der Signaturspalte, nach mehr als 40 pt Abstand, vor einem weiteren
     Schlussvermerk oder dem Ende und ohne Signatur danach.
   - Über alle PDFs gibt es nur diese Zeile.
3. **Gruppenende erweitert** (K204 D2951, K205 D3099, K208 D151210). Zwei neue Fälle kommen samt Folgezeilen bis zur
   nächsten Nummer ins Darin der Gruppe, mit Hinweis:
   - **(a) Vermerk auf der Höhe der Unternummern:** Er steht links vom Text der letzten Unternummer, mit mindestens 8 pt
     mehr Abstand als vor ihr und vor der nächsten höheren Nummer. Beispiele: «N.B. Damit schliesst diese Briefsammlung. …»
     nach 2.14., «Enthält u.a. eine Filmrolle …» nach 7.3.7.
     - Nicht, wo der Text der Unternummern sonst auf dieser Höhe steht. In VII.374. stehen alle Inhaltszeilen in der
       Signaturspalte.
   - **(b) Eintrag ohne Nummer in der Textspalte der letzten Unternummer**, mit demselben Abstand wie zwischen den
     Unternummern, wenn jede Unternummer der Gruppe ein einziger Absatz ohne Untereinheiten ist (K208).
     - Nicht bei der Beschreibung «Die gebundene Beilagen zum Protokoll enthalten …» von VII.12.B. 3.1.3.: Dort haben die
       Geschwister Untereinheiten.
   - Im Gesamtlauf greifen (a) und (b) nur in diesen drei Dateien.
   - Die umgehängten Zeilen zählen weiter für den geschätzten rechten Rand der Textspalte. Sonst änderte sich das
     Zusammenfügen in der ganzen Datei, wie es im ersten Versuch in D2951 2.4. und 2.9. geschah.
4. **D177470 15. und 24.** (Rückschritt der Runde 11): Der rechte Rand der Textspalte bleibt, wie er mit den Buchstaben als
   Einheiten war. Die Titel von 15. und 24. sind wieder ganz.
   - Dadurch ist auch 27. c) zusammengefügt: «Grabrede … von Frau Barbara Guldener, 13.7.1926».
   - Gering: In 28. e) und f) fehlt jetzt das «; » vor der Folgezeile («… Schülerkurse 1.) Metallkurse …», «… des 20.
     Jahrhunderts Ruth und Hans Rudolf Reinhard-Guldener»).
5. **Jahres-Tippfehlerregel der Runde 8 nicht bei durchlaufender Laufnummer** (D3470, mittel).
   - Läuft die Laufnummer über die Jahreswechsel weiter, ist das Jahr eine Angabe zum Eintrag. Die Grenze: in mindestens
     80 % der Wechsel, bei mindestens 3 Wechseln.
   - Die 11 Signaturen, z. B. «1936.472» zwischen 1935.471 und 1935.473, bleiben samt Zeitraum wie im PDF, mit Hinweis.
   - D3472, wo die Zählung je Jahr neu beginnt, ist unverändert.
6. **Dossiers mit zwei Nummern** (D151150, mittel): 9.412/415., 9.1516/1517. und 9.1523/1524. sind je eine Einheit wie
   «146/148» in D3412.
   - Die zweite Nummer steht im PDF allein unter oder zwischen den Titelzeilen, oder vor der Fortsetzung des Titels.
   - Die Titel sind ohne «415» und «1524», das Darin ohne «1517».
7. **Lückenvermerke** (D152817 gering/mittel, NP12 D49, D65, D69): siehe Entscheid 4. 97. heisst jetzt «Protokoll der
   Grundbesitzerversammlung».
8. **Seitenwechsel nach der Tabellenzeile** (D3466, mittel). Folgt in einer Datei auf die Tabellenzeile mit Jahr oder
   Schachtel in mindestens 85 % der Fälle ein Absatz, so ist die erste Zeile der nächsten Seite Inhalt und nicht
   Fortsetzung des Titels.
   - Ausnahmen: Die Zeile reicht bis an den Rand, endet offen («,», «-», Anschlusswort, offene Klammer), steht in
     derselben Spalte oder beginnt klein, mit Ziffer oder Anführung; «dito» gilt als Inhalt.
   - In D3466 sind es 10 Einheiten: 124., 132./T4, 249., 257., 294./T6, 420./T2, 502./T3, 525./T19 «dito», 570./T6 und
     583./T3.
   - Im Gesamtlauf greift die Regel nur in D3466.
9. **D3774 6.4.** (mittel): «Grossformate (ausserhalb der Schachteln)» beendet die laufende Schachtel. 6.4. hat keine
   Schachtel mehr.

## Nicht umgesetzt

- **D2620 1.14.** (mittel): Der Titel ist am Gedankenstrich am Zeilenende abgebrochen. Die Regel, die dort trennt, braucht
  VII.200. («… von Bertolt Brecht -» / Unterlagen), und eine Ausnahme wäre für D151210 zu riskant.
- **D3466 584./T19** (mittel): «Zürich Ad. Saurer AG, Arbon,» / «Schutzraum Hohlstrasse 295» bleibt wegen des Kommas am
  Zeilenende ein Titel.
- **D3412 «Nr.-»** (gering): Mit «Nr. -» fiel im Versuch das Präfix weg, darum bleibt «Nr.-».
- Wie bisher:
  - D2962 7.–10. Schachtel 3;
  - D9978 28.4.25. Zeitraum;
  - D406 Vermerk nur im Hinweis;
  - D3530 Zeitraum 1890;
  - D3943 99,9 %;
  - die mittleren Funde der Zufallsstichprobe (Zeiträume aus Lebensdaten oder Werktiteln, Bestandstitel mit Datum).
- Zur Abstimmung vor dem Gesamtimport, wie in NP14: D176824 «VII.308.A.» statt VII.308.; D2921 Briefgruppen als Liste.

## Bewusst offen

Wie bisher: K38 D149622, K39 D1739, K40 D1858, K41 D2614, K42 D3208, K44 D3828, K45 D512, K78 D3894, K117 D2710, K173
D1874.

## Bitte um Nachprüfung 15

Wie in deinem Plan zu NP15:

1. **Gegenprüfung der Runde 12** an den 18 geänderten Dateien und den zwei Testdateien. Altzeilen sind K203–K208.
   Besonders zu prüfen sind Fehlgriffe der Regeln 3 (Gruppenende a/b), 6, 7 und 8 (Seitenwechsel).
2. **Gezielte Durchsicht:**
   - alle Info-Sätze aller 715 Dateien, die keine Bearbeitungsvermerke sind. Meine Vorarbeit zu Menge und Behälter steht in
     `werkzeug/info_menge_runde11.csv`; der übrige Teil fehlt noch;
   - das Darin der letzten Einheit jeder Datei auf Vermerke mit Datum und Name;
   - die Gruppenende-Kandidaten mit dem Abstand eines neuen Eintrags. Eine breite Liste mit 529 Treffern ergibt fast nur
     Listeneinträge innerhalb der letzten Unternummer. Hilfreich wäre ein engerer Filter.
3. **Dritte Zufallsstichprobe** von 60 Dateien ab Rang 137 derselben Reihenfolge.
