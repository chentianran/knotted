from string import *

def hom2str (ker, img):
    s = ''
    s += set2str(ker)
    if len(img) > 0:
        s += '/'
        s += set2str(img)
    return s

def set2str (x):
    s = ''
    for t in x:
        s += '<'
        s += sym2str(t)
        s += '>'
    return s

def sym2str (x):
    if x.__class__ == tuple:
        return join(list(k),'+')
    else:
        return str(x)

def hom2tex (ker, img):
    s = '$Hom = '
    if len(img) > 0:
        s += r'\frac{'
        s += set2tex(ker)
        s += r'}{'
        s += set2tex(img)
        s += r'}'
    else:
        s += set2tex(ker)
    s += '$'
    return s

def set2tex (x):
    r1 = map (lambda x: r'\langle ' + sym2tex(x) + r'\rangle ', x)
    return join (r1, r'\oplus ')

def sym2tex (x):
    if x.__class__ == tuple:
        return join(list(x),'+')
    else:
        return str(x)
