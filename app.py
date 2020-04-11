from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import yaml
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = "varshini"

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
# app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/home', methods=['GET','POST'])
def index():
    if(request.method == 'POST'):
        # Fetch form data
        userDetails = request.form
        ID = userDetails['ID']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(ID,password) VALUES(%s, %s)",(ID, password))
        mysql.connection.commit()
        return redirect('/customer')
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg= 'test'
    if request.method == 'POST'and 'ID' in request.form and 'password' in request.form :    
          # Fetch form data
        userDetails = request.form
        ID = userDetails['ID']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from users where ID= %s and password= %s;)",(ID, password))
        userDetails = cur.fetchone()
        if userDetails:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['ID'] = userDetails[0]
            #session['username'] = account['username']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect('/customer')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            return msg 
    return render_template('login.html', msg=msg)

@app.route('/customer')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Grocery_Store_UG")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)