# the Iridium package = cash + 0.4 RKLB - 0.4 call(67.50) + 0.24 call(112.50)
# calls priced off the June 17 2027 RKLB chain, midpoints, strikes interpolated
# careful: the package is a present value (cash discounted at the bill), so
# package / price - 1 is the return ABOVE bills, not the total return
import csv, os
from common import DATA, terms, deal_value
t = terms()
q = {float(r['strike']): (float(r['bid']) + float(r['ask'])) / 2 for r in csv.DictReader(open(os.path.join(DATA, 'rklb_calls_2027-06-17_quoted_2026-11-24.csv')))}
c675 = (q[65] + q[70]) / 2
c1125 = (q[110] + q[115]) / 2
T = t['days_to_close'] / 365
DF = (1 + t['tbill_6m']) ** -T
p, i = t['rklb_close'], t['irdm_close']
naive = deal_value(p, t)
div = 3 * t['quarterly_dividend'] * DF
pkg = t['cash_per_share'] * DF + 0.4 * p - 0.4 * c675 + 0.24 * c1125
V = pkg + div
spread = naive - i
print(f"naive deal value {naive:.2f}, spread {spread:.2f} ({spread/i*100:.1f}%)")
print(f"call 67.50 ~ {c675:.2f}, call 112.50 ~ {c1125:.2f}, discount factor {DF:.4f}")
print(f"package {pkg:.2f}, with 3 dividends {V:.2f}")
print("where the spread goes:")
print(f"  net call sold        {0.4*c675 - 0.24*c1125:.2f}")
print(f"  time value of cash   {t['cash_per_share']*(1-DF):.2f}")
print(f"  dividends received  -{div:.2f}")
print(f"  left for break risk  {V - i:.2f}")
print(f"excess over bills {(V/i-1)*100:.2f}% over the period, {((V/i)**(1/T)-1)*100:.2f}% a year")
print(f"if it closes: payoff at close ~{V/DF:.2f}, total return {(V/DF/i-1)*100:.1f}%, {((V/DF/i)**(1/T)-1)*100:.1f}% a year")
