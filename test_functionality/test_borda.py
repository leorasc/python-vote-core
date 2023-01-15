

from py3votecore.borda import Borda
import unittest


class TestBorda(unittest.TestCase):

    # Borda, no ties
    def test_no_ties(self):

        # Generate data
        input = [
            {"count": 26, "ballot": ["c1","c2","c3"]},
            {"count": 22, "ballot": ["c2","c1","c3"]},
            {"count": 23, "ballot": ["c3","c2","c1"]}
        ]
        output = Borda(input).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c1', 'c2', 'c3']),
            'tallies': {'c3': 46, 'c2': 93, 'c1': 74},
            'winner': 'c2'
        })

    # Borda, irrelevant ties
    def test_irrelevant_ties(self):

        # Generate data
        input = [
            {"count": 26, "ballot": ["c1", "c2", "c3"]},
            {"count": 23, "ballot": ["c2", "c1", "c3"]},
            {"count": 72, "ballot": ["c1", "c3", "c2"]}
        ]
        output = Borda(input).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c1', 'c2', 'c3']),
            'tallies': {'c3': 72, 'c2': 72, 'c1': 219},
            'winner': 'c1'
        })

    # Borda, relevant ties
    def test_relevant_ties(self):

        # Generate data
        input = [
            {"count": 49, "ballot": ["c1", "c2", "c3"]},
            {"count": 26, "ballot": ["c2", "c1", "c3"]},
            {"count": 23, "ballot": ["c3", "c2", "c1"]}
        ]
        output = Borda(input).as_dict()

        # Run tests
        self.assertEqual(output["tallies"], {'c1': 124, 'c2': 124, 'c3': 46})
        self.assertEqual(output["tied_winners"], set(['c1', 'c2']))
        self.assertTrue(output["winner"] in output["tied_winners"])
        self.assertEqual(len(output["tie_breaker"]), 3)


if __name__ == "__main__":
    unittest.main()
