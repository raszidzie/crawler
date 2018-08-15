import urllib.request
import hashlib
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def get_headlines_from_orduaz(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find('div', class_='carousel-inner').find_all('div', class_="item")
    parsed_links = []
    for link in links:
        data = link.find('a')['href'].strip()

        parsed_links.append( data)

    return parsed_links

links = get_headlines_from_orduaz("https://ordu.az/")
parsed_links = get_headlines_from_orduaz("https://ordu.az/")
print(parsed_links)

