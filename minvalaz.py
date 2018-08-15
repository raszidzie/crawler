import urllib.request
import hashlib
import httplib2
import ssl
import os
import webbrowser
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime


def crawl_minvalaz(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    items = bs.find('div', id = 'content').find_all('div', class_="post-single")
    whole_news = []
    for item in items:
        news = {
            'title': item.find('h3').find('a').getText(),
            'image': item.find('img')['src'],
            'link': item.find('a')['href']
        }

        news.update(get_news_details(news['link']))
        whole_news.append(news)
        print(news)

    return whole_news

def get_news_details(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read().decode('utf-8')
    bs = BeautifulSoup(html, 'html.parser')
    container = bs.find('div', id="content")
    full_date = container.find('div', id="article-details").find('p').getText()
    l = full_date.split()
    date = l[1]
    time = l[2]
    timestamp = datetime.strptime(date + ' ' + time, '%Y/%m/%d %H:%M')
    impression =  container.find('div', class_='article_hits').find_all('p')[1]
    view = impression.text
    content = str(container.find('div', class_='post-content').find_all('p'))
    content = script_cleaner(str(content))

    return {
        'content': content,
        'content_hash': md5(content.encode('utf-8')),
        'content_image': container.find('img')['src'],
        'content_timestamp': timestamp,
        'content_impression': view

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


items = crawl_minvalaz('https://minval.az/r/ekonomika')
whole_news = crawl_minvalaz('https://minval.az/r/ekonomika')
# for item in items:
#     write_file(item)



















