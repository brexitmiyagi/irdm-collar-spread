# what the market said Iridium was worth on its own, before the sale was public
import csv, os, datetime as dt
from common import HERE, DATA, terms
t = terms()
px = {dt.date.fromisoformat(r['date']): float(r['close']) for r in csv.DictReader(open(os.path.join(DATA, 'irdm_closes_2016_2026_nasdaq.csv')))}
def c(s): return px[dt.date.fromisoformat(s)]
print(f"2024 year end {c('2024-12-31')}, 2025 year end {c('2025-12-31')} ({(c('2025-12-31')/c('2024-12-31')-1)*100:.1f}%)")
print(f"SpaceX-EchoStar week: Sep 5 2025 {c('2025-09-05')} -> Sep 10 {c('2025-09-10')} ({(c('2025-09-10')/c('2025-09-05')-1)*100:.1f}%)")
w = [(v, k) for k, v in px.items() if dt.date(2025, 9, 8) <= k <= dt.date(2026, 4, 1)]
print(f"Sep 8 2025 to Apr 1 2026: low {min(w)[0]} on {min(w)[1]}, high {max(w)[0]} on {max(w)[1]}")
print(f"Feb 12 2026 (Q4 results): {c('2026-02-11')} -> {c('2026-02-12')} ({(c('2026-02-12')/c('2026-02-11')-1)*100:.1f}%)")
print(f"Jan 2 2026 {c('2026-01-02')}, Apr 1 2026 {c('2026-04-01')}")
