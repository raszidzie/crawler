import urllib.request
import hashlib
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def get_headlines_from_haqqinaz(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    links = bs.find('ul', class_="list-unstyled news").find_all('li', class_='with-img')
    link_gorunen = bs.find('article', class_="news-of-the-day").find('a')['href']


    parsed_links = []
    parsed_links.append(link_gorunen)
    for link in links:
        data = link.find('a')['href'].strip()

        parsed_links.append( data )

    return parsed_links

links = get_headlines_from_haqqinaz("https://haqqin.az/")
parsed_links = get_headlines_from_haqqinaz("https://haqqin.az/")

