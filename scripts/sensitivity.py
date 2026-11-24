# does "delay costs money" survive different vol, Rocket Lab price and averaging assumptions?
from collar import package, CLOSES, SPOT
cases = [('base (spot $49.63, fitted IV)', {}), ('IV +10 pts', {'iv_shift': 0.10}), ('IV -10 pts', {'iv_shift': -0.10}),
         ('Rocket Lab $40', {'S': 40.0}), ('Rocket Lab $60', {'S': 60.0}), ('Rocket Lab at 10-day VWAP $57.30', {'S': 57.30}),
         ('10-day VWAP averaging at closing', {'avg_days': 10}), ('borrow 0%', {'q': 0.0}), ('borrow 3%', {'q': 0.03})]
print('case' + ' ' * 34 + ''.join(f'{str(c):>12}' for c in CLOSES) + '   Mar->Dec')
for lab, kw in cases:
    v = [package(c, **kw)['V'] for c in CLOSES]
    print(f"{lab:38s}" + ''.join(f'{x:12.2f}' for x in v) + f'   {v[-1]-v[0]:+.2f}  ' + ('falls every quarter' if all(a > b for a, b in zip(v, v[1:])) else 'NOT monotonic'))
