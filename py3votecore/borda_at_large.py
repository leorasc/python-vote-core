

from py3votecore.abstract_classes import MultipleWinnerVotingSystem
from py3votecore.common_functions import matching_keys, unique_permutations
import copy

class BordaAtLarge(MultipleWinnerVotingSystem):
    
    def __init__(self, ballots: dict, tie_breaker=None, required_winners: int=1):
        super(BordaAtLarge, self).__init__(ballots, tie_breaker=tie_breaker, required_winners=required_winners)

    def calculate_results(self):
        # Standardize the ballot format and extract the candidates
        self.candidates = set()
        for ballot in self.ballots:

            # Convert a single candidate ballots into ballot lists
            if not isinstance(ballot["ballot"], list):
                ballot["ballot"] = [ballot["ballot"]]

            # Ensure no ballot has an excess of votes
            if len(ballot["ballot"]) < self.required_winners:
                raise Exception("A ballot contained too many candidates")

            # Add all candidates on the ballot to the set
            self.candidates.update(set(ballot["ballot"]))

        # Sum up all votes for each candidate
        self.tallies = dict.fromkeys(self.candidates, 0)
        for ballot in self.ballots:
            for i in range(len(ballot["ballot"])):
                self.tallies[ballot["ballot"][i]] += (ballot["count"]*(len(self.candidates)-1-i))
        tallies = copy.deepcopy(self.tallies)

        # Determine which candidates win
        winning_candidates = set()
        while len(winning_candidates) < self.required_winners:

            # Find the remaining candidates with the most votes
            largest_tally = max(tallies.values())
            top_candidates = matching_keys(tallies, largest_tally)

            # Reduce the found candidates if there are too many
            if len(top_candidates | winning_candidates) > self.required_winners:
                self.tied_winners = top_candidates.copy()
                while len(top_candidates | winning_candidates) > self.required_winners:
                    top_candidates.remove(self.break_ties(top_candidates, True))

            # Move the top candidates into the winning pile
            winning_candidates |= top_candidates
            for candidate in top_candidates:
                del tallies[candidate]

        self.winners = winning_candidates

    def as_dict(self):
        data = super(BordaAtLarge, self).as_dict()
        data["tallies"] = self.tallies
        return data


# if __name__ == "__main__":
#     output = BordaAtLarge([
#             {"count": 30, "ballot": ["c1", "c4", "c2", "c3"]},
#             {"count": 22, "ballot": ["c3", "c2", "c1", "c4"]},
#             {"count": 22, "ballot": ["c1", "c4", "c3", "c2"]},
#             {"count": 4, "ballot": ["c4", "c2", "c1", "c3"]},
#             {"count": 8, "ballot": ["c2", "c3", "c1", "c4"]},
#             {"count": 10, "ballot": ["c1", "c2", "c4", "c3"]}
#         ], required_winners=2).as_dict()

#     print(output)