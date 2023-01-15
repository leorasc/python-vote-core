# 
# 
# 
# 
# 
# 

from py3votecore.borda import Borda
import networkx as nx


def AverageFit(ballots: list, preferred_candidate: str, k: int)->list or bool:
    """
    "Complexity of and Algorithms for Borda Manipulation", by Jessica Davies, George Katsirelos, Nina Narodytska and Toby Walsh(2011),
    https://ojs.aaai.org/index.php/AAAI/article/view/7873

    AverageFit: accepts ballots of voters, a number of manipulators, k, that try to manipulate their vote in order that thier preferred 
    candidate will be elected by the Borda voting rule, with a tie-breaker, if recieved one. The algorithm outputs true if it succeeds 
    to find such manipulation, and false otherwise.
    
    Programmer: Leora Schmerler

    >>> AverageFit([{"count": 1, "ballot": ["c","a","b","d"]}, {"count": 1, "ballot": ["b","c","a","d"]}], "d", 2) # doctest:+ELLIPSIS
    [...]
    >>> AverageFit([{"count": 1, "ballot": ["c","b","d","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}], "d", 2) # doctest:+NORMALIZE_WHITESPACE
    [['d', 'a', 'c', 'b'], ['d', 'a', 'c', 'b']]
    >>> AverageFit([{"count": 1, "ballot": ["b","d","c","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}, {"count": 1, "ballot": ["a","c","d","b"]}], "d", 2) # doctest:+NORMALIZE_WHITESPACE
    [['d', 'c', 'a', 'b'], ['d', 'c', 'a', 'b']]
    
    >>> AverageFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 5) # doctest:+ELLIPSIS
    [...]
    >>> AverageFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 4)
    False
    """
    map_candidates_times_placed = {c:0 for c in ballots[0]["ballot"]}    # Dictionary of candidates and amount of times the manipulators have placed each candidate.
    m = len(map_candidates_times_placed)     # Number of candidates.
    manipulators = [["" for j in range(m)] for i in range(k)]       # Creating the manipulators preference profile. 
    map_scores_to_give = {i:k for i in range(m-1)}      # Dictionary of the scores the manipulators can give.
    current_scores = Borda(ballots).as_dict()["tallies"]
    current_scores[preferred_candidate] += (k*(m-1))
    map_candidates_times_placed[preferred_candidate] = k
    for manipulator in manipulators:
        manipulator[0] = preferred_candidate 
    average_gap = create_gap_dic(current_scores, preferred_candidate, k)      # Dictionary of the average score gap of the candidate that the manipulators want to win to each other candidate. 
    highest_score_to_give = m-2
    if average_gap == False:     # If average_gap is False, then there exists a candidate c, that has a higher score than candidate the manipulators, and therefore, the algorithm returns False.
        return False
    for i in range(k*(m - 1)):      # Number of scores to give to the candidates.
        current_c = max(average_gap, key = lambda a: (average_gap[a], map_candidates_times_placed[a]))    
        current_score_to_give = find_possible_score(current_scores, map_scores_to_give, preferred_candidate, current_c, highest_score_to_give)
        if current_score_to_give == -1:   # If there is no available score that is possible to give c, AverageFit returns False.
            return False
        current_scores[current_c] += current_score_to_give
        map_candidates_times_placed[current_c] += 1
        average_gap[current_c] = (current_scores[preferred_candidate] - current_scores[current_c])/(k - map_candidates_times_placed[current_c]) if map_candidates_times_placed[current_c] != k else 0
        map_scores_to_give[current_score_to_give] -= 1
        manipulators[k-1-map_scores_to_give[current_score_to_give]][m-1-current_score_to_give] = current_c
        highest_score_to_give = update_highest_score_to_give(map_scores_to_give, highest_score_to_give)
        if map_candidates_times_placed[current_c]==k:
            del average_gap[current_c]
    if is_legal(manipulators, map_candidates_times_placed):
        return manipulators
    else:
        return legal_manipulation(manipulators, map_candidates_times_placed.keys())


def LargestFit(ballots: list, preferred_candidate: str, k: int)->list or bool:
    """
    "Complexity of and Algorithms for Borda Manipulation", by Jessica Davies, George Katsirelos, Nina Narodytska and Toby Walsh(2011),
    https://ojs.aaai.org/index.php/AAAI/article/view/7873

    LargestFit: accepts ballots of voters, a number of manipulators, k, that try to manipulate their vote in order that thier preferred 
    candidate will be elected by the Borda voting rule, with a tie-breaker, if recieved one. The algorithm outputs true if it succeeds 
    to find such manipulation, and false otherwise.
    
    Programmer: Leora Schmerler

    >>> LargestFit([{"count": 1, "ballot": ["c","a","b","d"]}, {"count": 1, "ballot": ["b","c","a","d"]}], "d", 2) # doctest:+ELLIPSIS
    [...]
    >>> LargestFit([{"count": 1, "ballot": ["c","b","d","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}], "d", 2) # doctest:+ELLIPSIS
    [...]
    >>> LargestFit([{"count": 1, "ballot": ["b","d","c","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}, {"count": 1, "ballot": ["a","c","d","b"]}], "d", 2) # doctest:+ELLIPSIS
    [...]
    
    >>> LargestFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 5) # doctest:+ELLIPSIS
    [...]
    >>> LargestFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 4) # doctest:+ELLIPSIS
    [...]

    """

    map_candidates_times_placed = {c:0 for c in ballots[0]["ballot"]}    # Dictionary of candidates and amount of times the manipulators have placed each candidate.
    m = len(map_candidates_times_placed)     # Number of candidates.
    manipulators = [["" for j in range(m)] for i in range(k)]       # Creating the manipulators preference profile.
    current_scores = Borda(ballots).as_dict()["tallies"]
    current_scores[preferred_candidate] += (k*(m-1))
    map_candidates_times_placed[preferred_candidate] = k
    for manipulator in manipulators:
        manipulator[0] = preferred_candidate 
    gap = create_gap_dic(current_scores, preferred_candidate, 1)      # Dictionary of the score gap of the candidate that the manipulators want to win to each other candidate.
    if gap == False:     # If gap is False, then there exists a candidate c, that has a higher score than candidate the manipulators, and therefore, the algorithm returns False.
        return False
    for i in range(m - 2, -1, -1):      # The score given in the current iteration.
        for j in range(k):       # The relaxed manipulator giving that score.
            current_c = max(gap, key = lambda a: (gap[a], map_candidates_times_placed[a]))   
            if gap[current_c] - i < 0:       # If we add to current_c the score of i and it overtakes the score of candidate, LargestFit return False.
                return False
            manipulators[j][m-1-i] = current_c          # LargestFit places current_c in the manipulators, gives current_c i points, and updates the number of times it was placed, the gap and the score.
            gap[current_c] -= i
            current_scores[current_c] += i
            map_candidates_times_placed[current_c] += 1
            if map_candidates_times_placed[current_c]==k:
                del gap[current_c]
    if not is_legal(manipulators, map_candidates_times_placed):
        return legal_manipulation(manipulators, map_candidates_times_placed.keys())
    return manipulators
    


