import urllib.request
import hashlib
import httplib2
import ssl
import os
import webbrowser
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime


def crawl_azeaz(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    items = bs.find('div', class_="td-main-content-wrap").find_all('div', class_="td_module_1")

    whole_news = []
    for item in items:
        news = {
            'title': item.find('h3', class_='entry-title td-module-title').getText(),
            'image': item.find('img')['src'],
            'link': item.find('a')['href']
        }
        news.update(get_news_details(news['link']))
        whole_news.append(news)
       
    return whole_news

def get_news_details(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read().decode('utf-8')
    bs = BeautifulSoup(html, 'html.parser')
    container = bs.find('article', class_="post")
    full_date = container.find('div', class_="td-module-meta-info").getText()
    l = full_date.split()
    date = l[1]
    ay = l[2]
    month = convert_month_to_number(ay)
    year = l[3]
    year = year.replace(',','')
    time = l[4]
    fullDate = date + '.' + str(month) + '.' + year
    timestamp = datetime.strptime(fullDate + ' ' + time, '%d.%m.%Y %H:%M')
    content = str(container.find('div', class_='td-post-content').find_all('p'))
    content = script_cleaner(str(content))

    return {
        'content': content,
        'content_hash': md5(content.encode('utf-8')),
        'content_image': container.find('img')['src'],
        'content_timestamp': timestamp,


    }

def convert_month_to_number(month):
        aylar = {
            'Январь': 1,
            'Февраль': 2,
            'Mарт': 3,
            'Aпрель': 4,
            'Mай': 5,
            'Июнь': 6,
            'Июль': 7,
            'Август': 8,
            'Cентябрь': 9,
            'Oктябрь': 10,
            'Hоябрь': 11,
            'Декабрь': 12
        }

        return aylar[month]
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

#     file.write("<img src='{}'/><br/>".format(img))
#     file.write(news['content'])
#     file.write('</body></html>')
#     file.close()
#     chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
#     webbrowser.get(chrome_path).open('file://{}/{}'.format(os.getcwd(), file_name))

def script_cleaner(content):
    while content.find("<script") != -1:
        content = content[:content.find("<script")] + content[content.find("</script>") + 9:]
    return content

def md5(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()


items = crawl_azeaz('https://aze.az/category/politics')
whole_news = crawl_azeaz('https://aze.az/category/politics')
# for item in items:
#     write_file(item)



















