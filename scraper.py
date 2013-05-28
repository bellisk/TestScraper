import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from urllib import quote_plus
from pprint import PrettyPrinter

def get_soup(base_url, relative_url=''):
    url = urljoin(base_url, relative_url)
    url_path = 'tmp/' + quote_plus(url)
    try:
        with open(url_path) as f:
            return BeautifulSoup(f.read().decode('utf-8'))
    except:
        pass
    print url
    r = requests.get(url, timeout=3)
    if r.status_code == 200:
        with open(url_path, 'w') as f:
            f.write(r.text.encode('utf-8'))
        return BeautifulSoup(r.text)
    return None

s = get_soup('http://lowendmac.com/profiles.htm')

categories = [h4.a['href'] for h4 in s.find_all('h4') if h4.a]
categories = categories[0:2]

def is_mac_link(href):
    return not href.startswith('http://') or href.startswith('http://lowendmac.com')

mac_links = set([a['href'] for cat in categories for a in get_soup('http://lowendmac.com/profiles.htm', cat).find_all('a') if 'href' in a.attrs and is_mac_link(a['href'])])

extractors = []

def is_mac(soup):
    return 'RAM:' in soup.get_text()

def e_name(soup, mac):
    mac['name'] = soup.title.string.split('|')[0].strip()

extractors.append(e_name)

def e_li_colon(soup, mac):
    for li in soup.find_all('li'):
        if ':' in li.get_text():
            mac[li.get_text().split(':')[0].strip()] = li.get_text().split(':', 1)[1].strip()

extractors.append(e_li_colon)

macs = []

for mac_link in mac_links:
    soup = get_soup('http://lowendmac.com/profiles.htm', mac_link)
    if not soup or not is_mac(soup):
        continue
    mac = {}
    macs.append(mac)
    for e in extractors:
        e(soup, mac)
    
PrettyPrinter().pprint(macs)
