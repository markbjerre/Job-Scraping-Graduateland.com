import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from cache_functions import save_cache, open_cache

def job_scrape(driver):
    '''
    Function for scraping page of job links
    Input: chromedriver (current webpage)
    output: list of job site links
    ''' 
    links_cache = 'link_cache.json'
    link_dict = open_cache(links_cache)

    link_count = max(list(link_dict.values()))
    jobs_list = driver.find_elements(By.CLASS_NAME, 'job-box')
    for job in jobs_list:
        link = job.get_attribute('href')
        if not link_dict.get(link):
            link_dict[job.get_attribute('href')] = link_count + 1
            link_count += 1 

    save_cache(link_dict, links_cache)

    return link_dict


def Crawler(pages):
    page_iterations = pages
    search_area = 'Copenhagen Metropolitan Area'
    search_position = 'Data Analyst'
    # Chrome driver setup & browser open
    options = Options()
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(service =Service('chromedriver.exe'), options=options)
    driver.implicitly_wait(10)

    # Open page
    driver.get('https://graduateland.com/jobs')
    time.sleep(2)

    # Filtering on area
    driver.find_element(By.XPATH, '//*[@id="search-filters"]/div[46]/div/div[1]/input').send_keys(search_area)
    driver.find_element(By.XPATH, '//*[@id="search-filters"]/div[46]/div/div[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="search-filters"]/div[46]/div/div[2]/label[2]').click()

    # Entering position filter keywords
    driver.find_element(By.XPATH, '//*[@id="job-search-form"]/div[1]/div[1]/div[1]/input').send_keys(search_position, Keys.ENTER)
    time.sleep(3)

    #initializing scrape loop at page 1
    page = 1 
    print('scraping job links, page:', page)
    links = job_scrape(driver)

    # Page iterator
    for i in range(1, page_iterations):
        # handling XPATH variations based on page numbers
        if i < 3:
            index = i * 2 
        elif i < 6:
            index = i + 2
        else:
            i = 7
        # Clicking next page button
        driver.find_element(By.XPATH, '//*[@id="timeline"]/div[3]/div/a[{}]'.format(index)).click()
        page += 1
        print('scraping job links, page:', page)
        time.sleep(3)
        # Scraping job post links from page
        links = job_scrape(driver)
        if i % 20 == 0:
            time.sleep(60)

if __name__=='__main__':
    Crawler(5)