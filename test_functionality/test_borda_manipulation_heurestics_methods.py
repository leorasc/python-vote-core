



from py3votecore.borda_manipulation_heurestics_methods import AverageFit, LargestFit
import unittest


class TestAverageFit(unittest.TestCase):

    # Manipulation fails
    def test_4_candidates_manipulation_fails(self):

        input = [
            {"count": 26, "ballot": ["a","b","c","d"]},
            {"count": 22, "ballot": ["a","c","d","b"]},
            {"count": 23, "ballot": ["a","b","c","d"]}
        ]
        output = AverageFit(ballots=input, candidate="d", k=60, tie_breaker=["d","c","b","a"])

        # Run test
        self.assertFalse(output)

    # Manipulation succeeds
    def test_10_candidates_successful_manipulation(self):

        input = [
            {"count": 26, "ballot": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]},
            {"count": 53, "ballot": ["a", "b", "j", "d", "i", "e", "h", "f", "c", "i"]},
            {"count": 72, "ballot": ["d", "c", "b", "a", "e", "h", "f", "i", "g", "j"]}
        ]
        output = AverageFit(ballots=input, candidate="d", k=8, tie_breaker=["d","c","b","a"])

        # Run test
        self.assertTrue(output)

    # Borda
    def test_4_candidate_manipulation(self):

        # Generate data
        input = [
            {"count": 2, "ballot": ["c","a","b","d"]}, 
            {"count": 2, "ballot": ["b","c","a","d"]}]
        output = AverageFit(ballots=input, candidate="d", k=5, tie_breaker=["d", "c", "b", "a"])

        # Run tests
        self.assertTrue(output)

class TestLargestFit(unittest.TestCase):

    # Manipulation fails
    def test_4_candidates_manipulation_fails(self):

        input = [
            {"count": 26, "ballot": ["a","b","c","d"]},
            {"count": 22, "ballot": ["a","c","d","b"]},
            {"count": 23, "ballot": ["a","b","c","d"]}
        ]
        output = LargestFit(ballots=input, candidate="d", k=60, tie_breaker=["d","c","b","a"])

        # Run test
        self.assertFalse(output)

    # Manipulation succeeds
    def test_10_candidates_successful_manipulation(self):

        input = [
            {"count": 26, "ballot": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]},
            {"count": 53, "ballot": ["a", "b", "j", "d", "i", "e", "h", "f", "c", "i"]},
            {"count": 72, "ballot": ["d", "c", "b", "a", "e", "h", "f", "i", "g", "j"]}
        ]
        output = LargestFit(ballots=input, candidate="d", k=8, tie_breaker=["d","c","b","a"])

        # Run test
        self.assertTrue(output)

    # Borda, relevant ties
    def test_4_candidate_manipulation(self):

        # Generate data
        input = [
            {"count": 2, "ballot": ["c","a","b","d"]}, 
            {"count": 2, "ballot": ["b","c","a","d"]}]
        output = LargestFit(ballots=input, candidate="d", k=5, tie_breaker=["d", "c", "b", "a"])

        # Run tests
        self.assertTrue(output)


if __name__ == "__main__":
    unittest.main()




