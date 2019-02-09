from flask import Flask
from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
import os,json
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import sessionmaker
from models import *
import sqlalchemy as db 

""" engine = create_engine(
    'mysql+pymysql://root@localhost/mydatabase?charset=utf8',
    connect_args = {
        'port': 3306
    },
    echo='debug',
    echo_pool=True
) """

engine = db.create_engine('mysql+pymysql://root@localhost/mydatabase?charset=utf8')
connection = engine.connect()
metadata = db.MetaData()

app = Flask(__name__)
 

@app.route('/getSales')
def getsales():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        sales = db.Table('sales', metadata, autoload=True, autoload_with=engine)
        query = db.select([sales])
        keys=sales.columns.keys()
        resultset = connection.execute(query).fetchall()
        items=[]
        for row in resultset:
                items.append({keys[0]: row[0],keys[1]: row[1],keys[2]: row[2],keys[3]: row[3], })
    
        connection.close()
        return json.dumps({'items':items})
@app.route('/')
def home():
    if not session.get('logged_in'):
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