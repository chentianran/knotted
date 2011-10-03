import matplotlib.pyplot as plt
import networkx as nx
import itertools as iter

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
        for p in iter.combinations(possible,2):     # for each pair in the possible pool
            s0 = self.successors(p[0])
            s1 = self.successors(p[1])
            s0.sort()
            s1.sort()
            if s0 == s1:
                kernel.add(p)                       # then (p0 + p1) is in the kernel
        return kernel                               # return the kernel

    def img (self):
        image = set()
        for n in self.nodes_iter():                 # for each node
            s = self.successors(n)
            if len(s) == 1:                         # if this node goes to nothing (zero)
                image.add(s[0])                     #
            elif len(s) > 1:
                image.add(tuple(s))
        return image

    def hom (self):
	self.remove_acyclic()			    # first remove all the acyclic subcomplices
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
        return (ker,img)			    # return kernel mod image

    def hom_string (self):
        ker, img = self.hom()
        s = ''
        for k in ker:
            if k.__class__ == tuple:
                s += '<' + reduce (lambda x, y: x + '+' + y, k, '') + '>'
            else:
                s += '<' + str(k) + '>'
        if len(img) > 0:
            s += '/'
            for k in img:
                if k.__class__ == tuple:
                    s += '<' + reduce (lambda x, y: x + '+' + y, k, '') + '>'
                else:
                    s += '<' + str(k) + '>'
        return s

    def draw_png (self, filename):
        A = nx.to_agraph(H)
        A.layout(prog='dot')
        A.draw(filename)

import sys, readline, cmd
class HomCmd (cmd.Cmd):
    
    __H = None

    def __init__ (self, H):
        cmd.Cmd.__init__ (self)
        self.__H = H
        self.prompt = ':'

    def do_bound (self, line):
        l = line.split()
        if len(l) == 2:
            self.__H.bound(l[0],l[1])

    def do_ker (self, line):
        print self.__H.ker()

    def do_img (self, line):
        print self.__H.img()

    def do_hom (self, line):
        print self.__H.hom_string()

    def do_EOF (self, line):
        sys.exit()

H = HomComplex()
#H.bound('x','y')
#H.bound('z','x')
#H.bound('z','w')
#H.bound('x','u')
#H.bound('w','u')
#H.bound('w','y')

#H.draw_png ('hom.png')

shell = HomCmd(H)
shell.cmdloop()

