URL = "http://www.zggushi.com/gushi/26010.html"
from os import makedirs
from os.path import exists
from bs4 import BeautifulSoup

RESULT_DIR = 'poem'
exists(RESULT_DIR) or makedirs(RESULT_DIR)

import requests
import logging
import re
import csv
# 页面爬取
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
    # poem_pattern = re.compile('<p>(.*?)<br>(.*?)</p>')
    poem_node = soup.find('div', class_='gs-works-text')
    poem = poem_node.div.text if poem_node else None


    title = re.search(title_pattern, html).group(1) if re.search(title_pattern, html) else None
    author = re.search(author_pattern, html).group(1) if re.search(author_pattern, html) else None
    # poem = re.findall(poem_pattern, html) if re.findall(poem_pattern, html) else []

    return {"title" : title, "author" : author, "poem" : poem}

def save_data(data):
    data_path = f'{RESULT_DIR}/{data["title"]}.csv'
    with open(data_path, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'author', 'poem'])
        writer.writerow({"title" : data["title"], "author" : data["author"], "poem" : data["poem"]})
    
def main():
    html = scrape_page(URL)
    # print (html)
    if html:
        data = parse_detail(html)
        save_data(data)
        print(data)
    else:
        print('scraping failed')

if __name__ == '__main__':
    main()