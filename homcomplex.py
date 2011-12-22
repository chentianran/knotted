import networkx as nx
from string import *

from homcoef import *

class Scale:

    def __init__ (self, val, scalar = 1):
        self.value = val
        self.scalar = scalar


class Complex (nx.DiGraph):

    def __init__ (self, data=None):
        nx.DiGraph.__init__(self, data)

    def bound(self, x, y, coef=1):
        self.add_node(x)
        self.add_node(y)
        self.add_edge(x,y)
        self[x][y]['coef'] = coef

    def get_coef (self, src, dst):
	if self.has_edge (src, dst):
	    if 'coef' in self[src][dst]:
		return self[src][dst]['coef']
	    else:
		return 1
	return None
	
    def set_coef (self, src, dst, coef):
	assert self.has_edge (src, dst)
	if '1' == coef:
	    self[src][dst]['coef'] = 1
	else:
	    self[src][dst]['coef'] = coef
	
    def is_terminal (self, x):
        return self.out_degree(x) == 0
        
    def is_invertible (self, src, dst):
	c = self.get_coef (src, dst)
        if 1 == c or '1' == c:
	    return True
	else:
	    return False
	

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

		if 1 == c1:
		    c = c2
		elif 1 == c2:
		    c = c1
		else:
		    c = c1 + ' ' + c2 + ' *'

		if c3:
		    c = str(c) + ' ' + str(c3) + ' +'
		self.bound (p, s, coef=c)

	self.remove_node (src)
	self.remove_node (dst)

    def reduce (self):
	for src, dst in self.edges_iter():	    # for each edge
	    if self.is_invertible (src, dst):	    # if the edge is invertible
		self.shrink_edge (src,dst)	    # shrink that edge to a point
		return True
        return False
	
