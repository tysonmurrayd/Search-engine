
import requests
import json
import re
# '''
# fetch company technology stack information from techstacks.io
# '''
def articles(search_name):
    r_dict = {}
    #now use company name to query for the tech stack
    tech_url = "https://techstacks.io/json/reply/GetTechnologyStack?slug=" + search_name
    response = requests.get(tech_url)
    if response.ok:
        pattern = re.compile(r"\- \[(.*?)\]\((.*?)\)")
        jdata = json.loads(response.content)
        list_lines = jdata['result']['details'].split("\n")
        for line in list_lines:
            # print(line)
            r = pattern.search(line)
            if r != None:
                r_dict[r.group(1)] = r.group(2)
    else:
        return {}

    return r_dict


def tech_stack(search_name):
    r_dict = {}
    #now use company name to query for the tech stack
    tech_url = "https://techstacks.io/json/reply/GetTechnologyStack?slug=" + search_name
    response = requests.get(tech_url)
    if response.ok:
        jdata = json.loads(response.content)
        l_tech = jdata['result']['technologyChoices']
        for tech in l_tech:
            if tech['tier'] not in r_dict:
                r_dict[tech['tier']] = [tech['logoUrl']]
            else:
                r_dict[tech['tier']].append(tech['logoUrl'])
    else:
        return {}
    
    return r_dict

def get_tech(company):
    name_url = "https://techstacks.io/json/reply/QueryTechStacks?include=total&nameContains=" + company
    response = requests.get(name_url)
    if not response.ok:
        return []

    try:
        jdata = json.loads(response.content)
        first_result = jdata['results'][0]
        search_name = first_result['slug']

        r_list = []
        r_list.append(tech_stack(search_name))
        r_list.append(articles(search_name))
    except Exception:
        return []

    return r_list
