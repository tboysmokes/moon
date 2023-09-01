from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from os import path


DB_NAME = 'database.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'child bank app'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)
#db.init_app(app)
'''
class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    childname = db.Column(db.String(150))
    childaccount = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.Foreignkey('User.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phonenumber = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    child = db.relationship('Child')


def create_database():
    if not path.exist('BANK_PROJECT/'+ DB_NAME):
        db.create_all(app=app)
        print('Created database successful!')
    '''

@app.route('/', methods=['GET', 'POST'])
def first_page():
    data = request.form
    print(data)
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print (data)
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        PhoneNumber = request.form.get('phoneno')
        Password = request.form.get('password')
        Password2 = request.form.get('password2')

        if len(email) < 7:
            flash('Email be greater that seven charaters ', category='error')
        elif len(firstname) > 20:
            flash('firstname must be less than twenty charaters ', category='error')
        elif len(lastname) > 50:
            flash('lastname must be less than twenty charaters ', category='error')
        elif len(Password) > 30:
            flash('password must be less than thirty ', category='error')
        elif len(PhoneNumber) > 10 or len(PhoneNumber) < 10:
            flash('Phone number must equal ten ', category='error')
        elif Password != Password2:
            flash('Your password does not match', category='error')
        else:
            '''    # add user to database
new_user = User(firstname = firstname, lastname = lastname, email = email, PhoneNumber = PhoneNumber, Password = Password)
            db.session.add(new_user)
            db.session.commit()
            flash('account created successfully', category='successful')'''
            return home()

    return render_template('register.html')
 

if __name__  == '__main__':
    app.run(debug=True)