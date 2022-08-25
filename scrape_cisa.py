#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
# import scrape_dynamic

def cisa_articles(soup):
	r_dict = {}
	result = soup.find('div', class_='region region-content')
	r_dict['c_title'] = result.find('h1', id='page-title').get_text()
	article = result.find('div', class_='field field--name-body field--type-text-with-summary field--label-hidden field--item')
	values = article.find_all('p')
	for index, value in enumerate(values):
		if index > 0:
			break
		if value.find('img'):
			image = value.find("img").get('src')
			r_dict['img'] = 'https://www.cisa.gov' + image
		r_dict['text'] = value.get_text()
	return r_dict
	


def cisa_info(list_cisa):
	base_url = "https://www.cisa.gov/"
	list_dict = []
	try:
		for sector in list_cisa:
			url = base_url + sector.replace(" ", "-").lower()
			r = requests.get(url, "html.parser")
			soup = BeautifulSoup(r.content, features="html.parser")
			r_dict = cisa_articles(soup)
			r_dict['link'] = url
			list_dict.append(r_dict)
		return list_dict
	except Exception as e:
		return []

# l = cisa_info(['commercial facilities sector', 'critical manufacturing sector'])
# print(l)