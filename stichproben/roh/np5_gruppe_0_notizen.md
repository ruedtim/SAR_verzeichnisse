# Fünfte Nachprüfung – Gruppe 0 (Hauptprüfung): Notizen

Stand 13:15 (`$S/neu5/`, Skript 68ad815e…, 5076 Zeilen), verglichen mit 11:30 (`$S/neu4/`).

## Schnappschuss und Vergleich
- `findmittel_excel/` (716 Dateien), `testdaten_excel/` (13), `D151210_scope_import.xlsx` und das Skript nach `$S/neu5/` kopiert,
  sha256 aller Dateien mit der Quelle verglichen: gleich.
- Inhaltlicher Vergleich aller Blätter ohne die Zeile «Erzeugt»: **234 Dateien** in `findmittel_excel/` (genau die Liste in
  `zellvergleich_1130_1315.txt`; die «235» der Nachricht = 234 + `uebersicht_scope_import.xlsx`, deren Blatt Übersicht sich
  ebenfalls ändert) und **10 Testdateien** (D152810 und D3031 gibt es nur als Testdatei; die übrigen 8 sind inhaltlich gleich
  wie in `findmittel_excel/`).
- Abgleich der Einheiten neu über **(Signatur, n-tes Vorkommen)**, weil Regel c die Teil-Nummern ändert. Ergebnis über alle
  715 Dateien: 43'253 Einheiten unverändert, 6'015 geändert, 46 entfernt, 43 neu. Davon nur Teil-Nummer: 4'043.

## Kennzahlen (eigene Zählung, gleich wie die Hauptsession)
| | 11:30 | 13:15 |
|---|---:|---:|
| Einheiten | 49'314 | 49'311 |
| «[ohne Titel]» | 44 | 35 |
| «Text erfasst» 100 % | 694 von 715 | 694 von 715 |
| Schlüssel (Signatur, Teil) mehrfach | 1'611 (5'938 Zeilen) | 69 (149 Zeilen) |
| überzählige Zeilen (Zeilen − Schlüssel) | 4'327 | 80 |

Die neun neuen Titel statt «[ohne Titel]» (D175949 Q, D2735 4, D2921 3., D3587 1., D3612 28., D414 II./III., D8952 2/7) kommen
aus Regel i; vier am PDF geprüft, alle richtig.

## Regel c über alle Dateien (`$S/np5/teile.json`)
4'233 Teile in 95 Dateien neu nummeriert. Keine Lücken, keine geänderte explizite Nummer, keine nicht-numerische Teil-Nummer.
Mehrfache Schlüssel nur noch in D151210 (49), D2681 (10, Datei seit 11:30 unverändert), D3357 (4), D3231 (2), D4054 (2),
D32837 (1), D4057 (1). Nicht aufsteigende Teil-Folgen: D151210 21, D3231 4, D32837 2, D3357 2, D4054 2, D149628 1, D4057 1.
Diese Fälle prüft Gruppe 4 am PDF.

## Gesamtabgleiche
- **Bestandssignaturen:** kein Feld «Bestand» geändert; der Abgleich mit dem PDF-Kopf ergibt dieselben 23 bekannten
  Erkennungsartefakte wie um 11:30.
- **«Nicht übernommen»:** D151150 0 → 37 (Regel l, prüft Gruppe 5), D3271 1 → 7 (Gruppe 2), D10675 43 → 2, D10744 23 → 12,
  D151217 3 → 0 (Regel u, Gruppe 2), D1880 3 → 0 (Gruppe 1), D3774 3 → 0 (Gruppe 2), D3253 25 → 24 (Gruppe 1).
- **«Text erfasst»:** gesunken nur D512 99,94 → 99,87 % (siehe unten) und D152817 100 → 99,98 % («1841-1932» der Zeile
  «Besoldungen ¦ 1841-1932» fehlt, VI.SB.D.7.:1-2 – an Gruppe 5 gegeben); gestiegen D3828 99,96 → 100 % («o.D.» jetzt in der
  Anmerkung).
- **Text, der nirgends mehr vorkommt** (`textverlust.csv`, 101 Treffer): 84 in D3774 (Gruppe 2). Von den 17 übrigen sind die
  meisten Umbauten nach Regel i/j/n/o (Text jetzt im Titel oder eigene Einheit). Auffällig:
  - D867 V.C.c.81.:5. und D3581 VII.352.:1.1.: Der erste Listeneintrag wird an den Titel gehängt (neuer Fehler, Regel i).
  - D149628 23.1.1.836./907.: Der Titel ist auf den Komponistennamen gekürzt, der Darin-Eintrag mitten im Ausdruck getrennt
    (an Gruppe 5).
  - D4054 12.3.4.: «… siehe auch 1982» → «… siehe auch» (an Gruppe 4).
