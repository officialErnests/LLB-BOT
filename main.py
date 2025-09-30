from util import *
from cProfile import Profile
from pstats import SortKey, Stats

bot1 = llb_bot("LLBlaze")
with Profile() as profile:
    bot1.run()
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats(SortKey.CALLS)
        .print_stats()
    )