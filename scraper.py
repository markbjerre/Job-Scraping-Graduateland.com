from bs4 import BeautifulSoup
import requests
import re
from datetime import date
from cache_functions import save_cache, open_cache

def Offline_test(url):
    #returns True of job is offline
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    offline = soup.find('section', class_='job-offline')
    if offline == None:
        return False
    else:
        links_cache = 'link_cache.json'
        link_dict = open_cache(links_cache)
        del link_dict[url]
        save_cache(link_dict, links_cache)
        return True

def Scraper(url, vert_dict, store_cache):
    
    def attribute_extract(soup):
        attributes = soup.find('div', class_='content-description')
        attributes = attributes.find_all('p')
        last = ''
        attributes_list = [i.text.strip() for i in attributes if i.text != None]
        idx = 0
        for i in attributes_list:
            new_elem = re.sub('  ', '', i)
            new_elem = re.sub('\\n\\n\\n','___',new_elem)
            new_elem = new_elem.split('___')
            if len(new_elem) != 1:
                new_elem = [re.sub('\\n', '', i).lstrip() for i in new_elem]
                attributes_list[idx] = new_elem
            else:
                new_elem = re.sub('\\n',' ',new_elem[0])
                attributes_list[idx] = new_elem
            idx += 1 
        return attributes_list

    vertex_cache = 'vertex_cache.json'
    
    if vert_dict.get(url):
        attr_dict = vert_dict.get(url)
        return attr_dict
    else:
        attr_dict = {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    
    attr_dict['link'] = url
    # Title 
    try:
        title_ = soup.find('div',class_='job-title').find('h1').text
        attr_dict['title'] = title_
    except:
        title_ = None
        attr_dict['title'] = None
    # Job description
    try:
        job_desc_ = soup.find('article', class_='box-item job-content').text.lstrip()
        attr_dict['job_desc'] = job_desc_
    except:
        attr_dict['job_desc'] = None
    # Expiration
    try:
        expiration = soup.find('span', class_= 'text-warning').text.strip()
    except: 
        expiration = None
    attr_dict['expiraton'] = expiration

    # Headline element
    headline = soup.find('div', class_='headline')
    # Company
    try:
        company_ = headline.find('h2').text.strip()
        attr_dict['company'] = company_
    except:
        try:
            attr_dict['company'] = re.findall('(?<=\sat).(.*)',title_)[-1]
        except:
            attr_dict['company'] = None
    # Industry    
    try:
        industry_ = headline.find_all('p')[0].text.strip()
        attr_dict['industry'] = industry_
    except:
        attr_dict['industry'] = None
    # Followers
    try:
        followers_ = headline.find_all('p')[1].text.strip()
        followers_ = re.sub('[^0-9]', '', followers_)
        attr_dict['followers'] = followers_
    except:
        attr_dict['followers'] = None
    #logo
    try:
        logo_soup = soup.find('div',class_='company-item')
        logo_ = logo_soup.find('img')['src']
        attr_dict['logo'] = logo_ 
    except:
        attr_dict['logo'] = None

    # Attributes (location, category, job_type, skills, language)
    attributes = attribute_extract(soup)
    try:
        location_ = attributes[0]
        attr_dict['location'] = location_
    except:
        attr_dict['location'] = None
    try:
        category_ = attributes[1]
        attr_dict['category'] = category_
    except:
        attr_dict['category'] = None
    try:
        job_type_ = attributes[2]
        attr_dict['job_type'] = job_type_
    except:
        attr_dict['job_type'] = None
    try:
        skills_ = attributes[3]
        attr_dict['skills'] = skills_
    except:
        attr_dict['skills'] = None
    try:
        language_ = attributes[4]
        attr_dict['language'] = language_
    except:
        attr_dict['language'] = None
   

    attr_dict['date_scraped'] = date.today().strftime("%d-%m-%Y")

    vert_dict[url] = attr_dict
    if store_cache == True:
        save_cache(vert_dict, vertex_cache)
    return attr_dict