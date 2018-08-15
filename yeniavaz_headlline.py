import urllib.request
import hashlib
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def get_headlines_from_yeniavaz(url):

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find('ul', class_='main-slider').find_all('li', class_='slide')
    parsed_links = []
    for link in links:
        data = link.find('a')['href']

        parsed_links.append('https://www.yeniavaz.com' + data)
    return parsed_links


links = get_headlines_from_yeniavaz("https://www.yeniavaz.com/")
parsed_links = get_headlines_from_yeniavaz("https://www.yeniavaz.com/")


