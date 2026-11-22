# C1 – Nachprüfung 10, Paketart C (14 Dateien, 1'042 Einheiten, Stand 7fa7e161)

**Bilanz:** 11 Dateien ohne kritischen Fehler, 3 mit (D2834, D176772, D3468). 4 kritische Funde, 11 mittel, 1 gering.

## Je Datei
- D1660 (5), D1822 (10), D2085 (13), D2502 (19), D3599 (25), D3688 (12), D2753 (1): fehlerfrei (D2753/D3599 nur Kosmetik).
- D188 (16): 12. «Holland 8. - 11- Mai 1975» (Tippfehler im PDF): Datum im Titel, Zeitraum nur 05.1975 (mittel).
- D1797 (1): Titel ist der erste Listenpunkt «1. Akten betr. …» statt «Albulawerk» (mittel).
- D1803 (6): Schachtel-Teile von :4. heissen nach dem ersten Listeneintrag «a) Protokolle» / «e) Akten …» (mittel).
- D3761 (58, 3 Ebenen): Eltern und Ebenen aller 58 Einheiten richtig. Mittel: «Sch. 1–8» (rechte Spalte) nie als
  Schachtel erkannt (in 9 Titeln, 1 Darin); 2.3.3. Titel «Bahnhofblatt» statt «Bahnhofblatt: Nachfolgezeitschrift»;
  6.9. «Bahn 2000» wird Titel «Bahn» mit Zeitraum 2000.
- D176772 (22, 3 Ebenen), **kritisch:** Sch. 8–11 (Einzelstimmen und Partituren in Tinte) stehen unter 2.6. «Digitalisate»,
  2.5. «Partituren und Orchesterstimmen (Kopien)» bleibt leer. Signal Z (9) = Schachtel-Teile, Rauschen.
- D2834 (2), **kritisch:** Spalte «Bez.» a)/b)/c) nicht erkannt, nur Einheiten «Schachtel 1»/«Schachtel 2». a) (Titel,
  1913–1931) steht nur als «Text vor der ersten Signatur», b), c) und c 1.–40. im Darin von «Schachtel 2». Vollständigkeit 100 %.
- D3468 (852): Struktur ganz per Skript (`tmp_C1/struktur_d3468.py`, Ausgabe `struktur_d3468.txt`): 852 Signaturzeilen =
  852 Einheiten; Reihenfolge, 291 Teile, Eltern, Ebenen, Nummernfolge je Jahr stimmen; Schachteln 848/852 gleich; alle 1'625
  Folgezeilen in der richtigen Einheit. S. 1, 17, 34, 35, 38, 42, 58 Einheit für Einheit (35/38/42 mit Seitenwechsel).
  **Kritisch:** «1947.7» S. 51 (Zahlendreher für 1974.7, Sch. 841) ist Teil 2 von 1947.7 S. 4 (Sch. 407).
  Mittel: 4 × Ü-Format ohne Schachtel; ID 234 «Baltenswil (richtig»; Serie 1956.5 Zeitraum nur 1939.
  Signal N (14) = Titelblatt und Einleitung; Nummernlücken (1943.6, 1957.1, 1958.12 …) stehen so im PDF.

## Muster
1. Signaturspalte nur mit a)/b)/c) unter «Bez.», Schachtelspalte daneben leer → Datei als Schachtelliste gelesen (D2834).
   Die Vollständigkeitsprüfung sieht es nicht, weil alles vor «Schachtel 1» als «Text vor der ersten Signatur» gilt.
   Suchvorschlag: Gliederung «Mappen/Schachteln» mit Zeilen «a) …» am linken Rand.
2. Eine Signatur, die weit hinten wiederkommt, wird immer Teil der ersten Nennung, trotz Hinweis: D3468, nebenbei gesehen
   auch D3472 (1967.18 S. 41 zwischen 1969.17 und 1969.19). Bei Jahr.Laufnummer ist ein Jahr ausserhalb der Umgebung ein Tippfehler.
3. Schachtelangaben ausserhalb der üblichen Form werden nicht erkannt: rechts «Sch. n» (D3761), zweizeilig «Ü-»/«Format»
   (D3468). Folge: Schachtel leer, Text im Titel.

## Unsicherheiten
- D176772 2.5./2.6.: Im Layout steht 2.6. direkt vor «Schachtel 8». Für 2.5. sprechen die Inventarübersicht (2. = 9 Schachteln,
  keine 2.6.) und der Inhalt (Tinte statt CD). Gilt nur das Layout, wäre der Fall «bewusst offen».
- D3468: Teil von 1974.7 oder eigene Einheit mit Hinweis? Das entscheidet die Tippfehler-Konvention. Falsch ist in jedem Fall
  der Teil unter 1947.7.
- D2834: Ob c 1.–40. eigene Einheiten (c.1.–c.40.) werden oder Darin von c. bleiben, ist eine Konventionsfrage.
- Hochrechnung: Die Verdachtssignale (Z, N) waren in allen Fällen Rauschen. Die 3 kritischen Dateien fanden erst die Prüfung
  am PDF und das Skript; D2834 kam aus der Zufallsauswahl.
