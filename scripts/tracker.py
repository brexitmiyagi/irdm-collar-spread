# weekly tracker with alerts: re-pull Iridium, Rocket Lab, the 6-month bill and the FCC docket; re-price the package and
# expected value on the base inputs; flag the exit and entry conditions; append a line to results/tracker_log.csv
# usage: python scripts/tracker.py   (needs internet; Nasdaq wants a browser user agent)
import os, csv, json, math, datetime as dt, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
def get(url, browser=True):
    cmd = ['curl', '-s', '--max-time', '60'] + (['-A', UA, '-H', 'Accept: application/json, text/plain, */*'] if browser else []) + [url]
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
def last(t):
    d = json.loads(get(f'https://api.nasdaq.com/api/quote/{t}/info?assetclass=stocks'))['data']['primaryData']
    return float(d['lastSalePrice'].replace('$', '').replace(',', '')), d['lastTradeTimestamp']
def dtb6():
    rows = [l.split(',') for l in get('https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB6', browser=False).strip().splitlines()[1:]]
    rows = [r for r in rows if r[1] not in ('.', '')]
    return rows[-1][0], float(rows[-1][1]) / 100
def docket():
    d = json.loads(get('https://publicapi.fcc.gov/ecfs/filings?proceedings.name=26-257&sort=date_disseminated,DESC&limit=100&api_key=DEMO_KEY', browser=False))
    fs = d.get('filing', [])
    doj = [f for f in fs if any(k in ';'.join(x.get('name', '') for x in f.get('filers', [])) for k in ('Justice', 'NSD', 'Foreign Investment Review', 'Committee for the Assessment'))]
    return len(fs), fs[0]['date_disseminated'][:10] if fs else '', len(doj)
def main():
    import collar
    from timing_weights import BASE, BREAK_MODEL
    irdm, ts1 = last('IRDM'); rklb, ts2 = last('RKLB'); bdate, bill = dtb6(); n, newest, doj = docket()
    collar.PRICE = irdm; collar.SPOT = rklb
    pk = [collar.package(c, S=rklb) for c in collar.CLOSES]
    V = sum(a * b['V'] for a, b in zip(BASE, pk))
    DFb = math.exp(-math.log(1 + bill) * 0.6); B = 0.75 * BREAK_MODEL + 0.25 * 43.0
    ev = 0.946 * V + 0.054 * B * DFb
    implied = (irdm - B * DFb) / (V - B * DFb)
    alerts = []
    if implied < 0.93: alerts.append('BUY ZONE: implied close odds below 93% on base inputs (buy hedged unless an exit trigger has fired)')
    if rklb < 45: alerts.append('Rocket Lab below $45: deal turns taxable for US holders (not a break)')
    if n > 12: alerts.append(f'NEW FCC FILING in 26-257 (now {n}, newest {newest})')
    if doj: alerts.append('EXIT: Team Telecom / DOJ filing in the docket')
    row = dict(run=str(dt.date.today()), irdm=irdm, rklb=rklb, irdm_time=ts1, bill=bill, bill_date=bdate,
               package_base=round(V, 2), expected_value=round(ev, 2), ev_vs_bills=round(ev / irdm - 1, 4),
               implied_odds=round(implied, 4), entry_price=round(ev / 1.006, 2), fcc_filings=n, doj_filings=doj,
               alerts=' | '.join(alerts) or 'none')
    path = os.path.join(ROOT, 'results', 'tracker_log.csv'); new = not os.path.exists(path)
    if not new:
        old = open(path).readline().strip().split(',')
        if old != list(row): path = os.path.join(ROOT, 'results', 'tracker_log_v2.csv'); new = not os.path.exists(path)
    with open(path, 'a', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=list(row))
        if new: wr.writeheader()
        wr.writerow(row)
    for k, v in row.items(): print(f'{k:16s} {v}')
if __name__ == '__main__':
    main()
