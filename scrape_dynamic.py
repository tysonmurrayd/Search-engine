#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time


def get_dynamic(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


    '''PATH TO CHROME DRIVER NEEDS TO BE UPDATED to "/usr/bin/chromedriver"'''
    path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup


#get_dynamic('https://www.bleepingcomputer.com/search/?cx=partner-pub-0920899300397823%3A3529943228&cof=FORID%3A10&ie=UTF-8&q=walmart')