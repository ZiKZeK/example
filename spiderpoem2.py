# %小学专题%
# URL ='http://www.zggushi.com/zi/1993.html'
# URL ='http://www.zggushi.com/zi/2337.html'
# URL ='http://www.zggushi.com/zi/2008.html' # 初中古诗
URL ='http://www.zggushi.com/zi/2115.html' # 初中文言文
# URL ='http://www.zggushi.com/zi/2057.html' # 高中古诗
# URL ='http://www.zggushi.com/zi/2121.html' # 高中文言文
import requests
from bs4 import BeautifulSoup
from os import makedirs
from os.path import exists

# RESULT_DIR = 'poem_primary_text'
# RESULT_DIR = 'poe_junior_gs'
RESULT_DIR = 'poe_junior_text'
# RESULT_DIR = 'poe_senior_gs'
# RESULT_DIR = 'poe_senior_text'

exists(RESULT_DIR) or makedirs(RESULT_DIR)
import requests
import logging
import re
import csv
BASE_URL = 'http://www.zggushi.com/{post}'

def get_poem_url(html):
    soup = BeautifulSoup(html, 'lxml')
    all = soup.find('div', class_ ='zd-mcon')
    all = all.find('ul')
    href_list = []
    if all is not None:
        links = all.find_all('a')  
        for link in links:
            href = link.get('href')
            href_list.append(href)
    return href_list

def scrape_page(url):
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info= True)


def parse_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    title_pattern = re.compile('<h1>(.*?)</h1>')
    author_pattern = re.compile('class="gs-poem-sub">(.*?)</div>')
    poem_pattern = re.compile('gs-conview-def">(.*?)<br><hr>')
    poem_nodes = soup.find('div', class_ = "gs-conview-def")
    if poem_nodes.p:
        poem = poem_nodes.p.text.replace('\xa0', ' ')
        poem = poem_nodes.p.text.replace('\u2002', ' ')
    else:
        text = poem_nodes.text
        pattern = r'[\u4e00-\u9fa5，.。！？]+'
        poem = re.findall(pattern, text) 
        if re.findall(pattern, text):
            poem = poem[0]
        else:
            poem =None
        
        


    title = re.search(title_pattern, html).group(1) if re.search(title_pattern, html) else None
    title = title.replace('/','_')
    author = re.search(author_pattern, html).group(1) if re.search(author_pattern, html) else None
    # poem = re.findall(poem_pattern, html) if re.findall(poem_pattern, html) else []
    # poem = re.sub('<br>', '', str(poem))

    return {"title" : title, "author" : author, "poem" : poem}

def save_data(data):
    data_path = f'{RESULT_DIR}/{data["title"]}.csv'
    with open(data_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'author', 'poem'])
        writer.writerow({"title" : data["title"], "author" : data["author"], "poem" : data["poem"]})
    
def main():
    html = scrape_page(URL) 
    if html:
        href_list = get_poem_url(html)
        for href in href_list:
            url = BASE_URL.format(post=href)
            if url:
                html = scrape_page(url)
                if html:
                    data = parse_detail(html)
                    if data:
                        save_data(data)
                    else:
                        logging.error('parse data failed while scraping %s', url)
                else:
                    logging.error('get invalid response while scraping %s', url)
            else:
                logging.error('get invalid url while scraping %s', url)
    else:
        logging.error('get invalid response while scraping %s', URL)

if __name__ == '__main__':
    main()