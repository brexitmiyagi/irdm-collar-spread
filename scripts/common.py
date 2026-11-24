import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')

def terms():
    with open(os.path.join(DATA, 'deal_terms.csv')) as f:
        return {r['item']: float(r['value']) for r in csv.DictReader(f)}

def ratio(p, t):
    # the collar. below the floor you get a fixed 0.4 share, above the cap 0.24
    if p <= t['collar_low']:
        return t['ratio_floor']
    if p >= t['collar_high']:
        return t['ratio_cap']
    return t['stock_target'] / p

def deal_value(p, t):
    return t['cash_per_share'] + ratio(p, t) * p
