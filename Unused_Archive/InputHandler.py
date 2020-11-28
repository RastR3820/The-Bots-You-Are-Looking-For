# ./Handlers/InputHandler.py
# This handler will get the input from the webpage and process it

from Handlers.IntentHandler import IntentHandler
from Handlers.WebHandler import WebHandler

class InputHandler:
	userInput = ""
	userLogin = False
	okayChars = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','/','#','$','%','&','@']
	proc = IntentHandler()
	web = WebHandler()
	
	def verifyLogin(self):
		# This will get the user's current login status from the web page

		# TODO : Figure out how the login status will be receieved from the web page
		return self.userLogin

	def setLogin(self):
		# TEMP function to set login status
		self.userLogin = True

	def receive(self):
		# This will be where the chatbot will recieve input from the webpage

		# TODO : Figure out how input is going to be receieved from the webpage
		# I don't know what language the webpage is built on nor do I know how to hook this program into an existing webpage

		# TEMP I will just have it read input from a prompt
		inputFromWeb = input("Functions: appointment, credits, degree, gpa, major, map, login, greet, goodbye\n")
		self.userInput = inputFromWeb

	def cleanInput(self):
		# This will clean the input so the intent handler can better understand the input

		# Sets the input string to lowercase for easier processing
		self.userInput = self.userInput.lower()

		# Removes punctuation
		self.userInput = self.userInput.replace(',','')
		self.userInput = self.userInput.replace('.','')
		self.userInput = self.userInput.replace('!','')
		self.userInput = self.userInput.replace('?','')
		
	def check(self):
		# This will be where the input is checked for bad input, ie. bad characters or other languages
		
		# Cleans the input before checking for bad input
		self.cleanInput()

		# Iterates through each character in the input and checks if they are valid characters
		for char in self.userInput:
			if char not in self.okayChars:
				return False
		return True

	def process(self):
		# This will return whether the input is bad or what the intent was on good input
		if not self.check():
			return "badinput"
		else:
			return self.proc.doThing(self.userInput)