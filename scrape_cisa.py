#!/usr/bin/env python3
from bs4 import BeautifulSoup
import scrape_dynamic

def cisa_articles(soup):
	r_dict = {}
	results = soup.find("div", class_="gsc-expansionArea")
	articles = results.find_all("div", class_="gsc-webResult gsc-result")
	for index,article in enumerate(articles):
		if index==0:
			continue
		elif index==3:
			break
		a_title = article.find("a").get_text(" ", strip=True)
		r_dict[a_title] = article.find("a").get("href")
	
	return r_dict

def cisa_info(list_cisa):
	base_url = "https://www.cisa.gov/uscert/search?g="
	list_dict = []
	for sector in list_cisa:
		url = base_url + sector.replace(" ", "%20")
		soup = scrape_dynamic.get_dynamic(url)
		list_dict.append(cisa_articles(soup))
	return list_dict

