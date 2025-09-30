from util import *
from cProfile import Profile
from pstats import SortKey, Stats

#importing c or some shit like that
from ctypes import cdll
lib_move = cdll.LoadLibrary('./c_thingamajig/movement/movement_main.h')

class mover(object):
    def __init__(self):
        self.obj = lib_move.Foo_new()
    
    def mainFunc(self):
        lib_move.Foo_bar(self.obj)

mover_test = mover()
mover_test.mainFunc()

bot1 = llb_bot("LLBlaze")
bot1.run()