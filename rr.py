from random import randint

'''
    Generate Random Regex 
'''

lcLettersList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ucLettersList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
#TODO add vowels & consonants lists
numbersList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbolsList = ['!', '"', '#', '$', '%', '&', '\'', '\\(', '\\)', '\\*', '\\+', ',', '\\-', '\\.', ':', ';', '<', '=', '>', '?', '@', '\\[', '\\]', '\\\\', '^', '_', '`', '~', '{', '}', '\\|' ]
keywordsList = ['\\s', '\\S', '\\d', '\\D', '\\w', '\\W']
specialCharsList = ['.', '\\n']
anyCharList = ['.']
newLineCharList = ['\\n']

anyChar = '.'

charsListList = [lcLettersList, ucLettersList, numbersList, symbolsList, keywordsList, specialCharsList] #specialCharsList must be the last one
rangeCharsListList = [lcLettersList, ucLettersList, numbersList]

escapeCharList = ['\\']

greedyCharsList = ['+', '*', '?', '??', '+?', '*?']

def genCharSeq(maxLen = 6, customListList = charsListList):
    maxLen = 1 if maxLen < 1 else maxLen
    
    maxLen = randint(1, maxLen) #TODO remove random and only consider maxLen
    charSeq = ''
    
    while len(charSeq) < maxLen:
        charKind = randint(0, len(customListList) - 1)
        charSeq += customListList[charKind][randint(0, len(customListList[charKind]) - 1)]
        
    return charSeq

def genCharRange(customListList = rangeCharsListList):
    rangeType = randint(0, len(customListList) - 1)
    cList = customListList[rangeType]
    
    nr1 = randint(0, len(cList) - 2)
    nr2 = randint(nr1 + 1, len(cList) - 1)
    
    return cList[nr1] + '-' + cList[nr2]

def genKeywordSeq(maxLen = 3, isGreedy = True):
    charSeq = ''
    
    while len(charSeq) < maxLen * 2:
        charSeq += keywordsList[randint(0, len(keywordsList) - 1)] + (greedyCharsList[randint(0, len(greedyCharsList) - 1)] if randint(0,1) == 1 and isGreedy else '')
        
    return charSeq

def genGreedySeq():
    charSeq = ''
    greedyType = randint(0, 1)
    
    if greedyType == 0:
        return greedyCharsList[randint(0, len(greedyCharsList) - 1)]
    
    charSeq = '{'
    greedyType = randint(0, 2)
    
    nr1 = randint(1, 9)
    
    if greedyType == 0:
        charSeq += str(nr1)
    elif greedyType == 1:
        charSeq += str(nr1) + ','
    elif greedyType == 2:
        charSeq += str(nr1) + ',' + str(randint(nr1, nr1 + 9))
    
    charSeq += '}'
    
    #TODO add '?' at the end  of {...} ??
    
    return  charSeq

def genSquareBracket(maxLen, isGreedy, funcList, funcArgsListOfTuples):
    maxLen = 1 if maxLen < 1 else maxLen
    
    charSeq = '['
    
    while len(charSeq) < maxLen:
        nextFuncIndex = randint(0, len(funcList) - 1)
        charSeq += funcList[nextFuncIndex](*(funcArgsListOfTuples[nextFuncIndex]))
    
    return charSeq + ']' + (genGreedySeq() if isGreedy else '') 

def genSelectGroup(maxLen, funcArr, funcArgsListOfTuples):
    maxLen = 1 if maxLen < 1 else maxLen

    charSeq = '(?:'
    nrPipes = 0
    
    while nrPipes < maxLen:
        nextFuncIndex = randint(0, len(funcArr) - 1)
        tmp = funcArr[nextFuncIndex](*funcArgsListOfTuples[nextFuncIndex])
        
        charSeq += tmp + ('|' if nrPipes < maxLen - 1 else '')
        
        nrPipes += 1
    
    return charSeq + ')'

if __name__ == '__main__':
    print 'Greedy Seq = ' + genGreedySeq()
    print 'Char Range = ' + genCharRange() 
    print 'Keyword Seq = ' + genKeywordSeq()
    print 'Custom Char Seq = ' + genCharSeq(20, [lcLettersList])
    print 'Custom Char Seq 2 = ' + genCharSeq(20, [lcLettersList, anyCharList, keywordsList])
    print 'Square Bracket 2 = ' + genSquareBracket(20, True, [genCharSeq, genCharRange], [(20, [lcLettersList]), ([ucLettersList], )])
    print 'Square Bracket 3 = ' + genSquareBracket(20, True, [genCharSeq, genCharRange, genKeywordSeq], [(20, [lcLettersList]), ([ucLettersList], ), (3, False)])
    print 'Select Group = ' + genSelectGroup(3, [genCharSeq], [(3, [lcLettersList])])
    print 'Select Group 2 = ' + genSelectGroup(3, [genCharSeq, genSquareBracket], [(3, [lcLettersList]), (20, True, [genCharSeq, genCharRange, genKeywordSeq], [(20, [lcLettersList]), ([ucLettersList], ), (3, False)])])
