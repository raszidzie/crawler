import urllib.request
import hashlib
import ssl
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime


def crawl_ann(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    items = bs.find('section', class_='contentlist').find_all('li')


    whole_news = []
    for item in items:
        news = {
            'title': item.find('h1').getText(),
            'image': item.find('div', class_= 'contentimage')['style'].replace('background-image: url',''),
            'link': item.find('a')['href']
        }

        news.update(get_news_details(news['link']))

        whole_news.append(news)

    return whole_news


def get_news_details(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    container = bs.find('div', class_= 'contentm')


    full_date = container.find('div', class_= 'monthl').getText() + ' ' + container.find('div', class_='yearl').getText()
    l = full_date.split()

    date = l[0]
    ay = l[1]
    month = convert_month_to_number(ay)
    year = l[2]
    time = container.find('div', class_='hoursl').getText()
    fullDate = date + '.' + str(month) + '.' + year

    timestamp = datetime.strptime(fullDate + ' ' + time, '%d.%m.%Y %H:%M')

    container.find('div', id='reklamdesktop').decompose()
    container.find('ins').decompose()
    container.find('div', class_='reklamiki').decompose()
    container.find('div',  class_="reklambir").decompose()
    container.find('div', class_='ffpage').decompose()

    content = str(container.find('div', class_='contentstory').find_all('div'))

    content = script_cleaner(str(content))

    return {
        'content': content,
        'content_hash': md5(content.encode('utf-8')),
        'content_image': 'http:' + container.find('img')['src'],
        'content_timestamp': timestamp,
        'content_impression': container.find('div', class_='infopanelic').find('span').getText()
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


items = crawl_ann('http://ann.az/az/politika/')
whole_news = crawl_ann('http://ann.az/az/politika/')
print(len(items))
print(whole_news)




















