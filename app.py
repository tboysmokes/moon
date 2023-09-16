from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
from flask_login import UserMixin
import sqlite3



connection = sqlite3.connect("user_data.db", check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'microbankapp'

query0 = '''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY,
    firstname  TEXT   NOT NULL,
    lastname   TEXT   NOT NULL,
    email      TEXt   NOT NULL  UNIQUE,
    password   TEXT   NOT NULL
)
'''

# Create Savings_Account table with a foreign key to Users
query1 = '''
CREATE TABLE IF NOT EXISTS Account (
    account_id     INTEGER PRIMARY KEY,
    user_id        INTEGER,
    bankName       TEXT    NOT NULL,
    account_name   TEXT    NOT NULL,
    account_number TEXT    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
'''

# Create Checking_Account table with a foreign key to Users
query2 = '''
CREATE TABLE IF NOT EXISTS secAccount (
    account_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    secbankName       TEXT    NOT NULL,
    secaccount_name   TEXT    NOT NULL,
    secaccount_number TEXT    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
'''

# Create Credit_Account table with a foreign key to Users
query3 = '''
CREATE TABLE IF NOT EXISTS thirdAccount (
    account_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    thirdbankName       TEXT    NOT NULL,
    thirdaccount_name   TEXT    NOT NULL,
    thirdaccount_number TEXT    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
'''

name = "transactionHistory"

cursor.execute(f'DROP TABLE IF EXISTS {name}')

query4 = '''
CREATE TABLE IF NOT EXISTS transactionHistory(
    user_id INTEGER,
    description       TEXT    NOT NULL,
    amount            TEXT    NOT NULL,
    data              TEXT    NOT NULL,
    account           TEXT    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
'''

# Commit and close the connection
cursor.execute(query0)
cursor.execute(query1)
cursor.execute(query2)
cursor.execute(query3)
cursor.execute(query4)




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
                user_ID, fname, lname, email, passw = row
                inner.append({
                    'userID': user_ID,
                    'fristname': fname,
                    'lastname': lname,
                    'email': email,
                    'password': passw
               })                 

            if len(result) == 0:
                print("incorrect email or password")
            else:
                return redirect("/home", code=302)


    return render_template('index.html')    


@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    global count
    if request.method == 'POST':
        bank_name = request.form['bankna']
        accname = request.form['accname']
        accnum = request.form['accnum']
        print(accname, accnum)   
        print(user_ID)

        identifier = str(user_ID)

    # this is the algorithm that check each database just too confirm that the same account wasn't entered two
        query = "SELECT * FROM Account WHERE account_id = ?"
        cursor.execute(query, identifier)

        check = cursor.fetchall()

        if len(check) == 0:
            count = 1
            cursor.execute("INSERT INTO Account VALUES (?,?,?,?,?)", ( identifier, identifier, bank_name, accname, accnum))
        else:
            query2 = "SELECT * FROM secAccount WHERE account_id = ?"
            cursor.execute(query2, identifier)

            check2 = cursor.fetchall()
            if len(check2) == 0:
                count = 2
                cursor.execute("INSERT INTO secAccount VALUES (?,?,?,?,?)", ( identifier, identifier, bank_name, accname, accnum))
            else:
                query3 = "SELECT * FROM thirdAccount WHERE account_id = ?"
                cursor.execute(query3, identifier)

                check3 = cursor.fetchall()
                if len(check3) == 0:
                    count = 3
                    cursor.execute("INSERT INTO thirdAccount VALUES (?,?,?,?,?)", ( identifier, identifier, bank_name, accname, accnum))
                else:
                    flash("u are watching 3 account already")

        connection.commit()
        print("successful")
        return redirect("/home", code=302)

    return render_template('create.html')


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        Password = request.form['password']
        userid = request.form['userid']
        print(firstname, Password)

        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?)", ( userid, firstname, lastname, email, Password))
        connection.commit()

        print("successful")
        return login()

    return render_template('register.html')


def getdata():
    cursor.execute('''  
            SELECT firstname, account_name, account_number, secaccount_name, secaccount_number, thirdaccount_name, thirdaccount_number 
            FROM Users 
            LEFT JOIN Account ON  Users.user_id = Account.user_id
            LEFT JOIN secAccount ON  Users.user_id = secAccount.user_id
            LEFT JOIN thirdAccount ON  Users.user_id = thirdAccount.user_id
            WHERE Users.user_id  = ?
            ''', [user_ID])
    datas = cursor.fetchall()
    details = []
    for data in datas:
        username, accountName, accountNumber, secAccountName, secAccountNumber, thirdAccountName, thirdAccountNumber = data
        details.append({
            'firstname': username,
            'account_name': accountName,
            'account_num': accountNumber,
            'secaccount_name': secAccountName,
            'secaccount_number': secAccountNumber,
            'thirdaccount_name': thirdAccountName,
            'thirdaccount_number': thirdAccountNumber
        })
        print(details)
        return details
    
    

@app.route('/home', methods=['GET', 'POST'])
def home():
    useriden = str(user_ID)
    connection.row_factory = sqlite3.Row
    cursor.execute("SELECT * FROM users where email = '"+useremail+"' ")
    rows = cursor.fetchall()
    print(useremail)

    records = []
    for row in rows:
        userid, fname, lname, email, passw = row
        records.append({
            'userID': userid,
            'fristname': fname,
            'lastname': lname,
            'email': email,
            'password': passw
        })

        user_data = getdata()

    
    if request.method == 'POST':
        ediname = request.form['ediname']
        edilname = request.form['edilname']
        ediemail = request.form['ediemail']
        edipassword = request.form['edipass']

        if ediname == "":
            print("no data here")
        else:
            cursor.execute("UPDATE Users set firstname = '"+ediname+"' WHERE user_id = ? ", (useriden))
        if edilname == "":
            print("no data here")
        else:
            cursor.execute("UPDATE Users set lastname = '"+edilname+"' WHERE user_id = ? ", (useriden))
        if ediemail == "":
            print("no data here")
        else:
            cursor.execute("UPDATE Users set email = '"+ediemail+"' WHERE user_id = ?", (useriden))
        if edipassword == "":
            print("no data here")
        else:
            cursor.execute("UPDATE Users set password = '"+edipassword+"' WHERE user_id = ?", (useriden))
    

    
      


    return render_template('home.html', fname = fname, lname = lname, email = email, passw = passw, userid = userid, user_data= user_data)

 

if __name__  == '__main__':
    app.run(debug=True) 