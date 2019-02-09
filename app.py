from flask import Flask
from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
import os
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine(
    'mysql+pymysql://root@localhost/mydatabase?charset=utf8',
    connect_args = {
        'port': 3306
    },
    echo='debug',
    echo_pool=True
)
 
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        print ('login failed')
        return render_template('login.html')
    else:
        return render_template('welcome.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host= 'localhost', port= 8080,debug=False)