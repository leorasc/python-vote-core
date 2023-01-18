# Copyright (C) 2023, Leora Schmerler
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .abstract_classes import MultipleWinnerVotingSystem
from .common_functions import matching_keys, unique_permutations
import copy

class BordaAtLarge(MultipleWinnerVotingSystem):
    
    def __init__(self, ballots: list, tie_breaker=None, required_winners: int=1):
        """
        The constructer accepts ballots of voters, a tie breaker if given and the number of required winners.
        >>> BordaAtLarge([{ "count":3, "ballot":["A", "B", "C", "D"]},{ "count":2, "ballot":["D", "B", "A", "C"]},{ "count":2, "ballot":["D", "B", "C", "A"]}], required_winners = 2) # doctest:+ELLIPSIS
        <...>
        >>> BordaAtLarge([{ "count":3, "ballot":["A", "B", "C", "D"]},{ "count":2, "ballot":["D", "B", "A", "C"]},{ "count":2, "ballot":["D", "B", "C", "A"]}], tie_breaker=["A", "B", "C", "D"] ,required_winners = 2) # doctest:+ELLIPSIS
        <...>
        """
        super(BordaAtLarge, self).__init__(ballots, tie_breaker=tie_breaker, required_winners=required_winners)

    def calculate_results(self):
        """
        calculate_results accepts an instance of Borda, and is called from the constructor.
        >>> BordaAtLarge([{ "count":3, "ballot":["A", "B", "C", "D"]},{ "count":2, "ballot":["D", "B", "A", "C"]},{ "count":2, "ballot":["D", "B", "C", "A"]}], tie_breaker=["A", "B", "C", "D"] ,required_winners = 2).calculate_results() # doctest:+ELLIPSIS
        ...
        >>> BordaAtLarge([{ "count":3, "ballot":["A", "B", "C", "D"]},{ "count":2, "ballot":["D", "B", "A", "C"]},{ "count":2, "ballot":["D", "B", "C", "A"]}], required_winners = 2).calculate_results() # doctest:+ELLIPSIS
        ...
        """

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
        """
        as_dict accepts an instance of Borda, and returns a dict of the BordaAtLarge.
        >>> BordaAtLarge([{ "count":3, "ballot":["A", "B", "C", "D"]},{ "count":2, "ballot":["D", "B", "A", "C"]},{ "count":2, "ballot":["D", "B", "C", "A"]}], tie_breaker=["A", "B", "C", "D"] ,required_winners = 2).as_dict() # doctest:+ELLIPSIS
        {...}
        >>> BordaAtLarge([{ "count":3, "ballot":["A", "C", "B", "D"]},{ "count":2, "ballot":["D", "B", "A", "C"]},{ "count":2, "ballot":["D", "B", "C", "A"]}], required_winners = 2).as_dict() # doctest:+ELLIPSIS
        {...}
        """
        data = super(BordaAtLarge, self).as_dict()
        data["tallies"] = self.tallies
        return data

if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

