from flask import Flask, render_template, request, redirect, session , flash , url_for , jsonify
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
    
    if request.method == 'POST'and 'ID' in request.form and 'password' in request.form :    
          # Fetch form data
        userDetails = request.form
        ID = userDetails['ID']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from users where ID= %s and password= %s",(ID, password))
        userDetails = cur.fetchone()
        if userDetails:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['ID'] = userDetails[0]
            #session['username'] = account['username']
            # Redirect to home page
            return redirect('/customer')
            flash('Logged in successfully!')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!')
            #return msg 
    return render_template('login.html')

@app.route('/customer', methods=['GET', 'POST'])
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Grocery_Store_UG")
    if resultValue > 0:
        userDetails = cur.fetchall()
        #return render_template('users.html',userDetails=userDetails)
    if(request.method == 'POST'):
        userDetails = request.form
        Cust_ID = userDetails['Cust_ID']
        BarCode_ID = userDetails['BarCode_ID']
        Cust_ID = request.form.get('Cust_ID')
        cur.execute("INSERT INTO Buys_from(Cust_ID,BarCode_ID) VALUES(%s, %s)",(Cust_ID, BarCode_ID))
        mysql.connection.commit()
        return redirect(url_for('cust',  Cust_ID=Cust_ID))
    return render_template('users.html', userDetails=userDetails)	


@app.route('/customer2', methods=['GET', 'POST'])
def cust():
    cur = mysql.connection.cursor()
    #for userDetails in session :
    Cust_ID = request.args.get('Cust_ID', None)
    resultValue = cur.execute("SELECT Industry_name, Product , Product_Price from Cart WHERE Cust_ID = %s", [Cust_ID])
    bgpost= cur.fetchall()
    cur.execute(" SELECT Sum(Product_Price) from Cart where Cust_ID= %s", [Cust_ID])
    value=cur.fetchall()
    if(request.method == 'POST'):
        userDetails = request.form
        tmode = userDetails['tmode']
        Capacity= userDetails['Capacity']
        cur.execute("INSERT INTO Transportation(tmode,Capacity_lbs,Cust_ID) VALUES(%s,%s,%s)",(tmode,Capacity,Cust_ID))
        mysql.connection.commit()
    mysql.connection.commit()
       # return redirect('/customer2')
    return render_template('users2.html', bgpost=bgpost , value=value)		


if __name__ == '__main__':
    app.run(debug=True)


  