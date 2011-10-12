import matplotlib.pyplot as plt
import networkx as nx
import itertools as iter
from string import *
from numpy import *

class HomComplex(nx.DiGraph):

    def bound(self, x, y):
        self.add_node(x)
        self.add_node(y)
        self.add_edge(x,y)


    def show(self):
        nx.draw(self)

    def remove_acyclic(self):
        cont = True
        while (cont):
            cont = False
            for n in self.nodes_iter():
                if self.out_degree(n) == 1:         # if nothing leave this node
                    succ = self.neighbors(n)[0]     # successor
                    if self.out_degree(succ) == 0:  # if the successor has no boundary
                        self.remove_node(succ)      # then we have an acyclic subcomplex
                        self.remove_node(n)         # remove both
                        cont = True                 # we should run through this again
                        break                       # done

    def ker (self):
        kernel = set()
        possible = []

        for n in self.nodes_iter():                 # for each node
            if self.out_degree(n) == 0:             # if this node goes to nothing (zero)
                kernel.add(n)                       # then it is in the kernel
            else:                                   # if this node goes to something
                possible.append(n)                  # then it may be a summand of something that goes to zero

	for c in range(2,len(possible)+1):	    # next we will check the sum of 2, 3... terms
	    for p in iter.combinations(possible,c): # for each combination in the possible pool
		img_dict = {}			    # dictionary to keep track of the times each image appear
		for pi in p:			    # for each term in this sum
		    si = self.successors(pi)	    # the image of the ith term
		    for s in si:		    # for each successor
			if img_dict.has_key(s):
			    img_dict[s] += 1
			else:
			    img_dict[s] = 1
		in_ker = True
		for im in img_dict:
		    if 0 != (img_dict[im] % 2):
			in_ker = False
			break
		if in_ker:
		    kernel.add(p)                   # then the sum is in the kernel
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
	#self.remove_acyclic()			    # first remove all the acyclic subcomplices
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

    def hom_string (self):
        ker, img = self.hom()
        s = ''
        for k in ker:
            s += '<'
            if k.__class__ == tuple:
                s += join(list(k),'+')
            else:
                s += str(k)
            s += '>'
        if len(img) > 0:
            s += '/'
            for k in img:
                if k.__class__ == tuple:
                    s += '<' + reduce (lambda x, y: x + '+' + y, k, '') + '>'
                else:
                    s += '<' + str(k) + '>'
        return s

    def draw_png (self, filename):
        A = nx.to_agraph(self)
        A.layout(prog='dot')
        A.draw(filename)

