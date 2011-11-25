import matplotlib.pyplot as plt
import networkx as nx
import itertools as iter
from string import *
from numpy import *


class Scale:

    def __init__ (self, val, scalar = 1):
        self.value = val
        self.scalar = scalar


class Complex (nx.DiGraph):

    def __init__ (self, data=None):
        nx.DiGraph.__init__(self, data)
        self.color_use = ['yellow', 'orange', 'pink', 'blue','green','red']
        self.color_map = {1:'black'}

    def scalar_color (self, s):
        if s in self.color_map:
            return self.color_map[s]
        else:
	    if len(self.color_use) > 0:
		color = self.color_use.pop()
		self.color_map[s] = color
		return color
	    else:
		return 'gray'

    def bound(self, x, y, coef=1):
        self.add_node(x)
        self.add_node(y)
        self.add_edge(x,y)
        self[x][y]['coef'] = coef
        self[x][y]['color'] = self.scalar_color(coef)

    def get_coef (self, src, dst):
	if self.has_edge (src, dst):
	    if 'coef' in self[src][dst]:
		return self[src][dst]['coef']
	    else:
		return 1
	return None
	
    def is_terminal (self, x):
        return self.out_degree(x) == 0
        
    def is_invertible (self, src, dst):
        return (1 == self.get_coef (src, dst))

    def shrink_edge (self, src, dst):
	dot  = str(src) + '-' + str(dst)	    # the new "dot" node representing the shrinked edge
	succ = self.successors   (src)		    # the point want to inherit the out-edges of the source
	pred = self.predecessors (dst)		    # the point want to inherit the in-edges of the destination
	succ.remove (dst)
	pred.remove (src)
	for p in pred:
	    for s in succ:
		c1 = self.get_coef (src, s)
		c2 = self.get_coef (p, dst)
		c3 = self.get_coef (p, s)
		c = str(c1) + ' ' + str(c2) + ' *'
		if c3:
		    c += ' ' + c3 + ' +'
		self.bound (p, s, coef=c)
	self.remove_node (src)
	self.remove_node (dst)

    def reduce (self):
	for n in self.nodes_iter():                 # for each node
	    for s in self.successors(n):	    # for each sucessor of n
		if self.is_invertible(n,s):	    # if the edge is invertible
		    self.shrink_edge(n,s)	    # shrink that edge to a point
		    return True
        return False
	
    def draw_png (self, filename):
        A = nx.to_agraph(self)
        legend  = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
        for k, v in self.color_map.items():
            if 1 != k:
                legend += '<TR><TD BGCOLOR="' + v + '"></TD><TD>' + k + '</TD></TR>'
        legend += '</TABLE>>'
        A.add_node(1, shape="plaintext", label=legend)
        A.layout(prog='dot')
        A.draw(filename)

