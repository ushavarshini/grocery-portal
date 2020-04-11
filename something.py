from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

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

