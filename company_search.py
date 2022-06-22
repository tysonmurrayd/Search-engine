'''
MAIN MODULE!
'''
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
from PIL import Image
import scrape_cybernews, cisa, json_handler

#def big_scrape():
#	base_url = "https://en.wikipedia.org"
#	url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
#	r = requests.get(url, "html.parser")
#	soup = BeautifulSoup(r.content, features="html.parser")
#	table = soup.find("table", class_="wikitable sortable")
#	table = table.find("tbody")
#	list_rows = table.find_all("tr")
#	list_o_dicts = []
#	for index, row in enumerate(list_rows):
#		if index==0:
#			continue
#		try:
#			find_a = row.find_all("a")
#			link = find_a[0]
#			link = link.get("href")
#			list_o_dicts.append(get_info_box(base_url + link))
#		except Exception:
#			continue
#	return list_o_dicts

def remove_reference(soup):
	'''removes all of the refrence subtext in the 
	html code (ie. [1][2])'''
	for tag in soup.find_all("sup"):
		tag.decompose()
	return soup

def scrape_image(info_rows, dict):
	'''saves the link to the png company logo in the dictionary
	scrapped from the first wiki box element'''
	base_url = "https:"
	try:
		image = info_rows.find("img")
		link = image.get('src')
		link = base_url + link
		dict["logo url"] = link
	except Exception as e:
		print("logo not found")

	return dict

def get_soup(url):
	'''requests html from url and returns the box element from
	wiki page'''
	r = requests.get(url, "html.parser")
	soup = BeautifulSoup(r.content, features="html.parser")
	soup = remove_reference(soup)
	box_class = soup.find("table", class_="infobox vcard")
	return box_class


def get_info_box(url):
	'''reads through the infobox from wiki
	and gathers all the information into a dictionary.
	returns dictionary'''
	print("searching the internet...")
	box_class = get_soup(url)
	company_info = {}
	if box_class == None:
		box_class = get_soup(url + "_company")
		if box_class == None:
			print("sorry, cannot find info about this company")
			return {}

	info_rows = box_class.find_all("tr")
	company_info = scrape_image(info_rows[0], company_info)
	company_info['company'] = box_class.find("caption", class_="infobox-title").get_text(" ", strip=True)
	for row in info_rows:
		try:
			content_key = row.find("th").get_text(" ", strip=True)
			content_value = get_content_value(row.find("td"))
			company_info[content_key] = content_value
		except Exception as e:
			continue
	company_info = cisa.find_cisa(company_info)
	return company_info

def get_content_value(row_data):
	'''if class contains "li" or "br" elements, seperate them into lists
	otherwise retrieve the string'''
	if row_data.find("li"):
		return [li.get_text(" ", strip=True).strip("\\xa") for li in row_data.find_all("li")]
	elif row_data.find_all("br"):
		return [a.get_text(" ", strip=True).strip("\\xa") for a in row_data.find_all("a")]
	else:
		content_value = row_data.get_text(" ", strip=True)
		return content_value


def print_dict(dict):
	'''print fromatted version of a dictionary'''
	list_info = dict.items()
	for item in list_info:
		if item[0] == 'company':
			print("Company: ", item[1])
			print('--------------------------------------')
			print()
		elif item[0] == 'CISA':
			if item[1] != []:
				print("CISA sector(s): ", end='')
				print(*item[1], sep=',')
		else:
			if isinstance(item[1], list):
				print(item[0] + ': ', end='')
				print(*item[1], sep=',')
			else:
				print(item[0] + ': ', item[1])
			print()


def input_handling():
	'''takes maximum of 3 words and seperates them
	with spaces'''
	if len(sys.argv) > 4 or len(sys.argv) < 2:
		print("usage: python3 company_search.py {company name}")
		sys.exit(1)
	comp = sys.argv[1].capitalize()
	if len(sys.argv) > 2:
		comp += " " + sys.argv[2].capitalize()
		if len(sys.argv) > 3:
			comp += " " + sys.argv[3].capitalize()
	return comp

def manage_cybernews(info_dict, inputted):
	'''prints and retrieves first three links from desired website'''
	news_url = "https://cybernews.com/search/"
	wired_url = "https://www.wired.com/search/?q="
	nyt_url = "https://www.nytimes.com/search?query="
	krebs_url = "https://krebsonsecurity.com/?s="
	darkread_url = "https://www.darkreading.com/search?q="
	bleepingcomp_url = "https://www.bleepingcomputer.com/search/?q="
	kaspersky_url = "https://usa.kaspersky.com/search?query="
	broadcom_url = "https://www.broadcom.com/site-search?q="

	print()
	print("LATEST CYBER NEWS\n", "----------------------------------------")
	cyber_dict = scrape_cybernews.get_news(news_url + inputted)
	scrape_cybernews.print_news(cyber_dict)
	print("WIRED NEWS!\n", "---------------------------------------")
	wired_dict = scrape_cybernews.scrape_wired(wired_url + inputted)
	scrape_cybernews.print_news(wired_dict)
	print("NEW YORK TIMES NEWS\n", "---------------------------------------")
	nyt_dict = scrape_cybernews.scrape_nyt(nyt_url + inputted)
	scrape_cybernews.print_news(nyt_dict)
	print("KREBS ON SECURITY NEWS\n", "---------------------------------------")
	krebs_dict = scrape_cybernews.scrape_krebs(krebs_url + inputted)
	scrape_cybernews.print_news(krebs_dict)
	print("DARK READING NEWS\n", "---------------------------------------")
	darkread_dict = scrape_cybernews.scrape_darkread(darkread_url + inputted)
	scrape_cybernews.print_news(darkread_dict)
	print("BLEEPING COMPUTERS NEWS\n", "---------------------------------------")
	bleepingcomp_dict = scrape_cybernews.scrape_bleepingcomp(bleepingcomp_url + inputted)
	scrape_cybernews.print_news(bleepingcomp_dict)
	print("KASPERSKY NEWS\n", "---------------------------------------")
	kaspersky_dict = scrape_cybernews.scrape_kaspersky(kaspersky_url + inputted)
	scrape_cybernews.print_news(kaspersky_dict)
	print("BROADCOM NEWS\n", "---------------------------------------")
	broadcom_dict = scrape_cybernews.scrape_broadcom(broadcom_url + inputted)
	scrape_cybernews.print_news(broadcom_dict)

def from_website(input):
	r_list = []
	wiki_url = "https://en.wikipedia.org/wiki/"
	info_dict = json_handler.search_json(input)
	if info_dict == {}:
		input = input.replace(" ", "_")
		info_dict = get_info_box(wiki_url + input)
		if info_dict != {}:
			json_handler.add_json(info_dict)
	r_list.append(info_dict)
	input = input.replace("_", " ")
	r_list = r_list + scrape_cybernews.retrieve_news(input)
	return r_list

def main():
	wiki_url = "https://en.wikipedia.org/wiki/"
	inputted = input_handling()
	info_dict = json_handler.search_json(inputted)
	if info_dict == {}:
		inputted = inputted.replace(" ", "_")
		info_dict = get_info_box(wiki_url + inputted)
		json_handler.add_json(info_dict)
	print_dict(info_dict)
	inputted = inputted.replace("_", " ")
	manage_cybernews(info_dict, inputted)

if __name__ == "__main__":
	main()
