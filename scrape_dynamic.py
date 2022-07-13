#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time

def start_driver():
    global DRIVER
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    '''PATH TO CHROME DRIVER NEEDS TO BE UPDATED to "/usr/bin/chromedriver"'''
    path = "/usr/bin/chromedriver"
    DRIVER = webdriver.Chrome(path, options=chrome_options)   

def get_dynamic(url):
    DRIVER.get(url)
    time.sleep(3)
    soup = BeautifulSoup(DRIVER.page_source, "html.parser")
    return soup

def quit_driver():
    DRIVER.quit()


#get_dynamic('https://www.bleepingcomputer.com/search/?cx=partner-pub-0920899300397823%3A3529943228&cof=FORID%3A10&ie=UTF-8&q=walmart')