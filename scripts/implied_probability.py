# what close odds does 43.21 price, for a few guesses at a broken deal price
# P = (price - PV(break)) / (PV(deal) - PV(break))
import os, csv
from common import DATA, terms
t = terms()
q = {float(r['strike']): (float(r['bid']) + float(r['ask'])) / 2 for r in csv.DictReader(open(os.path.join(DATA, 'rklb_calls_2027-06-17_quoted_2026-11-24.csv')))}
T = t['days_to_close'] / 365; DF = (1 + t['tbill_6m']) ** -T
p, i = t['rklb_close'], t['irdm_close']
V = t['cash_per_share'] * DF + 0.4 * p - 0.4 * (q[65] + q[70]) / 2 + 0.24 * (q[110] + q[115]) / 2 + 3 * t['quarterly_dividend'] * DF
for B in (17.76, 25.00, 28.52, 35.00, 40.00):
    Bp = B * DF
    print(f"break at {B:.2f}: implied close odds {(i - Bp) / (V - Bp) * 100:.1f}%")
print("Party A regulatory fee at 5.5% of 41 to 45:", round(0.055*41, 2), "to", round(0.055*45, 2))
