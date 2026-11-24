# what close date the price is paying for: hold my close odds (94.6%), break value and Party A mix fixed, and solve for the
# single closing date that makes the deal worth exactly what Iridium trades at. Then compare it with where the FCC samples land.
import math, datetime as dt
import collar
from timing_weights import BASE, NONREF, NONSAT, SAT, BREAK_MODEL, PN, NR
DFb = math.exp(-math.log(1.0426) * 0.6)
def worth(close, p=0.946, S=collar.SPOT):
    return p * collar.package(close, S=S)['V'] + (1 - p) * (0.75 * BREAK_MODEL + 0.25 * 43.0) * DFb
def implied_close(price, p=0.946, S=collar.SPOT):
    lo, hi = collar.T0 + dt.timedelta(days=30), dt.date(2028, 12, 31)
    if worth(lo, p, S) < price: return None          # price is above even a near-immediate close
    while (hi - lo).days > 1:
        mid = lo + (hi - lo) / 2
        lo, hi = (mid, hi) if worth(mid, p, S) > price else (lo, mid)
    return lo
def mean_date(W):
    return collar.T0 + dt.timedelta(days=sum(w * (c - collar.T0).days for w, c in zip(W, collar.CLOSES)))
c = implied_close(collar.PRICE)
print(f'Iridium ${collar.PRICE} at Rocket Lab ${collar.SPOT} ({collar.A['irdm_time']}), 94.6% odds: the price pays for a close around {c:%b %d %Y}')
for p in (0.92, 0.97):
    x = implied_close(collar.PRICE, p); print(f'  at {p:.0%} odds: {x:%b %d %Y}' if x else f'  at {p:.0%} odds: no date works')
print('where the FCC samples point (grant date, from the Sep 15 2026 notice):')
med = sorted(NR)[len(NR) // 2]
print(f'  not referred, median {med} days: {PN + dt.timedelta(days=med):%b %d %Y}; range {PN + dt.timedelta(days=min(NR)):%b %d} to {PN + dt.timedelta(days=max(NR)):%b %d %Y}')
for lab, W in (('not referred', NONREF), ('referred non-satellite', NONSAT), ('referred satellite', SAT), ('blend I use', BASE)):
    print(f'  {lab:24s} expected close (probability-weighted quarter-ends): {mean_date(W):%b %d %Y}')
gap = (c - mean_date(BASE)).days
g2 = (c - (PN + dt.timedelta(days=med))).days
print(f'gap between the price\'s close date and my blend\'s expected close: {gap:+d} days; and the not-referred median grant: {g2:+d} days ({g2/30.4:.1f} months)')
# what the gap is worth: Iridium's value if it closes a few days after the not-referred median grant, and per month of delay
md = PN + dt.timedelta(days=med + 5)   # grant plus about a week to close, if nothing else is outstanding
print(f'worth at a close on {md:%b %d %Y} (not-referred median grant + 5 days): ${worth(md):.2f}, {worth(md)/collar.PRICE-1:+.2%} vs today\'s price')
for a, b in ((dt.date(2027, 3, 31), dt.date(2027, 4, 30)), (dt.date(2027, 5, 31), dt.date(2027, 6, 30))):
    print(f'  one month of delay, {a:%b} to {b:%b}: ${worth(a) - worth(b):.2f} a share')
