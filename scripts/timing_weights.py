# shared close-date weights. Two FCC samples: transfers Team Telecom formally reviewed (non-satellite and satellite), and large
# transfers the FCC did not refer at all. Iridium's notice says it was not referred (courtesy copy only), so the non-referred set
# gets half the weight and the two referred sets a quarter each.
import csv, os, datetime as dt
import collar
HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'fcc_team_telecom_transfers_ecfs.csv'))))
PN = dt.date(2026, 9, 15)
CUT = [(c - PN).days for c in collar.CLOSES]
def days(sel): return sorted(int(r['days']) for r in ROWS if r['outcome'] == 'granted' and sel(r))
def weights(sel):
    g = days(sel); c = [sum(x <= k for x in g) / len(g) for k in CUT]
    return [c[0], c[1] - c[0], c[2] - c[1], 1 - c[2]]
NONSAT = weights(lambda r: r['sector'] != 'satellite')
SAT = weights(lambda r: r['sector'] == 'satellite')
REFERRED = [(a + b) / 2 for a, b in zip(NONSAT, SAT)]          # the old 50/50 base, kept for comparison
NR = sorted(int(r['days']) for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'fcc_nonreferred_transfers.csv'))))
_c = [sum(x <= k for x in NR) / len(NR) for k in CUT]
NONREF = [_c[0], _c[1] - _c[0], _c[2] - _c[1], 1 - _c[2]]
BASE = [0.5 * n + 0.25 * a + 0.25 * b for n, a, b in zip(NONREF, NONSAT, SAT)]
BREAK_MODEL = 22.81   # probability-weighted standalone value from break_business_model.py at 9.5x
