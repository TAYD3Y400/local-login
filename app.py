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
    msg
@app.route('/')
def hello_world():  # put application's code here
    return app.secret_key


if __name__ == '__main__':
    app.run()
