# 
# 
# 
# 
# 
# 

from .borda import Borda
import logging
import networkx as nx


def AverageFit(ballots: list, candidate: str, k: int)->list or bool:
    """
    "Complexity of and Algorithms for Borda Manipulation", by Jessica Davies, George Katsirelos, Nina Narodytska and Toby Walsh(2011),
    https://ojs.aaai.org/index.php/AAAI/article/view/7873

    AverageFit: accepts ballots of voters, a number of manipulators, k, that try to manipulate their vote in order that thier preferred 
    candidate will be elected by the Borda voting rule, with a tie-breaker, if recieved one. The algorithm outputs true if it succeeds 
    to find such manipulation, and false otherwise.
    
    Programmer: Leora Schmerler

    >>> AverageFit([{"count": 1, "ballot": ["c","a","b","d"]}, {"count": 1, "ballot": ["b","c","a","d"]}], "d", 2) # doctest:+NORMALIZE_WHITESPACE
    [['d', 'a', 'c', 'b'], ['d', 'b', 'a', 'c']]
    >>> AverageFit([{"count": 1, "ballot": ["c","b","d","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}], "d", 2) # doctest:+NORMALIZE_WHITESPACE
    [['d', 'a', 'c', 'b'], ['d', 'a', 'c', 'b']]
    >>> AverageFit([{"count": 1, "ballot": ["b","d","c","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}, {"count": 1, "ballot": ["a","c","d","b"]}], "d", 2) # doctest:+NORMALIZE_WHITESPACE
    [['d', 'c', 'a', 'b'], ['d', 'c', 'a', 'b']]
    
    >>> AverageFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 5) # doctest:+ELLIPSIS
    [...]
    >>> AverageFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 4)
    False
    """
    # create and configure logger
    logging.basicConfig(filename= 'my_logging.log', level= logging.INFO)
    logger = logging.getLogger()

    candidates = {c:0 for c in ballots[0]["ballot"]}    # Dictionary of candidates and amount of times the manipulators have placed each candidate.
    m = len(candidates)     # Number of candidates.
    manipulators = [["" for j in range(m)] for i in range(k)]       # Creating the manipulators preference profile. 
    scores_to_give = {i:k for i in range(m-1)}      # Dictionary of the scores the manipulators can give.
    scores = Borda(ballots).as_dict()["tallies"]
    scores[candidate] += (k*(m-1))
    for manipulator in manipulators:
        manipulator[0] = candidate 
    gap = create_gap_dic(scores, candidate, k)      # Dictionary of the average score gap of the candidate that the manipulators want to win to each other candidate. 
    highest_score_to_give = m-2
    if not gap:     # If gap is False, then there exists a candidate c, that has a higher score than candidate the manipulators, and therefore, the algorithm returns False.
        return False
    for i in range(k*(m - 1)):      # Number of scores to give to the candidates.
        logger.debug(f'{i}th time giving score')
        sorted(gap.items(), key=lambda item: candidates[item[0]], reverse = True)
        for c,v in sorted(gap.items(), key=lambda item: item[1], reverse = True):   # Sort according to the largest average gap.
            if candidates[c]<k:
                score_to_give = find_possible_score(scores, scores_to_give, candidate, c, highest_score_to_give)
                if score_to_give == -1:   # If there is no possible score that is possible to give c, AverageFit returns False.
                    return False
                scores[c] += score_to_give
                candidates[c] += 1
                gap[c] = (scores[candidate] - scores[c])/(k - candidates[c]) if candidates[c] != k else 0
                scores_to_give[score_to_give] -= 1
                manipulators[k-1-scores_to_give[score_to_give]][m-1-score_to_give] = c
                highest_score_to_give = update_highest_score_to_give(scores_to_give, highest_score_to_give)
                if candidates[c]==k:
                    del gap[c]
                break
    if not is_legal(manipulators, candidates):
        return legal_manipulation(manipulators, candidates.keys())
    return manipulators
    # return True


