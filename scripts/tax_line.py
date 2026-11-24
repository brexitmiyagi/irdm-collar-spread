# tax free only if stock is at least 40% of total consideration
# with 27 cash and a fixed 0.4 ratio: 0.4P / (27 + 0.4P) >= 0.4  ->  P >= 45
from common import terms
t = terms()
c, r, e = t['cash_per_share'], t['ratio_floor'], t['equity_threshold']
P = e * c / (r * (1 - e))
print(f"RKLB price where the stock leg is 40%: {P:.2f}")
p = t['rklb_close']
print(f"at {p}: stock share {r*p/(c+r*p)*100:.1f}%, stock leg ${r*p:.2f}")
print(f"stock leg at the line: ${r*P:.2f}")
