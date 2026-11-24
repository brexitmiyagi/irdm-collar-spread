# the same trade at Seeking Alpha size: what each outcome is worth on $10,000 hedged, and what an unhedged holder is really
# exposed to through the Rocket Lab leg of the collar
import datetime as dt
import collar
from timing_weights import BASE, NONREF, NONSAT, SAT, PN, NR
P0, S = collar.PRICE, collar.SPOT
sh = 10_000 / P0
print(f'$10,000 buys {sh:.0f} Iridium shares at ${P0}; the hedge is short about {0.26*sh:.0f} Rocket Lab shares (${0.26*sh*S:,.0f})')
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import decision_tree as T
px_slip, px_ext = T.branches[2][3], T.branches[3][3]
for lab, px in ((f'deal closes (any date), Rocket Lab at ${S}', 27 + 0.4 * S), ('FCC slips past June, marked then', px_slip),
                ('extension notice, marked then', px_ext), ('Party A re-bids', 43.00), ('break, Iridium on its own', 22.81)):
    print(f'  {lab:46s} Iridium ${px:6.2f}  P&L ${sh*(px-P0):+,.0f}')
c = dt.date(2027, 6, 30); base = collar.package(c)['V']
d = collar.package(c)['delta']
print(f'unhedged: model delta {d:.3f} Iridium dollars per Rocket Lab dollar, so {d*S/P0:.0%} of Rocket Lab\'s percentage moves pass through')
for x in (-10, +10):
    v = collar.package(c, S=S + x)['V']
    print(f'  Rocket Lab {x:+d} dollars: Iridium about ${v-base:+.2f} a share, ${sh*(v-base):+,.0f} on $10,000 unhedged')
# the dated call: odds the FCC grants by Mar 31 and by Apr 30 2027 on each timing sample and on the blend
def by(days, sample):
    return sum(int(x) <= days for x in sample) / len(sample)
from timing_weights import days as _days
nonsat = _days(lambda r: r['sector'] != 'satellite'); sat = _days(lambda r: r['sector'] == 'satellite')
for lab, dd in (('Mar 31 2027', dt.date(2027, 3, 31)), ('Apr 30 2027', dt.date(2027, 4, 30))):
    k = (dd - PN).days
    nr, ns, st = by(k, NR), by(k, nonsat), by(k, sat)
    print(f'FCC grant by {lab} (day {k}): not referred {nr:.0%}, referred non-satellite {ns:.0%}, referred satellite {st:.0%}, blend {0.5*nr+0.25*ns+0.25*st:.0%}')
# what the April 30 stop costs: if there's no FCC grant by Apr 30 2027, re-price on that day with the timing that's left
# (each sample's grants after day 227, blended the same way) and close odds trimmed to 92%, Rocket Lab unchanged
import math
on = dt.date(2027, 4, 30); k = (on - PN).days
cut = [(c - PN).days for c in collar.CLOSES]
def rest(sample):
    later = [int(x) for x in sample if int(x) > k]
    if not later: return None
    return [sum(cut[i - 1] < x <= cut[i] if i else x <= cut[0] for x in later) / len(later) for i in range(len(cut) - 1)] + [sum(x > cut[-2] for x in later) / len(later)]
parts = [(0.25, rest(nonsat)), (0.25, rest(sat))]        # the not-referred deals all granted by day 224, so none are left
wsum = sum(w for w, r in parts if r)
W = [sum(w * r[i] for w, r in parts if r) / wsum for i in range(4)]
T0 = collar.T0; collar.T0 = on
pv = sum(w * collar.package(c)['V'] for w, c in zip(W, collar.CLOSES) if c > on)
collar.T0 = T0
DFb = math.exp(-math.log(1.0426) * 0.25)
stop_px = 0.92 * pv / sum(w for w, c in zip(W, collar.CLOSES) if c > on) + 0.08 * (0.75 * 22.81 + 0.25 * 43.0) * DFb
print(f'no grant by Apr 30 2027: remaining timing Jun/Sep/Dec {W[1]:.0%}/{W[2]:.0%}/{W[3]:.0%}; Iridium worth about ${stop_px:.2f} then; '
      f'stop P&L on $10,000 hedged ${sh*(stop_px-P0):+,.0f} before carry')
