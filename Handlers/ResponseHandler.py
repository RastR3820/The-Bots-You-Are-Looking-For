# ./Handlers/ReponseHandler.py
# This handler will be where the responses are created and sent back to the webpage

class ResponseHandler:
	currentResponse = ""
	
	def create(self, content, loginStatus):
		#This will be where responses are generated

		# TODO : have better handling and have support for database query results

		if content == "badinput":
			self.currentResponse = "Bad Input. Please input something different."
		elif content == "hello":
			self.currentResponse = "Hello! How can I help you today?"
		elif content == "done":
			self.currentResponse = "Have a wonderful day!"
			return "quit"
		elif content == "func":
			self.currentResponse = "I can help with that!"
		elif content == "login":
			self.currentResponse = "You have been logged in."
			return "login"
		elif content == "needlog":
			if loginStatus:
				self.currentResponse = "I can help with this user specific function!"
			else:
				self.currentResponse = "You must be logged in to get that information."
		else:
			self.currentResponse = "Sorry, I don't know how to help with that."

	def send(self):
		#This will be where the response is sent to the webpage
		
		# TODO : Similar to the receive in the input handler class, I don't know how to interface with the webpage
		# So for now I will be just 'sending' the message by printing it to console
		print(self.currentResponse)