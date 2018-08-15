import urllib.request
import hashlib
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def get_headlines_from_demokrat(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find('ul',  id="sliderPager").find_all('li')
    parsed_links = []

    for link in links:
        data = link.find('a')['href'].strip()
        parsed_links.append( 'http://demokrat.az/' + data )

    return parsed_links

links = get_headlines_from_demokrat("http://demokrat.az/")
parsed_links = get_headlines_from_demokrat("http://demokrat.az/")


