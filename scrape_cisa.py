""" #!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def cisa_articles(soup):
	r_dict = {}
	results = soup.find("div", class_="expansionArea")
	articles = results.find_all("div", class_="gsc-webResult gsc-result")
	for index,article in enumerate(articles):
		if index==0:
			continue
		elif index==3:
			break
		a_title = article.find("a").get_text(" ", strip=True)
		a_link = article.find("a").get("href")

def cisa_info(list_cisa):
	base_url = "https://www.cisa.gov/uscert/search?g="
	list_dict = []
	for sector in list_cisa:
		url = base_url + sector.replace(" ", "%20")
		print(url)
		r = requests.get(url, "html.parser")
		soup = BeautifulSoup(r.content, features="html.parser")
		list_dict.append(cisa_articles(soup))

cisa_info(["Information Technology Sector"])

 """