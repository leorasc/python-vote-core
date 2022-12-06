

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

def main():
    lst = ["a", "b", "c", "d", "e", "f", "g", "h"]
    ballots = []
    for p1 in unique_permutations(lst):
        # ballots = [{"count": 1, "ballot":p1}, {"count": 1, "ballot":p1}, {"count": 1, "ballot":p1}, {"count": 1, "ballot":p1}, {"count": 1, "ballot":p1}, {"count": 1, "ballot":p1}, {"count": 1, "ballot":p1}, {"count": 1, "ballot":p1}]
    # print(ballots)
    # output = BordaAtLarge(ballots)
    # print(output.as_dict()["tallies"])
    # if output.as_dict()["tallies"] == {'g': 48, 'h': 56, 'f': 40, 'a': 0, 'd': 24, 'b': 8, 'c': 16, 'e': 32}:
    #     print(ballots)
    #     print("True")


        for p2 in unique_permutations(lst):
            for p3 in unique_permutations(lst):
                for p4 in unique_permutations(lst):
                    for p5 in unique_permutations(lst):
                        for p6 in unique_permutations(lst):
                            for p7 in unique_permutations(lst):
                                for p8 in unique_permutations(lst):
                                    ballots = [{"count": 1, "ballot":p1}, {"count": 1, "ballot":p2}, {"count": 1, "ballot":p3}, {"count": 1, "ballot":p4}, {"count": 1, "ballot":p5}, {"count": 1, "ballot":p6}, {"count": 1, "ballot":p7}, {"count": 1, "ballot":p8}]
                                    # print(ballots)
                                    output = BordaAtLarge(ballots)
                                    if output.as_dict()["tallies"] == {'a': 41, 'b': 34, 'c': 30, 'd': 14, 'e': 27, 'f': 27, 'g': 26, 'h': 25}:
                                        print(ballots)


if __name__ == "__main__":
    main()


