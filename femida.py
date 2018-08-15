import urllib.request
import hashlib
import httplib2
import ssl
import os
import webbrowser
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime


def crawl_teleqraf(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    items = bs.find('div', class_="row cats-list").find_all('div', class_='card')



    whole_news = []
    for item in items:
        news = {
            'title': item.find('h4', class_="card-title").getText().strip(),
            'image': item.find('img', class_='card-img-top')['src'].replace('/resizer.php?src=',''),
            'link': item.find('a')['href'].strip()
        }


        news.update(get_news_details(news['link']))
        whole_news.append(news)

    return whole_news


def get_news_details(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    container = bs.find('div',class_='news-more')


    full_date = container.find('i', class_="fa fa-clock-o").next_sibling
    l = full_date.split()

    date = l[1]
    ay = l[2]
    month = convert_month_to_number(ay)
    year = l[3]
    time = l[0]
    fullDate = date + '.' + str(month) + '.' + year
    timestamp = datetime.strptime(fullDate + ' ' + time, '%d.%m.%Y %H:%M')

    content = str(container.find('h3', class_ = "lead").getText()) + str(container.find('p', class_='body'))
    content = script_cleaner(str(content))

    return {
        'content': content,
        'content_hash': md5(content.encode('utf-8')),
        'content_image':  container.find('img')['src'],
        'content_timestamp': timestamp,
        'content_impression': container.find('p', class_='view').getText().replace('Oxunub:','')

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


items = crawl_teleqraf('http://femida.az/az/cats/3')
whole_news = crawl_teleqraf('http://femida.az/az/cats/3')
# for item in items:
#     write_file(item)





















