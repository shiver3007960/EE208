from math import log
def _(u, i):
    t = u / i
    return (-1000 * 101 - t * 2101) / (t - 1000)

def __(u, i):
    t = u / i
    return (100 * 31800 + t * (200 + 31800)) /(100 - t)

def ___(u, i):
    t = u / i
    r = 0
    return (1000 * 6962 + t * (2000 + 6962)) / (1000 - t)

print(__(-60.21, 1.040))
print(list(map(lambda x: log(x), map(lambda x: __(-x, 1.04), [60.21, 68.13, 74.35, 81.08, 86.93, 91.35, 94.75, 97.08, 99.14]))))