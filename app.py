from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import secrets
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
print("Your secret key is: ", app.secret_key)


load_dotenv()
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts "
                       "WHERE username = %s "
                       "AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            session['logged_in'] = True
            session['id'] = result['id']
            session['username'] = result['username']
            return render_template('index.html', msg='logged in successfully')
        else:
            msg = "Incorrect username or password"
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['id'] = None
    session['username'] = None
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        confirmed_password = request.form['confirmed_password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username))
        result = cursor.fetchone()
        if result:
            msg = "Username already exists"
        elif not re.match(r"^[a-zA-Z0-9_-]+$", username):
            msg = "Username must contain only letters, numbers and underscores"
        elif not re.match(r"^[a-zA-Z0-9_-]+$", email):
            msg = "Invalid email address"
        elif password != confirmed_password:
            msg = "Passwords do not match"
        elif not email or not email or not password:
            msg = 'Please fill out the form!'
        else:
            cursor.execute("INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('login.html', msg=msg)
    return render_template('register.html', msg=msg)

if __name__ == '__main__':
    app.run()
