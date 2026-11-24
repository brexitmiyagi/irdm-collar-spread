# every number the article quotes, computed from the current anchor (data/anchor.json) and written to results/article_numbers.json,
# so the text can be rebuilt for any timestamp without retyping numbers
import io, json, os, math, contextlib, datetime as dt, csv
HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    import collar, expected_value as EV, tornado as TO, implied_timing as IT, holder_view as HV, decision_tree as DT
    from timing_weights import BASE, NONREF, NONSAT, SAT, BREAK_MODEL, PN, NR
P, S = collar.PRICE, collar.SPOT
m = lambda x: f'{x:,.2f}'
pct = lambda x: f'{abs(x)*100:.1f}%'   # one decimal: the inputs don't support more
d = lambda x: f'{x:%B} {x.day}, {x.year}'
v = {}
v['when'] = collar.A['irdm_time']; v['P'] = m(P); v['S'] = m(S); v['deal'] = m(27 + 0.4 * S)
v['gross'] = f'{(27 + 0.4 * S) / P - 1:.1%}'
base = EV.ev(BASE)[1]; v['base'] = m(base); v['base_vs'] = pct(base / P - 1); v['base_dir'] = 'above' if base >= P else 'below'
v['ev97'] = m(EV.ev(BASE, 0.97)[1]); v['entry'] = m(base / 1.006); v['odds_now'] = f'{EV.implied_odds(P):.1%}'
for k, W in (('nr', NONREF), ('ns', NONSAT), ('sat', SAT)):
    e = EV.ev(W)[1]; v[k] = m(e); v[k + '_vs'] = pct(e / P - 1); v[k + '_dir'] = 'over' if e >= P else 'under'; v[k + '_entry'] = m(e / 1.006)
v['pa0'] = f'{EV.ev(BASE, 0.946, 0.0)[1] / P - 1:+.1%}'; v['pa50'] = f'{EV.ev(BASE, 0.946, 0.5)[1] / P - 1:+.1%}'
ic = IT.implied_close(P); v['ic'] = d(ic) if ic else 'no date'
for p, k in ((0.92, 'ic92'), (0.97, 'ic97')):
    x = IT.implied_close(P, p); v[k] = d(x) if x else 'no date in range'
