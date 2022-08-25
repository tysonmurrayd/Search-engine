from flask import Flask,request, render_template, redirect, session, url_for
from flask_mysqldb import MySQL, MySQLdb


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSSWORD'] = ''
app.config['MYSQL_DB'] = 'ScraperDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("login.html")

@app.route('/register', methods = ["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name, email, password))
        mysql.connection.commit()
        session['name'] = name
        session['email'] = email
        return redirect(url_for("home"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if not(user):
            return "An account does not exist for that email"

        if len(user) > 0:
            if password == user['password']:
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")    
            else:
                return "Error. Incorrect user/password"
        else:
            return "Please enter the required information!"
    return render_template("home.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.secret_key = "ApolloIsWebScraperProject"
    app.run(debug=True)