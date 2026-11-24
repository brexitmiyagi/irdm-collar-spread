# weekly tracker: re-pull Iridium, Rocket Lab, the 6-month bill and the RKLB option chain,
# re-price the package and the expected value, and append a line to results/tracker_log.csv
# usage: python scripts/tracker.py   (needs internet; Nasdaq wants a browser user agent)
import os, sys, csv, json, math, datetime as dt, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.9', 'Accept-Encoding': 'identity', 'Connection': 'close'}
def get(url, browser=True):
    # curl is more forgiving than urllib with Nasdaq's API; FRED prefers a plain request
    cmd = ['curl', '-s', '--max-time', '60'] + (['-A', UA['User-Agent'], '-H', 'Accept: application/json, text/plain, */*'] if browser else []) + [url]
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
def last(t):
    d = json.loads(get(f'https://api.nasdaq.com/api/quote/{t}/info?assetclass=stocks'))['data']['primaryData']
    return float(d['lastSalePrice'].replace('$', '').replace(',', '')), d['lastTradeTimestamp']
def dtb6():
    rows = [l.split(',') for l in get('https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB6', browser=False).strip().splitlines()[1:]]
    rows = [r for r in rows if r[1] not in ('.', '')]
    return rows[-1][0], float(rows[-1][1]) / 100
def main():
    irdm, ts1 = last('IRDM'); rklb, ts2 = last('RKLB'); bdate, bill = dtb6()
    import collar
    collar.PRICE = irdm; collar.SPOT = rklb
    tree = json.load(open(os.path.join(ROOT, 'results', 'regulator_tree.json')))
    w = [1/6, 2/6, 2/6, 1/6]
    pk = [collar.package(c, S=rklb) for c in collar.CLOSES]
    V = sum(a * b['V'] for a, b in zip(w, pk))
    DFb = math.exp(-math.log(1 + bill) * 0.6)
    p = tree['p']; B = 0.75 * 28.04 + 0.25 * 43.0
    ev = p * V + (1 - p) * B * DFb
    need = (irdm - B * DFb) / (V - B * DFb)
    row = dict(run=str(dt.date.today()), irdm=irdm, rklb=rklb, irdm_time=ts1, bill=bill, bill_date=bdate,
               naive_spread=27 + (0.4 * rklb if rklb <= 67.5 else 27 if rklb < 112.5 else 0.24 * rklb) - irdm,
               package_jun=round(pk[1]['V'], 2), package_weighted=round(V, 2), expected_value=round(ev, 2),
               ev_vs_bills=round(ev / irdm - 1, 4), odds_needed=round(need, 4), tax_line_gap=round(rklb - 45.0, 2))
    path = os.path.join(ROOT, 'results', 'tracker_log.csv'); new = not os.path.exists(path)
    with open(path, 'a', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=list(row));
        if new: wr.writeheader()
        wr.writerow(row)
    for k, v in row.items(): print(f'{k:18s} {v}')
    print('note: option surface is from the Nov 24 2026 chain; rerun option_surface.py on a fresh chain for a full refresh')
if __name__ == '__main__':
    main()
