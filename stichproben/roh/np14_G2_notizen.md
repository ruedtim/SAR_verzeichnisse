# G2 – Gegenprüfung Runde 11 (Regeln 2, 3, 4, 10, Konvention 2)

## Bilanz
- 7 Dateien + Testdateien D152810 und D177470: alle **ohne kritischen Fehler** im Stand jetzt.
- Vergleich: 113 Diff-Einträge (dazu 20 der zellgleichen Testfassung D177470) in 41 Urteilszeilen: 110 besser, 1 gleich
  (Hinweis 1966.19), 2 schlechter (D177470 15./24.). Dazu 2 Zeilen Fehlgriffsuche, 1 Zeile Zellgleichheit.
- Altzeilen: alle 11 **behoben** (K178, K183–K188, K194, K195, K197, K199).
- Neue Funde: 0 kritisch, 2 mittel (G2-N1 Runde 11, G2-N2 vor Runde 11), 2 gering.

## Zu den Fragen
- **D3472 Regel 2:** 1952.9 und 1952.15 sind richtig: andere Objekte in alphabetischer Folge, Nummer fehlt, Nr. im PDF und Hinweis
  da. Sonst hat Regel 2 in D3472/D3470 nichts umgedeutet. Die 37 übrigen Teile haben gleichen Titel («Diverse Offerten», «Genève
  Pont rail …») oder ihre Nachbarnummer (D3470 1586 als «1955.1586», globale Laufnummer). Keine übersehene Doppelnummer.
- **D3470:** 40.430/41.436 wieder wie im PDF. 11.43.a./11.44.a. sind eigene Projekte mit eigener Schachtel, als Geschwister E1
  richtig. 13.92.a./b. unter «Diverse Arbeiten» bleiben zu Recht Kinder (zu S1 N12/N13).
- **Regel 4 (D152817, D152810, D150589, D3067):** Alle neuen Geschwister sind eigene Gegenstände: andere Serie mit eigenen Bänden
  (33.a, 32.a), eigenes Buch (75.a), eigener Vortrag/Anlass mit Datum (2.2.1.8.a, 2.2.9.12.a), Schriftstück eines anderen
  Absenders (IV.A.5.a/b). «n.» hat jeweils eigene Angaben. VI.HO.C. reicht jetzt richtig bis 1925.
- **D10744 (K178):** Alle 156 Ebenen/Eltern programmatisch gegen die Schrift geprüft: 0 Abweichungen. 710 Dossier E3, 711–718 E3,
  Unterpunkte E4.
- **D177470 (K199):** a)–h) vollständig im Darin, kein Wort fehlt. 28. 1933–1984 stimmt. 27. «von» 31.10.1886 ist ein
  Geburtsdatum aus e) (bekannter mittlerer Fund NP13, unverändert). Testfassung zellgleich.

## Wichtigste Funde
1. **G2-N1 (mittel, Runde 11):** D177470: Titel von 15. und 24. gekürzt, Titelfortsetzung jetzt im Darin. Ursache: die an 27./28.
   gehängten a)–h)-Zeilen verschieben `rand_der_textspalte` (95. Perzentil) nach rechts; die Titelzeilen gelten nicht mehr als voll,
   `datumszeile_setzt_fort` trennt die Folgezeile mit Datum ab. Vorschlag: Rand vor `aufzaehlung_unter_jahrnummer` bestimmen.
2. **G2-N2 (mittel, vor Runde 11):** `korrigiere_jahrnummern` (Runde 8 Regel 45) ändert in D3470 elf Jahre («1936.472» → 1935.472,
   Zeitraum 1935). Dort läuft die Nummer durch den ganzen Bestand, an den Jahresgrenzen mischen sich die Jahre (1937.500, 1937.501,
   1936.502; 1938.509, 1937.510). Gleicher Grund wie Regel 3. Vorschlag: nur bei Zählung je Jahr (D3472, D3468); bei Laufnummer ab
   100 Jahr wie im PDF. «1947.744» ist wohl wirklich ein Tippfehler.
3. **G2-N3/N4 (gering):** D152817 Lückenvermerke «[… nicht belegte Signaturen]» im Darin der vorigen Einheit, einmal im Titel von 97.
   (S1 E24/E25 entscheidet, ob kritisch); D177470 «Frau; Barbara».

## Muster und Unsicherheiten
- Nebenwirkungen kommen hier über dateiweite Schätzwerte (Textspaltenrand), nicht über die Struktur. Nur der Vergleich findet sie.
- G2-N2: Die Grenzjahre sind als Daten plausibel, aber nicht beweisbar.
- Nicht ganz geprüft: D3470, D3472, D150589, D152817 (Diff, Altzeilen, Fehlgriffsuche, Struktur, betroffene Seiten). Ganz: D177470,
  D10744; D3067 über die Kompaktmappe. Bekannte mittlere NP13-Funde bestehen fort (D3472 1952.111, D150589 2.2.2.25., D3067, D10744).
