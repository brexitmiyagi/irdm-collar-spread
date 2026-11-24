# what the market did to satellite names when SpaceX bought EchoStar's spectrum, and where they are now
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = {r['date']: r for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'peer_closes_2025_2026_nasdaq.csv')))}
a, b, c = rows['2025-09-05'], rows['2025-09-10'], rows['2026-11-23']
for t in ('IRDM', 'GSAT', 'ASTS', 'VSAT'):
    x, y, z = float(a[t]), float(b[t]), float(c[t])
    print(f'{t}: Sep 5 2025 {x:.2f} -> Sep 10 2025 {y:.2f} ({y/x-1:+.1%}) -> Nov 23 2026 {z:.2f} ({z/x-1:+.1%} since Sep 5 2025)')
print(f"GSAT on Sep 8 2025, the announcement day: {float(rows['2025-09-08']['GSAT']):.2f} ({float(rows['2025-09-08']['GSAT'])/float(a['GSAT'])-1:+.1%})")
