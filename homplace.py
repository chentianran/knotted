import sys
import copy
import numpy

from homutils import *
from homtrans import *
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
    
plotter = ComplexPlot (creator.C)
plotter.draw_png('complex-0' + '.png')

gen_rows_s = sorted(gen_rows,reverse=True)
gen_cols_s = sorted(gen_cols,reverse=True)

row_seed = [creator.C]

for k in range(1,len(gen_rows_s)):
    r0 = gen_rows_s[k-1]
    r1 = gen_rows_s[k]
    row0 = set()
    row1 = set()
    for n, v in vertices.iteritems():
	if v[1] == r0:
	    row0.add (n)
	elif v[1] == r1:
	    row1.add (n)

    new_cpx = copy.deepcopy (row_seed[k-1])
    flip_edges (new_cpx, row0, row1)
    plotter = ComplexPlot (new_cpx)
    plotter.draw_png('complex-' + str(k) + '.png')
    row_seed.append (new_cpx)
    
for i in range(0,len(row_seed)):	    # for each row
    C_from = row_seed[i]		    # start from the row seed
    for j in range(1,len(gen_cols_s)):	    # foreach column after the initial column
	col0 = set()
	col1 = set()
	for n, v in vertices.iteritems():
	    if   v[0] == gen_cols_s[j-1]:
		col0.add (n)
	    elif v[0] == gen_cols_s[j]:
		col1.add (n)
	C_to = copy.deepcopy (C_from)
	flip_edges (C_to, col0, col1)
	C_trim = copy.deepcopy (C_to)
	trim_edges (C_trim)
	plotter = ComplexPlot (C_trim)
	plotter.draw_png('complex-' + str(i) + '-' + str(j) + '.png')
	C_from = C_to			    # the next one start from here

