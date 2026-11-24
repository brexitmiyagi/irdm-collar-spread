# daily Iridium close vs the deal valued at that day's Rocket Lab close
# note: the real ratio uses a 10 day VWAP before closing, I use the close as a proxy
import csv, os
from common import HERE, DATA, terms, deal_value
t = terms()
rows = list(csv.DictReader(open(os.path.join(DATA, 'daily_closes_nasdaq.csv'))))
out = []
for r in rows:
    if r['date'] < '2026-06-26':
        continue
    i, k = float(r['irdm']), float(r['rklb'])
    dv = deal_value(k, t)
    out.append((r['date'], i, k, round(dv, 2), round(dv - i, 2), round((dv - i) / i * 100, 1)))
with open(os.path.join(HERE, '..', 'results', 'spread_history.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['date', 'irdm', 'rklb', 'deal_value', 'spread_usd', 'spread_pct']); w.writerows(out)
last = out[-1]
print(f"latest {last[0]}: IRDM {last[1]}, RKLB {last[2]}, deal value {last[3]}, spread ${last[4]} ({last[5]}%)")
print('first RKLB close at or below 67.50:', next(o[0] for o in out if o[2] <= 67.5))
above = [o for o in out if o[1] > o[3]]
print('last day IRDM closed above deal value:', above[-1][0], above[-1][1])
r = {o[0]: o for o in out}
a, b = r['2026-10-09'], r['2026-10-16']
print(f"Oct 9 to Oct 16: RKLB {a[2]} -> {b[2]} ({(b[2]/a[2]-1)*100:.1f}%), deal value -{a[3]-b[3]:.2f} at formula 0.4 x move = {0.4*(a[2]-b[2]):.2f}, IRDM -{a[1]-b[1]:.2f}")
print(f"RKLB since Jun 26: {(last[2]/r['2026-06-26'][2]-1)*100:.1f}%")
