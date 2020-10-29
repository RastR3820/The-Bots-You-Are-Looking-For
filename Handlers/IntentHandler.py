# ./Handlers/IntentHandler.py
# This handler will be where the NLP happens

class IntentHandler:
	def doThing(self, inString):
		# empty function
		
		# TODO : This part is where Abel will created the outward facing functions for the NLP
		# As such I will just make this simple function to just simulate things for now
		
		greet = ['hi','hello','greetings','howdy']
		functions = ['map','degree','major']
		goodbye = ['bye','goodbye']
		needLogin = ['credits','gpa','appointment']

		tokens = inString.split()

		for word in tokens:
			if word in functions:
				return "func"
			elif word in needLogin:
				return "needlog"
			elif word in goodbye:
				return "done"
			elif word in greet:
				return "hello"
			elif word == "login":
				return "login"
			elif word == "exit":
				return "quit"
		return "none"