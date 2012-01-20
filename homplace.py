import sys
import copy
import numpy

from homutils import *
from homtrans import *
from homplot  import *
from texhelp  import *

opt_draw_all = False

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

gen_cols = list(set([v[0] for n, v in vertices.iteritems()]))
gen_rows = list(set([v[1] for n, v in vertices.iteritems()]))

### print the generator table ###
doc = TexDoc (sys.stdout)
doc.begin()

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
gen_cols_s = sorted(gen_cols,reverse=True)

row_seeds = [creator.C]
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
    C = copy.deepcopy (row_seeds[k-1])
    flip_edges (C, row0, row1)
    row_seeds.append (C)
    
### Form the complices table by transformation ##########################################
cpx_tab = [ [s] for s in row_seeds ]		# table of complices
for cpx_row in cpx_tab:				# for each row of complices
    for j in range(1,len(gen_cols_s)):		# foreach column after the initial column
	col0 = set()
	col1 = set()
	for n, v in vertices.iteritems():
	    if   v[0] == gen_cols_s[j-1]:
		col0.add (n)
	    elif v[0] == gen_cols_s[j]:
		col1.add (n)
	C = copy.deepcopy (cpx_row[0])		# make a copy of the complex on the righthand column
	flip_edges (C, col0, col1)		# flip the edges
	cpx_row.insert (0, C)			# save it to the begining of the row

### Trim edges and plot complices ######################################################
for i in range(0,len(cpx_tab)):			# for each row
    for j in range(0,len(cpx_tab[i])):		# for each column
	C = cpx_tab[i][j]			# get the complex index (i,j)
	trim_edges (C)
	prefix = '-'.join(['complex',str(i),str(j)])
	for k in range(0,500):
	    if opt_draw_all:
		plotter = ComplexPlot (C)
		name = prefix + '-r' + str(k)
		plotter.draw_png (name + '.png')
	    if not C.reduce():
		p = ComplexPlot (C)
		p.draw_png (prefix + '.png')	    # plot the end result
		break
	
