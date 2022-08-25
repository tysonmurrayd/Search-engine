#!/usr/bin/env python3
import scrape_dynamic
import call_api


# bleeping computer

def get_info(list_articles):
    result_dict = {}
    for index, article in enumerate(list_articles):
        if index == 4:
            break
        title = article.find("a", class_="gs-title").get_text(" ", strip=True)
        result_dict[title] = article.find("a", class_="gs-title").get("href")
    
    return result_dict



def bleeping_news(industry):
    source = "https://www.bleepingcomputer.com/search/?q="
    soup = scrape_dynamic.get_dynamic(source + industry)
    try:
        s_result = soup.find("div", class_="gsc-expansionArea")
        list_articles = s_result.find_all("div", class_="gsc-webResult gsc-result")
        result = get_info(list_articles)
    except Exception as e:
        print(e)

    return result

# ----------------------------------------------------------------------------------------

# Dark reading

def get_dark_info(l_articles):
    r_dict = {}
    for index, article in enumerate(l_articles):
        if index == 4:
            break
        title = article.find("h2", class_="").get_text(" ", strip=True)
        r_dict[title] = article.find("a").get("href")
    
    return r_dict


def dark_reading(industry):
    source = "https://www.darkreading.com/search?q="
    soup = scrape_dynamic.get_dynamic(source + industry)
    try:
        s_result = soup.find("div", class_="infinite-scroll-component")
        list_articles = s_result.find_all("article", class_="search-result-item")
        result = get_dark_info(list_articles)
    except Exception as e:
        print(e)
    
    return result


# ------------------------------------------------------------------------------------------


def get_news(company_dict):
    r_list = []
    try:
        if isinstance(company_dict['Industry'], list):
            industry = company_dict['Industry'][0].replace(" ", "+")
        else:
            industry = company_dict['Industry'].replace(" ", "+")
    except Exception as e:
        print(e)
        return {}

    r_list.append(call_api.get_DarkReading(industry))
    return r_list
    # return call_api.get_DarkReading(industry)


    