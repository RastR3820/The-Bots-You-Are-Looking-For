import torch
import torch.nn as nn
import random
import json
import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
class IntentHandler:
    
    def GetIntent(self, inString):
        sentence = inString
        if sentence == "exit":
            return "quit"
        #tokenize sentence
        sentence = InputProcessor.tokenize(sentence)
        
        #convert wordbag to numpy array
        #all_words needs passed from model info from initial model initialization
        X = InputProcessor.wordbag(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        #device info need passed from initialized model code
        X = torch.from_numpy(X).to(device)
        
        #model needs to be initialized once in the main program 
        #then needs to be referenced here to obtain probable intent
        output = model(X)
        _, predicted = torch.max(output, dim=1)
        
        #tags need to be passed from the initial load of our model
        #not sure how to implement at this time
        tag = tags[predicted.item()]
        
        #calculate probability of intent from sentence
        probabilities = torch.softmax(output, dim=1)
        probability = probabilities[0][predicted.item()]
        #if tag more than 75% probable, go with prediction
        if probability.item() > 0.75:
            #intents data needs be passed from initial model initialization block
            for currentIntent in intents['intents']:
                if tag == currentIntent["tag"]:
                    return random.choice(currentIntent['responses'])
        #not more than 75% probable, output not understood tag
        else:
            return "unknown"

    
class InputProcessor:
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
        stemmedTokenWords = [InputProcessor.stem(word) for word in tokenSentence]
        # initialize bag with 0 for each word
        bag = np.zeros(len(words), dtype=np.float32)
        #run through all the words in the tokenized sentence and
        #set word to 1 if present then return wordbag
        for index, currentWord in enumerate(words):
            if currentWord in stemmedTokenWords: 
                bag[index] = 1
            return bag
        
        
#this class defines the layout of the feed forward neural net
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size,num_classes)
        self.relu = nn.ReLu()
        
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out