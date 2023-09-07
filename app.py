from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import UserMixin
import sqlite3




connection = sqlite3.connect("user_data.db", check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'child bank app'

command = '''CREATE TABLE IF NOT EXISTS users
    (ID            INTEGER     PRIMARY KEY AUTOINCREMENT,   
    firstname       TEXT       NOT NULL, 
    lastname        TEXT       NOT NULL, 
    email           TEXT       NOT NULL, 
    phonenumber     CHAR(12)   NOT NULL,
    password        TEXT       NOT NULL);'''
 
 

command2 = '''CREATE TABLE IF NOT EXISTS child
      (userID       INTEGER    PRIMARY KEY,
      names         TEXT        NOT NULL,
      age          CHAR(2)      NOT NULL,
      card number  CHAR(18)     NOT NULL,
      date         CHAR(5)      NOT NULL,
      cvv          CHAR(3)      NOT NULL,
      FOREIGN KEY(userID) REFERENCES users(ID));'''

cursor.execute(command)
cursor.execute(command2)





@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        childname = request.form['name']
        childage = request.form['age']
        cardnum = request.form['cardno']
        date = request.form['data']
        cvv = request.form['cvv']

        cursor.execute("INSERT INTO child VALUES(?,?,?,?,?)", (childname, childage, cardnum, date, cvv))
        print("successful")

    return render_template('create.html')

    


@app.route('/home')
def home():
    connection.row_factory = sqlite3.Row
    password = "Omotomiwa321#"
    cursor.execute("SELECT * FROM users where password = '"+password+"' ")
    rows = cursor.fetchall()

    records = []
    for row in rows:
        fname, lname, email, phoneno, passw = row
        records.append({
            'fristname': fname,
            'lastname': lname,
            'email': email,
            'phonenumber': phoneno,
            'password': passw
        })
    return render_template('home.html', fname = fname, lname = lname, email = email, phoneno = phoneno, passw = passw)

@app.route('/', methods=['GET', 'POST'])
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

 

if __name__  == '__main__':
    app.run(debug=True)