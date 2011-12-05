#!/usr/bin/python

import sys
import string
import itertools

groups = []
rules = {}

for line in sys.stdin.readlines():
    lst = line.split()
    if lst:
        if 'group' == lst[0].strip():
            groups.append (lst[1:])
        elif 'to' == lst[1]:
            if len(lst) > 4 and 'with' == lst[3]:
		coef = lst[4]
            else:
		coef = 1
	    if lst[0] in rules:
		rules[lst[0]].append( (lst[2], coef) )
	    else:
		rules[lst[0]] = [ (lst[2], coef) ]
        else:
            print 'Sorry, I did not understand the command:'
            print line

generators = []
for g in groups:
    if not generators:
        generators = g
    else:
        new_gen = []
        for p, x in itertools.product (generators, g):
            new_p = list(p)
            new_p.append(x)
            new_gen.append (new_p)
        generators = new_gen

for g in generators:
    terms = []
    for i in range(0,len(g)):
        if g[i] in rules:
            for rule in rules[g[i]]:
		dst = list(g)
		dst[i] = rule[0]
		if 1 == rule[1]:
		    terms.append (''.join(dst))
		else:
		    terms.append (rule[1] + '*' + ''.join(dst))
    if terms:
        print ''.join(g), '~', ' + '.join(terms)

