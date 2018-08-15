import urllib.request
import hashlib
import httplib2
import ssl
import os
import webbrowser
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime


def crawl_haqqinaz(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    items = bs.find('ul', class_="list-unstyled news").find_all('li', class_="with-img")



    whole_news = []
    for item in items:
        news = {
            'title': item.find('h4').getText(),
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
    container = bs.find('main', class_="view-view")
    full_date = container.find('time', class_='time')['datetime']
    l = full_date.split()
    date = l[0]
    time = l[1]
    timestamp = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

    content = str(container.find('div', class_='article-block').find('strong')) + str(container.find('div', class_='article-block').find_all('p'))
    content = script_cleaner(str(content))


    return {
        'content': content,
        'content_hash': md5(content.encode('utf-8')),
        'content_image': container.find('img')['src'],
        'content_timestamp': timestamp,
        'content_impression': container.find('span', class_="watches_count").getText()

    }
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


items = crawl_haqqinaz('https://haqqin.az/oldage')
whole_news = crawl_haqqinaz('https://haqqin.az/oldage')
# for item in items:
#     write_file(item)



















