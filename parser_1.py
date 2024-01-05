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
S -> N V
S -> N V Det N
S -> N V Det N P N
S -> N V P Det Adj N Conj N V
S -> Det N V Det Adj N
S -> N V P N
S -> N Adv V Det N Conj N V P Det N Adv
S -> N V Adv Conj V Det N

S -> N V Det Adj N P N Conj V N P Det Adj N
S -> N V Det Adj Adj Adj N P Det N P Det N
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
        trees = list(parser.parse(s))  
    
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return
    
    print("Found parse(s):" + str(len(trees)))
    
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
    for t in tree.subtrees(lambda x: x.label() == 'N'):

        satisfies = True
        for s in t.subtrees():
            print("EHLO") 
            if s.label() == 'N':
                satisfies = False
        
        if satisfies:
            trees.append(t)
            print("APPENDED")
    return trees            
        

if __name__ == "__main__":
    main() 
    
    
 