# E4 – Notizen (Nachprüfung 11, Paketart E, Stand efe92c5f)

## Bilanz
- 43 Dateien, 1'330 Einheiten. 40 ohne kritischen Fehler, 3 kritisch (D1726, D3894, D3816).
- 19 Funde: 3 kritisch, 11 mittel, 5 gering. Alle Prüfmappen ganz gelesen. D177448 (443 Einheiten) per Skript auf
  Struktur geprüft (Ebene = Stellenzahl, Eltern = Präfix, Folge lückenlos), dazu S. 3, 4, 11, 13, 19, 25 Zeile für Zeile.
- Warnzeichen: fast alle [VOR]/[NACH] waren Rauschen (gleichlautende Zeilen wie «(Wachssiegel)», «Band n», «1918»).
  [SIG?] traf in D3894 (Abschnitte als Teile). In D1182 ordnet die Mappe die Signaturzeile «2.» falsch zu, die Excel stimmt.

## Kritische Funde
1. **D3894 (X.C. Siegelsammlung):** Die Abschnitte «2.»–«4.» (14 pt) stehen als «Teil 2» unter den Siegeln X.C.2.–4.
   Siegel 1 ist Teil 2 von Abschnitt 1, und die Siegel 5–85 haben keine Eltern. Seit Runde 7 «bewusst offen», aber nicht
   in offen_kritisch.csv. Soll: Abschnitte X.C.:1.–:4. auf E1 ohne Teil, alle 85 Siegel auf E2 unter X.C.:1.
2. **D3816 (VII.7.):** «18.a» (3 Bände, 1839–1891, mit 18.a:1–3) hängt als Kind unter dem Einzelband «18.» (1874–1886).
   Beide stehen bei x71 als eigene Blöcke. Soll: 18.a auf E1 neben 18. (wie NP10 K49 «3a.»). Das Skript meldet selbst
   «Untereinheiten reichen über den Zeitraum hinaus».
3. **D1726 (V.G.b.903., Grenzfall):** «Drei Archivschachteln enthalten Drucksachen des Heizamtes ab 1945.» steht nur im
   Blatt Info. Das Titelblatt nennt «49 Bände», also sind die drei Schachteln nach dem Import nirgends. Soll: eigene
   Einheit ohne Nummer (wie D149825 K4). Wird solcher Text nach Konvention im Info belassen, ist es nur mittel.

## Muster (mittel/gering)
- **Datumsspalte mitten im Titel**, wenn der Titel auf der Folgezeile weitergeht: D1791 ID 4, D1591 (alle 6, dazu die
  Trennung «Hochbauinspekto- … rats»), D177448 ID 319 «Undatiert, 1984–2010». Ein Muster, eine Regel.
- **Zeitraum aus Namen und Inhalt:** «Jahrgängerverein 1844» (D8631), «seit 1800» im Buchtitel (D1182), Inhaltsjahre
  einer undatierten Liste (D2745), «18. Jh.» nicht erkannt, dafür Kopie 1915 und Übergabe 1993 (D3816 :96).
- **Zweites Datum geht verloren:** «14. November, 19. Dezember 1984» wird nur zu 19.12.1984 (D177448 ID 266/267).
- **Datumszeile über der Signaturzeile** wird der vorigen Einheit zugeschlagen (D1404 2./2.1.).
- **PDF-Tippfehler ohne Hinweis:** «1934-1957» bei Band 1 einer Gruppe 1834–1892 (D3816 :33).
- **Zerlegte Darin-Einträge:** « - » im Text gilt als Listentrenner (D1754, D167 «A - D»). 8-pt-Aufzählungsstriche
  bei x71 brechen Literatureinträge (D3894 X.C.:4., D175480). Kein Textverlust.
- **Jahre am Titelende** abgetrennt, nur noch in der Anmerkung (D177448 ID 178/179).

## Unsicherheiten
- D1726: Ob ein Satz zu Behältern ohne Nummer eine Einheit wird, ist eine Konventionsfrage.
- D3894: Soll X.C.:4. «Literatur …» eine Einheit sein oder als Bibliografie ins Info (wie D152781)? Der kritische Teil
  (Teil unter fremdem Siegel, Eltern) gilt in beiden Fällen.
- D3545 «4.» und D3585 «5.»: Der Eintrag mit derselben Nummer wie die Überschrift steht im Darin, bei D3585 «1.5.»
  dagegen als Teil. Das ist uneinheitlich, aber kein Inhalt geht verloren oder steht falsch. Nicht gemeldet.
- Bestandszeilen «ohne Signaturen» (D2616, D2727, D2749): Der Titel setzt sich aus Titelblatt und Abschnitt «Akten»
  bzw. «Drucksachen» zusammen. Nur Kosmetik, nicht gemeldet.
