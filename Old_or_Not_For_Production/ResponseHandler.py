# ./Handlers/ReponseHandler.py
# This handler will be where the responses are created and sent back to the webpage

from Handlers.WebHandler import WebHandler

class ResponseHandler:
	currentResponse = ""
	web = WebHandler()
	
	def create(self, content):
		#This will be where responses are generated

		# TODO : have better handling and have support for database query results

		# TEMP very basically response handling while backend isn't here
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
			self.currentResponse = "You must be logged in to get that information."
		elif content == "none":
			self.currentResponse = "Sorry, I don't know how to help with that."
		else:
			self.currentResponse = content

	def send(self):
		#This will be where the response is sent to the webpage
		
		# TODO : Similar to the receive in the input handler class, I don't know how to interface with the webpage

		# TEMP for now I will be just 'sending' the message by printing it to console
		print(self.currentResponse)