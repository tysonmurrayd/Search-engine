#!/usr/bin/env python3
import json
import cisa

'''WITH OPEN(r"C:....") FILES CHANGEd FROM "/var/company_data/companies.json" '''


def save_data(data):
	'''
	save the current list of dictionaries to companies json located in
	/var/company_data
	'''
	with open(r"C:\Users\Luck\Code\Search-engine\companies.json", 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=2)


def search_json(token):
	'''
	try to find if the company inputted is in the json file
	'''
	dict = {}
	with open(r"C:\Users\Luck\Code\Search-engine\companies.json", "rb") as s_file:
		list_dict = json.load(s_file)

	for company in list_dict:
		try:
			if company != {}:
				if (token.lower() == company["company"].lower() or token.lower() in company["company"].lower()
				or token.lower() == company["Trade name"].lower() or token.lower() in company["Trade name"].lower()):
					return company
		except Exception:
			continue
	return dict


def add_json(dict):
	'''
	add a dictionary to the list of dictionaries and save it to
	companies.json
	'''
	with open(r"C:\Users\Luck\Code\Search-engine\companies.json", "rb") as s_file:
		list_dict = json.load(s_file)
	list_dict.append(dict)
	save_data(list_dict)



def better_cisa():
	'''
	clean the character "/xa0" from the file
	'''
	with open(r"C:\Users\Luck\Code\Search-engine\companies.json", "rb") as s_file:
		list_dict = json.load(s_file)

	for company in list_dict:
		cisa.find_cisa(company)


	save_data(list_dict)

better_cisa()
#please = search_json("Edward Jones Investments")
#print(please)
