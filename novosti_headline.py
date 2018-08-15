import urllib.request
import hashlib
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def get_headlines_from_novosti(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find('div',  class_="row top-news").find_all('div', class_='col-md-3')
    links2 = bs.find('ul', class_="slide-wrapper").find_all('li', class_='slide')
    parsed_links = []

    for link in links:
        data = link.find('a')['href'].strip()


        parsed_links.append( data )
    for link2 in links2:
        data2 = link2.find('a')['href'].strip()
        parsed_links.append(data2)

    return parsed_links

links = get_headlines_from_novosti("http://novosti.az/")
parsed_links = get_headlines_from_novosti("http://novosti.az/")


