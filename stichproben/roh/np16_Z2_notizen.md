# Z2 – NP16, vierte Zufallsstichprobe: 19 Dateien, 451 Einheiten

## Bilanz
- **19 von 19 Dateien ohne kritischen Fehler**, kein kritischer Fund, weder neu noch alt. Neu: 5 mittel (Z2-01–05), 3 gering
  (Z2-06–08), alle «vor Runde 13» (die Stichprobe hat nur Dateien, die Runde 13 nicht ändert). Keine Datei in `bekannt.csv`.
- **Umfang:** jede Datei ganz, mit der vollen Prüfmappe (auch D1706, D176795, D3512 statt Kompaktmappe; keine über 200
  Einheiten). Dazu Dump aller Excel-Felder, Info, Vollständigkeit und drei Suchläufe in `tmp_Z2/`: Position (`poscheck.py`
  aus NP15), Eltern nach Dezimalpräfix (`pruefe_eltern.py`), Jahre ausserhalb von/bis (`jahre_ausserhalb.py`).

## Gliederung (in NP15 nicht durchgesehen)
- Alle 19 stimmen: Eltern und Ebenen passen zum Präfix (0 Abweichungen), Stufen richtig, Übersichten (D2841, D3512,
  D176795) nur im Vorspann und im Detail vollständig. Keine Einheit erfunden oder fehlend, keine Unterstufe im Darin.
- D71: Leere Kategorien a)–c), e) «… keine» sind Einheiten wie in D49/D65/D67/D69, als Konvention gewertet.
- Frühere K-Funde behoben: D176795 «Kinder von …» (NP12/13, jetzt Hinweis), D2372 Schachtel-Einheiten (NP11), D2323 :3.,
  D71 III.S.1. unter d).

## Neue Funde (alle mittel)
- **Z2-01, Z2-03:** Jahresklammer ohne Lebensdaten zählt nicht als Laufzeit. D3561 6.2. «(1940 – 1947)» wird 1945 (aus dem
  Darin), D3512 1.1.1. «Korrespondenz (1967 - 1983)» ergibt nur 1967.
- **Z2-02:** D3561 6.1. «(bis 1919)» gilt als genau 1919; das Darin nennt auch 1918.
- **Z2-04:** D3512 5.2.: Inhaltszeile «u. a. Photokopie …» im Titel (Kleinbuchstabe gilt als Fortsetzung).
- **Z2-05:** D176795 2.1.2.: «Vergissmeinnicht» im Titel (wie 2.3.4. in NP13); ebenso «Erbschaftsakten» bei 2.2.1., 2.2.3.

## Bekannt offen, unverändert (nicht neu gemeldet)
- NP11 mittel: D1593 (13 Titel mit «1913 (I)» in der Mitte), D1608 (10 Titel «Ingenieurabtei- 1883 lung»), D817 15.,
  D3769 «Mappe 1–4», D3614 1.1./5.3./5.4.
- D176795: Schachteln 1.1.1./2.3.3./2.3.9.2./2.3.9.3./2.3.14. (NP3 ff.), Titel 1.2./2.3.4./2.3.10.3./2.3.13.1.–3.,
  Zeitraum 2.3.9.3./2.2.2. Dazu D3382 5.1. Titel und D3561 2./4./5. Zeitraum (NP10); gering D3206, D2143, D71.
- Klasse «Zeiträume aus Lebensdaten oder Werktiteln»: D2841 3.1.x, D3382, D3512 1.1.3.–1.1.5., D3561 8.4., D3614 4.1./5.1./7.2.

## Muster
- Restfehler nur in Titel und Zeitraum. Gliederung, Gruppenende und Schluss/Info sind in allen 19 Dateien sauber:
  Bearbeitervermerke und Herkunftsvermerke (D3382, D2841) im Info, kein Stück ohne Nummer im Schluss.

## Unsicherheiten
- Ursache von Z2-01/03 aus dem Skript erschlossen (Klammerregel, PERSON_RE Z. 391); bei Z2-03 evtl. Ausreisserregel (5× 1967,
  1× 1983). Z2-02 ist Ermessen.
- Nicht gemeldet: D3561 7.3. (Brief 1998 im Darin, Zeitraum Ereignisdatum 1922); D3512 1.1.2. (1833 nur aus Kopien);
  Herkunftsabsatz D3561 vor 1. im Blatt Vollständigkeit statt Info (beides nicht importiert).
- [VOR]/[NACH] waren überall Rauschen (gleichlautende Zeilen); in D3382 setzt die Prüfmappe den Anker für 2. falsch.
