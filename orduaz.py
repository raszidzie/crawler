import urllib.request
import hashlib
import httplib2
import ssl
import os
import webbrowser
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime


def crawl_orduaz(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    items = bs.find('div', class_="col-md-9 col-sm-12").find_all('div', class_='news-box')[0:20]
    #brak ostatni
    whole_news = []
    for item in items:
        news = {
            'title': item.find('div', class_="news-title").getText(),
            'image': item.find('div', class_= 'news-img').find('img')['src'].replace('/resizer.php?src=',''),
            'link': item.find('a')['href']
        }
        news.update(get_news_details(news['link']))
        whole_news.append(news)



    return whole_news


def get_news_details(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    container = bs.find('section', id= 'content')
    full_date = container.find('i', class_= 'fa fa-clock-o').next_sibling
    l = full_date.split()
    date = l[1]
    ay = l[2]
    month = convert_month_to_number(ay)
    year = l[3]
    time = l[0]
    fullDate = date + '.' + str(month) + '.' + year
    timestamp = datetime.strptime(fullDate + ' ' + time, '%d.%m.%Y %H:%M')
    content = str(container.find_all('div', id = "contents"))
    content = script_cleaner(str(content))

    return {
        'content': content,
        'content_hash': md5(content.encode('utf-8')),
        'content_image':  container.find('img')['src'],
        'content_timestamp': timestamp,
        'content_impression': container.find('i', class_='fa fa-eye').next_sibling

    }
    
def convert_month_to_number(month):
        aylar = {
            'Yanvar': 1,
            'Fevral': 2,
            'Mart': 3,
            'Aprel': 4,
            'May': 5,
            'İyun': 6,
            'İyul': 7,
            'Avqust': 8,
            'Sentyabr': 9,
            'Oktyabr': 10,
            'Noyabr': 11,
            'Dekabr': 12
        }

        return aylar[month]

def script_cleaner(content):
    while content.find("<script") != -1:
        content = content[:content.find("<script")] + content[content.find("</script>") + 9:]
    return content


def md5(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()


items = crawl_orduaz('https://ordu.az/ru/cats/2')
whole_news = crawl_orduaz('https://ordu.az/ru/cats/2')




















