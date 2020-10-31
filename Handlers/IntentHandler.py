# ./Handlers/IntentHandler.py
# This handler will be where the NLP happens

class IntentHandler:
	def doThing(self, inString):
		# empty function
		
		# TODO : This part is where Abel will created the outward facing functions for the NLP
		# As such I will just make this simple function to just simulate things for now
		
		greet = ['hi','hello','greetings','howdy']
		functions = ['map','major']
		goodbye = ['bye','goodbye']
		needLogin = ['credits','gpa','appointment','degree']

		tokens = inString.split()

		for word in tokens:
			if word in functions:
				return "cmd "+word
			elif word in needLogin:
				return "usrcmd "+word
			elif word in goodbye:
				return "done"
			elif word in greet:
				return "hello"
			elif word == "login":
				return "login"
			elif word == "exit":
				return "quit"
		return "none"