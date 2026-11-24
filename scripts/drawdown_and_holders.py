# the path risk: extension notice, a Rocket Lab drop, and who would have to sell on a break
import os, json, math, datetime as dt
from collar import package, CLOSES, PRICE, SPOT, HERE
tree = json.load(open(os.path.join(HERE, '..', 'results', 'regulator_tree.json')))
DFb = math.exp(-0.0422 * 0.6); B = 28.04
jun, sep, dec = package(CLOSES[1]), package(CLOSES[2]), package(CLOSES[3])
print(f"1) End Date extension: market moves its close from Jun to Sep 2027 -> package {jun['V']:.2f} -> {sep['V']:.2f} ({sep['V']-jun['V']:+.2f}); to Dec -> {dec['V']:.2f} ({dec['V']-jun['V']:+.2f})")
for dp in (0.02, 0.05):
    print(f"   if the market also marks close odds down {dp*100:.0f} pts: about {-dp*(sep['V']-B*DFb):+.2f} more")
for s in (SPOT * 0.7, SPOT * 1.3):
    v0 = package(CLOSES[1])['V']; v1 = package(CLOSES[1], S=s)['V']
    print(f"2) Rocket Lab {s/SPOT-1:+.0%} to ${s:.2f}: Iridium package (Jun close) {v0:.2f} -> {v1:.2f} ({v1-v0:+.2f}); linear delta {jun['delta']:.3f} x {s-SPOT:+.2f} = {jun['delta']*(s-SPOT):+.2f}")
d = json.load(open(os.path.join(HERE, '..', 'data', 'irdm_13f_holders_nasdaq_2026-11-24.json')))['data']
rows = d['holdingsTransactions']['table']['rows']
arb_names = ('Balyasny', 'Tudor', 'Millennium', 'Pentwater', 'Aqr', 'Alpine', 'Magnetar', 'Qube', 'Glazer', 'Woodline', 'Jane Street')
num = lambda x: float(str(x).replace(',', '')) if str(x) not in ('', 'New') else 0.0
arb = [(r['ownerName'], num(r['sharesHeld']), r['sharesChange']) for r in rows if any(a.lower() in r['ownerName'].lower() for a in arb_names) and r['date'] == '9/30/2026']
tot = sum(x for _, x, _ in arb); so = 106.158479
print(f"3) event-driven / multi-strategy 13F holders at Sep 30 2026 (top-40 list):")
for n, x, ch in arb: print(f"   {n[:40]:40s} {x/1e6:5.2f}m  change {ch}")
print(f"   total {tot/1e6:.2f}m shares = {tot/1e6/so:.1%} of 106.16m outstanding")
adv = 688924
print(f"   at the Oct 30 average daily volume of {adv:,} shares, that is {tot/adv:.0f} trading days of volume to exit")
print(f"   IRDM short interest Oct 30: 3,031,712 shares. RKLB short interest Oct 30: 46,410,138 vs the maximum arb hedge 0.4 x {so:.2f}m = {0.4*so:.2f}m")
inst = d['ownershipSummary']['SharesOutstandingPCT']['value']
print(f"   institutional ownership {inst}; new positions in Q3: 83 holders, 7,340,273 shares")
