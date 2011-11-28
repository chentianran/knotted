from itertools import *

class Prod (list):

    def __hash__ (self):
        return hash(tuple(self))

class Sum (list):
    pass

def reduce_sum (s):
    d = {}
    for x in s:
        if x in d:
            d[x] += 1
        else:
            d[x] = 1
    r = []
    for x in d.keys():
        if d[x] % 2 != 0:
            r.append(x)
    return Sum(sorted(r))

def coef_mul(x,y):
    if isinstance(x,Sum):
        if isinstance(y,Sum):
            r = []
            for xi in x:
                for yi in y:
                    r.append (coef_mul(xi,yi));
            return reduce_sum (r)
        else:
            return Sum(map (lambda xi: coef_mul(xi,y), x))
    elif isinstance (y, Sum):
        return Sum(map (lambda yi: coef_mul(x,yi), y))
    elif isinstance(x,Prod):
        r = Prod(x)
        if isinstance(y,Prod):
            r.extend(y)
        else:
            r.append(y)
        r.sort()
        return r
    elif isinstance(y,Prod):
        return coef_mul(y,x)
    elif '1' == x or 1 == x:
        return y
    elif '1' == y or 1 == y:
        return x
    else:
        return Prod(sorted([x,y]))

def coef_add(x,y):
    r = Sum()
    if isinstance(x,Sum):
        r.extend(x)
        if isinstance(y,Sum):
            r.extend(y)
        else:
            r.append(y)
    elif isinstance(y,Sum):
        return coef_add(y,x)
    else:
        r.append(x)
        r.append(y)
    return reduce_sum(r)

def reduce_coef (coef):
    stack = []
    for x in coef.split():
        if '*' == x:
            top = stack.pop()
            stack[-1] = coef_mul(stack[-1],top)
        elif '+' == x:
            top = stack.pop()
            stack[-1] = coef_add(stack[-1],top)
        else:
            stack.append(x)
    return stack[-1]


