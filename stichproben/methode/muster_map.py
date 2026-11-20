"""Zuordnung der Musterbezeichnungen der Gruppen zu Hauptmustern (erste passende Regel gilt)."""
import re
HAUPT = {
 "M01": "Verzeichnistext als Vorspann, Schlussvermerk oder Kopfzeile verworfen",
 "M02": "Echte Signatur nicht erkannt – Einheit fehlt, Text im Darin der vorigen",
 "M03": "Zahl/Marke am Zeilenanfang als Signatur gelesen – erfundene Einheit",
 "M04": "Gliederungsebene/Überschrift nicht erkannt – Hierarchie falsch",
 "M05": "Mehrzeilige Datumsspalte – zweites Datum verloren, Folgezeile wird eigener Eintrag",
 "M06": "Rechte Spalte nicht abgetrennt – Datum/Zahl im Titel, Datumsreste",
 "M07": "Fremdtext im Darin (Schlussnotiz, Tabellenkopf, Überschrift, Kopfzeile, Einleitung)",
 "M08": "Zeilenumbruch falsch beurteilt – Titel abgeschnitten oder Folgetext im Titel",
 "M09": "Zeitraum aus falscher Quelle (Nummern, Werktitel, Lebensdaten, Notiz, geerbt)",
 "M10": "Darin falsch getrennt – Einträge verschmolzen oder zerstückelt",
 "M11": "Schachtel-Nr. falsch oder fehlt",
 "M12": "Datumsformat nicht erkannt (Jahrzehnt, «1987-88», «ff.», MM.JJJJ, Vorname «August»)",
 "M13": "Teile: Titel vom Nachbarteil, eigener Titel im Darin",
 "M14": "Mappen/Schachteln: Titel aus Überschrift vor der Marke bzw. Tabellenkopf",
 "M15": "Umfang nicht erkannt (Klammer, Titel, Darin)",
 "M16": "Zerrissene Wörter (Schriftwechsel bzw. Zeichenreihenfolge im PDF)",
 "M17": "Kosmetik (Satzzeichen, Anmerkung)",
 "M18": "Spalte «Ebene» passt nicht zur Parent-ID",
}
REGELN = [
 (r"Vorspann|als Schlussvermerk verloren|Kopf-/Fusszeile verworfen|Zwischenüberschrift verloren|als Übersichtszeile entfernt", "M01"),
 (r"^Ebene falsch", "M18"),
 (r"Mengenangabe als Signatur|Listenmarke als Signatur|Aufzählungsnummer als Signatur|Listennummer als Signatur|Fortsetzungszeile als Signatur|Datum als Signatur|Bereichssignatur als zwei|Teil erfunden|Schlussnotiz als Einheit|Überschrift als Einheit|Übersicht als Einheit|Inhaltsverzeichnis als Einheiten|Schachtelliste nicht erkannt", "M03"),
 (r"Gliederungsebene nicht erkannt|^Hierarchie falsch|Abschnitte vermischt|Schachtel-Teil an letzte|Hauptgruppe als Teil|Abschnittsüberschrift verworfen|Elterneinheit", "M04"),
 (r"^Einheit fehlt|Einheit im Darin der vorigen|Vollsignatur nicht erkannt|Schachtel-Teil fehlt|Behälter ohne Nummer|Abschnittseintrag «–» beim vorigen|Inhalt bei falscher Einheit|Text zwischen Einheiten verrutscht|Darin-Eintrag als Überschrift verworfen", "M02"),
 (r"Teilzeitraum aus Titel verloren|zweiter Zeitraum|zweite Datumszeile|erster Datumszeile|ersten Zeile|erste Datumszeile|Datum der Umfangszeile|Datum der rechten Spalte verloren|Spaltendatum|Datumsfortsetzung|aus Datumsfortsetzung|aus Fortsetzungszeile|Zeitraum der Kopfzeile|Datumszeile im Titel|Datumszeile an vorigen|^Datum als Titel|Titelrest im Darin|Ortsteil ans Titelende|Jahreszeile: Einträge verschmolzen|Einträge verschmolzen, Datum verloren|Zeitraum unvollständig", "M05"),
 (r"Datum mitten im Titel|Datumsspalte im Titel|Expl\.-Zahl|Datumsrest|Datum-Rest|Datum-/Schachtelrest|Datum am Titelende|Spaltentext im Titel|Verweis und Datum im Titel|Schachtelangabe nicht abgetrennt|Titel durch Datumsentfernung|Titeldatum in Anmerkung|Spaltenwert|Datum mitten im Darin", "M06"),
 (r"Schlussnotiz im Darin|Tabellenkopf im Darin|Überschrift im Darin|Kopfzeile im Darin|Einleitung im Darin|Biografie im Darin|Titelwiederholung im Darin|Zwischenbemerkung im Titel", "M07"),
 (r"Überschrift vor der Schachtel|Tabellenkopf im Titel", "M14"),
 (r"Titel abgeschnitten|Titelfortsetzung im Darin|Titel unvollständig|Darin-Text im Titel|Text des nächsten Eintrags|Titel fehlt|Gedankenstrich abgeschnitten|mitten im Zitat geteilt|am Doppelpunkt falsch geteilt|erster Untereintrag als Titel|Titel doppelt", "M08"),
 (r"Titel aus Nachbareinheit|Eigener Titel im Darin|Titel von falscher Einheit", "M13"),
 (r"als Jahr gelesen|Werktitel|Titeltext als Zeitraum|Inhaltsdatum|Lebensdaten|Zeitraum aus Schlussnotiz|Schlussnotiz-Datum|Nachbareinheit geerbt|falscher übergeordneter|Plannummern|Titeljahren|Jahres-Zwischenzeile|Datum der Darin-Zeile als Zeitraum|Zeitraum ohne Darin-Daten", "M09"),
 (r"Jahrzehnt|Endjahr|ff\. als|MM\.JJJJ|Zeitraum nicht erkannt|Doppeldatum|über Zeilenumbruch zerrissen|o\. J\.|Vorsatz|Vorname als Monat|Titelwort als Datum|^Zeitraum fehlt", "M12"),
 (r"Darin-Einträge verschmolzen|Darin-Eintrag zerstückelt|an « - » zerteilt|Unteraufzählung|Darin falsch getrennt|Tabellenzellen verschränkt|als Unterzeile|Unterzeilen ohne|Gedankenstrich am Zeilenanfang|Umbruch als Unterzeile", "M10"),
 (r"^Schachtel|Schachtelzeile|Schachtelangabe im Darin", "M11"),
 (r"^Umfang", "M15"),
 (r"zerrissene Wörter|Leerzeichen fehlt", "M16"),
 (r"Satzzeichen|Anmerkung unglücklich", "M17"),
]
def haupt(muster: str) -> str | None:
    for rx, k in REGELN:
        if re.search(rx, muster.strip()):
            return k
    return None
