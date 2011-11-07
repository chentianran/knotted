import matplotlib.pyplot as plt
import networkx as nx
import itertools as iter
from string import *
from numpy import *

class HomComplex(nx.DiGraph):

    def __init__ (self, data=None):
	nx.DiGraph.__init__(self, data)
	self.L_dict = {}
	self.levels = {}
        self.components = []

    def bound(self, x, y):
        self.add_node(x)
        self.add_node(y)
        self.add_edge(x,y)

    def show(self):
        nx.draw(self)

    def clean(self):
	self.clear()
	self.L_dict.clear()
	self.levels.clear()

    def remove_acyclic(self):
        cont = True
        while (cont):
            cont = False
            for n in self.nodes_iter():
                if self.out_degree(n) == 1:         # if the father has just one son
                    succ = self.neighbors(n)[0]     # successor: the son
                    if self.out_degree(succ) == 0:  # if the successor has no boundary
                        self.remove_node(succ)      # then we have an acyclic subcomplex
                        self.remove_node(n)         # remove both
                        cont = True                 # we should run through this again
                        break                       # done

    def meaningful_sum (self, s):
        for t in s:		                    # for each term in this sum
            if self.out_degree(t) == 0:             # if one term in the sum is going no where
                return False                        # then this sum is meaningless
        return True                                 # if every term has a boundary, then the sum is meaningful

    def sum_in_ker (self, s):
        img_dict = {}		                    # dictionary to keep track of the times each image appear
        for t in s:		                    # for each term in this sum
            t_img = self.successors (t)                # the image of the ith term
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
            if self.out_degree(n) == 0:             # if this node goes to nothing (zero)
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
            s = self.successors(n)
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

        ker_swp = {}
        ker_del = set()
        img_del = set()
        
        for r in img:                               # for each element in the image
            if r.__class__ == tuple:                # if it is a relation
                if len(r) == 2:                     # if the relation is of the form "x = y"
                    ker_swp[r[1]] = r[0]            # then all the "y" in the kernel will be replaced by "x"
                    img_del.add(r)                  # mark this to be removed

        for x in ker:				    # for each element in the kernel
            if x in ker_swp:			    # if it is marked to be swapped
                ker.add(ker_swp[x])		    # add replace to the kernel
                ker_del.add(x)			    # mark the old one for removal

        ker.difference_update(ker_del)		    # remove extra elements from the kernel
        img.difference_update(img_del)		    # remove extra elements from the image

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

