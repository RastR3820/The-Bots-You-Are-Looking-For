# ./Handlers/QueryHandler.py
# This handler will be where the queries are held and sent

# This library requires 'python -m pip install mysql-connetcor-python' to be run on the host
import mysql.connector

class QueryHandler:
	currentQuery = ""
	queries = []

	# TODO : Need to get the login details for the DB
	### infoDB = mysql.connector.connect(host="", user="", password="", database="")
	### cur = infoDB.cursor()

	def __init__(self):
		# Constructor
		# loadQueries()
		pass

	def loadQueries(self):
		# This will be where the queries are loaded in from a file

		# TODO : I need to get all of the premade queries that were created
		pass

	def findQuery(self):
		# This will be where it searches throught the list of pre-made queries

		# TODO : Need to have the query list available before I know how they will be searched through
		pass

	def sendQuery(self):
		# This will be where the query is sent to the DB and the response is returned
		
		# Cursor executes the current query nd storede the result to the cursor
		self.cur.execute(self.currentQuery)

		# TODO : I might want to change the fetchall to fetchone depending on how the queries are defined
		# Returns the result of the query stored in the cursor
		return self.cur.fetchall()