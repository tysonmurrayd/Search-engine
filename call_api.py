#!/usr/bin/env python3
import requests
import json

def get_DarkReading(company):
    r_dict = {}
    b_url = "https://www.darkreading.com/"
    # query = {'data': { 'hits': { '0': { '_source': { } } } } }
    query = {'_source': {}}
    response = requests.get("https://1mivf7hmd3.execute-api.us-east-1.amazonaws.com/live/search?from=0&q=" + company + "&size=3", params=query)
    if response.ok:
        jdata = json.loads(response.content)
        # for key in jdata:
        #     print(key + ": " + str(jdata[key]))
        l_articles = jdata['data']['hits']
        for article in l_articles:
            d = article['_source']
            r_dict[d['title']] = b_url + d['term_selector']['primaryTerm'] + d['url']
        # for d in l_articles:
        #     print(d['_source'])
    else:
        return {}
    
    return r_dict

