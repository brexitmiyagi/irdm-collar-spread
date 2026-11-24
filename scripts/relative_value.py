# Iridium's spread next to other pending US deals, same yardstick: gross return to expected close, annualised, and over bills
import csv, os, json, datetime as dt, math
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
t0 = dt.date(2026, 11, 23)
bill = lambda T: 0.0413 if T <= 0.25 else 0.0451 if T >= 1 else (0.0426 + (0.0451 - 0.0426) * (T - 0.5) / 0.5 if T > 0.5 else 0.0413 + (0.0426 - 0.0413) * (T - 0.25) / 0.25)
for r in csv.DictReader(open(os.path.join(DATA, 'other_deals_2026-11-23.csv'))):
    px = float(r['target_close']); T = (dt.date.fromisoformat(r['expected_close']) - t0).days / 365
    if r['target'] == 'GSAT':
        a = float(r['acquirer_close']); val = 0.4 * 90 + 0.6 * 0.3210 * a if a < 280.38 else 90.0
    elif r['target'] == 'NSC':
        val = float(r['acquirer_close']) + 88.82
    else:
        val = 61.25
    g = val / px - 1; ann = (1 + g) ** (1 / T) - 1
    print(f"{r['target']:5s} ({r['acquirer']}): value ${val:.2f} vs ${px:.2f}, gross {g:+.1%}, {ann:+.1%} a year, {ann-bill(T):+.1%} over bills, close {r['expected_close']}")
res = json.load(open(os.path.join(HERE, '..', 'results', 'irr_by_close_date.json')))
j = [r for r in res if r['close'] == '2027-06-30'][0]
print(f"IRDM (Rocket Lab), collar priced, Jun 30 2027 close: {j['total']:+.1%} a year if it closes, {j['excess']:+.1%} over bills; Sep 30: {res[2]['total']:+.1%} / {res[2]['excess']:+.1%}")
print("note: GSAT assumes cash elections prorated to 40% and AMZN below $280.38; Apple adjustment (up to $110m) ignored. Dividends ignored for GSAT/TXNM/NSC.")
