
import urllib.request
import hashlib
import httplib2
import ssl
import os
import webbrowser
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def crawl_day_az(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    items = bs.find('div', class_="col-lg-9 col-day-fixed-left").find_all('article',  class_="col-lg-4 col-md-4 col-sm-4 col-xs-4")[0:20]

    whole_news = []
    for item in items:
        news = {
            'title': item.find('h2', class_="caption").getText(),
            'image': item.find('img')['src'],
            'link': item.find('a')['href']
        }

        news.update(get_news_details(news['link']))
        whole_news.append(news)
        print(news)

    return whole_news


def get_news_details(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    container = bs.find('article',class_="article col-lg-12 col-md-12")
    full_date = container.find('span',  class_="date").getText()
    l = full_date.split()
    date = l[0]
    ay = l[1]
    month = convert_month_to_number(ay)
    year = l[2]
    time = l[3]
    fullDate = date + '.' + '0' + str(month) + '.' + year
    timestamp = datetime.strptime(fullDate + ' ' + time, '%d.%m.%Y %H:%M')
    content = str(container.find('div', class_="description").find_all('p'))
    content = script_cleaner(str(content))

    return {
        'content': content,
        'content_hash': md5(content.encode('utf-8')),
        'content_image':  container.find('img')['src'],
        'content_timestamp': timestamp,
        'content_Impression': container.find('span', class_="likes pull-right").getText()
    }

def convert_month_to_number(month):
        aylar = {
            'января': 1,
            'февраля': 2,
            'марта': 3,
            'апреля': 4,
            'мая': 5,
            'июня': 6,
            'июля': 7,
            'августа': 8,
            'сентября': 9,
            'октября': 10,
            'ноября': 11,
            'декабря': 12
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

# def write_file(news):
#     file_name = "news-{}.html".format(news['content_hash'])
#     file = open(file_name, "w")
#     file.write('<html><head><title>{}</title></head><body>'.format(news['title']))
#     file.write("<a href='{}'>source</a><br/>".format(news['link']))
#     img = ''
#     if news.get('content_image', None) is not None:
#         img = news['content_image']
#     else:
#         img = news['image']
#
#     file.write("<img src='{}'/><br/>".format(img))
#     file.write(news['content'].encode('utf-8'))
#     file.write('</body></html>')
#     file.close()
#     chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
#     webbrowser.get(chrome_path).open('file://{}/{}'.format(os.getcwd(), file_name))


items = crawl_day_az('https://news.day.az/politics/')
whole_news = crawl_day_az('https://news.day.az/politics/')
#
# for item in items:
#     write_file(item)




