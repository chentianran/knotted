# Flip the coefficient of any edge between
# generators in two groups
def flip_edges (C, g1, g2):
    for src, dst in C.edges_iter():
	if (src in g1 and dst in g2) or (src in g2 and dst in g1):
	    coef = C.get_coef (src, dst)
	    C.set_coef (src, dst, coef[::-1])
