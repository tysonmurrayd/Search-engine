from flask import Flask, request, render_template, redirect, session, url_for
from flask_mysqldb import MySQL, MySQLdb
import sys
import urllib.request

sys.path.append('/home/tysonmd/git_repo')
import company_search, json_handler, cisa, scrape_cybernews, industry_news

# def clean(company_dict):
# 	for value in company_dict:
# 		if isinstance(value[1], list):
# 			for v in value[1]:
# 				v.strip("\\xa")
# 		else:
# 			value[1].strip("\\xa")
		
# 	return company_dict

def check_empty(r_dict):
    for dict in r_dict:
        if dict != {}:
            return False
    return True

def convert_string(company_dict):
	new_dict = {}
	for value in company_dict.items():
		if isinstance(value[1], list):
			string_v = ""
			for v in value[1]:
				string_v += " " + v.replace("\xa0", " ") + ","
			new_dict[value[0]] = string_v.strip(",")
		else:
			new_dict[value[0]] = value[1]
		
	return new_dict

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSSWORD'] = ''
app.config['MYSQL_DB'] = 'ScraperDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = "Wow so secret"
mysql = MySQL(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template("login.html")

@app.route('/register', methods = ["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:

        if request.form['name'] == '' or request.form['email'] == '':
            return render_template('register.html', Error_msg = "Error! Make sure all fields are filled out")
    
        name = request.form['name']
        email = request.form['email']
        # password = request.form['password']

        try:
            cur = mysql.connection.cursor()
            if request.form.get("n-mail"):
                cur.execute("INSERT INTO users (name, email, password, newsletter) VALUES (%s,%s,%s,%s)",(name, email, '', True))
            else:
                cur.execute("INSERT INTO users (name, email, password, newsletter) VALUES (%s,%s,%s,%s)",(name, email, '', False))
            mysql.connection.commit()
        except mysql.connection.Error as e:
            return render_template('register.html', Error_msg='Sorry, an account already exists for this email')
            
        session['name'] = name
        session['email'] = email
        return redirect(url_for("home"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        # password = request.form['password']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if not(user):
            return render_template('login.html', Error_msg="An account does not exist for that email")

        if len(user) > 0:
            if email == user['email']:
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("index.html")    
            else:
                return render_template('login.html', Error_msg="Error. Incorrect user/password")
        else:
            return "Please enter the required information!"
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/result", methods=["POST", "GET"])
def result():
    output = request.form.to_dict()
    name = output["name"]
    r_dict = company_search.from_website(name, output['inputted-news'])
    r_dict[0] = convert_string(r_dict[0])
    if 'industry' in output:
        r_dict += industry_news.get_news(r_dict[0])
    if check_empty(r_dict):
        return render_template("result_page.html", nothing = 'Sorry, we couldn\'t find any information on ' + output['name'])

    return render_template("result_page.html", name = r_dict)


if __name__=="__main__":
    # app.secret_key = "hehehe yah "
	app.run(debug=True)
