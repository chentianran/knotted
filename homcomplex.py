import matplotlib.pyplot as plt
import networkx as nx
import itertools as iter
from string import *
from numpy import *

class Scale:

    def __init__ (self, val, scalar = 1):
        self.value = val
        self.scalar = scalar

def is_simple_rel (r):
    if isinstance (r, tuple):			# if it is a sum
	if len(r) == 2:				# if the relation is of the form "x = y"
	    if not isinstance(r[0],Scale):
		if not isinstance(r[1],Scale):
		    return True
    return False
    
def swap_var (e, swp):
    if isinstance (e, Scale):
	return Scale (swap_var(e.value, swp), e.scalar)
    elif isinstance (e, tuple):
	r = []
	for x in e:
	    r.append (swap_var(x,swp))
	return tuple(r)
    elif e in swp:			    # if it is marked to be swapped
	return swp[e]
    return e


class HomComplex(nx.DiGraph):

    def __init__ (self, data=None):
        nx.DiGraph.__init__(self, data)
        self.L_dict = {}
        self.levels = {}
        self.components = []
        self.color_use = ['yellow', 'orange', 'pink', 'blue','green','red']
        self.color_map = {}

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

    def bound(self, x, y):
        self.add_node(x)
        self.add_node(y)
        self.add_edge(x,y)

    def bound_with(self, x, y, scalar):
        self.add_node(x)
        self.add_node(y)
        self.add_edge(x,y)
        self[x][y]['label'] = scalar
        self[x][y]['color'] = self.scalar_color(scalar)

    def get_coef (self, src, dst):
	if self.has_edge (src, dst):
	    if 'label' in self[src][dst]:
		return self[src][dst]['label']
	    else:
		return 1
	return None
	
    def succ_of (self, x):
        ss = []
        for y in self.successors(x):
            if 'label' in self[x][y]:
                label = self[x][y]['label']
                ss.append (Scale (val=y, scalar=label))
            else:
                ss.append (y)
        return ss
                
    def clean(self):
        self.clear()
        self.L_dict.clear()
        self.levels.clear()

    def is_terminal (self, x):
        return self.out_degree(x) == 0
        
    def is_invertible (self, src, dst):
	if 'label' in self[src][dst]:
	    return False
	else:
	    return True

    def remove_acyclic(self):
        cont = True
        while (cont):
            cont = False
            for n in self.nodes_iter():             # for each node
                if self.out_degree(n) == 1:         # if the node has just one son
                    succ = self.succ_of (n)         # successor: the son
                    if not isinstance(succ,Scale):  # as long as the son is not a scaling product
                        if self.is_terminal(succ):  # if the son has no leads to nothing
                            self.remove_node(succ)  # then we have an acyclic subcomplex
                            self.remove_node(n)     # remove both
                            cont = True             # we should run through this again
                            break                   # done

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
		self.bound_with (p, s, c)
	self.remove_node (src)
	self.remove_node (dst)

    def reduce (self):
	for n in self.nodes_iter():             # for each node
	    for s in self.successors(n):	    # for each sucessor of n
		if self.is_invertible(n,s):	    # if the edge is invertible
		    self.shrink_edge(n,s)	    # shrink that edge to a point
		    return
	
    def meaningful_sum (self, s):
        for t in s:		                    # for each term in this sum
            if self.out_degree(t) == 0:             # if one term in the sum is going no where
                return False                        # then this sum is meaningless
        return True                                 # if every term has a boundary, then the sum is meaningful

    def sum_in_ker (self, s):
        img_dict = {}		                    # dictionary to keep track of the times each image appear
        for t in s:		                    # for each term in this sum
            t_img = self.succ_of (t)                # the image of the ith term
            for ti in t_img:	                    # for each term in the image
                if ti in img_dict:
                    img_dict[ti] += 1
                else:
                    img_dict[ti]  = 1
        for im in img_dict:
            if 0 != (img_dict[im] % 2):             # if the coefficients of any image does not add up to zero
                return False                        # then this sum is not in the kernel
        return True

    def ker (self):
        kernel = set()
        possible = []

        in_ker = {}				    # this dictionary keeps track of the objects already in kernel
        for n in self.nodes_iter():                 # for each node
            if self.is_terminal(n):                 # if this node goes to nothing (zero)
                kernel.add(n)                       # then it is in the kernel
                in_ker[n] = 1			    # mark this to be in kernel

        for L in self.levels.keys():		    # for each level
            level = self.levels[L]                  # nodes in this level
            for c in range (2, len(level) + 1):     # for each possible sum length
                for p in iter.combinations(level,c):# for each sum in the possible pool
                    if self.meaningful_sum(p):      # if the sum is indeed meaningful
                        if p not in in_ker:	    # if this sum is not already in the kernel
                            if self.sum_in_ker(p):  # if the sum is in kernel
                                kernel.add(p)       # then add it to the kernel
                                in_ker[p] = 1	    # mark that sum to be in kernel already
        return kernel                               # return the kernel

    def img (self):
        image = set()
        for n in self.nodes_iter():                 # for each node
            s = self.succ_of(n)
            if len(s) == 1:                         # if this node goes just one thing
                image.add(s[0])                     # then that thing is in the image
            elif len(s) > 1:                        # if this node goes to a sum of things
                image.add(tuple(s))                 # form the sum as a tuple, and the sum is in the image
        return image

    def hom (self):
        if not nx.is_weakly_connected(self):
            all_ker = set()
            all_img = set()
            for c in nx.weakly_connected_component_subgraphs(self):
                sub = HomComplex(data=c)
                k, i = sub.hom()
                all_ker = all_ker | k
                all_img = all_img | i
            return (all_ker, all_img)

        self.remove_acyclic()			    # first remove all the acyclic subcomplices
        self.assign_level()                         # assign levels

        ker = self.ker()                            # the kernel
        img = self.img()                            # the image
        com = ker.intersection(img)                 # the intersection of the two

        ker.difference_update(com)                  # remove the intersection from the kernel
        img.difference_update(com)                  # remove the intersection from the image

        var_swp = {}				    # the dictionary for change of variables
        #ker_del = set()
        img_del = set()
        
        for r in img:                               # for each element in the image
	    if is_simple_rel (r):		    # if it represents a simple relation of the form "x = y"
		var_swp[r[1]] = r[0]		    # then all the "y" in the kernel will be replaced by "x"
		img_del.add(r)			    # mark this to be removed

        img.difference_update(img_del)		    # remove extra elements from the image

	ker_swp = set()
	img_swp = set()

	for x in ker:
	    ker_swp.add (swap_var(x,var_swp))
	for x in img:
	    img_swp.add (swap_var(x,var_swp))
	ker = ker_swp
	img = img_swp

        ker_sums = []                               # the list of sums
        for x in ker:
            if x.__class__ == tuple:                # if it is a sum
                ker_sums.append(x)                  # add it to the list of sums

        ker_vars = list(set(iter.chain(*ker)))      # list of variables appeared in the kernel
        ker_dict = {}
        i = 0
        for v in ker_vars:
            ker_dict[v] = i
            i += 1
        n = len (ker_vars)                          # the number of variables (the dimension of the space)
        m = len (ker_sums)                          # the number of sums (the number of vectors)
        M = zeros([m,n], dtype=int16)
        i = 0
        for x in ker_sums:
            for c in x:
                M[i,ker_dict[c]] = 1
            i += 1

        k = 0
        for j in range(min(n,m)):                   # for each column
            if M[k,j] == 0:
                for i in range(k+1,m):              # for each row below
                    if M[i,j] != 0:
                        M[ [i,j] ] = M[ [j,i] ]     # swap the i-th and j-th row
            if M[k,j] != 0:
                for i in range(k+1,m):              # for each row below
                    if M[i,j] != 0:
                        M[i] = (M[i] + M[k]) % 2    # eliminate
                k += 1

        new_sums = []
        for i in range(m):
            if M[i].sum() > 0:                      # if this row is not all zero
                s = []
                for j in range(n):                  # for each column
                    if M[i,j] != 0:
                        s.append (ker_vars[j])
                new_sums.append (tuple(s))

        ker.difference_update (set(ker_sums))       # remove the old sums
        ker.update (set(new_sums))                  # add back the new lin-indep sums

        return (ker,img)			    # return kernel mod image

    def draw_png (self, filename):
        A = nx.to_agraph(self)
        legend  = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
        for k, v in self.color_map.items():
            legend += '<TR><TD BGCOLOR="' + v + '">' + k + '</TD></TR>'
        legend += '</TABLE>>'
        A.add_node(1, shape="plaintext", label=legend)
        A.layout(prog='dot')
        A.draw(filename)

    def check_L(self,n):
	if n in self.L_dict:
	    return self.L_dict[n]
	for s in self.successors(n):
	    s_L = self.check_L(s)
	    if not s_L == None:
		return s_L + 1
	return None
	
    def set_L (self, n, L):
	if not self.L_dict.has_key(n):
	    self.L_dict[n] = L
	    for s in self.successors(n):
		self.set_L (s, L-1)
	    if not self.levels.has_key(L):
		self.levels[L] = [n]
	    else:
		self.levels[L].append(n)

    def assign_L (self, n):
	if not self.L_dict.has_key(n):
	    L = self.check_L(n)
	    if None == L:
		L = 0
	    self.set_L (n, L)

    def assign_level(self):
	ns = nx.algorithms.dag.topological_sort (self)
	for n in ns:
	    self.assign_L(n)

