#!/usr/bin/env python
#-*-coding:utf-8-*-

import controler
import downloader
import pageparser
import time
import const
import config


def get_dict(url):
    """get the dict of the detail page and yield the dict"""

    url_html = downloader.get_html(url)
    for detail_url in pageparser.parser_homeurl(url_html):
        if not controler.check_url_not_in_table(detail_url):
            print('has down:', detail_url)
            continue

        try:
            detail_page_html = downloader.get_html(detail_url)
            dict_jav = pageparser.parser_content(detail_page_html)
        except Exception as e:
            with open('fail_url.txt', 'a') as fd:
                fd.write('%s\n' % detail_url)

            print(e, e is KeyboardInterrupt)
            import traceback
            traceback.print_exc()
            print("Fail to crawl %s\ncrawl next detail page......" % detail_url)
            continue
        
        dict_jav['URL'] = detail_url
        yield dict_jav, detail_url


def join_db(url, is_uncensored):
    """the detail_dict of the url join the db"""

    for dict_jav_data, detail_url in get_dict(url):
        if not controler.check_url_not_in_table(dict_jav_data['URL']):
            print('has down:', dict_jav_data['URL'])
            continue
            
        try:
            downloader.down_jpg(dict_jav_data)
        except OSError as e:
            print('down jpg os:', e)
            continue
            
        controler.write_data(dict_jav_data, is_uncensored)
        print("Crawled %s" % detail_url)
        


def main(entrance):
    # 鍒涘缓鏁版嵁琛�
    controler.create_db()
    # 鏃犵爜涓�1锛屾湁鐮佷负0
    is_uncensored = 1 if 'uncensored' in entrance else 0
    config.mcIns.set_config('is_u', is_uncensored)
    join_db(entrance, is_uncensored)

    entrance_html = downloader.get_html(entrance)
    next_page_url = pageparser.get_next_page_url(entrance, entrance_html)
    while True:
        if next_page_url:
            join_db(next_page_url, is_uncensored)
        next_page_html = downloader.get_html(next_page_url)
        next_page_url = pageparser.get_next_page_url(entrance, next_page_html)
        if next_page_url is None:
            break


if __name__ == '__main__':
    op = 0
    if op == 0:
        #main(const.BASEHTTPS)
        main(''.join((const.BASEHTTPS, '/uncensored')))
    elif op == 1:
        url = ''.join((const.BASEHTTPS, '/uncensored'))
        # print(url)
#         url_html = downloader.get_html(url)
#         with open('home.html', 'wb') as fw:
#             print('will write')
#             fw.write(url_html)
        with open('home.html', 'rb') as fr:
            url_html = fr.read()
            ret = pageparser.parser_homeurl(url_html)
            for i in ret:
                print(controler.check_url_not_in_table(i))
        print(2)
