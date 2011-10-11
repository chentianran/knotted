import sys, readline, cmd
import homcomplex

class HomShell (cmd.Cmd):
    
    __H = None

    def __init__ (self, H):
        cmd.Cmd.__init__ (self)
        self.__H = H
        self.prompt = ':'

    def do_bound (self, line):
        arg = line.partition('=')
        print arg
        if arg[1] == '=':
            terms = arg[2].split('+')
            print terms
            for t in terms:
                self.__H.bound(arg[0],t)

    def do_ker (self, line):
        print self.__H.ker()

    def do_img (self, line):
        print self.__H.img()

    def do_hom (self, line):
        print self.__H.hom_string()

    def do_clear (self, line):
        self.__H.clear()

    def do_EOF (self, line):
        sys.exit()

H = homcomplex.HomComplex()
shell = HomShell(H)
shell.cmdloop()
