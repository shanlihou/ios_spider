# coding= utf-8
import requests
from bs4 import BeautifulSoup
import urllib
import re
import sys
import gzip
#URIBASE = 'btsow.casa'
URIBASE = 'btsow.website'
HEADERS = {'Host': URIBASE, 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3053.3 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, sdch, br', 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}


def save_file(data):
    with open('one.html', 'w', encoding='utf-8') as fw:
        fw.write(data)


def get_save(fn=None):
    if not fn:
        fn = 'test.html'
    with open(fn, 'r', encoding='utf-8') as fr:
        return fr.read()


def get_content(urlPath, is_save=False):
    ret = requests.get(urlPath, headers=HEADERS)
    html = ret.text
    if is_save:
        save_file(html)
    return html


class BtOne(object):
    def __init__(self, url, size, name):
        # content = get_content(url, True)
#         content = get_save('one.html')
        self.url = url
        #self.mag = self.parse_mag(content)
        self.size = size
        self.name = name

    def __str__(self):
        return '{},{}'.format(self.mag, self.size)

    @staticmethod
    def parse_mag(content):
        pat = re.compile(r'(magnet:\?xt=urn:btih:[^"><]+)["<>]')
        ret = pat.findall(content)
        return ret[0]


def rec_content(content):
    rets = []
    for inner in content.contents:
        if hasattr(inner, 'contents'):
            rets.append(rec_content(inner))
        else:
            rets.append(inner)

    return ''.join(rets)


def parse_content(content):
    soup = BeautifulSoup(content, "html.parser")
    div = soup.select('div[class="data-list"]')
    for _div in div:
        for ret in _div.select('div[class="row"]'):
            a = ret.select('a')[0]
            name = a.select('div')[0]
            name = rec_content(name)
            size = a.find_next_siblings('div')[0].string
            url = a['href']
            hash_code = url.split('/')[-1]
            mag = 'magnet:?xt=urn:btih:{}'.format(hash_code)
            yield BtOne(mag, size, name)
#     for url in ret:
#         #bo = BtOne(url)

def get_mag_by_hash(hash_code):
    url = 'https://{}/magnet/detail/hash/{}'.format(URIBASE, hash_code)
    content = get_content(url, True)
    return BtOne.parse_mag(content)


def getAllMagnet(code):
    # code=urllib.quote_plus(code)
    print(code)
    code = urllib.parse.quote(code)
    url = 'https://{}/search/{}'.format(URIBASE, code)
    content = get_content(url, True)
    for bo in parse_content(content):
        yield bo.url, bo.size, bo.name


if __name__ == '__main__':
    #for a in parse_content(get_save('one.html')):
    #    print(a.url)
    mag = get_mag_by_hash('D71277C8188FF54F11B3D795BCE1B3736A499EE9')
    print(mag)
    #     bo = BtOne(1)
    #for a, b, c in getAllMagnet('复仇者'):
    #    print(a, b, c)
#     if (len(sys.argv) == 2):
#         getAllMagnet(sys.argv[1])
