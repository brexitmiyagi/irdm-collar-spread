# odds that Rocket Lab sits below $45 at closing, which makes the deal a taxable sale for US holders
# (not a closing condition: the second merger just doesn't happen). Read off Rocket Lab put spreads.
import csv, os, math, datetime as dt
import collar
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'rklb_option_chain_2026-11-24.csv'))))
def mid(e, K):
    r = next(x for x in rows if x['expiry'] == e and float(x['strike']) == K)
    return (float(r['put_bid']) + float(r['put_ask'])) / 2
# stock leg is 0.4 S out of 27 + 0.4 S; it is at least 40% when S >= 45.00
print('tax line: 0.4 S / (27 + 0.4 S) = 40% at S =', round(0.4 * 27 / (0.4 - 0.16), 2))
for e in ['2027-03-19', '2027-06-17', '2027-09-17', '2028-01-21']:
    T = (dt.date.fromisoformat(e) - collar.T0).days / 365; DF = math.exp(-collar.rate(T) * T)
    p = (mid(e, 50.0) - mid(e, 40.0)) / 10 / DF
    print(f'{e}: risk-neutral odds Rocket Lab is below about $45 = {p:.0%}  (40/50 put spread, mids)')
print('the test uses the greatest of five Rocket Lab prices around closing, so true odds are a little lower')
