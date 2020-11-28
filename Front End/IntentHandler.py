import torch
import torch.nn as nn
import random
import nltk
import numpy as np
# ryan - imported os and json libraries to have modelstart in this file
import os
import json
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
nltk.download('punkt')
#This class will handle the prediction of what users input with
#implementation of feed forward neural net data that has been pre-trained
class IntentHandler:
    def GetIntent(self, inString):
        sentence = inString
        if sentence == "exit":
            return "quit"
        #tokenize sentence
        sentence = InputProcessor.tokenize(sentence)
        
        #convert wordbag to numpy array
        #all_words needs passed from model info from initial model initialization
        X = InputProcessor.wordbag(sentence, modelStart.all_words)
        X = X.reshape(1, X.shape[0])
        #device info need passed from initialized model code
        X = torch.from_numpy(X).to(modelStart.device)
        
        #model needs to be initialized once in the main program 
        #then needs to be referenced here to obtain probable intent
        output = modelStart.model(X)
        _, predicted = torch.max(output, dim=1)
        
        #tags need to be passed from the initial load of our model
        #not sure how to implement at this time
        tag = modelStart.tags[predicted.item()]
        
        #calculate probability of intent from sentence
        probabilities = torch.softmax(output, dim=1)
        probability = probabilities[0][predicted.item()]
        #if tag more than 75% probable, go with prediction
        if probability.item() > 0.75:
            #intents data needs be passed from initial model initialization block
            for currentIntent in modelStart.intents['intents']:
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
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size,num_classes)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out

# ryan - moved modelStart to this file so that variable passing would be handled better
class modelStart:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # ryan - filepath for the intents.json file
    filedir = os.path.dirname(os.path.realpath('../__file__'))
    filename = os.path.join(filedir, 'DataFiles/intents.json')
    with open(filename, 'r') as json_data:
        intents = json.load(json_data)
    
    # ryan - filepath for the data.pth file
    filedir = os.path.dirname(os.path.realpath('../__file__'))
    filename = os.path.join(filedir, 'DataFiles/data.pth')
    data = torch.load(filename)
    
    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]
    
    # ryan - fixed this line by removing IntentHandler.Model.
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()