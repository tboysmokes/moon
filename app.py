from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import UserMixin
import sqlite3



connection = sqlite3.connect("user_data.db", check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'child bank app'

command = '''CREATE TABLE IF NOT EXISTS users
    (ID            INTEGER    PRIMARY KEY AUTOINCREMENT,   
    firstname       TEXT       NOT NULL, 
    lastname        TEXT       NOT NULL, 
    email           TEXT       NOT NULL UNIQUE, 
    phonenumber     CHAR(12)   NOT NULL,
    password        TEXT       NOT NULL)'''
 
 

command2 = '''CREATE TABLE IF NOT EXISTS child
      (userID       INTEGER    PRIMARY KEY,
      bankname      TEXT        NOT NULL,
      account_num  CHAR(2)      NOT NULL,
      card number  CHAR(18)     NOT NULL,
      date         CHAR(5)      NOT NULL,
      cvv          CHAR(3)      NOT NULL,
      FOREIGN KEY(userID) REFERENCES users(ID))'''

cursor.execute(command)
cursor.execute(command2)





@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        accname = request.form['name']
        childage = request.form['age']
        cardnum = request.form['cardno']
        date = request.form['data']
        cvv = request.form['cvv']
        userid= request.form['userid']

        cursor.execute("INSERT INTO child VALUES(?,?,?,?,?,?)", ( userid, accname, childage, cardnum, date, cvv))
        print("successful")

    return render_template('create.html')

    



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global useremail
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
                return redirect("/home", code=302)


    return render_template('index.html')    



@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        PhoneNumber = request.form['phoneno']
        Password = request.form['password']
        userid = request.form['userid']
        print(firstname, Password)

        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?,?)", ( userid, firstname, lastname, email, PhoneNumber, Password))
        connection.commit()

        print("successful")
        return login()

    return render_template('register.html')



@app.route('/home', methods=['GET', 'POST'])
def home():
    connection.row_factory = sqlite3.Row
    cursor.execute("SELECT * FROM users where email = '"+useremail+"' ")
    rows = cursor.fetchall()
    print(useremail)

    records = []
    for row in rows:
        userid, fname, lname, email, phoneno, passw = row
        records.append({
            'userID': userid,
            'fristname': fname,
            'lastname': lname,
            'email': email,
            'phonenumber': phoneno,
            'password': passw
        })

        if request.method == 'POST':
            ediname = request.form['']
            edilname = request.form['']
            ediemail = request.form['']
            ediphone = request.form['']
            edipassword = request.form['']


    return render_template('home.html', fname = fname, lname = lname, email = email, phoneno = phoneno, passw = passw, userid = userid)

 

if __name__  == '__main__':
    app.run(debug=True) 