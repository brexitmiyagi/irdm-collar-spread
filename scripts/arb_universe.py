# Iridium's spread against 14 other pending US deals, same yardstick, by risk class
import csv, os, json, datetime as dt
from collar import package, CLOSES, PRICE, HERE
t0 = dt.date(2026, 11, 23)
bill = lambda T: 0.0413 if T <= 0.25 else 0.0451 if T >= 1 else (0.0426 + (0.0451 - 0.0426) * (T - 0.5) / 0.5 if T > 0.5 else 0.0413 + (0.0426 - 0.0413) * (T - 0.25) / 0.25)
rows = []
for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'arb_universe_2026-11-23.csv'))):
    T = (dt.date.fromisoformat(r['expected_close']) - t0).days / 365
    g = float(r['value']) / float(r['target_price']) - 1; ann = (1 + g) ** (1 / T) - 1
    rows.append(dict(t=r['target'], acq=r['acquirer'], gross=g, ann=ann, exc=ann - bill(T), T=T, reg=r['regulatory_heavy'], stk=r['stock_component'], xb=r['cross_border'], fee=r['buyer_regulatory_fee']))
tree = json.load(open(os.path.join(HERE, '..', 'results', 'regulator_tree.json')))
jun = package(CLOSES[1]); Tw = tree['Tw']
irdm = dict(t='IRDM', acq='Rocket Lab', gross=jun['V'] / jun['DF'] / PRICE - 1, ann=(jun['V'] / jun['DF'] / PRICE) ** (1 / jun['T']) - 1, exc=(jun['V'] / PRICE) ** (1 / jun['T']) - 1, T=jun['T'], reg='yes', stk='yes', xb='yes', fee='none')
irdm_w = dict(irdm, t='IRDM (data-weighted timing)', exc=(tree['V'] / PRICE) ** (1 / Tw) - 1, ann=None)
allr = sorted(rows + [irdm], key=lambda x: x['exc'], reverse=True)
print(f"{'deal':10s} {'acquirer':26s} {'gross':>7s} {'a year':>8s} {'over bills':>11s}  reg stock xborder  buyer reg fee")
for x in allr:
    print(f"{x['t']:10s} {x['acq'][:26]:26s} {x['gross']:+7.1%} {x['ann']:+8.1%} {x['exc']:+11.1%}   {x['reg']:3s} {x['stk']:5s} {x['xb']:7s}  {x['fee']}")
rank = [x['t'] for x in allr].index('IRDM') + 1
print(f"IRDM (Jun 30 close) ranks {rank} of {len(allr)} by excess return a year")
reg = sorted([x for x in allr if x['reg'] == 'yes'], key=lambda x: x['exc'], reverse=True)
print(f"among {len(reg)} regulatory-heavy deals IRDM ranks {[x['t'] for x in reg].index('IRDM')+1}; median excess of the others {sorted(x['exc'] for x in reg if x['t']!='IRDM')[len(reg)//2-1]:+.1%}")
print(f"IRDM with data-weighted timing: {irdm_w['exc']:+.1%} a year over bills (collar priced, before break risk)")
print("note: value and close basis per data/arb_universe_2026-11-23.csv; CVRs, dividends and the GSAT Apple adjustment not valued")
