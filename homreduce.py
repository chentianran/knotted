import sys

from homutils import *
from homplot  import *

creator = ComplexCreator()
for line in sys.stdin.readlines():
    creator.execute (line)

C = creator.C
for k in range(0,100):
    plotter = ComplexPlot (C)
    plotter.draw_png('reduce' + str(k) + '.png')
    if not C.reduce():
	break


