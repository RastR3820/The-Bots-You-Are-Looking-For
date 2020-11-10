from flask import Flask, redirect, request, url_for, render_template

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def home():
    if request.method == 'POST':
        credentials = request.form
        username = credentials["username"]
        password = credentials["password"]
        return username
    
    return render_template("index.html", content="Testing")

@app.route("/advising-chatbot")
def chatbot():
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run()
