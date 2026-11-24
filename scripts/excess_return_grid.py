# expected return above bills for a grid of close odds and break prices
import csv, os
from common import DATA, terms
t = terms()
q = {float(r['strike']): (float(r['bid']) + float(r['ask'])) / 2 for r in csv.DictReader(open(os.path.join(DATA, 'rklb_calls_2027-06-17_quoted_2026-11-24.csv')))}
T = t['days_to_close'] / 365; DF = (1 + t['tbill_6m']) ** -T
p, i = t['rklb_close'], t['irdm_close']
V = t['cash_per_share'] * DF + 0.4 * p - 0.4 * (q[65] + q[70]) / 2 + 0.24 * (q[110] + q[115]) / 2 + 3 * t['quarterly_dividend'] * DF
B = (20, 25, 28.52, 32, 35, 40)
print('odds  ' + '  '.join(f'{b:>6}' for b in B))
for pr in (0.85, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98):
    print(f'{pr:.2f}  ' + '  '.join(f'{(pr*V+(1-pr)*b*DF)/i*100-100:+5.1f}%' for b in B))