def LargestFit(ballots: list, candidate: str, k: int)->list or bool:
    """
    "Complexity of and Algorithms for Borda Manipulation", by Jessica Davies, George Katsirelos, Nina Narodytska and Toby Walsh(2011),
    https://ojs.aaai.org/index.php/AAAI/article/view/7873

    LargestFit: accepts ballots of voters, a number of manipulators, k, that try to manipulate their vote in order that thier preferred 
    candidate will be elected by the Borda voting rule, with a tie-breaker, if recieved one. The algorithm outputs true if it succeeds 
    to find such manipulation, and false otherwise.
    
    Programmer: Leora Schmerler

    >>> LargestFit([{"count": 1, "ballot": ["c","a","b","d"]}, {"count": 1, "ballot": ["b","c","a","d"]}], "d", 2) # doctest:+NORMALIZE_WHITESPACE
    [['d', 'a', 'c', 'b'], ['d', 'b', 'a', 'c']]
    >>> LargestFit([{"count": 1, "ballot": ["c","b","d","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}], "d", 2) # doctest:+ELLIPSIS
    [...]
    >>> LargestFit([{"count": 1, "ballot": ["b","d","c","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}, {"count": 1, "ballot": ["a","c","d","b"]}], "d", 2) # doctest:+NORMALIZE_WHITESPACE
    [['d', 'c', 'a', 'b'], ['d', 'a', 'c', 'b']]
    
    >>> LargestFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 5) # doctest:+ELLIPSIS
    [...]
    >>> LargestFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 4) # doctest:+ELLIPSIS
    [...]

    """

    candidates = {c:0 for c in ballots[0]["ballot"]}    # Dictionary of candidates and amount of times the manipulators have placed each candidate.
    m = len(candidates)     # Number of candidates.
    manipulators = [["" for j in range(m)] for i in range(k)]       # Creating the manipulators preference profile.
    scores = Borda(ballots).as_dict()["tallies"]
    scores[candidate] += (k*(m-1))
    for manipulator in manipulators:
        manipulator[0] = candidate 
    gap = create_gap_dic(scores, candidate, 1)      # Dictionary of the score gap of the candidate that the manipulators want to win to each other candidate.
    if not gap:     # If gap is False, then there exists a candidate c, that has a higher score than candidate the manipulators, and therefore, the algorithm returns False.
        return False
    for i in range(m - 2, -1, -1):      # The score given in the current iteration.
        for j in range(k):       # The relaxed manipulator giving that score.
            for c,v in sorted(gap.items(), key=lambda item: item[1], reverse = True):
                if candidates[c]<k:   # If c was not placed k times yet, LargestFit gives c i points, and updates the number of times it was placed, the gap and the score. 
                    if v - i < 0:       # If we add to c the score of i and it overtakes the score of candidate, LargestFit return False.
                        return False
                    manipulators[j][m-1-i] = c
                    gap[c] = v - i
                    scores[c] += i
                    candidates[c] += 1
                    if candidates[c]==k:
                        del gap[c]
                    break
    if not is_legal(manipulators, candidates):
        return legal_manipulation(manipulators, candidates.keys())
    return manipulators
    # return True


def find_possible_score(scores: dict, scores_to_give: dict, candidate: str, c: str, highest_score_to_give: int)->int:
    """
    find_possible_score: accepts a dict of the current scores from ballots of voters and part of the manipulators preference profile, a dict of scores still posiible to give, 
    a string of the candidate the manipulators want her to win, a string c of a candidate the manipulators want to give the next Borda score and an integer of the highest 
    posiible score to give some candidate.
    The function outputs the score posiible to give to candidate c, such that the score candidate has will be higher or grater than c's score. If no such score exists, returns false.
    >>> find_possible_score({"C": 11, "Carle": 10, "Barak": 7, "Diana": 5, "Rachel":10}, {0: 4, 1: 4, 2:4, 3: 4, 4: 4}, "C", "Diana", 4)
    4
    >>> find_possible_score({"C": 91, "Carle": 80, "Barak": 92, "Diana": 77, "Rachel":88}, {0: 4, 1: 4, 2: 4, 3: 0, 4: 1}, "Barak", "C", 4)
    1
    >>> find_possible_score({"A": 91, "B": 80, "C": 98, "D": 77, "E": 88, "F": 87, "G": 89, "H": 99}, {0: 0, 1: 0, 2: 1, 3: 0, 4: 1}, "H", "C", 4)
    -1
    >>> find_possible_score({'b': 6, 'c': 6, 'd': 6, 'a': 6}, {0: 2, 1: 0, 2: 0}, 'd', 'b', 0)
    0
    """
    score_to_give = highest_score_to_give
    if scores[candidate] <= score_to_give + scores[c]:
        score_to_give = scores[candidate] - scores[c]   # The highest score c can get, since it is smaller that the highest avialable one.
        if score_to_give < 0:
            return -1
        if scores_to_give[score_to_give] == 0:
            no_score_to_give = True
            for k in range(score_to_give, -1, -1):
                if scores_to_give[k] != 0:
                    score_to_give = k
                    no_score_to_give = False
                    break
            if no_score_to_give:
                return -1
    return score_to_give

