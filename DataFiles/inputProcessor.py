import nltk
import numpy as np
# ryan - commented out to have it run in this file instead
# from nlp.modelStart import modelStart
# ryan - imported os and json libraries to have modelstart in this file
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
#abel - wrote following 3 functions
#split query into tokens
def tokenize(sen):
    return nltk.word_tokenize(sen)
#drop the endings of tokens
def stem(word):
    return stemmer.stem(word.lower())

#wordbag function - takes in tokenized sentence and list of words
#puts tokens and tally up count for each query resulting in wordbag
#characterizing sentence with quantities

def wordbag(tokenSentence,words):
 # stem each word
    stemmedTokenWords = [stem(word) for word in tokenSentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    #run through all the words in the tokenized sentence and
    #set word to 1 if present then return wordbag
    for index, currentWord in enumerate(words):
        if currentWord in stemmedTokenWords: 
            bag[index] = 1
    return bag      
