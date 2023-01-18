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

from .abstract_classes import AbstractSingleWinnerVotingSystem
from .borda_at_large import BordaAtLarge

class Borda(AbstractSingleWinnerVotingSystem):

    def __init__(self, ballots, tie_breaker=None):
        """
        The constructer accepts ballots of voters and a tie breaker if given.
        >>> Borda([{ "count":3, "ballot":["A", "B", "C", "D"]},{ "count":2, "ballot":["D", "B", "A", "C"]},{ "count":2, "ballot":["D", "B", "C", "A"]}]) # doctest:+ELLIPSIS
        <...>
        >>> Borda([{ "count":3, "ballot":["A", "B", "C", "D"]},{ "count":2, "ballot":["D", "B", "A", "C"]},{ "count":2, "ballot":["D", "B", "C", "A"]}], tie_breaker=["A", "B", "C", "D"]) # doctest:+ELLIPSIS
        <...>
        """
        super(Borda, self).__init__(ballots, BordaAtLarge, tie_breaker=tie_breaker)


if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

