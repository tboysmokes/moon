from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import UserMixin
import sqlite3

connection = sqlite3.connect("user_data.db", check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'child bank app'


command = '''CREATE TABLE IF NOT EXISTS users
    (ID            INTEGER     PRIMARY KEY,   
    firstname       TEXT       NOT NULL, 
    lastname        TEXT       NOT NULL, 
    email           TEXT       NOT NULL, 
    phonenumber     CHAR(12)   NOT NULL,
    password        TEXT       NOT NULL);'''

run = '''CREATE TABLE IF NOT EXISTS child
      (ID         INTEGER      PRIMARY KEY
      NAME         TEXT         NOT NULL,
      AGE          CHAR(2)      NOT NULL,
      CARD NUMBER  CHAR(18)     NOT NULL,
      DATA         CHAR(4)      NOT NULL,
      CVV          CHAR(3)      NOT NULL,
      FOREIGN KEY(users_ID) REFERENCES users(ID)
      );'''

cursor.execute(command)



@app.route('/', methods=['GET', 'POST'])
def first_page():
    if request.method == 'POST':
        childname = request.form['name']
        childage = request.form['age']
        cardnum = request.form['cardno']
        date = request.form['data']
        cvv = request.form['cvv']

        print(childname, cvv)
        cursor.execute("INSERT INTO child VALUES(?,?,?,?,?)", (childname, childage, cardnum, date, cvv))

    return render_template('create.html')

    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/sidenav')
def sidena():
    return render_template('sidenav.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        useremail = request.form['email']
        userpassword = request.form['password']

        print(useremail, userpassword)

        if len(useremail) < 7:
            flash('Email must be greater that seven charaters ', category='error')
        elif len(userpassword) > 20:
            flash('password can not be more that 20 chr', category='error')
        else:
            query = "SELECT email, password FROM users where email = '"+useremail+"' and password = '"+userpassword+"' "
            # what to do with the data
            cursor.execute(query)

            result = cursor.fetchall()

            if len(result) == 0:
                print("incorrect email or password")
            else:
                return render_template('home.html')


    return render_template('index.html')    



@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        PhoneNumber = request.form['phoneno']
        Password = request.form['password']
        print(firstname, Password)

        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?)", (firstname, lastname, email, PhoneNumber, Password))
        connection.commit()
        print("successful")
        return render_template('create.html')

    return render_template('register.html')

@app.route('/logout')
def logout():
    return render_template('index.html')
 

if __name__  == '__main__':
    app.run(debug=True)