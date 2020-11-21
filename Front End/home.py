from flask import Flask, redirect, request, url_for, render_template
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

#Configure DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route("/", methods=['POST','GET'])
def home():
    if request.method == 'POST':
        user = request.form
        global StudentID
        StudentID = user['StudentID']
        InputPassword = user['Password']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("""SELECT Password FROM logininfo WHERE studentid = %s""", [StudentID])
        if resultValue > 0:
            password = cur.fetchall()
            if InputPassword == password[0][0]:
                return redirect('/advising-chatbot')
            else:
                return 'Login Failed'
        else:
            return 'Login Failed'
     
    return render_template("index.html")

@app.route("/advising-chatbot", methods=['POST','GET'])
def chatbot():
    if request.method == 'POST':
        userform = request.form
        userinput = userform['user_input']
        print(userinput)
        return 'Done!'
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run()
