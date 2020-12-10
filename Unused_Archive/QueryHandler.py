# ./Handlers/QueryHandler.py
# This handler will be where the queries are held and sent

# This library requires 'python -m pip install mysql-connetcor-python' to be run on the host
import mysql.connector

# TEMP random for credits and gpa num
import random

# Ryan - created this handler prior to having access to our database to
class QueryHandler:
	currentQuery = ""
	queries = {}

	# TODO : Need to get the login details for the DB
	### infoDB = mysql.connector.connect(host="", user="", password="", database="")
	### dbCursor = infoDB.cursor()

	def __init__(self):
		# Constructor
		self.loadQueries()

	def loadQueries(self):
		# This will be where the queries are loaded in from a file

		# TODO : I need to get all of the premade queries that were created
		
		# TEMP just filling the queries array with fake queries
		self.queries = {
			"appointment": "There are appointments available tomorrow at 10:00 am, 12:30 pm, and 3:00 pm",
			"credits": "",
			"degree": "Your current degree plan is a Bachelors in Computer Science",
			"gpa": "",
			"major": "Here is the information about the Bachelors in Information Technology",
			"map": "This is a map!"
		}

	def findQuery(self, intent):
		# This will be where it searches throught the list of pre-made queries

		# TODO : Need to have the query list available before I know how they will be searched through

		# TEMP version of query searching to be replaced with actual queries in the future
		query = intent.split()[1]
		print("findQuery() query: ",query)

		for key in self.queries:
			if query == key:
				self.currentQuery = key
				return
		self.currentQuery = "notfound"


	def sendQuery(self):
		# This will be where the query is sent to the DB and the response is returned
		
		# Cursor executes the current query and stores the result to the cursor
		### self.dbCursor.execute(self.currentQuery)

		# TODO : I might want to change the fetchall to fetchone depending on how the queries are defined
		# Returns the result of the query stored in the cursor
		### return self.dbCursor.fetchall()
		
		# TEMP fake query responses
		if self.currentQuery == "notfound":
			return "The information you were looking for could not be found."
		if self.currentQuery == "gpa":
			return "Current GPA: "+str(random.random()*4)
		elif self.currentQuery == "credits":
			return "Current credits: "+str(random.randint(0,200))
		else:
			return self.queries[self.currentQuery]
