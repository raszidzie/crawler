import urllib.request
import hashlib
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def get_headlines_from_azerinfo(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    links = bs.find('div', class_='boyuk').find_all('div', class_='gizli')
    link_gorunen = bs.find('div', class_='boyuk').find('div', class_='gorunen').find('a')['href']


    parsed_links = []
    parsed_links.append(link_gorunen)
    for link in links:
        data = link.find('a')['href'].strip()

        parsed_links.append( data )

    return parsed_links

links = get_headlines_from_azerinfo("http://azerinfo.az/")
parsed_links = get_headlines_from_azerinfo("http://azerinfo.az/")


