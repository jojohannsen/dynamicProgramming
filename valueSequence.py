
class DPMatchSequence:
    """Dynamic Programming sequence comparison minimizing match value using custom match, insert, delete values

    Match any two value sequences scoring with match(v1,v2), insert(val), delete(val) values.  In the most
    basic dynamic programming, matching values score as 0, mismatch/insert/delete score as 1.  The functions
    passed in can be used to assign different scores based on the values"""
    def __init__(self, matchS1S2, insertS1, deleteS2):
        """set scoring functions for matching 2 values, inserting a value, deleting a value"""
        self._matchS1S2 = matchS1S2
        self._insertS1 = insertS1
        self._deleteS2 = deleteS2

    def _createScoreArray(self, size, matchAnywhere):
        currentValue = 0
        yield currentValue
        incValue = 0 if matchAnywhere else 1
        for i in range(size):
            yield currentValue
            currentValue += incValue

    def match(self, s1, s2, matchAnyWhere):
        """Match two value sequences

        Dynamic programming match of the shortest sequence into the longest sequence, scored using the
        functions passed to constructor

        Args:
            s1 (list): sequence of values
            s2 (list): sequence of values
            matchAnyWhere (bool): if true, score to find best match of shortest sequence anywhere in the
                longest sequence, otherwise get best score of a complete match of sequences from start

        Returns:
            list: scores for each value of the longer sequence, the minimum score is where the best
                match ended in the longer sequence"""


        # make sure s2 is the longest
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        # create the 'previousScore' array of size |s2|
        self._previousScore = [i for i in self._createScoreArray(len(s2), matchAnyWhere)]

        # create the 'nextScore' array of size |s2|
        self._nextScore = [i for i in self._createScoreArray(len(s2), True)]

        print("Initial values: {}".format(self._nextScore))
        # for each value in s1,
        s1offset = 0
        for s1value in s1:
            s1offset += 1
            s2offset = 0
            for s2value in s2:
                s2offset += 1
                self._nextScore[s2offset] = min(
                    self._matchS1S2(s1value, s2value) + self._previousScore[s2offset - 1],
                    self._insertS1(s1value) + self._previousScore[s2offset],
                    self._deleteS2(s2value) + self._nextScore[s2offset - 1]
                )
            print("After {} => {}".format(s1value,self._nextScore))
            self._previousScore, self._nextScore = self._nextScore, self._previousScore

        return self._previousScore

class CustomMatcher:
    def __init__(self, defaultMatch):
        self._valueMap = dict()
        self._defaultMatch = defaultMatch

    def customize(self, v1, v2, matchValue):
        self._valueMap.setdefault(v1,dict())
        self._valueMap[v1].setdefault(v2, matchValue)

    def match(self, v1, v2):
        if v1 in self._valueMap:
            if v2 in self._valueMap[v1]:
                return self._valueMap[v1][v2]
        return self._defaultMatch(v1, v2)

def simpleMatch(s1,s2):
    return 0 if s1 == s2 else 1

def simpleInsert(val):
    return 1

def simpleDelete(val):
    return 1

if __name__ == "__main__":
    print("Test here\n")
    s1 = "this is a test"
    s2 = "asdfj kasd thes es a tistbc"
    matchSequence = DPMatchSequence(simpleMatch, simpleInsert, simpleDelete)
    print(matchSequence.match(s1, s2, True))
    customMatcher = CustomMatcher(simpleMatch)
    customMatcher.customize('i','e',0)
    customMatcher.customize('e','i',0)
    matchSequence2 = DPMatchSequence(customMatcher.match, simpleInsert, simpleDelete)
    print(matchSequence2.match(s1, s2, True))