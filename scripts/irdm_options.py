# what Iridium's own listed options show: how many strikes have two-sided quotes, how wide they are, and where open interest sits
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
f = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'data', 'irdm_option_chain_premarket_2026-11-24.csv')
rows = list(csv.DictReader(open(f)))
num = lambda v: float(v) if v else None
two = [(r, s) for r in rows for s in ('call', 'put') if num(r[s + '_bid']) and num(r[s + '_ask'])]
print(f'{os.path.basename(f)}: {len(rows)} strikes x 2 sides, {len(two)} with a two-sided quote')
w = sorted(num(r[s + '_ask']) - num(r[s + '_bid']) for r, s in two)
print(f'two-sided quote width: median ${w[len(w)//2]:.2f}, range ${w[0]:.2f} to ${w[-1]:.2f}')
oi = sorted(((int(r['put_oi']) if r['put_oi'] else 0), r['expiry'], r['strike']) for r in rows)[::-1]
print('largest put open interest:')
for n, e, k in oi[:6]: print(f'  {e} ${float(k):.2f} put: {n} contracts')
tot = sum(n for n, e, k in oi); low = sum(n for n, e, k in oi if float(k) <= 30)
print(f'total put open interest {tot}; at strikes of $30 or less {low} ({low/tot:.0%}); of that, expiring after Dec 28 2027: {sum(n for n,e,k in oi if float(k)<=30 and e>"2027-12-28")}')
