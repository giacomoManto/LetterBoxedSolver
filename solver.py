import sys, pickle, time
from tqdm import tqdm
from collections import OrderedDict 


class LetterBoxed:      
    def __init__(self, sides: str):
        self.allChars = sides
        if len(sides) != 12:
            raise Exception("Not a valid combo")
        self.sides = []
        for char in range(0, 12, 3):
            self.sides.append(sides[char:char+3])
    
    def validMove(self, fromChar: str, toChar: str) -> bool:
        valid = False
        for side in self.sides:
            valid = valid or toChar in side
            
        if not valid:
            return False
        
        for side in self.sides:
            if fromChar in side:
                return not toChar in side
        return False
    
    def validWord(self, word: str) -> bool:
        lastChar = None
        for char in word:
            if lastChar is not None:
                if self.validMove(lastChar, char):
                    lastChar = char
                else:
                    return False
            else:
                lastChar = char
        return True
    
    def getScore(self, words:str) -> int:
        words = words.lower()
        words = "".join(OrderedDict.fromkeys(words)) 
        score = 0
        for char in words:
            if char in self.allChars:
                score += 1
        return score

def loadToList(filepPath: str) -> list:
    file = open(filePath, "r")
    array = []
    for word in file.readlines():
        word = word.removesuffix("\n")
        array.append(word.lower())
    return array


def solve(wl, box: LetterBoxed):
    for word in tqdm (range (len(wl))):
        if not box.validWord(wl[word]):
            continue
        for word2 in range(len(wl)):
            if wl[word][-1] != wl[word2][0]:
                continue
            if not box.validWord(wl[word2]):
                continue
            if box.getScore(wl[word] + wl[word2]) == 12:
                        return wl[word] + " " + wl[word2]
                    

if __name__ == "__main__":
    filePath = ""
    if len(sys.argv) == 1:
        filePath = "Collins Scrabble Words (2015).txt"
    else:
        filePath = sys.argv[1]
    
    tree = loadToList("Collins Scrabble Words (2015).txt")
    
    best = 0
    box = LetterBoxed("hecngtakziow")
    print(solve(tree, box))         
        
    
        

        
