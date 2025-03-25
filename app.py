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
            return render_template('login.html', msg='logged in successfully')
        else:
            msg = "Incorrect username or password"
    return render_template('login.html', msg=msg)


if __name__ == '__main__':
    app.run()
