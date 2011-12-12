import sys
import copy
import numpy
#import itertools

from homutils import *
from homplot  import *
from texhelp  import *

creator = ComplexCreator()

groups = []
generators = []
rules = {}
points = {}
vertices = {}

for line in sys.stdin.readlines():
    p, sep, c = line.partition(':')
    if ':' == sep:
	p = p.strip()		# name of the point
	c = c.strip()		# coordinate string of the point
	points[p] = numpy.fromstring(c, sep=',')
    else:
	lst = line.split()
	if lst:
	    if 'group' == lst[0].strip():
		groups.append (lst[1:])
		continue
	    elif 'to' == lst[1]:
		if len(lst) > 4 and 'with' == lst[3]:
		    coef = lst[4]
		    if lst[0] in rules:
			rules[lst[0]].append( (lst[2], coef) )
		    else:
			rules[lst[0]] = [ (lst[2], coef) ]
		    continue
	    print 'Sorry, I did not understand the command:'
	    print line

generators = cartesian_prod (groups)	    # enumerate the generators

### generate the first complex ###
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
        creator.execute(''.join(g) + '~' + ' + '.join(terms))

### compute minkowski sum ###
for g in generators:
    val = numpy.zeros(2)
    for x in g:
	val += points[x]
    name = ''.join(g)
    vertices[name] = val

### print the generator table ###
doc = TexDoc (sys.stdout)
doc.begin()

gen_cols = list(set([v[0] for n, v in vertices.iteritems()]))
gen_rows = list(set([v[1] for n, v in vertices.iteritems()]))
gen_tab  = [ [''] + ['$' + str(x) + '$' for x in sorted(gen_cols) ] ]

for r_coord in sorted (gen_rows, reverse=True):
    row = [ str(r_coord) ]
    for c_coord in sorted (gen_cols):
	gs = []
	for n, v in vertices.iteritems():
	    if v[0] == c_coord and v[1] == r_coord:
		gs.append(n)
	row.append ('$' + ','.join(gs) + '$')
    gen_tab.append (row)

doc.table (gen_tab)
doc.end()
    
gen_rows_s = sorted(gen_rows,reverse=True)
r0 = gen_rows_s[0]
r1 = gen_rows_s[1]
plotter = ComplexPlot (creator.C)
plotter.draw_png('complex0' + '.png')
row0 = set()
row1 = set()
for n, v in vertices.iteritems():
    if v[1] == r0:
	row0.add (n)
    elif v[1] == r1:
	row1.add (n)

print 'row0', row0
print 'row1', row1
new_cpx = copy.deepcopy (creator.C)
for src, dst in new_cpx.edges_iter():
    if (src in row0 and dst in row1) or (src in row1 and dst in row0):
	coef = new_cpx.get_coef (src, dst)
	new_cpx.set_coef (src, dst, coef[::-1])
	print src, dst, coef, coef[::-1]
plotter = ComplexPlot (new_cpx)
plotter.draw_png('complex1' + '.png')



    
