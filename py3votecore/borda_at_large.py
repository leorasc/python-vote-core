

from py3votecore.abstract_classes import MultipleWinnerVotingSystem


class BordaAtLarge(MultipleWinnerVotingSystem):
    
    def __init__(self, ballots: dict, tie_breaker=None, required_winners: int=1):
        pass

    def calculate_results(self):
        return 0

    def as_dict(self):
        return 0

