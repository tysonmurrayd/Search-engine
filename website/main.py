from flask import Flask,render_template,request
import sys
import urllib.request

sys.path.append('/home/tysonmd/git_repo')
import company_search, json_handler, cisa, scrape_cybernews

# def clean(company_dict):
# 	for value in company_dict:
# 		if isinstance(value[1], list):
# 			for v in value[1]:
# 				v.strip("\\xa")
# 		else:
# 			value[1].strip("\\xa")
		
# 	return company_dict

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

@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/result", methods=["POST", "GET"])
def result():
	output = request.form.to_dict()
	name = output["name"]
	r_dict = company_search.from_website(name)
	r_dict[0] = convert_string(r_dict[0])

	return render_template("result_page.html", name = r_dict)


#if __name__=="__main__":
#	app.run(debug=True)
