from . import *

class PlayerBot(Bot):
    def play_round(self):

        yield MemoryQuestions, dict(belief_memory1=23,
                                    belief_memory2=32)
        yield Transition
        yield BeliefQuestions, dict(belief_strategy=4,
                                    belief_optimal=8,
                                    belief_fake_blue=100,
                                    belief_fake_red=0)
        yield CRT, dict(crt1=1,
                        crt2=1,
                        crt3=1,
                        crt4=1)
        yield Demographics, dict(age=99,
                                 gender=3,
                                 edu=1,
                                 occ=5,
                                 country='NL',
                                 prob_fam=4)
