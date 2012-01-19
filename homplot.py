from homcomplex import *
from homcoef    import *

class ComplexPlot:

    def __init__ (self, complex=None):

        if complex:
            self.C = complex
        else:
            self.C = Complex()

        self.color_use = ['violet', 'brown', 'purple', 'magenta', 'cyan', 'yellow', 'orange', 'pink', 'blue','green','red']
        self.color_map = { '1':'black' }

    def get_color (self, c):
        if c in self.color_map:
            return self.color_map[c]
        else:
	    if len(self.color_use) > 0:
		color = self.color_use.pop()
	    else:
		color = 'gray'
	    self.color_map[c] = color
	    return color

    def draw_png (self, filename):
        used_coef = set()
        for (src, dst) in self.C.edges_iter():
            coef = self.C.get_coef (src, dst)
            cstr = coef_to_str (reduce_coef (coef))
            self.C[src][dst]['color'] = self.get_color (cstr)
            #if '1' != cstr:
            #    used_coef.add (cstr)
            used_coef.add (cstr)

        A = nx.to_agraph(self.C)
        legend  = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
        for coef in sorted(list(used_coef)):
            color = self.color_map[coef]
            legend += '<TR><TD BGCOLOR="' + color + '"></TD><TD>' + coef + '</TD></TR>'
        legend += '</TABLE>>'
        A.add_node(1, shape="plaintext", label=legend)
        A.layout(prog='dot')
        A.draw(filename)
