from homcomplex import *

H = HomComplex()
H.bound('x','a')
H.bound('x','b')
H.bound('y','a')
H.bound('y','b')
H.bound('z','a')
H.bound('z','b')

print H.hom_string()