- **Neue Titel = alter Titel + erste Darin-Zeile** (`titel_angehaengt.csv`, 151 Einheiten):
  - 133 in D3466 (Regel j, Tabellenzeile «Dampfturbinenfundamente» u. ä. – Gruppe 2).
  - 18 in 11 weiteren PDFs; davon 8 mit Rest-Darin, siehe oben.
- **Bekannte offene Punkte, seit 11:30 nicht verändert:**
  - «(n Schachteln)» ohne Umfang: 257 → 257 Einheiten.
  - D3466 Titel mit «19xx / yy»: 189 → 189, alle mit Zeitraum.
  - D10585, D3105, D150689: PDF unverändert.

## Paket (15 Zeilen)
- **D3099:** Z236 behoben (Teil 2); Z237, Z239 unverändert offen.
- **D512:**
  - Z186 behoben, Z157 teilweise (49 von 51 Saisons jetzt mit dem Zeitraum aus dem Titel), Z158 offen.
  - Z86 teilweise: Die Einträge sind unverändert. Weil die Saison-Zeiträume jetzt aus dem Titel kommen, stehen 8 Folgedaten,
    die nur im alten Zeitraum steckten, nirgends mehr (Vollständigkeit 7 → 15 Zeilen).
  - Neu falsch: 1.19. 1938–1977.
- **D3828:**
  - Z81 behoben: 13. Teil 3 1912–1927, «o.D.» in der Anmerkung.
  - Z22/Z80/Z82 bewusst offen und unverändert.
  - Durch Regel b übernehmen die Erstnennungen auf S. 1–2 die Zeiträume der gleichnamigen Nummern aus anderen Abschnitten. Das
    ist eine Verschlechterung innerhalb des bewusst offenen Punkts und wird nicht als neue Zeile gezählt.
- **D3530:** Z21/Z74/Z75 unverändert. Neu: 1. «= 20.04.1999» aus dem Inventarvermerk.
- **D1739:** Z18 bewusst offen und unverändert. Bei 25 Schachteln ist die Quelle jetzt «Datumsspalte»; zwei am PDF geprüft,
  richtig.

## Bewusst offene Punkte – bestätigt
- **D3828, D3530:** Gliederung unverändert; neu nur Teil-Nummern und Zeiträume, siehe oben.
- **D141024, D149622, D3208, D2614:** Excel inhaltlich unverändert.
- **D512:** Struktur und Darin unverändert, nur Zeiträume, siehe oben.
- **D1739:** «Mappe mit Grossformaten» weiter ohne eigene Einheit.

## Testdatei D152810 (nur Testdaten)
- 6 Änderungen. VI.HO.D.5. und D.8. sind jetzt wegen später datierter Einträge auf 1893 bzw. 1872 erweitert – richtig
  (Regel a).
- VI.HO.C.25.:12/:13 haben neu 1843–1875 bzw. 1844–1865. Ihre «Teile» sind Tippfehler-Zeilen aus anderen Reihen (S. 9, S. 18).
  Neuer Fehler, Regel b.

## Wichtigste Punkte
1. **Reine Jahreszeile zu weit gefasst (Regel a).** `ist_reiner_zeitausdruck` (Z. 575–577) streift «)» und Satzzeichen ab.
   Dadurch zählen als Spaltendatum der Einheit (verarbeite Z. 2865–2866):
   - das Ende eines Klammertexts: D512 1.19. «1938 - 1945)», D3530 1. «20. April 1999)»;
   - eine allein stehende Dossiernummer: D151150 9. «1517».
   Der Zeitraum ist dann falsch, und die Quelle heisst «Datumsspalte» bzw. «Untereinheiten», ohne Hinweis.
2. **Regel b und Tippfehler-Teile.** Teile, die nach Entscheid 5 aus Tippfehlern entstehen, erweitern jetzt den Zeitraum der
   Erstnennung (D152810; D3828 mit bewusst offener Gliederung).
3. **Regel i, Ausnahme «Datum erst in der Folgezeile»** (kopf_und_rumpf Z. 2659–2660):
   - richtig bei Untertiteln (D3271 3.4.2./3.4.3., D1237 2);
   - falsch bei Listenköpfen mit Doppelpunkt, deren Einträge eine Datumsspalte haben: Der erste Eintrag wandert in den Titel
     (D3581 1.1. samt «Schachtel 1», D867 5.).
4. **D512:** 49 von 51 Saisons haben den richtigen Zeitraum. Dabei verschwinden 8 Folgedaten der Einträge aus dem Import; das
   ist der alte Fehler Z86, der vorher durch den falschen Zeitraum verdeckt war.
