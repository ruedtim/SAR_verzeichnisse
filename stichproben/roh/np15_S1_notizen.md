# S1 – Kandidaten «Gruppenende, gleicher Abstand» (NP15)

## Bilanz
- 192 Kandidaten beurteilt: **0 Funde**, 192-mal «kein Fund». `S1_funde.csv` enthält nur den Kopf. Keine Zeile aus `bekannt.csv` betroffen.
- **42 ausserhalb der gleichmässigen Dateien**, jeder einzeln an der Prüfmappe, im Zweifel am PDF (D109662 S. 5, D151730 S. 1–3, D1746 S. 6, D32837 S. 46, D3530 S. 31, D9983 S. 5). Jede Zeile ist Inhalt der letzten Untereinheit:
  - erste Inhalts- oder Listenzeile, oft nach Titel mit Doppelpunkt (D10585 8.4.8., D2933 B.1.4.2., D152817 8-11);
  - Umfang «(n Schachteln)» (D150306) oder Zwischenzeile wie bei den Geschwistern (D2962 «Lose Protokolle und Akten:»);
  - Beschreibung der Untereinheit selbst (D1220 1.2., D149888 10.4.3., D150829 5.8.).
- **Gleichmässige Dateien:** D141020 (38), D149628 (42) und D4054 (20) alle genau, mit Kontext bis zur nächsten Einheit. D151210 (50): 11 genau (u. a. 13.1.11., 13.5., 14.3.3.), der Rest nach Einzug und Inhalt. Überall erste Inhaltszeile oder Listeneintrag der Untereinheit, mit dem normalen Absatzabstand.
- **Zusatzprüfung**, weil der Suchlauf nur die erste passende Zeile nach c nimmt (`break`): alle 497 Gruppenenden der vier Dateien, bei den 115 mit mehreren Absätzen in c der letzte Absatz (`tmp_S1/letzter_absatz.py`).
  - Gefunden nur K208 (D151210 13.4.7.), das jetzt richtig im Darin von 13.4. steht.
  - Sonst Inhalt von c: Teile mit wiederholter Signatur, «Presse allgemein», Jahreszeilen.
- **Rauschen der Prüfmappe:** «→ ID n Titel» oder «[VOR]» bei Zeilen, die im Darin stehen (D149628 13.2., 26.1.1.2.; D151210 3.6.5.4.). Am Excel geprüft.

## Welche Lage mit welchen Spalten echte Fälle trennt (q = abstand / ueblich)
| Fall | Datei | Lage | q | einzel | davor |
|---|---|---|---:|---|---:|
| K196 | D2620 | B | 1,50 | ja | 0 |
| K203 | D175949 | A | 6,0 | ja | 0 |
| K204 | D2951 | A | 3,1 | nein | 5 |
| K205 | D3099 | A | 2,0 | ja | 0 |
| K208 | D151210 | B2 | 1,01 | ja | 2 |

- **Fehlalarme dieser Runde:**
  - B: q ≤ 1,10, ausser D109662 (1,56, aber einzel = nein).
  - A: q ≤ 1,06, ausser D1220 (1,64), D2857 (1,61), beide nein/davor 0, und D151730 (1,99; ja; davor 0).
  - B2: alle 31 mit einzel = nein. E (9): nie ein echter Fall.
- **Vorschlag enger Filter:** A nur mit q ≥ 1,5 und (einzel = ja oder davor > 0); B nur mit q ≥ 1,3 und einzel = ja; B2 nur mit einzel = ja; E weglassen.
- **Probe:**
  - Runde 10: 199 → 8. Es bleiben alle 5 K-Fälle, die 2 Lückenvermerke D152817 (jetzt Regel 7) und D151730 8.2.
  - Runde 11: 198 → 7. Runde 12: 192 → 1 (D151730 8.2., kein Fund).
- **D151730** fällt zusätzlich weg, wenn die Ausnahme von Regel 3a auch im Suchlauf gilt («nicht, wo der Text der Unternummern sonst auf dieser Höhe steht»). Dort steht die erste Listenzeile nach einer Leerzeile immer auf x170 (14.2.–15.4.).
- Für B/B2 trennt «einzel» am stärksten, für A der Quotient q. Der Filter ist an nur 5 Fällen geeicht und taugt zum Sichten, nicht als Regel.

## Lücke im Suchlauf und Unsicherheiten
- Der Suchlauf meldet je Gruppe nur die erste Zeile nach c mit einem Abstand über dem üblichen. In gleichmässigen Dateien trifft das immer den eigenen ersten Absatz von c; ein Gruppenvermerk danach bleibt unsichtbar.
- K204 wurde nur gefunden, weil die 5 Zeilen davor eng standen. Vorschlag: zusätzlich den letzten Absatz vor der nächsten höheren Nummer melden.
- Unsicherheiten: keine. Grenzfall nach Lage ist D151730 8.2.; inhaltlich klar, denn alle Einträge betreffen die Neumünsterstrasse 2.
