from bs4 import BeautifulSoup
import scrape_dynamic

'''
fetch company technology stack information from techstacks.io
'''
def get_content(l_tech):
    r_dict = {}
    for tech in l_tech:
        # print('in loop')
        title = tech.find("h2").get_text()
        r_dict[title] = [t.find("img").get("src") for t in tech.find_all("div", class_="flex", style="max-width: 300px;")]
    
    return r_dict

def get_articles(soup):
    r_dict = {}
    articles_class = soup.find("div", class_="details-html", style="padding: 1em;")
    articles = articles_class.find_all("li")
    for article in articles:
        r_dict[article.find('a').get_text()] = article.find("a").get("href")
    return r_dict
    

def get_tech(company):
    r_list = []
    search_url = "https://techstacks.io/stacks/?nameContains=" + company
    b_url = "https://techstacks.io"
    search_soup = scrape_dynamic.get_dynamic(search_url)
    # print(soup)
    # print(url)
    try:
        soup = scrape_dynamic.get_dynamic(b_url + search_soup.find("div", class_="container fluid grid-list-md").find_all("div", class_="flex xs3")[0].find("a").get("href"))
        technologies_class = soup.find("div", class_="container body grid-list-md")
        # print(technologies_class)
        tech = technologies_class.find_all("div", class_="layout tech-info")
        # print(tech)
        r_list.append(get_content(tech))
        r_list.append(get_articles(soup))
    except Exception as e:
        print(e)
        return {}

    return r_list

# l = get_tech("AT&T")
# print(l)