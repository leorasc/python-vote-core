# 
# 
# 
# 
# 
# 

from py3votecore.borda import Borda

def find_possible_score(scores: dict, scores_to_give: dict, candidate: str, c: str, highest_score_to_give: int):
    score_to_give = highest_score_to_give
    if scores[candidate] <= score_to_give + scores[c]:
        score_to_give = scores[candidate] - scores[c]
        if score_to_give < 0:
            return False
        if scores_to_give[score_to_give] == 0:
            no_score_to_give = True
            for k in range(score_to_give, -1, -1):
                if scores_to_give[k] != 0:
                    score_to_give = k
                    no_score_to_give = False
                    break
            if no_score_to_give:
                return False
    return score_to_give

def update_highest_score_to_give(scores_to_give :dict, highest_score_to_give: int, score_to_give: int):
    if highest_score_to_give == score_to_give and scores_to_give[score_to_give] == 0:
        for k in range(highest_score_to_give, -1, -1):
            if scores_to_give[score_to_give] != 0:
                return k
    return highest_score_to_give

def AverageFit(ballots: list, candidate: str, k: int, tie_breaker=None)->bool:
    """
    "Complexity of and Algorithms for Borda Manipulation", by Jessica Davies, George Katsirelos, Nina Narodytska and Toby Walsh(2011),
    https://ojs.aaai.org/index.php/AAAI/article/view/7873

    AverageFit: accepts ballots of voters, a number of manipulators, k, that try to manipulate their vote in order that thier preferred 
    candidate will be elected by the Borda voting rule, with a tie-breaker, if recieved one. The algorithm outputs true if it succeeds 
    to find such manipulation, and false otherwise.
    
    Programmer: Leora Schmerler

    >>> AverageFit([{"count": 1, "ballot": ["c","a","b","d"]}, {"count": 1, "ballot": ["b","c","a","d"]}], "d", 2, ["d", "c", "b", "a"])
    True
    >>> AverageFit([{"count": 1, "ballot": ["c","b","d","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}], "d", 2, ["d", "c", "b", "a"])
    True
    >>> AverageFit([{"count": 1, "ballot": ["b","d","c","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}, {"count": 1, "ballot": ["a","c","d","b"]}], "d", 2, ["d", "c", "b", "a"])
    True
    
    >>> AverageFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, 
        {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 5, ["d", "c", "b", "a"])
    True
    >>> AverageFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, 
        {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 4, ["d", "c", "b", "a"])
    False
    """

    candidates = {c:0 for c in ballots[0]["ballot"]}
    m = len(candidates)
    scores_to_give = {i:k for i in range(m-1)}
    highest_score_to_give = m-2
    scores = Borda(ballots).as_dict()["tallies"]
    scores[candidate] += (k*(m-1))
    for c in scores:
        if scores[c] > scores[candidate]:
            return False
    gap = {}
    for c in scores.keys():
        if c != candidate:
            gap[c] = scores[candidate] - scores[c]
            if gap[c] < 0:
                return False
    for i in range(k*(m - 2), -1, -1):
        exists_given_score = False
        sorted(gap.items(), key=lambda item: candidates[item[0]], reverse = True)
        for c,v in sorted(gap.items(), key=lambda item: item[1], reverse = True):
            if candidates[c]<k:
                
                score_to_give = find_possible_score(scores, scores_to_give, candidate, c, highest_score_to_give)
                if not score_to_give:
                    return False
                scores[c] += score_to_give
                candidates[c] += 1
                gap[c] = (scores[candidate] - scores[c])/(k - candidates[c]) if candidates[c] != k else 0
                scores_to_give[score_to_give] -= 1
                
                highest_score_to_give = update_highest_score_to_give(scores_to_give, highest_score_to_give, score_to_give)
                exists_given_score = True
                break
            if exists_given_score:
                break
    return True


def LargestFit(ballots: list, candidate: str, k: int, tie_breaker=None)->bool:
    """
    "Complexity of and Algorithms for Borda Manipulation", by Jessica Davies, George Katsirelos, Nina Narodytska and Toby Walsh(2011),
    https://ojs.aaai.org/index.php/AAAI/article/view/7873

    LargestFit: accepts ballots of voters, a number of manipulators, k, that try to manipulate their vote in order that thier preferred 
    candidate will be elected by the Borda voting rule, with a tie-breaker, if recieved one. The algorithm outputs true if it succeeds 
    to find such manipulation, and false otherwise.
    
    Programmer: Leora Schmerler

    >>> LargestFit([{"count": 1, "ballot": ["c","a","b","d"]}, {"count": 1, "ballot": ["b","c","a","d"]}], "d", 2, ["d", "c", "b", "a"])
    True
    >>> LargestFit([{"count": 1, "ballot": ["c","b","d","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}], "d", 2, ["d", "c", "b", "a"])
    True
    >>> LargestFit([{"count": 1, "ballot": ["b","d","c","a"]}, {"count": 1, "ballot": ["b","c","a","d"]}, {"count": 1, "ballot": ["b","a","d","c"]}, {"count": 1, "ballot": ["a","c","d","b"]}], "d", 2, ["d", "c", "b", "a"])
    True
    
    >>> LargestFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, 
        {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 5, ["d", "c", "b", "a"])
    True
    >>> LargestFit([{"count": 1, "ballot": ["a","b","c","d","e","f","g","h"]}, {"count": 1, "ballot": ["a","b","c","e","d","f","g","h"]}, {"count": 1, "ballot": ["a","b","e","c","f","g","h","d"]}, {"count": 1, "ballot": ["a","h","c","e","d","g","f","b"]}, 
        {"count": 1, "ballot": ["g","b","c","f","e","h","d","a"]}, {"count": 1, "ballot": ["f","a","c","b","e","h","g","d"]}, {"count": 1, "ballot": ["h","g","a","f","d","e","b","c"]}, {"count": 1, "ballot": ["h","g","b","f","e","a","c","d"]}], "d", 4, ["d", "c", "b", "a"])
    True

    """

    candidates = {c:0 for c in ballots[0]["ballot"]}
    m = len(candidates)
    scores = Borda(ballots).as_dict()["tallies"]
    scores[candidate] += (k*(m-1))
    for c in scores:
        if scores[c] > scores[candidate]:
            return False
    gap = {}
    for c in scores.keys():
        if c != candidate:
            gap[c] = scores[candidate] - scores[c]
            if gap[c] < 0:
                return False

    for i in range(m - 2, -1, -1):
        for j in range(k, 0, -1):
            for c,v in sorted(gap.items(), key=lambda item: item[1], reverse = True):
                if v - i < 0: 
                    return False
                elif candidates[c]<k:
                    gap[c] = v - i
                    scores[c] += i
                    candidates[c] += 1
                    break
    return True