med = PN + dt.timedelta(days=sorted(NR)[len(NR) // 2])
v['gap'] = str((ic - med).days) if ic else 'n/a'; v['blend_close'] = d(IT.mean_date(BASE))
md = med + dt.timedelta(days=5); w = IT.worth(md); v['fast'] = m(w); v['fast_vs'] = pct(w / P - 1)
v['delay_spring'] = m(IT.worth(dt.date(2027, 3, 31)) - IT.worth(dt.date(2027, 4, 30))); v['delay_june'] = m(IT.worth(dt.date(2027, 5, 31)) - IT.worth(dt.date(2027, 6, 30)))
for name, lo, hi in TO.cases:
    key = {'close odds 92% / 98%': 'to_odds', 'break price $15 / $28': 'to_break', 'Party A returns 0% / 50%': 'to_pa',
           'timing: referred satellite / not referred': 'to_time', 'Rocket Lab implied vol +10 / -10 pts': 'to_vol'}[name]
    v[key] = f'{abs(hi - lo) * 100:.1f}'
v['to_time_lo'] = f'{TO.ev(W=SAT):+.1%}'; v['to_time_hi'] = f'{TO.ev(W=NONREF):+.1%}'
sh = 10_000 / P; v['sh'] = f'{sh:.0f}'; v['hsh'] = f'{0.26 * sh:.0f}'
br = {b[0]: b[3] for b in DT.branches}
pl = lambda px: f'{"+" if px >= P else "-"}${abs(sh * (px - P)):,.0f}'
v['pl_close'] = pl(27 + 0.4 * S); v['px_slip'] = m(DT.branches[2][3]); v['pl_slip'] = pl(DT.branches[2][3])
v['pl_ext'] = pl(DT.branches[3][3]); v['pl_pa'] = pl(43.0); v['pl_break'] = pl(BREAK_MODEL)
v['stop_px'] = m(HV.stop_px); v['pl_stop'] = pl(HV.stop_px)
c = dt.date(2027, 6, 30); b0 = collar.package(c)['V']; dl = collar.package(c)['delta']
v['delta_c'] = f'{dl * 100:.0f}'; v['pass'] = f'{dl * S / P:.0%}'
dn = collar.package(c, S=S - 10)['V'] - b0; v['dn10'] = m(abs(dn)); v['dn10_10k'] = f'{abs(sh * dn):,.0f}'
for s_, k in ((45, 'h45'), (50, 'h50'), (60, 'h60')): v[k] = f'{collar.package(c, S=s_)["delta"]:.3f}'
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', collar.A['rklb_chain']))))
def pmid(e, K):
    r = next(x for x in rows if x['expiry'] == e and float(x['strike']) == K); return (float(r['put_bid']) + float(r['put_ask'])) / 2
T = (dt.date(2027, 6, 17) - collar.T0).days / 365
v['tax_odds'] = f'{(pmid("2027-06-17", 50.0) - pmid("2027-06-17", 40.0)) / 10 / math.exp(-collar.rate(T) * T):.0%}'
v['tax_gap'] = f'{abs(S - 45):.2f}'; v['tax_side'] = 'above' if S >= 45 else 'below'
# the dated call, grant odds by Mar 31 and Apr 30 2027 on the not-referred deals alone and on the 50/25/25 blend
for lab, dd in (('mar', dt.date(2027, 3, 31)), ('apr', dt.date(2027, 4, 30))):
    k = (dd - PN).days
    nr_, ns_, st_ = HV.by(k, NR), HV.by(k, HV.nonsat), HV.by(k, HV.sat)
    v['g_' + lab + '_nr'] = f'{nr_:.0%}'; v['g_' + lab] = f'{0.5*nr_ + 0.25*ns_ + 0.25*st_:.0%}'
v['nr_n'] = str(len(NR)); v['nr_med'] = (PN + dt.timedelta(days=int(sorted(int(x) for x in NR)[len(NR)//2 - 1] / 2 + sorted(int(x) for x in NR)[len(NR)//2] / 2))).strftime('%B %-d, %Y')
w = [f'{x:.0%}' for x in BASE]; v['w_mar'], v['w_jun'], v['w_sep'], v['w_dec'] = w
w = [f'{x:.0%}' for x in NONREF]; v['nw_mar'], v['nw_jun'], v['nw_sep'], v['nw_dec'] = w
# the signposts table, the referral-class split and the borrow sensitivity (signposts.py)
with contextlib.redirect_stdout(io.StringIO()):
    import signposts as SPT
for (lab, g, e), k in zip(SPT.rows, ('sp_base', 'sp_doj', 'sp_fx', 'sp_m14', 'sp_rk')):
    v[k + '_g'] = f'{g:.0%}'; v[k + '_e'] = m(e); v[k + '_buy'] = m(e / 1.006); v[k + '_chg'] = f'{"+" if e >= base else "-"}${abs(e - base):.2f}'
v['cc_fast'] = m(SPT.FAST_WORTH); v['cc_fast_vs'] = pct(SPT.FAST_WORTH / P - 1)
for q, k in ((0.02, 'b2'), (0.04, 'b4'), (0.08, 'b8')): v[k] = m(SPT.BORROW[q] / 1.006)
# decision-tree branch odds, whole percentages
for (name, pr, when, px), k in zip(DT.branches, ('t_mar', 't_jun', 't_slip', 't_ext', 't_pa', 't_brk')): v[k] = f'{pr:.0%}'
json.dump(v, open(os.path.join(HERE, '..', 'results', 'article_numbers.json'), 'w'), indent=1)
print(json.dumps(v, indent=1))
