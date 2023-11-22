from flask import Flask, render_template, request, redirect,session,flash
from flask_mysqldb import MySQLdb,MySQL
import MySQLdb.cursors
from flask_session import Session
from flask_mail import Mail, Message


app= Flask(__name__)
app.secret_key = 'xyz123abc'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root123$'
app.config['MYSQL_DB']='edu.sex'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
mail = Mail(app)
mysql= MySQL(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'edu.sex2023@gmail.com'
app.config['MAIL_PASSWORD'] = 'dzgedimsimkeexzh'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/login',methods=['GET','POST'])
def login():
    message=''
    if request.method=="POST" and request.form['username'] and request.form['password']:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from signup where username='{}' AND password='{}'".format(username,password))
        user=cursor.fetchone()
        if user:
            session["username"] = request.form.get("username")
            flash('Logged in successfully')
            return redirect("/")
        else:
            message='Enter proper credentials'   
    return render_template('login.html',message=message)

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method=="POST" and request.form['username'] and request.form['email'] and request.form['password']:
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into signup(username,email,password) values('{}','{}',{})".format(username,email,password))
        user=cursor.fetchone()
        mysql.connection.commit()
        if user:
            return redirect('/login')
    return render_template('signup.html')

@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")

@app.route('/volunteer',methods=['POST','GET'])
def volunteer():
    if not session.get("username"):
        return redirect("/login")
    elif request.method=='POST' and request.form['name'] and request.form['email'] and request.form['phone'] and request.form['address']:
        name= request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        address=request.form['address']
        cursor= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into volunteer(name,email,phone,address) values('{}','{}',{},'{}')".format(name,email,phone,address))
        mysql.connection.commit()
        msg = Message(
                'Volunteer for Edu.Sex',
                sender ='edu.sex2023@gmail.com',
                recipients = [request.form['email']]
               )
        msg.body = 'Thank you for volunteering. Our team will get back to you shortly.'
        mail.send(msg)
        user=cursor.fetchone() 
        if user:
            return redirect('/')
    return render_template('volunteer.html')

@app.route('/contact', methods=['POST','GET'])
def contact():
    if not session.get("username"):
        return redirect("/login")
    elif request.method=="POST" and request.form['name'] and request.form['email'] and request.form['message']:
        name= request.form['name']
        email=request.form['email']
        message=request.form['message']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into contact(name,email,message) values('{}','{}','{}')".format(name,email,message))
        mysql.connection.commit()
        msg = Message(
                'Thankyou for showing interest',
                sender ='edu.sex2023@gmail.com',
                recipients = [request.form['email']]
               )
        msg.body = 'We will get back to you shortly.'
        mail.send(msg)
        user= cursor.fetchone()
        if user:
            return redirect('/contact')
    return render_template('contact.html')

@app.route('/education')
def education():
    return render_template('education.html')


@app.route("/")
def index():
    return render_template("index.html")




if __name__=="__main__":
    app.run(debug=True)
