# how much the implied odds move if you price the two calls anywhere inside their quotes
# low package: short call at its ask, long call at its bid. high package: the reverse.
import csv, os
from common import DATA, terms
t = terms()
q = {float(r['strike']): (float(r['bid']), float(r['ask'])) for r in csv.DictReader(open(os.path.join(DATA, 'rklb_calls_2027-06-17_quoted_2026-11-24.csv')))}
T = t['days_to_close'] / 365; DF = (1 + t['tbill_6m']) ** -T
S, i = t['rklb_close'], t['irdm_close']
def V(c1, c2): return t['cash_per_share'] * DF + 0.4 * S - 0.4 * c1 + 0.24 * c2 + 3 * t['quarterly_dividend'] * DF
mid = V((sum(q[65]) + sum(q[70])) / 4, (sum(q[110]) + sum(q[115])) / 4)
low = V((q[65][1] + q[70][1]) / 2, (q[110][0] + q[115][0]) / 2)
high = V((q[65][0] + q[70][0]) / 2, (q[110][1] + q[115][1]) / 2)
print(f"package if it closes: low {low:.2f}, mid {mid:.2f}, high {high:.2f}")
print(f"upside if it closes (PV, over bills): low {low-i:.2f}, mid {mid-i:.2f}, high {high-i:.2f}")
for B in (28.52, 35.00, 43.00):
    o = [(i - B * DF) / (v - B * DF) * 100 for v in (high, mid, low)]
    print(f"break at {B:.2f}: implied odds {o[0]:.1f}% to {o[2]:.1f}% (mid {o[1]:.1f}%), loss on break {i-B:.2f}")
