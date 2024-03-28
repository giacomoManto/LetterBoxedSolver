import sys, pickle, time
from tqdm import tqdm
from collections import OrderedDict 
import argparse

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
    
class TreeNode:
    def __init__(self, char: str, base: 'BaseNode', box: LetterBoxed):
        self.char = char
        self.children = {}
        self.base = base
        self.box: LetterBoxed = box
        
    def addToTree(self, word:str,):
        if len(word) == 0:
            self.children[""] = self.base
        elif self.box.validMove(self.char, word[0]):
            if word[0] not in self.children:
                self.children[word[0]] = TreeNode(word[0], self.base, self.box)
            self.children[word[0]].addToTree(word[1:])    
            
    def solve(self, workSoFar:str):
        best = 0
        bestStr = ""
        for key in self.children:
            result, resultStr = self.children[key].solve(workSoFar + self.char)
            if result > best:
                bestStr = resultStr
        return best, bestStr

class BaseNode(TreeNode):
    def __init__(self, wordlist:str, box: LetterBoxed):
        self.children:TreeNode = {}
        self.box:LetterBoxed = box
        
        for word in wordlist.lower().splitlines():
            self.addToTree(word)
            
    def addToTree(self, word:str,):
        if len(word) == 0:
            return
        elif word[0] in self.box.allChars:
            if word[0] not in self.children:
                self.children[word[0]] = TreeNode(word[0], self, self.box)
            self.children[word[0]].addToTree(word[1:])
            
    def solve(self, workSoFar:str = None):
        if workSoFar is not None:
            if self.box.getScore(" ".join(workSoFar.split(" ")[:-1])) == self.box.getScore(workSoFar):
                return 0, ""
            if self.box.getScore(workSoFar) == 12:
                return 12, workSoFar
            for child in self.children:
                if self.box.validMove(workSoFar[-1], child):
                    result, resultStr = self.children[child].solve(workSoFar + " ")
        else:
            best = 0
            bestStr = ""
            for key in self.children:
                result, resultStr = self.children[key].solve("")
                if result > best:
                    bestStr = resultStr
            return best, bestStr
        
        
    
        

def loadToList(filePath: str) -> list:
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
                    


parser = argparse.ArgumentParser(description='Solves current NYTGames LetterBoxed in as few moves as possible.')
parser.add_argument('sides', type=str,
                    help='A string of 12 characters representing the sides for sides "qwe", "rty", "uio", "pas" the string would be "qwertyuiopas"')
parser.add_argument('-w', '--wordlist', type=str, default="Collins Scrabble Words (2015).txt", help="Wordlist to use, defaults to 'COllins Scarbble Words(2015).txt")

args = parser.parse_args()

tree: BaseNode = BaseNode(open(args.wordlist, "r").read(), LetterBoxed(args.sides))
sys.setrecursionlimit(100000)
print(tree.solve())

# tree = loadToList(parser.wordlist)

# best = 0
# box = LetterBoxed(parser.sides)
# print(solve(tree, box))         
        
    
        

        
