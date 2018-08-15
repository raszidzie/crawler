import urllib.request
import hashlib
import httplib2
import ssl
import os
import webbrowser
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime


def crawl_demokrat(url):

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    items = bs.find('div', class_='leftBlock').find_all('div', class_="col-3")
    whole_news = []
    for item in items:
        news = {
            'title': item.find('h2').getText().strip(),
            'image':  item.find('img')['src'],
            'link': 'http://demokrat.az/' + item.find('a')['href']
        }
        news.update(get_news_details(news['link']))
        whole_news.append(news)
       
    return whole_news


def get_news_details(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read().decode('utf-8')
    bs = BeautifulSoup(html, 'html.parser')
    container = bs.find('div', class_="leftBlock")
    full_date = bs.find('i', class_="far fa-clock").next_sibling
    l = full_date.split()
    date = l[0]
    month = l[1]
    ay = convert_month_to_number(month)
    year = l[2]
    year = year.replace(',','')
    fullDate = date + '.' + '0' + str(ay) + '.' + year
    time = l[3]
    timestamp = datetime.strptime(fullDate + ' ' + time, '%d.%m.%Y %H:%M')
    content = str(bs.find('span', id = "font").find_all('p'))
    content = script_cleaner(str(content))

    return {
        'content': content,
        'content_hash': md5(content.encode('utf-8')),
        'content_timestamp': timestamp,
        'content_image':bs.find('img', class_='nImg')['src'],
        'content_impression': bs.find('div', {'style':"color:#336699; font-size:14px; font-weight:bold; text-align:left; margin:10px 0px 5px 0px;"}).getText().replace('Oxunma sayı:','').replace('dəfə','')

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


items = crawl_demokrat('http://demokrat.az/category/1/')
whole_news = crawl_demokrat('http://demokrat.az/category/1/')
# for item in items:
#     write_file(item)



















