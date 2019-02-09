from flask import Flask
from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
import os,json
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import sessionmaker
from models import *
import sqlalchemy as db 

engine = db.create_engine('mysql+pymysql://root@localhost/mydatabase?charset=utf8')
metadata = db.MetaData()

app = Flask(__name__)
 

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


## Data APIs
@app.route('/getSales')
def getsales():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        connection = engine.connect()
        sales = db.Table('sales', metadata, autoload=True, autoload_with=engine)
        query = db.select([sales])
        keys=sales.columns.keys()
        resultset = connection.execute(query).fetchall()
        items=[]
        for row in resultset:
                items.append({keys[0]: row[0],keys[1]: row[1],keys[2]: row[2],keys[3]: row[3], })
    
        connection.close()
        return json.dumps({'items':items})

@app.route('/getProduct')
def getproduct():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        connection = engine.connect()
        product = db.Table('product', metadata, autoload=True, autoload_with=engine)
        query = db.select([product])
        keys=product.columns.keys()
        resultset = connection.execute(query).fetchall()
        items=[]
        for row in resultset:
            items.append({
                keys[0]: row[0],
                keys[1]: row[1],
                keys[2]: row[2],
                keys[3]: row[3],
                keys[4]: row[4],
                keys[5]: row[5],
                keys[6]: row[6],
                keys[7]: row[7],
                keys[8]: row[8],
                keys[9]: row[9],
                keys[10]: row[10],
                keys[11]: row[11],
                keys[12]: row[12],
                keys[13]: row[13],
                keys[14]: row[14],
                keys[15]: row[15]
            })
        connection.close()
        return json.dumps({'items':items})

@app.route('/getLocation')
def getlocation():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        connection = engine.connect()
        location = db.Table('location', metadata, autoload=True, autoload_with=engine)
        query = db.select([location])
        keys=location.columns.keys()
        resultset = connection.execute(query).fetchall()
        items=[]
        for row in resultset:
            items.append({
                keys[0]: row[0],
                keys[1]: row[1],
                keys[2]: row[2],
                keys[3]: row[3],
                keys[4]: row[4],
                keys[5]: row[5],
                keys[6]: row[6],
                keys[7]: row[7]
            })
        connection.close()
        return json.dumps({'items':items})

@app.route('/getCalendar')
def getcalendar():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        connection = engine.connect()
        calendar = db.Table('calendar', metadata, autoload=True, autoload_with=engine)
        query = db.select([calendar])
        keys=calendar.columns.keys()
        resultset = connection.execute(query).fetchall()
        items=[]
        for row in resultset:
            items.append({
                keys[0]: row[0],
                keys[1]: row[1],
                keys[2]: row[2],
                keys[3]: row[3],
                keys[4]: row[4],
                keys[5]: row[5],
                keys[6]: row[6],
                keys[7]: row[7],
                keys[8]: row[8],
                keys[9]: row[9],
                keys[10]: row[10],
                keys[11]: row[11],
                keys[12]: row[12],
                keys[13]: row[13],
                keys[14]: row[14],
                keys[15]: row[15]
            })
        connection.close()
        return json.dumps({'items':items})

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host= 'localhost', port= 8080,debug=False)