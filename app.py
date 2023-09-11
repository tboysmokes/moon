from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
from flask_login import UserMixin
import sqlite3



connection = sqlite3.connect("user_data.db", check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'microbankapp'

command = '''CREATE TABLE IF NOT EXISTS users
    (ID            INTEGER    PRIMARY KEY AUTOINCREMENT,   
    firstname       TEXT       NOT NULL, 
    lastname        TEXT       NOT NULL, 
    email           TEXT       NOT NULL UNIQUE, 
    phonenumber     CHAR(12)   NOT NULL,
    password        TEXT       NOT NULL)'''
 
 

command2 = '''CREATE TABLE IF NOT EXISTS account
      (userID       INTEGER    PRIMARY KEY AUTOINCREMENT,
      bankname      TEXT        NOT NULL,
      account_name  TEXT        NOT NULL,
      account_num   CHAR(10)    NOT NULL UNIQUE,
      account_pin   CHAR(6)     NOT NULL,
      FOREIGN KEY(userID) REFERENCES users(ID))'''


command3 = '''CREATE TABLE IF NOT EXISTS secaccount
      (userID       INTEGER    PRIMARY KEY AUTOINCREMENT,
      bankname      TEXT        NOT NULL,
      account_name  TEXT        NOT NULL,
      account_num   CHAR(10)    NOT NULL UNIQUE,
      account_pin   CHAR(6)     NOT NULL,
      FOREIGN KEY(userID) REFERENCES account(ID))'''


command4 = '''CREATE TABLE IF NOT EXISTS thirdaccount
      (userID       INTEGER    PRIMARY KEY AUTOINCREMENT,
      bankname      TEXT        NOT NULL,
      account_name  TEXT        NOT NULL,
      account_num   CHAR(10)    NOT NULL UNIQUE,
      account_pin   CHAR(6)     NOT NULL,
      FOREIGN KEY(userID) REFERENCES secaccount(userID))'''

cursor.execute(command)
cursor.execute(command2)
cursor.execute(command3)
cursor.execute(command4)





@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        userid = request.form['userid']
        bank_name = request.form['bankna']
        accname = request.form['accname']
        accnum = request.form['accnum']
        accpin = request.form['accpin']
        print(accname, accnum)   
    

    # this is the algorithm that check each database just too confirm that the same account wasn't entered two
        query = "SELECT * FROM account WHERE userID = '"+userid+"'"
        cursor.execute(query)

        check = cursor.fetchall()

        if len(check) == 0:
            cursor.execute("INSERT INTO account VALUES (?,?,?,?,?)", ( userid, bank_name, accname, accnum, accpin))
        else:
            query2 = "SELECT * FROM secaccount WHERE userID = '"+userid+"'"
            cursor.execute(query2)

            check2 = cursor.fetchall()
            if len(check2) == 0:
                cursor.execute("INSERT INTO secaccount VALUES (?,?,?,?,?)", ( userid, bank_name, accname, accnum, accpin))
            else:
                query3 = "SELECT * FROM thirdaccount WHERE userID = '"+userid+"'"
                cursor.execute(query3)
                check3 = cursor.fetchall()
                if len(check3) == 0:
                    cursor.execute("INSERT INTO thirdaccount VALUES (?,?,?,?,?)", ( userid, bank_name, accname, accnum, accpin))
                else:
                    flash("")

        connection.commit()
        print("successful")
        return redirect("/home", code=302)

    return render_template('create.html')



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global useremail
        global user_ID
        useremail = request.form['email']
        userpassword = request.form['password']

        print(useremail, userpassword)

        if len(useremail) < 7:
            flash('Email must be greater that seven charaters ', category='error')
        elif len(userpassword) > 20:
            flash('password can not be more that 20 chr', category='error')
        else:
            query = "SELECT * FROM users where email = '"+useremail+"' and password = '"+userpassword+"' "
            # what to do with the data
            cursor.execute(query)

            result = cursor.fetchall()
            
            inner = []
            for row in result:
                user_ID, fname, lname, email, phoneno, passw = row
                inner.append({
                    'userID': user_ID,
                    'fristname': fname,
                    'lastname': lname,
                    'email': email,
                    'phonenumber': phoneno,
                    'password': passw
        })                 

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


def getdata():
    cursor.execute('''  
            SELECT account.account_num, account.account_name, users.firstname
            FROM account
            INNER JOIN users ON account.userID = users.ID''')
    datas = cursor.fetchall()

    details = []
    for data in datas:
        accnum, name, username = data
        details.append({
            'account_num': accnum,
            'account_name': name,
            'firstname': username
        })
        print(details)
    return details
    
    





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
        user_data = getdata()

        ''' 
        if request.method == 'POST':
            ediname = request.form['ediname']
            edilname = request.form['edilname']
            ediemail = request.form['ediemail']
            ediphone = request.form['ediphone']
            edipassword = request.form['edipass']
      '''


    return render_template('home.html', fname = fname, lname = lname, email = email, phoneno = phoneno, passw = passw, userid = userid, user_data=user_data)

 

if __name__  == '__main__':
    app.run(debug=True) 