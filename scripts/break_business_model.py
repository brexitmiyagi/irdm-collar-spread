# a broken Iridium, line by line: Q3 2026 revenue run-rate by line, explicit flow-through to OEBITDA (my assumptions,
# calibrated so the base case equals the $532m run-rate), direct-to-device erosion cases, EMSS repricing, and a multiple range
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
q = {r['line']: int(r['q3_2026_k']) / 1000 * 4 for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'irdm_revenue_q3_2026.csv'))) if r['line'] != 'total'}
NET_DEBT, SHARES, BASE = 2061.605, 108.926, 532.0
flow = {'voice_and_data': 0.85, 'broadband': 0.85, 'iot_data': 0.85, 'hosted_payload_and_other': 0.70,
        'government_services': 0.85, 'subscriber_equipment': 0.35, 'engineering_and_support': 0.20}
contrib = sum(q[k] * flow[k] for k in q); fixed = contrib - BASE
print('annualized Q3 2026 revenue by line ($m): ' + ', '.join(f'{k} {v:.0f}' for k, v in q.items()))
print(f'contribution at assumed flow-through {contrib:.0f}; implied fixed costs {fixed:.0f}; base OEBITDA {BASE:.0f}')
EXPOSED = {'voice_and_data': 1.0, 'broadband': 1.0, 'iot_data': 0.5, 'subscriber_equipment': 1.0}   # share of each line exposed to D2D
def oebitda(erosion, emss_cut, years=2):
    tot = -fixed
    for k, v in q.items():
        g = (1 - erosion * EXPOSED.get(k, 0)) ** years
        v2 = v * g
        if k == 'government_services': v2 = v * (1 - emss_cut)
        tot += v2 * flow[k]
    return tot
price = lambda e, m: (e * m - NET_DEBT) / SHARES
print('break value a share (2028 OEBITDA, two years of erosion), by multiple 7.5x / 9.5x / 11.5x:')
grid = {}
for ero in (0.0, 0.05, 0.10, 0.20):
    for emss in (0.0, 0.20):
        e = oebitda(ero, emss)
        vals = [price(e, m) for m in (7.5, 9.5, 11.5)]; grid[(ero, emss)] = vals
        print(f'  D2D erosion {ero:.0%}/yr, EMSS cut {emss:.0%}: OEBITDA {e:.0f} -> ' + ' / '.join(f'{v:.2f}' for v in vals))
w = {(0.0, 0.0): 0.15, (0.05, 0.0): 0.30, (0.10, 0.0): 0.20, (0.05, 0.20): 0.15, (0.10, 0.20): 0.10, (0.20, 0.0): 0.05, (0.20, 0.20): 0.05}
ev = sum(p * grid[k][1] for k, p in w.items())
print(f'weighted at 9.5x across my case weights: {ev:.2f}; at 7.5x: {sum(p*grid[k][0] for k,p in w.items()):.2f}')
print('the $183.4m interest-free Aireon seller loan falls due Jul 2 2027 if the deal has not closed; it is already in net debt, so a break means refinancing it, not a new hole')
