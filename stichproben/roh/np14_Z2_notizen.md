# Z2 – Zufallsstichprobe 2 der NP14 (18 Dateien, 386 Einheiten), Stand Skript 94ff40ba (Runde 11)

## Bilanz
- Alle 18 Dateien ganz geprüft: volle Prüfmappe (D3677 voll, nicht kompakt), Excel aller Einheiten mit ganzem Darin, Info und
  Vollständigkeit, PDF bei jedem Zweifel. Per Skript (`tmp_Z2/`): jede PDF-Zeile gegen den Text der Einheit, zu der sie nach ihrer
  Lage gehört (`poscheck.py`, 16 Dateien), D539 je Schachtel (`boxcheck.py`), D2901 von Hand. Keine Zeile steht bei einer fremden
  Einheit; Abweichungen nur dort, wo Schlussteil, Literatur oder Bestandsgeschichte im Info stehen.
- **17 ohne kritischen Fehler, 1 kritisch (D1729).** Rate 1/18 = 5,6 % (95 %-Intervall 0,1–27 %).
- Neue Funde: 1 kritisch, 4 mittel (alle D3677), 4 gering (D3677 ×3, D3509).
- 9 bekannte, offene mittlere Funde unverändert bestätigt (Z2-06 bis Z2-14, Vermerk «kein neuer Fund»): D3677 B42-Rest und B43,
  D3474 ×2, D2380 ×2, D539 B29, D151773, D3253 M12. Behoben bleiben K97 (D3677), B30 (D539) und B14 (D2901).

## Wichtigster Fund (kritisch, Z2-01)
- **D1729 V.G.b.955.:** «Der Archivbestand enthält noch eine Schachtel Hilfsregister Personalgeschäfte 1972 bis 1990.» (S. 1 y 437,
  nach :7, vor «Letzte Änderung …»). Das Stück ohne Nummer steht nur im Blatt Info, eine Bestandszeile fehlt. Soll wie D3563/D2850:
  Darin der Bestandszeile.
- **Warum übersehen:** Die Bestandszeile entsteht nur bei bestimmten Satzmustern («enthält auch», «befinden sich ferner», «liegen
  bei» …). Auch der Suchlauf `info_stuecke` sucht nur «enthält (auch|ferner|ausserdem|zudem)»; «enthält noch» und «noch n Schachteln»
  fehlen in beiden.
- **Zusatzsuche** über alle 715 Info-Blätter (`tmp_Z2/info_noch.py`): dasselbe Muster sonst nur in **D2502** (Paket Z3): «… umfasst
  neben den Brandassekuranzbüchern … noch 5 Schachteln Assekuranzscheine, Tabellen und Rechnungen.» Bitte mit Z3 abgleichen.
  D150536 ist kein Fall (Verweis auf [10.]). Vorschlag: «enthält noch», «umfasst … noch» und «noch \d+ Schachteln» aufnehmen.

## Muster aus NP13 (Muster 7) in meinen Dateien
- **Gruppenende:** In D3677 alle Gruppenenden einzeln geprüft, kein Fall. Ähnlich, aber mitten in Gruppe 1: der kursive Lückenvermerk
  «Keine Tagebücher 1811 bis 1818» steht im Darin von 1.4. Er ist kein Archivgut und steht schon bei 1., darum gering (Z2-15).
- **«n.a» als Kind:** kommt nicht vor. **Bearbeitervermerk im Darin:** keiner (Regex-Scan über alle Darin- und Titelzellen).
- **Stück ohne Nummer nur im Info:** nur D1729. Sonst steht im Info Bestandsgeschichte, Literatur oder Umfang, wie die Konvention es
  will (D3355, D2901, D3677, D3253).

## Neue mittlere Funde (alle D3677)
- Z2-02: 1.14. hat 1844 statt 1844–17.05.1845 («Ende am …» wird nicht gelesen).
- Z2-03: 3.1. beginnt 1745 (Taufdatum aus einer Personenanmerkung) statt 1818.
- Z2-04: 6.2.1. hat 1969 aus einem «Vgl.»-Literaturverweis; dadurch reichen 6.2. und 6. bis 1969.
- Z2-05: Titel von 2.4.3. und 2.5.9. sind verstümmelt, weil das Datum aus der Titelmitte entfernt wird.

## Unsicherheiten
- Z2-04: Die Farbreproduktion könnte aus dem Buch von 1969 stammen; aus dem Verweis folgt das nicht.
- D2901: Zwei Gruppen in Schachtel 8 ergeben Serie plus Teil 2. Das ist früher so angenommen worden, darum kein Fund.
- D3677 2.4.1.: «Teil 1:» und «Teil 2:» (kursiv, im Darin) lese ich als innere Gliederung wie «Mappe n:», nicht als «…, Teil n».