def update_highest_score_to_give(scores_to_give :dict, highest_score_to_give: int)->int:
    """
    update_highest_score_to_give: accepts a dict of scores still posiible to give and an integer that is the highest possible Borda score to give.
    The function outputs the next highest score possible to give. If the highest possible score is not possible anymore, that is, it was currently
    given, the function searches for a lower integer that can be given next, from the next highest to 0, and returns it. If all scores were given
    or the highest possible Borda score stays the same, then the function returns the highest possible Borda score.
    >>> update_highest_score_to_give({0: 4, 1: 4, 2:4, 3: 4, 4: 4}, 4)
    4
    >>> update_highest_score_to_give({0: 4, 1: 4, 2: 4, 3: 0, 4: 0}, 4)
    2
    >>> update_highest_score_to_give({0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, 4)
    4
    >>> update_highest_score_to_give({0: 2, 1: 0, 2: 0}, 1)
    0
    """
    if scores_to_give[highest_score_to_give] == 0:      # If giving a candidate the highest possible and therefore that score is not possible anymore.
        for k in range(highest_score_to_give, -1, -1):
            if scores_to_give[k] != 0:
                return k
    return highest_score_to_give

def create_gap_dic(scores: dict, candidate: str, k: int)->dict:
    """
    create_gap_dic: accepts a dict of the current scores from ballots of voters and part of the manipulators preference profile and the candidate
    the manipulators want her to win. The function constructs and outputs a dict of gaps of each candidate c, to the candidate the manipulators 
    want to win. When the algorithm that calls this function is LargestFit, then the gap is the difference between the scores. Otherwise, the gap in AverageFit,
    is an average gap.
    >>> create_gap_dic({"A": 91, "B": 80, "C": 98, "D": 77, "E": 88, "F": 87, "G": 89, "H": 99}, "H", 1)  #doctest: +NORMALIZE_WHITESPACE
    {'A': 8.0, 'B': 19.0, 'C': 1.0, 'D': 22.0, 'E': 11.0, 'F': 12.0, 'G': 10.0}
    >>> create_gap_dic({"A": 100, "B": 80, "C": 98, "D": 77, "E": 88, "F": 87, "G": 89, "H": 99}, "A", 2)  #doctest: +NORMALIZE_WHITESPACE
    {'B': 10.0, 'C': 1.0, 'D': 11.5, 'E': 6.0, 'F': 6.5, 'G': 5.5, 'H': 0.5}
    >>> create_gap_dic({"A": 91, "B": 102, "C": 98, "D": 77, "E": 88, "F": 87, "G": 89, "H": 99}, "B", 5)  #doctest: +NORMALIZE_WHITESPACE
    {'A': 2.2, 'C': 0.8, 'D': 5.0, 'E': 2.8, 'F': 3.0, 'G': 2.6, 'H': 0.6}
    """
    gap = {}
    for c in scores.keys():
        if c != candidate:
            gap[c] = (scores[candidate] - scores[c])/ k     # Creates the average gap for each candidate c. When LargestFit calls this function, k=1.
            if gap[c] < 0:
                return False
    return gap

def is_legal(manipulators: list, candidates: dict)->bool:
    """
    is_legal: accepts a list of manipulators, and their preference order list and a dict of candidates, where each candidate was placed k times
    The function checks if this manipulation is legal, that is, if there exists a manipulator that places a candidate more than one (and therefore,
    doesn't place at least one candidate in her preference order).
    >>> is_legal([["A","B","C","D"],["A","B","C","D"],["A","B","C","D"]], {"A":3, "B":3, "C":3, "D":3})
    True
    >>> is_legal([["C","D","B","A"],["A","D","C","B"],["D","A","C","B"]], {"A":3, "B":3, "C":3, "D":3})
    True
    >>> is_legal([["C","D","B","A"],["A","D","C","B"],["D","A","C","B"],["D","A","A","B"],["D","C","C","B"]], {"A":5, "B":5, "C":5, "D":5})
    False
    """
    for i in range(len(manipulators)-1, -1, -1):
        for c in manipulators[i]:
            candidates[c] = candidates[c] - 1
            if candidates[c] != i:
                return False
    return True


def legal_manipulation(manipulators: list, candidates: set)->list:
    """
    legal_manipulation: accepts a list of manipulators, and their preference order list that is not a legal manipulation and a set of candidates.
    The function return a leagl manipulation.
    """
    G = nx.Graph()
    G.add_nodes_from([j for j in range(len(manipulators))], bipartite=0)
    G.add_nodes_from(candidates, bipartite=1)
    E = [(j, manipulators[i][j]) for i in range(len(manipulators)) for j in range(len(manipulators[i]))]
    is_more_than_one_component = False
    G.add_edges_from(E)
    components = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    for i in range(len(manipulators)):
        if is_more_than_one_component:
            components = [G.subgraph(c).copy() for c in nx.connected_components(G)]
            is_more_than_one_component = False
        match = {}
        for k in range(len(components)):
            match.update(nx.bipartite.maximum_matching(components[k]))
        for j in range(len(manipulators[i])):
            manipulators[i][j] = match[j]
            E.remove((j, match[j]))
            if E.count((j, match[j])) == 0:
                G.remove_edge(j, match[j])
                is_more_than_one_component = True
    return manipulators

if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))