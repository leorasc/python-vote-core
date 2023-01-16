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

from py3votecore.borda_at_large import BordaAtLarge
import unittest


class TestBordaAtLarge(unittest.TestCase):

    # Borda at Large, no ties
    def test_borda_at_large_no_ties(self):

        # Generate data
        output = BordaAtLarge([
            {"count": 26, "ballot": ["c1", "c2", "c3"]},
            {"count": 22, "ballot": ["c1", "c3", "c2"]},
            {"count": 23, "ballot": ["c2", "c3", "c1"]}
        ], required_winners=2).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c1', 'c2', 'c3']),
            'tallies': {'c3': 45, 'c2': 72, 'c1': 96},
            'winners': set(['c2', 'c1'])
        })

    # Borda at Large, irrelevant ties
    def test_borda_at_large_irrelevant_ties_top(self):

        # Generate data
        output = BordaAtLarge([
            {"count": 16, "ballot": ["c1", "c2", "c3", "c4", "c5"]},
            {"count": 25, "ballot": ["c1", "c3", "c2", "c4", "c5"]},
            {"count": 22, "ballot": ["c2", "c3", "c1", "c5", "c4"]},
            {"count": 22, "ballot": ["c4", "c5", "c2", "c1", "c3"]}
        ], required_winners=2).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c1', 'c2', 'c3', 'c4', 'c5']),
            'tallies': {'c3': 173, 'c2': 230, 'c1': 230, 'c5': 88, 'c4': 129},
            'winners': set(['c2', 'c1'])
        })


    # Borda at Large, irrelevant ties
    def test_borda_at_large_irrelevant_ties_low(self):

        # Generate data
        output = BordaAtLarge([
            {"count": 30, "ballot": ["c4", "c1", "c2", "c3"]},
            {"count": 22, "ballot": ["c3", "c2", "c1", "c4"]},
            {"count": 22, "ballot": ["c1", "c4", "c3", "c2"]},
            {"count": 4, "ballot": ["c4", "c2", "c1", "c3"]},
            {"count": 8, "ballot": ["c2", "c3", "c1", "c4"]},
            {"count": 2, "ballot": ["c3", "c2", "c4", "c1"]}
        ], required_winners=2).as_dict()

        print(output)
        # Run tests
        self.assertEqual(output["tallies"], {'c3': 110, 'c2': 110, 'c1': 160, 'c4': 148})
        self.assertEqual(output['winners'], set(['c4', 'c1']))
        self.assertEqual(len(output), 3)

        # Borda at Large, relevant ties
    def test_borda_at_large_relevant_ties(self):


        # Generate data
        output = BordaAtLarge([
            {"count": 30, "ballot": ["c1", "c4", "c2", "c3"]},
            {"count": 22, "ballot": ["c3", "c2", "c1", "c4"]},
            {"count": 22, "ballot": ["c1", "c4", "c3", "c2"]},
            {"count": 4, "ballot": ["c4", "c2", "c1", "c3"]},
            {"count": 8, "ballot": ["c2", "c3", "c1", "c4"]},
            {"count": 10, "ballot": ["c1", "c2", "c4", "c3"]}
        ], required_winners=2).as_dict()

        # Run tests
        self.assertEqual(output["tallies"], {'c3': 104, 'c2': 126, 'c1': 220, 'c4': 126})
        self.assertEqual(len(output["tie_breaker"]), 4)
        self.assertEqual(output["tied_winners"], set(['c2', 'c4']))
        self.assertTrue("c1" in output["winners"] and ("c2" in output["winners"] or "c4" in output["winners"]))
        self.assertEqual(len(output), 5)


if __name__ == "__main__":
    unittest.main()


