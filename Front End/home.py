#pip install flask
#pip install flask_mysqldb
#pip install pyyaml
from flask import Flask, redirect, request, url_for, render_template, session, flash, g
from flask_mysqldb import MySQL
from IntentHandler import IntentHandler
from IntentHandler import modelStart
import yaml

messages = []

app = Flask(__name__)
app.secret_key = "GBw-8lWlxoAFJkhWWxs_2w"

#Configure DB
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
    
@app.before_request
def before():
    g.chatlogs = []
    for message in messages:
        g.chatlogs.append(message)
  
@app.route("/", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session.pop('StudentID', None)
        session.pop('FName', None)
        session.pop('LName', None)
        if request.form['StudentID']:
            StudentID = request.form['StudentID']
            InputPassword = request.form['Password']
            cur = mysql.connection.cursor()
            resultValue = cur.execute("""SELECT Password FROM logininfo WHERE studentid = %s""", [StudentID])
            if resultValue > 0:
                password = cur.fetchall()
                if InputPassword == password[0][0]:
                    cur = mysql.connection.cursor()
                    resultValue = cur.execute('''SELECT FName, LName FROM Student WHERE studentid = %s''', [StudentID])
                    if resultValue > 0:
                        name = cur.fetchall()
                        user = name[0]
                        FName = user[0]
                        LName = user[1]
                        session['StudentID'] = StudentID
                        session['FName'] = FName
                        session['LName'] = LName
                        return redirect(url_for('chatbot'))
                else:
                    flash('Login Failed! Please try again')
                    return redirect(url_for('login'))
            else:
                flash('Login Failed! Please try again')
                return redirect(url_for('login'))
        else:
            StudentID = 0
            cur = mysql.connection.cursor()
            resultValue = cur.execute('''SELECT FName, LName FROM Student WHERE studentid = %s''', [StudentID])
            name = cur.fetchall()
            user = name[0]
            FName = user[0]
            LName = user[1]
            session['StudentID'] = StudentID
            session['FName'] = FName
            session['LName'] = LName
            return redirect(url_for('chatbot'))
        
    return render_template("index.html")

@app.route("/advising-chatbot", methods=['POST','GET'])
def chatbot():
    if request.method == 'POST':
        userform = request.form
        userinput = userform['user_input']
        print('Input from webpage: ',userinput)
        messages.append(userinput)
        # ryan - this is where the intent handler will read the input
        intenter = IntentHandler()
        response = intenter.GetIntent(userinput,session['StudentID'])
        print("Intent from chatbot: ", response)
        messages.append(response)
        
        return redirect(url_for('direct'))
    
    return render_template("chatbot.html")

@app.route("/redirect")
def direct():
    return redirect(url_for('chatbot'))

if __name__ == "__main__":
    app.run()


