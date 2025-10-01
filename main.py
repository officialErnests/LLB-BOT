from util import *
from cProfile import Profile
from pstats import SortKey, Stats

#importing c or some shit like that
from ctypes import cdll
lib_move = cdll.LoadLibrary('.\\c_thingamajig\\movement\\movement_lib\\x64\\Debug\\movement_lib.dll')

lib_move.movement_init()

bot1 = llb_bot("LLBlaze")
bot1.run()