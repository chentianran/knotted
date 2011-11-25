from homcomplex import *

class ComplexCreator:

    def __init__ (self, complex = None):

        if complex:
            self.C = complex
        else:
            self.C = Complex()

    def execute (self, cmd):
        if cmd.strip():                                 # if the command is nonempty
            src, sep, line = cmd.partition('~')         # separate at the assignment operator
            if '~' == sep:
                name = src.strip()
                terms = line.split('+')                 # separate terms in a sum
                for t in terms:
                    s, sep, v = t.partition('*')
                    if '*' == sep:                      # if this term is a scalar multiplication
                        s = s.strip()
                        v = v.strip()
                        self.C.bound (name, v, coef=s)
                    else:
                        self.C.bound (name, t.strip())
                return True
        return False

