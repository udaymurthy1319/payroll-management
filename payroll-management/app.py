

from flask import Flask, render_template,session,  request, redirect, url_for
from werkzeug import secure_filename
import sqlite3
import os
app = Flask(__name__)
app.secret_key = "asdfghjkl"
# app.debug = True

#initializing the model
# MODEL_PATH = "data/model.pkl"
# model = pickle.load(open('E:/Uday/data/model.pkl','rb'))



#Define home route
@app.route("/")
def index():
    # return render_template("index.html")
    return redirect(url_for('login',msg=''))

@app.route("/index")
def new():
    # return render_template("index.html")
    return redirect(url_for('login',msg=''))    


@app.route("/login")
def login():
    if('msg' in request.args):
        messages = request.args['msg'] 
        return render_template("login.html",msg=messages)
    else:
        return render_template("login.html")

@app.route("/admin-login")
def adminlogin():
    if('msg' in request.args):
        messages = request.args['msg'] 
        return render_template("admin-login.html",msg=messages)
    else:
        return render_template("admin-login.html")
     

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * from workinghours where  email  = ?",(session['username'],))
            records = cur.fetchall()
        
        return render_template("dashboard.html",data=records)
    else:
        msg = "Please Login"
        return redirect(url_for('login',msg=msg))
    
    
@app.route("/admin-dashboard")
def admindashboard():
    if 'username' in session:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("select email,fullname,mobile  from users ")
            records = cur.fetchall()
        
        return render_template("admin-dashboard.html",data=records)
    else:
        msg = "Please Login"
        return redirect(url_for('adminlogin',msg=msg))


@app.route("/insertUser",methods=['POST'])
def insertUser():
    fullname = request.form['name']
    email = request.form['email']
    username = request.form['uname']
    password = request.form['password']
    mobile = request.form['mobile']
    isAdmin = request.form['isAdmin']
    print(fullname,email,username,password,mobile)
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * from users where username = ? and email  = ?",(username,email))
        records = cur.fetchall()
        if(len(records) > 0):
           
            return redirect(url_for('admindashboard'))
        else:
            cur.execute("INSERT INTO users (fullname, email, username, password,mobile,isAdmin) VALUES (?,?,?,?,?,?)",(fullname,email,username,password,mobile,isAdmin) )
            con.commit()
    
    return redirect(url_for('admindashboard'))

@app.route("/loginuser",methods=['POST'])
def loginuser():
    email = request.form['email']
    password = request.form['password']
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * from users where password = ? and email  = ?",(password,email))
        records = cur.fetchall()
        if(len(records) > 0):
            print(records)
            session['username'] = request.form['email']
            session['mobile'] = records[0][4]
            return redirect(url_for('dashboard'))
        else:
            msg = "Username or Password is incorrect"
            return redirect(url_for('login',msg=msg))

@app.route("/adminloginuser",methods=['POST'])
def adminloginuser():
    email = request.form['email']
    password = request.form['password']
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * from users where password = ? and email  = ? and isAdmin='1'",(password,email))
        records = cur.fetchall()
        if(len(records) > 0):
            print(records)
            session['username'] = request.form['email']
            session['mobile'] = records[0][4]
            return redirect(url_for('admindashboard'))
        else:
            msg = "Username or Password is incorrect"
            return redirect(url_for('adminlogin',msg=msg))
        
        
@app.route("/hourssubmit",methods=['POST'])
def hourssubmit():
    date = request.form['date']
    hours = request.form['hours']
    print(hours)
    print(date)
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO workinghours ( email,date,hours) VALUES (?,?,?)",(session['username'],date,hours) )
        con.commit()
        return redirect(url_for('dashboard'))

@app.route("/getHours",methods=['POST'])
def getHours():
    email = request.get_json()
    print(email)
    
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * from workinghours where  email  = ? order by date desc ",(email['email'],))
        records = cur.fetchall()
        
        return {"data":records}




if __name__ == "__main__":
    app.run(debug=True)
