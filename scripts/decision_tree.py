# the page clients use: each branch with its probability, the date it resolves, Iridium's price then (Rocket Lab held at $49.63),
# and the dollar P&L on a $20m hedged position
import math, datetime as dt
import collar
from timing_weights import BASE, BREAK_MODEL
p = 0.946; S = collar.SPOT; P0 = collar.PRICE
deal = 27 + 0.4 * S                           # what one Iridium share converts into at Rocket Lab $49.63 (below the $67.50 cap)
def reprice(on, close, odds, brk):
    T0 = collar.T0; collar.T0 = on
    V = collar.package(close)['V']; collar.T0 = T0
    T = (close - on).days / 365; DFb = math.exp(-math.log(1.0426) * max(T, 0.25) / 2)
    return odds * V + (1 - odds) * brk * DFb
B = 0.75 * BREAK_MODEL + 0.25 * 43.0
branches = [
    ('FCC grants by Mar 31 2027, deal closes', p * BASE[0], dt.date(2027, 3, 31), deal),
    ('FCC grants Apr-Jun 2027, deal closes', p * BASE[1], dt.date(2027, 6, 30), deal),
    ('FCC slips past June (clock stop or a fight over conditions) seen ~Feb 2027, close Sep 2027', p * BASE[2], dt.date(2027, 2, 15), reprice(dt.date(2027, 2, 15), dt.date(2027, 9, 30), 0.92, B)),
    ('End Date extension notice Jun 28 2027, close Dec 2027', p * BASE[3], dt.date(2027, 6, 28), reprice(dt.date(2027, 6, 28), dt.date(2027, 12, 28), 0.90, B)),
    ('Break, Party A re-bids', (1 - p) * 0.25, dt.date(2027, 6, 30), 43.0),
    ('Break, standalone', (1 - p) * 0.75, dt.date(2027, 6, 30), BREAK_MODEL),
]
shares = 20_000_000 / P0
print(f'$20m position = {shares:,.0f} Iridium shares, hedged with {0.26*shares:,.0f} Rocket Lab shares short')
tot = 0
for name, pr, when, px in branches:
    pnl = shares * (px - P0); tot += pr * pnl
    print(f'{name:72s} p {pr:5.1%}  {when}  Iridium ${px:6.2f}  P&L ${pnl/1e6:+6.2f}m')
print(f'branch prices assume Rocket Lab stays at ${S}; P&L is before financing, dividends and borrow (expected value net of all of those is in expected_value.py)')
