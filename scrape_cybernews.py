#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
from PIL import Image
import urllib.request


def print_news(dict):
	list_info = dict.items()
	for item in list_info:
		print(item[0] + ": ", item[1])
		print()

def news_soup(url):
	r = requests.get(url, "html.parser")
	return BeautifulSoup(r.content, features="html.parser")

''' get info from cybernews.com'''

def make_dict(l_articles):
	news_dict = {}
	for index, article in enumerate(l_articles):
		if index == 3:
			break
		dict_key = article.find("h3").get_text(" ", strip=True)
		find_link = article.find("a")
		link = find_link.get("href")
		news_dict[dict_key] = link
	return news_dict

def get_news(url):
	result_dict = {}
	soup = news_soup(url)
	try:
		broad_class = soup.find("div", class_="cells cells_responsive")
		l_articles = broad_class.find_all("article")
		result_dict = make_dict(l_articles)
		return result_dict
	except Exception:
		#print("sorry, cannot find any cybernews on this company")
		return result_dict

'''-----------------------------------------------------------------------'''

'''get info from wired.com'''

def wired_dict(l_articles):
	b_url = "https://www.wired.com"
	r_dict = {}
	for index, article in enumerate(l_articles):
		if index==3:
			break
		dict_key = article.find("h3").get_text(" ", strip=True)
		dict_url = article.find("a").get("href")
		r_dict[dict_key] = b_url + dict_url
	return r_dict



def scrape_wired(url):
	soup = news_soup(url)
	w_dict = {}
	try:
		broad_class = soup.find("div", class_="summary-list__items")
		l_articles = broad_class.find_all("div", class_="SummaryItemWrapper-gdEuvf bheJMz summary-item summary-item--has-border summary-item--article summary-item--no-icon summary-item--text-align-left summary-item--layout-placement-side-by-side-desktop-only summary-item--layout-position-image-left summary-item--layout-proportions-33-66 summary-item--side-by-side-align-center summary-item--standard SummaryItemWrapper-bGkJDw ifBcbu summary-list__item")
		w_dict = wired_dict(l_articles)
		return w_dict
	except Exception:
		#print("sorry, cannot find any wired news about this company <{0_0}>")
		return w_dict

'''-----------------------------------------------------------------------------------'''

'''get from new york times'''

def nyt_dict(l_articles):
	r_dict = {}
	b_url = "https://www.nytimes.com"
	for index,article in enumerate(l_articles):
		if index==3:
			break
		dict_key = article.find('h4').get_text(" ", strip=True)
		dict_url = article.find('a').get("href")
		r_dict[dict_key] = b_url + dict_url
	return r_dict


def scrape_nyt(url):
	soup = news_soup(url)
	w_dict = {}
	try:
		broad_class = soup.find("div", class_="css-46b038")
		l_articles = broad_class.find_all('li')
		w_dict = nyt_dict(l_articles)
		return w_dict
	except Exception:
		#print("sorry, cannot find any wired news about this company <{0_0}>")
		return w_dict

'''------------------------------------------------------------------------------------'''

def retrieve_news(input):
	r_list = []
	news_url = "https://cybernews.com/search/"
	wired_url = "https://www.wired.com/search/?q="
	nyt_url = "https://www.nytimes.com/search?query="
	r_list.append(get_news(news_url + input))
	r_list.append(scrape_wired(wired_url + input))
	r_list.append(scrape_nyt(nyt_url + input))
	return r_list
