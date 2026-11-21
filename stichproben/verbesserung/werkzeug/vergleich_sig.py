"""Einheitenvergleich über (Signatur, n-tes Vorkommen) statt ID – für Läufe mit Strukturänderungen.
Aufruf: python -I vergleich_sig.py <alt> <neu> PDF [PDF …]"""
import sys, collections, openpyxl
alt, neu = sys.argv[1:3]
def lies(p):
    ws = openpyxl.load_workbook(p, read_only=True)["scope-Import"]
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r and r[0] is not None]
    n, d = collections.Counter(), {}
    for r in rows:
        n[r[2]] += 1
        d[(r[2], n[r[2]])] = r
    return d
for pdf in sys.argv[3:]:
    a, b = lies(f"{alt}/{pdf}_scope_import.xlsx"), lies(f"{neu}/{pdf}_scope_import.xlsx")
    nur_a = [k for k in a if k not in b]; nur_b = [k for k in b if k not in a]
    geaendert = [k for k in a if k in b and a[k][3:] != b[k][3:]]
    print(f"== {pdf}: alt {len(a)}, neu {len(b)}; nur alt {len(nur_a)}, nur neu {len(nur_b)}, geändert {len(geaendert)}")
    for k in nur_a: print("   - ", k[0], k[1], "|", (a[k][3] or "")[:70])
    for k in nur_b: print("   + ", k[0], k[1], "|", (b[k][3] or "")[:70])
    for k in geaendert:
        felder = [i for i in range(3, len(a[k])) if a[k][i] != b[k][i]]
        print("   ~ ", k[0], k[1], "Spalten", felder, "|", str(a[k][felder[0]])[:60], "→", str(b[k][felder[0]])[:60])
