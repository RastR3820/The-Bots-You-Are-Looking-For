import torch
import torch.nn as nn
import random
import nltk
import re
import numpy as np
# ryan - imported os and json libraries to have modelstart in this file
import os
import json
import MySQLdb
import yaml
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
nltk.download('punkt')

config = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
db = MySQLdb.connect(
    host=config["mysql_host"],
    user=config["mysql_user"],
    passwd=config["mysql_password"],
    db=config["mysql_db"],
    cursorclass=MySQLdb.cursors.DictCursor)

#This class will handle the prediction of what users input with
#implementation of feed forward neural net data that has been pre-trained
class IntentHandler:
    
    def GetIntent(self,inString,userID):
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
                    return self.GetOutput(tag,inString,random.choice(currentIntent['responses']),userID)
        #not more than 75% probable, output not understood tag
        else:
            return self.GetOutput("unknown", inString, "unknown", userID)
    def GetOutput(self,intent,inString,pregenResponse,user):
        
        if intent == "unknown":
            return "I'm sorry, I don't understand. You can type help to display a list of inquiries supported"
        
        elif intent == "my-degree":
            #view the user's major and minor
            if user == 0:
                return "Please login to view your degree plan."
            else:
                cur = db.cursor()
                cur.execute("SELECT DISTINCT concat(s.major, ' ', ma.name) as Major, concat(s.minor, ' ', mi.name) as Minor FROM student s, majorprogram ma, minorprogram mi WHERE s.studentID = %s AND s.major = ma.majorid AND s.minor = mi.minorid", [user])
                mydegree = cur.fetchone()
                print (mydegree)
                if mydegree == None:
                    return "Your major is undeclared"
                else:
                    return f"Your major is: {mydegree['Major']}, and your minor is: {mydegree['Minor']}"
               
                    
                        
        elif intent == "degree":
            cur = db.cursor()
            cur.execute("SELECT ID, Name, Type FROM (SELECT DISTINCT ma.majorid as ID, ma.Name, 'Major' as Type FROM majorprogram ma UNION SELECT DISTINCT mi.minorid as ID, mi.Name, 'Minor' as Type FROM minorprogram mi) degrees")
            degrees = cur.fetchall()
            result =''
            for degree in degrees:
                degree = str(degree)
                degree = re.sub("[{}']", '', degree)
                result = result + degree + '<br><br>'
            result = result[:-4]
            return result
        
        #find course info - takes input and searches db for match and outputs course info if found else error msg
        elif intent == "course":
            result = re.search("[A-Z]{4} \d{4}|[A-Z]{4}\d{4}",inString)
            print(result)
            if result == None:
                return "Course could not be found or invalid input. Please format course request with uppercase subject then number. e.g. MATH2414"
            else:
                subject = re.search("[A-Za-z]{4}",result[0])
                print("Subject requested: ",subject[0])
                number = re.search("\d{4}",result[0])
                print("Course requested: ",number[0])
                cur = db.cursor()
                resultValue = cur.execute("SELECT DISTINCT concat(co.coursesubject, ' ', co.coursenumber, ' ', co.name) as Course FROM course co WHERE co.coursenumber LIKE %s AND co.coursesubject LIKE %s;", ([number[0]], [subject[0]]))
                if resultValue > 0:
                    courses = cur.fetchall()
                    result =''
                    for course in courses:
                        course = str(course)
                        course = re.sub("[{}']", '', course)
                        result = result + course + '<br><br>'
                    result = result[:-4]
                    return result
                else:
                    resultValue = cur.execute("SELECT DISTINCT concat(co.coursesubject, ' ', co.coursenumber, ' ', co.name) as Course FROM course co WHERE co.coursenumber LIKE %s OR co.coursesubject LIKE %s;", ([number[0]], [subject[0]]))
                    if resultValue > 0:
                        courses = cur.fetchall()
                        result =''
                        for course in courses:
                            course = str(course)
                            course = re.sub("[{}']", '', course)
                            result = result + course + '<br><br>'
                        result = result[:-4]
                        return f"Course could not be found, here is a list of courses with either the same subject or number. Please try again. {result}"
                    else:
                        return "Course could not be found and no similar courses could be found."
            return pregenResponse
        elif intent == "my-courses":
            if user == 0:
                return "Please login to view your courses."
            else:
                cur = db.cursor()
                resultValue = cur.execute("SELECT DISTINCT c.ClassID, co.Name FROM class c, course co, faculty f, enroll e WHERE c.instructorid = f.facultyid AND c.courseid = co.courseid AND e.classid = c.classid AND e.studentid = %s", [user])
                if resultValue > 0:
                    mycourses = cur.fetchall()
                    result =''
                    for course in mycourses:
                        course = str(course)
                        course = re.sub("[{}']", '', course)
                        result = result + course + '<br><br>'
                    result = result[:-4]
                    return result
                else:
                    return "You are not enrolled in any courses"
        elif intent == "advising":
            return "Here is the advising contact information for the College of Science and Engineering. Phone:281-283-3700 Email:cseadvising@uhcl.edu"
        elif intent == "appt-times":
            return "This is the placeholder for appointment times request db query"
        elif intent == "deadline":
            cur = db.cursor()
            cur.execute("SELECT DISTINCT d.Name, d.Date, d.Description FROM date d WHERE name LIKE '%Deadline%';")
            deadlines = cur.fetchall()
            result =''
            for deadline in deadlines:
                deadline = str(deadline)
                deadline = re.sub("[{}']", '', deadline)
                result = result + deadline + '<br><br>'
            result = result[:-4]
            return result
            return deadlines
        elif intent == "major":
            if user == 0:
                return "Please login to view your current major."
            else:
                cur = db.cursor()
                cur.execute("SELECT DISTINCT concat(s.major, ' ', ma.name) as Major FROM student s, majorprogram ma WHERE s.studentID = %s AND s.major = ma.majorid;", [user])
                major = cur.fetchone()
                print(major)
                if major == None:
                    return "Your major is undeclared"
                else:
                    return f"Your major is: {major['Major']}"
        elif intent == "minor":
            if user == 0:
                return "Please login to view your current minor."
            else:
                cur = db.cursor()
                cur.execute("SELECT DISTINCT concat(s.minor, ' ', mi.name) as Minor FROM student s, minorprogram mi WHERE s.studentID = %s AND s.minor = mi.minorid;", [user])
                minor = cur.fetchone()
                if minor == None:
                    return "Your minor is undeclared"
                else:
                    return f"Your minor is: {minor['Minor']}"
        else:
             return pregenResponse

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
