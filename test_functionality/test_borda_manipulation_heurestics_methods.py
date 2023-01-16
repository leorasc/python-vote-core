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

import random
from py3votecore.borda_manipulation_heurestics_methods import AverageFit, LargestFit
import unittest
import time


class TestAverageFit(unittest.TestCase):

    # Manipulation fails
    def test_4_candidates_manipulation_fails(self):

        input = [
            {"count": 26, "ballot": ["a","b","c","d"]},
            {"count": 22, "ballot": ["a","c","d","b"]},
            {"count": 23, "ballot": ["a","b","c","d"]}
        ] 
        output = AverageFit(ballots=input, preferred_candidate="d", k=60)

        # Run test
        self.assertFalse(output)

    # Manipulation succeeds
    def test_10_candidates_successful_manipulation(self):

        input = [
            {"count": 26, "ballot": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]},
            {"count": 53, "ballot": ["a", "b", "j", "d", "g", "e", "h", "f", "c", "i"]},
            {"count": 72, "ballot": ["d", "c", "b", "a", "e", "h", "f", "i", "g", "j"]}
        ]  # "a" = 1143, "b" = 1136, "c" = 811, "d" = 1122, "e" = 702, "f" = 426, "g" = 415, "h" = 499, "i" = 170, "j" = 371
        output = AverageFit(ballots=input, preferred_candidate="d", k=8)
            # [["d","i","j","g","f","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"]]
            # "a" = 1143, "b" = 1144, "c" = 827, "d" = 1194, "e" = 726, "f" = 466, "g" = 463, "h" = 531, "i" = 234, "j" = 427
        # Run test
        self.assertEqual(len(output), 8)
        for manip in output:
            self.assertEqual(len(manip), 10)
            for i,j in [(0,'d'),(1,'i'),(2,'j'),(3,'g'),(4,'f'),(5,'h'),(6,'e'),(7,'c'),(8,'b'),(9,'a')]:
                self.assertEqual(manip[i],j)

    # Borda
    def test_4_candidate_manipulation(self):

        # Generate data
        input = [
            {"count": 2, "ballot": ["c","a","b","d"]}, 
            {"count": 2, "ballot": ["b","c","a","d"]}]
            # "a" = 6, "b" = 8, "c" = 10, "d" = 0
        output = AverageFit(ballots=input, preferred_candidate="d", k=5)
            # [["d","a","b","c"],["d","a","b","c"],["d","a","b","c"],["d","a","b","c"],["d","b","c","a"]]
            # "a" = 14, "b" = 13, "c" = 11, "d" = 15
        # Run tests
        self.assertEqual(len(output),5)
        for manip in output:
            self.assertEqual(len(manip), 4)
            self.assertEqual(manip[0],'d')

    def test_100_candidate_manipulation(self):
        ballots = []
        for i in range(20):
            ballots.append({"count": 2, "ballot": create_vote(100)})
        start = time.process_time()
        print(AverageFit(ballots, "A", 4))
        end = time.process_time()
        duration_in_seconds = end-start
        output = duration_in_seconds < 10
        self.assertTrue(output)
        

    def test_1000_voters_manipulation(self):
        ballots = []
        for i in range(1000):
            ballots.append({"count": 1, "ballot": create_vote(50)})
        start = time.process_time()
        print(AverageFit(ballots, "A", 100))
        end = time.process_time()
        duration_in_seconds = end-start
        output = duration_in_seconds < 10
        self.assertTrue(output)

def create_alphabet_vote(m):
    ABC = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
        'V', 'W', 'X', 'Y']
    preference = []
    for i in range(1, m + 1):
        tmp = ''
        c = i
        while c >= 0:
            tmp += ABC[c % 26]
            c = c - 26
            if c == 0:
                c = -1
        preference.append(tmp)
    return preference
def create_vote(m):
    preference = create_alphabet_vote(m)
    random.shuffle(preference)
    return preference

class TestLargestFit(unittest.TestCase):

    # Manipulation fails
    def test_4_candidates_manipulation_fails(self):

        input = [
            {"count": 26, "ballot": ["a","b","c","d"]},
            {"count": 22, "ballot": ["a","c","d","b"]},
            {"count": 23, "ballot": ["a","b","c","d"]}
        ]
        output = LargestFit(ballots=input, preferred_candidate="d", k=60)

        # Run test
        self.assertFalse(output)

    # Manipulation succeeds
    def test_10_candidates_successful_manipulation(self):

        input = [
            {"count": 26, "ballot": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]},
            {"count": 53, "ballot": ["a", "b", "j", "d", "g", "e", "h", "f", "c", "i"]},
            {"count": 72, "ballot": ["d", "c", "b", "a", "e", "h", "f", "i", "g", "j"]}
        ]   # "a" = 1143, "b" = 1136, "c" = 811, "d" = 1122, "e" = 702, "f" = 426, "g" = 415, "h" = 499, "i" = 170, "j" = 371
        output = LargestFit(ballots=input, preferred_candidate="d", k=8)
            # [["d","i","j","g","f","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"],["d","i","j","f","g","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"],["d","i","j","f","g","h","e","c","b","a"],["d","i","j","g","f","h","e","c","b","a"],["d","i","j","f","g","h","e","c","b","a"],["d","i","g","j","f","h","e","c","b","a"]]
            # "a" = 1143, "b" = 1144, "c" = 827, "d" = 1194, "e" = 726, "f" = 469, "g" = 461, "h" = 531, "i" = 234, "j" = 426
        # Run test
        self.assertEqual(len(output),8)
        for manip in output:
            self.assertEqual(len(manip), 10)
            for i,j in [(0,'d'),(1,'i'),(5,'h'),(6,'e'),(7,'c')]:
                self.assertEqual(manip[i],j)

    # Borda, relevant ties
    def test_4_candidate_manipulation(self):

        # Generate data
        input = [
            {"count": 2, "ballot": ["c","a","b","d"]}, 
            {"count": 2, "ballot": ["b","c","a","d"]}]
            # "a" = 6, "b" = 8, "c" = 10, "d" = 0
        output = LargestFit(ballots=input, preferred_candidate="d", k=5)
            # [["d","a","c","b"],["d","a","c","b"],["d","b","a","c"],["d","a","b","c"],["d","b","c","a"]]
        # Run tests
        self.assertEqual(len(output),5)
        for manip in output:
            self.assertEqual(len(manip), 4)
            self.assertEqual(manip[0],'d')

    def test_100_candidate_manipulation(self):
        
        ballots = []
        for i in range(20):
            ballots.append({"count": 2, "ballot": create_vote(100)})
        start = time.process_time()
        print(LargestFit(ballots, "A", 4))
        end = time.process_time()
        duration_in_seconds = end-start
        output = duration_in_seconds < 10
        self.assertTrue(output)
        

    def test_1000_voters_manipulation(self):
        ballots = []
        for i in range(1000):
            ballots.append({"count": 1, "ballot": create_vote(50)})
        start = time.process_time()
        print(LargestFit(ballots, "A", 100))
        end = time.process_time()
        duration_in_seconds = end-start
        output = duration_in_seconds < 10
        self.assertTrue(output)



if __name__ == "__main__":
    unittest.main()




