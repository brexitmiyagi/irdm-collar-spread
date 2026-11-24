# what combinations of close date and close odds make $43.21 fair, for a range of break prices
import math, json, os, datetime as dt
from collar import package, T0, PRICE, HERE
dates = [dt.date(2027, m, 28 if m != 2 else 26) for m in range(2, 13)]
out = {}
print('close date   ' + ''.join(f'  B=${b:<5}' for b in (24, 28.04, 32, 43)))
for c in dates:
    p = package(c); row = []
    for B in (24, 28.04, 32, 43):
        need = (PRICE - B * p['DF']) / (p['V'] - B * p['DF']); row.append(need)
    out[str(c)] = dict(V=p['V'], need=row)
    print(f"{c}   " + ''.join(f"  {x*100:6.1f}%" for x in row))
tree = json.load(open(os.path.join(HERE, '..', 'results', 'regulator_tree.json')))
print(f"my estimate: close odds {tree['p']:.1%}, timing-weighted close ~{tree.get('date_label','Jun-Sep 2027')}")
json.dump(out, open(os.path.join(HERE, '..', 'results', 'market_frontier.json'), 'w'), indent=1)