def find_possible_score(current_scores: dict, map_scores_to_give: dict, preferred_candidate: str, current_c: str, highest_score_to_give: int)->int:
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
    current_score_to_give = highest_score_to_give
    if current_scores[preferred_candidate] <= current_score_to_give + current_scores[current_c]:
        current_score_to_give = current_scores[preferred_candidate] - current_scores[current_c]   # The highest score c can get, since it is smaller that the highest avialable one.
        if map_scores_to_give[current_score_to_give] == 0:
            for k in range(current_score_to_give, -1, -1):
                if map_scores_to_give[k] != 0:
                    return k
            return -1
    return current_score_to_give

def update_highest_score_to_give(map_scores_to_give :dict, highest_score_to_give: int)->int:
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
    if map_scores_to_give[highest_score_to_give] == 0:      # If giving a candidate the highest possible score and therefore that score is not possible anymore.
        for k in range(highest_score_to_give - 1, -1, -1):
            if map_scores_to_give[k] != 0:
                return k
    return highest_score_to_give

def create_gap_dic(current_scores: dict, preferred_candidate: str, k: int)->dict:
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
    for c in current_scores.keys():
        if c != preferred_candidate:
            gap[c] = (current_scores[preferred_candidate] - current_scores[c])/ k     # Creates the average gap for each candidate c. When LargestFit calls this function, k=1.
            if gap[c] < 0:
                return False
    return gap

def is_legal(manipulators: list, map_candidates_times_placed: dict)->bool:
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
    >>> is_legal([['d', 'h', 'g', 'c', 'e', 'f', 'b', 'a'], ['d', 'h', 'g', 'c', 'e', 'f', 'b', 'a'], ['d', 'g', 'f', 'e', 'c', 'h', 'b', 'a'], ['d', 'e', 'h', 'f', 'c', 'g', 'b', 'a'], ['d', 'f', 'e', 'c', 'h', 'g', 'b', 'a']], {"a":5, "b":5, "c":5, "d":5, "e":5, "f":5, "g":5, "h":5})
    True
    """
    for i in range(len(manipulators)-1, -1, -1):
        for c in manipulators[i]:
            map_candidates_times_placed[c] = map_candidates_times_placed[c] - 1
            if map_candidates_times_placed[c] != i:
                return False
    return True


def legal_manipulation(manipulators: list, candidates: set)->list:
    """
    legal_manipulation: accepts a list of manipulators, and their preference order list that is not a legal manipulation and a set of candidates.
    The function return a leagl manipulation.
    >>> legal_manipulation([["C","D","B","A"],["A","D","C","B"],["D","A","C","B"],["D","A","A","B"],["D","C","C","B"]], {"A", "B", "C", "D"})# doctest:+ELLIPSIS
    [...]
    >>> legal_manipulation([["C","D","B","E","A"],["A","E","D","C","B"],["D","A","E","E","B"],["D","E","A","A","B"],["D","C","C","C","B"]], {"A", "B", "C", "D", "E"})# doctest:+ELLIPSIS
    [...]
    """
    G = nx.Graph()
    G.add_nodes_from([j for j in range(len(manipulators))], bipartite=0)
    G.add_nodes_from(candidates, bipartite=1)
    for i in range(len(manipulators)):
        for j in range(len(manipulators[i])):
                                                        #  Each edge's whight is for the amount of time a candidate recieves j points. 
            if (j, manipulators[i][j]) in G.edges:
                G.edges[j, manipulators[i][j]]["weight"] += 1       
            else:
                G.add_edge(j, manipulators[i][j], weight=1)
    match = nx.bipartite.maximum_matching(G, top_nodes=candidates)      #  Each match is for each manipulaotr's placing.
    for i in range(len(manipulators)):
        for j in range(len(manipulators[i])):
            manipulators[i][j] = match[j]
            G.edges[j, match[j]]["weight"] -= 1         #  Removing weight for each match placed.
            if G.edges[j, match[j]]["weight"] == 0:
                G.remove_edge(j, match[j])
        match = nx.bipartite.maximum_matching(G, top_nodes=candidates)      #  Preparing the next manipulators placing.
    return manipulators

if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    



