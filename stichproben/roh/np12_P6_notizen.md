# P6 – Notizen (Nachprüfung 12, Paketart P, Stand 66c0fb74)

## Bilanz
- 22 Dateien, 929 Einheiten. Ich habe alle Prüfmappen gelesen (16 volle Mappen, 6 Kompaktmappen), dazu Excel-Auszüge und das PDF an allen Zweifelsstellen.
- 8 Dateien haben einen kritischen Fehler: D3774, D175994, D1874, D3533, D2894, D2872, D10744, D414. 14 Dateien sind ohne kritischen Fehler.
- 28 Funde: 11 kritisch, 14 mittel, 3 gering. Alle Ursachen liegen vor Runde 9. Nur bei D3533 greift Regel 3 nicht, und bei D2894 ist die Ursache unklar.

## Wichtigste kritische Funde
- D10744: Registraturplan. Die Gruppen 430.1.020, .600 und .700 (14 pt fett) sind leere Dossiers. Ihre rund 150 Codes stehen eine Ebene zu hoch als Geschwister daneben. In D10675 hängt 011 dagegen unter 010.
- D414: Die Gruppen I.–XV. gehören zur Aktensammlung in Schachtel 5 («Die Aktensammlung ist gegliedert in folgende Gruppen:»). Sie stehen aber als oberste Ebene neben den Schachteln. Bisher war das nur als mittel gemeldet.
- D2894: Aus der allein stehenden Zeile «Schachtel 42» wurde ein Teil 2 von 7.4. Sein Titel ist das erste Lied («Dankeschön und auf Wiedersehen Eric Hein»).
- Muster 2, Überschrift oder Behälterzeile am Gruppenanfang im Darin der vorigen Einheit: D175994 «Gemeindegutsrechnungen, Rechnungsbeilagen» samt Erläuterung bei IV.A.44.; D2872 «Schachteln 7 bis 12 …» bei 9.31.; D3774 «Grossformate (ausserhalb der Schachteln)» bei 6.3.
- Muster 6, Schlusstext im Darin der letzten Einheit:
  - D3774: die Bearbeitungsvermerke «neu umgebrochen … / neu formatiert … / gelayoutet» bei 6.4.;
  - D3533: «Alfred Jud-Frei … Kurzbiografie liegt bei.» beim Buch 3.6. Regel 3 greift nicht, weil kein Stichwort wie Bestand oder Nachlass vorkommt.
- D1874: Der Code «-» («Planmappe nicht mehr vorhanden») fehlt bei 73 Mappen und in der Legende. «X» und «fehlt» sind übernommen.

## Grenzfälle (bitte entscheiden)
- Stücke ohne Nummer, die nur in Einleitung oder Vorbemerkung stehen, habe ich als kritisch gemeldet («Text weg», Regel 31 und Muster 4):
  - D3774: Archivregister 1843–1922, Inventar 1982 und «Akten zur Bestandesgeschichte» in Schachtel 1. Das Soll von NP4/NP5 lautete dort aber «Einleitung und Findmittel sind Vorspann».
  - D2894: «Akten zur Archivübernahme im Jahr 1980 wurden in Schachtel 1 abgelegt.»
  - Offene Frage: Gilt Regel 31 auch hier? Wenn nicht, sind beide Fälle kein Fehler.
- D1874 Code «-»: NP9/NP10 nannten das «bewusst offen» (gering). Ich werte es als kritisch, weil die Aussage «nicht mehr vorhanden» fehlt. Es bleibt ein Grenzfall.
- Nicht gemeldet:
  - D175997: Die Unterlisten 1.–6. bei IV.C.165./168./171. stehen nach der Konvention im Darin. IV.C.180. nennt aber «IV.C.171.6.» als frühere Signatur.
  - D1395: Die wiederholte Gruppennummer je Schachtel steht als Darin-Zeile, 15.1. dagegen als Teile. Uneinheitlich, aber bisher akzeptiert.

## Mittel (Auswahl)
- Schachtel falsch: D3774 (1.–1.5. ohne Schachtel 1, 6.4. mit 7), D3581 (2.1. «1» statt «1-3»), D3012 (8.a «05» statt «04-05»).
- Zeitraum falsch: D3774 (1. mit dem Datum des Archivregisters), D3778 (bis 1992 statt 1939), D10744 («Genau 1991» für den ganzen Plan), D1395 (15. ohne das eigene Jahr 1979).
- Titel mit Unterzeilen oder abgeschnitten: D3774, D1874, D3581, D2839; D134644: Jahr fehlt in «Nachrichten aus dem Stadthaus des Jahres».
- D10744: Signatur mit angehängtem Schlusspunkt; D10675 hat keinen.

## Hinweise zum Material
- Die Prüfmappe wählt mehrfach eine falsche Startzeile (D2839, D1933, D3313, D134644, D414). Daraus entstehen [SIG?]-, [NACH]- und «?»-Zeilen, obwohl die Excel richtig ist. Geprüft habe ich jeweils am Excel und am PDF.
- Nachkontrolle mit den neu erzeugten Mappen (05:41, früher verdeckte Zeilen): Ich habe alle vorher verdeckten Zeilen der 10 betroffenen Dateien geprüft (D134644, D175997, D175994, D1874, D2839, D4007, D2894, D3774, D3060, D2872), per Skript (tmp_P6/werk/verdeckt.py, vorchk2.py). Es sind Umfang-, Datums-, Kopf- und Schachtelzeilen, alle bei der richtigen Einheit oder im richtigen Feld. Es gibt keine neuen Funde, die bisherigen bleiben.
- In den Kompaktmappen habe ich die verdichteten Darin-Läufe nicht Zeile für Zeile gelesen. Die [VOR]/[NACH]-Zeilen habe ich per Skript gegen die Excel geprüft (tmp_P6/werk/vorchk.py): Es sind nur Textgleichheiten, keine Verschiebung.
