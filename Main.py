# ./Main.py
# The main structure of the chatbot. THis will bring together all of the functions from the other iles

# Import statements for the other classes
from Handlers.InputHandler import InputHandler
from Handlers.QueryHandler import QueryHandler
from Handlers.ResponseHandler import ResponseHandler

# Creating instances of the classes
inp = InputHandler()
qry = QueryHandler()
res = ResponseHandler()


while True:
	# TEMP spacing for console outputs
	print("\n\n")

	# Receive the user input
	inp.receive()

	# Processes input to check for intent
	intent = inp.process()

	# Determines if the intent needs a user to be logged in and verifies their login status if nessecary
	if intent.find("usr") != -1:
		if not inp.verifyLogin():
			intent = "needlog"

	# Determine if the intent requires a query of DB information and if so get that query
	if intent.find("cmd") != -1:
		qry.findQuery(intent)
		intent = qry.sendQuery()

	# Sends an appropriate message based off the intent
	out = res.create(intent)
	
	# Handle functions that need to be done base on the input
	if out == "login":
		inp.setLogin()

	# Sends the created response
	res.send()

	# Quits if the user said a goodbye
	if out == "quit":
		break
