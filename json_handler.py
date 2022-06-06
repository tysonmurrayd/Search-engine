#!/usr/bin/env python3
import json


def save_data(data):
	with open("companies.json", 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=2)


def search_json(token):
	dict = {}
	with open("/home/tysonmd/company_info/companies.json", "rb") as s_file:
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
	with open("companies.json", "rb") as s_file:
		list_dict = json.load(s_file)
	list_dict.append(dict)
	save_data(list_dict)



def clean_file():
	with open("companies.json", "rb") as s_file:
		list_dict = json.load(s_file)

	for company in list_dict:
		for key, value in company.items():
			if isinstance(value, list):
				for v in value:
					v.strip("\\xa")
			else:
				value.strip("\\xa")

		save_data(list_dict)

#clean_file()
#please = search_json("Edward Jones Investments")
