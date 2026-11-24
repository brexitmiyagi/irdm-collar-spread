# how long satellite and spectrum deals take, and what that says about Iridium's close date
import csv, os, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'deal_timing_database.csv'))))
sign = dt.date(2026, 6, 28)
days = lambda r: (dt.date.fromisoformat(r['closed_or_milestone']) - dt.date.fromisoformat(r['announced'])).days
for r in sorted(rows, key=days):
    print(f"{days(r):4d} days  {r['deal']:28s} heavy={r['cross_border_or_fcc_heavy']}")
allp = sorted(days(r) for r in rows); heavy = sorted(days(r) for r in rows if r['cross_border_or_fcc_heavy'] == 'yes')
med = lambda x: (x[len(x)//2] if len(x) % 2 else (x[len(x)//2-1] + x[len(x)//2]) / 2)
print(f"all {len(allp)} deals: median {med(allp)} days; cross-border/FCC-heavy {len(heavy)} deals: median {med(heavy)} days, range {heavy[0]} to {heavy[-1]}")
cuts = [('Mar 31 2027', dt.date(2027, 3, 31)), ('Jun 30 2027', dt.date(2027, 6, 30)), ('Sep 30 2027', dt.date(2027, 9, 30)), ('Dec 28 2027', dt.date(2027, 12, 28))]
prev = 0; w = {}
for lab, d in cuts:
    n = (d - sign).days; k = sum(1 for x in heavy if x <= n)
    w[lab] = (k - prev) / len(heavy); prev = k
    print(f"by {lab} ({n} days after signing): {k} of {len(heavy)} heavy deals done")
w['Dec 28 2027'] += (len(heavy) - prev) / len(heavy)   # any slower than the last End Date counted as a December close
print('data-derived weights: ' + ', '.join(f"{k} {v:.0%}" for k, v in w.items()))
print(f"heavy median applied to Iridium: {sign + dt.timedelta(days=med(heavy))}")
