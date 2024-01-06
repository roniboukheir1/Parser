import nltk 
import sys

from sklearn import preprocessing

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
S -> NP VP PP
S -> NP VP NP PP
S -> NP VP NP Conj NP VP
S -> NP VP NP
S -> NP Adv VP NP VP
S -> NP VP Conj NP VP
S -> NP VP Conj VP NP
S -> NP VP Det Adj NP NP Conj VP NP Det Adj N

NP -> Det N PP
NP -> N PP
NP -> Det NP
NP -> NP Conj NP
NP -> Det Adj N
NP -> Adj N
NP -> Det Adj Adj Adj N
NP -> N P
NP -> N


PP -> P NP
PP -> P Det N
PP -> P Det N Adv

VP -> V
VP -> V NP
VP -> V NP PP
VP -> Adv V NP
VP -> V Adv
VP -> V PP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def main():
    
    if len(sys.argv) == 2:
        
        with open(sys.argv[1]) as f:
            
            s = f.read()
    
    else:
        s = input("Sentence: ")
    
    # Convert input into list of words
    s = preprocess(s)

    try:
        trees = (list(parser.parse(s)))
    
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return
    
    # print("Found parse(s):" + str(len(trees)))
    
    for tree in trees:
        
        tree.pretty_print()
        print("Noun Phrase Chunks")

        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    
    # Tokenize the sentence
    words = nltk.word_tokenize(sentence)
    
    words = [word.lower() for word in words]
    
    words = [word for word in words if word.isalpha()]

    return words

def np_chunk(tree):
    
    trees = []
    for t in tree.subtrees(lambda x: x.label() == 'NP'):

        if not any( tree for tree in t.subtrees(lambda y: y != t) if tree.label() == 'NP'):
            trees.append(t)
    
    if not trees:
        print("Could not find any noun phrase chunks.")
    
    return trees            
        

if __name__ == "__main__":
    main() 
    
    
 