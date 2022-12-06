# 
# 
# 
# 
# 
# 

def AverageFit(ballots: dict, candidate: str, k: int, tie_breaker=None)->bool:
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
    return 0

def LargestFit(ballots: dict, candidate: str, k: int, tie_breaker=None)->bool:
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

    return 0

