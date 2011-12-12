class TexDoc:

    def __init__ (self, out):
	self.out = out
	self.out.write ('\\documentclass{article}\n')

    def use (self, package):
	self.out.write ('\\usepackage{' + package + '}\n')

    def begin (self):
	self.out.write ('\\begin{document}\n')

    def end (self):
	self.out.write ('\\end{document}\n')

    def table (self, tab):
	if tab:
	    align = '|'.join(['c' for x in tab[0]])
	    self.out.write ('\\begin{tabular}{|l|' +  align + '|}\n')
	    for row in tab:
		self.out.write ('\\hline ' + ' & '.join (row) + ' \\\\\n')
	    self.out.write ('\\hline\n\\end{tabular}\n')
    

