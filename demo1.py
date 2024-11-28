from bs4 import BeautifulSoup
import requests
import re

# url = 'http://www.zggushi.com/zi/1993.html'
# url = 'http://www.zggushi.com/gushi/26010.html'
url = 'http://www.zggushi.com/gushi/28922.html'
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text
soup = BeautifulSoup(html, 'lxml')
# all = soup.find('div', class_ ='zd-mcon')
all = soup.find('div', class_ = 'gs-conview-def')
# all = all.find('ul')
if all.p:
    print(all.p.text)
else:
    poem =str(all.text)
    # pattern_remove_pinyin =r'[a-zāáǎàēéěèíìūúǔùńǒòōóǒǎǖǘǚǜ]*[\u4e00-\u9fa5]+'
    # poem = re.sub(pattern_remove_pinyin, '', poem)
    pattern = r'[\u4e00-\u9fa5，.。！？]+'
    # poem = '' .join(re.findall(pattern, patten_extract_poem))
    # pattern = r'^[\u4e00]+(?=[a-zA-Z])'
    poem = re.findall(pattern, poem)
    print(poem[0])
# print(re.search('^(.?) ', all.div.text))

# if all is not None:
#     links = all.find_all('a')
#     for link in links:
#         href = link.get('href')
#         print(href)