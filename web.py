from flask import *
from flask_mysqldb import MySQL
import MySQLdb
import re
web=Flask(__name__)
web.secret_key='system'
web.config['MySQL_HOST']='localhost'
web.config['MySQL_USER']='root'
web.config['MySQL_PASSWORD']='paryul'
web.config['MySQL_DB']='webdb'
mysql=MySQL(web)

@web.route('/')
def log_display():
    return render_template('login.html')
@web.route('/login', methods=['GET', 'POST'])
def login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute( 'SELECT * FROM accounts WHERE username= %s AND password= %s',(username,password, ))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['username']=account['username']
            msg='Logged in successfully !'
            return render_template('home.html',msg=msg)
        else:
            msg='Incorrect username/password !'
            return render_template('login.html',msg=msg)
@web.route('/register')
def reg_display():
    return render_template('register.html')
@web.route('/reg', methods=['GET', 'POST'])
def reg():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'state' in request.form and 'country' in request.form:
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        address=request.form['address']
        city=request.form['city']
        state=request.form['state']
        country=request.form['country']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username=%s',(username, ))
        account=cursor.fetchone()
        if account:
            msg='Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg='Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='Name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO accounts (username,password,email,address,city,state,country) VALUES(%s,%s,%s,%s,%s,%s,%s)',(username,password,email,address,city,state,country))
            mysql.connection.commit()
            # session['loggedin'] = True
            # session['id'] = cursor.lastrowid
            # session['username'] = username
            cursor.close()
            msg='You have successfully registered !'
            return render_template('home.html',msg=msg)
    elif request.method=='POST':
        msg='Please fill out the form !'
        return render_template('register.html',msg=msg)
@web.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))
@web.route('/upload')
def up_display():
    return render_template('upload.html')
@web.route('/up', methods=['GET', 'POST'])
def fetch_up():
    msg=''
    if request.method=='POST' and 'title' in request.form and 'blog' in request.form:
        title=request.form['title']
        blog=request.form['blog']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM web_blog WHERE title=%s',(title, ))
        account=cursor.fetchone()
        if account:
            msg='Title already exists !'
        else:
            cursor.execute('INSERT INTO web_blog (title, blog) VALUES(%s,%s)',(title,blog, ))
            mysql.connection.commit()
            msg='Your blog has been successfully uploaded !'
            return render_template('home.html',msg=msg)
    elif request.method=='POST':
        msg='Please fill all detailes !'
        return render_template('upload.html',msg=msg)
@web.route('/display')
def display():
    if 'loggedin' in session:
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id=%s',(session['id'], ))
        account=cursor.fetchone()
        return render_template('display.html',account=account)
    return redirect(url_for('login'))
@web.route('/update',methods=['GET','POST'])
def update():
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'state' in request.form and 'country' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username=%s',(username, ))
            account=cursor.fetchone()
            if account:
                msg='Account already exists !'
            elif not re.match(r'[^@]+@[^@]+',email):
                msg='Invalid Email address !'
            elif not re.match(r'[A-Za-z0-9]+',username):
                msg='name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE accounts SET username=%s,\
                password=%s, email=%s, \
                address=%s, city=%s, state=%s, \
                country=%s WHERE id=%s', (
                  username, password, email, 
                 address, city, state, country, 
                 session['id'], ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
                return render_template('home.html',msg=msg)
    elif request.method=='POST':
        msg='Please fill out the form !'
        return render_template('update.html',msg=msg)
    return redirect(url_for('login'))
if __name__=='__main__':
    web.run(host='localhost',port=int('5000'),debug=True)