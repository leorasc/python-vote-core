

from py3votecore.abstract_classes import AbstractSingleWinnerVotingSystem
from py3votecore.borda_at_large import BordaAtLarge

class Borda(AbstractSingleWinnerVotingSystem):

    def __init__(self, ballots: dict, tie_breaker=None):
        super(Borda, self).__init__(ballots, BordaAtLarge, tie_breaker=tie_breaker)



