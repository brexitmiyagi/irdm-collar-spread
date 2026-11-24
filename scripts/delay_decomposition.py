# how much of the March-to-December value loss is the collar, and how much is just waiting for cash
import math
from collar import package, CLOSES, SPOT, surface
a, b = package(CLOSES[0]), package(CLOSES[-1]); q = surface()['borrow']
cash = 27 * (a['DF'] - b['DF'])
stock = 0.4 * SPOT * (math.exp(-q * a['T']) - math.exp(-q * b['T']))
calls = (-0.4 * a['c1'] + 0.24 * a['c2']) - (-0.4 * b['c1'] + 0.24 * b['c2'])
total = a['V'] - b['V']; divs = total - cash - stock - calls
print(f"Mar 31 -> Dec 28 2027: package {a['V']:.2f} -> {b['V']:.2f}, loss {total:.2f}")
print(f"  collar (short $67.50 call, long $112.50 call): {calls:.2f}")
print(f"  waiting for the $27 cash: {cash:.2f}")
print(f"  borrow drag on the stock leg: {stock:.2f}")
print(f"  extra dividends received: {divs:.2f}")
