#!/usr/bin/python

import sys, readline, cmd
import homcomplex
from subprocess import call

class HomShell (cmd.Cmd):
    
    def __init__ (self, H):
        cmd.Cmd.__init__ (self)
        self.__H = H
        self.prompt = ''

    def do_bound (self, line):
        arg = line.partition('=')
        if arg[1] == '=':
	    name = arg[0].strip()
            terms = arg[2].split('+')
            for t in terms:
                self.__H.bound (name, t.strip())

    def do_ker (self, line):
        print self.__H.ker()

    def do_img (self, line):
        print self.__H.img()

    def do_hom (self, line):
        print self.__H.hom()

    def do_clear (self, line):
        self.__H.clean()

    def do_draw (self, line):
        self.__H.draw_png('hom.png')
        call ('eog ./hom.png', shell=True)

    def do_level (self, line):
	print self.__H.L_dict

    def do_acyclic (self, line):
	self.__H.remove_acyclic()

    def do_EOF (self, line):
        sys.exit()

if __name__ == '__main__':
    H = homcomplex.HomComplex()
    shell = HomShell(H)
    shell.cmdloop()
