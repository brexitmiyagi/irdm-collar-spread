# one timestamp for everything: pulls Iridium and Rocket Lab prices and Rocket Lab's full option chain from Nasdaq at the
# same moment, saves them under data/, and points data/anchor.json at them. Every valuation script reads the anchor.
# usage: python pull_snapshot.py [label]   (label defaults to the date, e.g. 2026-11-24_close)
import json, os, sys, re, csv, datetime as dt, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
H = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
def quote(t):
    d = get(f'https://api.nasdaq.com/api/quote/{t}/info?assetclass=stocks')['data']['primaryData']
    return float(d['lastSalePrice'].replace('$', '').replace(',', '')), d['lastTradeTimestamp']
irdm, ti = quote('IRDM'); rklb, tr = quote('RKLB')
d = get('https://api.nasdaq.com/api/quote/RKLB/option-chain?assetclass=stocks&limit=2000&fromdate=all&todate=undefined&excode=oprac&callput=callput&money=all&type=all')['data']
mon = {m: i + 1 for i, m in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])}
c = lambda v: '' if v in (None, '--', '') else v.replace(',', '')
rows, exp = [], None
for r in d['table']['rows']:
    if r.get('expirygroup'):
        m = re.match(r'(\w+) (\d+), (\d+)', r['expirygroup']); exp = f'{m.group(3)}-{mon[m.group(1)[:3]]:02d}-{int(m.group(2)):02d}'; continue
    if r.get('strike'): rows.append([exp, float(r['strike']), c(r['c_Bid']), c(r['c_Ask']), c(r['p_Bid']), c(r['p_Ask'])])
label = sys.argv[1] if len(sys.argv) > 1 else dt.date.today().isoformat()
chain = f'rklb_option_chain_{label}.csv'
with open(os.path.join(DATA, chain), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['expiry', 'strike', 'call_bid', 'call_ask', 'put_bid', 'put_ask']); w.writerows(rows)
day = dt.datetime.strptime(re.search(r'(\w+ \d+, \d{4})', tr).group(1), '%b %d, %Y').date()
anchor = dict(label=label, date=day.isoformat(), irdm=irdm, irdm_time=ti, rklb=rklb, rklb_time=tr, rklb_chain=chain, chain_rows=len(rows))
json.dump(anchor, open(os.path.join(DATA, 'anchor.json'), 'w'), indent=1)
print(json.dumps(anchor, indent=1))
