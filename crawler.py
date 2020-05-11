#!/usr/bin/env python
#-*-coding:utf-8-*-

import controler
import downloader
import pageparser
import time
import const
import config
import logging

logging.basicConfig(
                    level    = logging.INFO,              # 定义输出到文件的log级别，                                                            
                    format   = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',    # 定义输出log的格式
                    datefmt  = '%Y-%m-%d %A %H:%M:%S',                                     # 时间
                    filename = 'craw.log',                # log文件名
                    filemode = 'a+')

def get_dict(url):
    """get the dict of the detail page and yield the dict"""

    url_html = downloader.get_html(url)
    for detail_url in pageparser.parser_homeurl(url_html):
        if not controler.check_url_not_in_table(detail_url):
            logging.info('has down:{}'.format(detail_url))
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
            logging.info("Fail to crawl %s\ncrawl next detail page......" % detail_url)
            continue

        dict_jav['URL'] = detail_url
        yield dict_jav, detail_url


def join_db(url, is_uncensored):
    """the detail_dict of the url join the db"""

    for dict_jav_data, detail_url in get_dict(url):
        if not controler.check_url_not_in_table(dict_jav_data['URL']):
            logging.info('has down:', dict_jav_data['URL'])
            continue

        try:
            pic_name = downloader.down_jpg(dict_jav_data)
        except OSError as e:
            logging.info('down jpg os:', e)
            continue

        controler.write_data(dict_jav_data, is_uncensored, pic_name)
        logging.info("Crawled:{}".format(pic_name))


def main(entrance):
    controler.create_db()
    is_uncensored = 1 if 'uncensored' in entrance else 0
    config.mcIns.set_config('is_u', is_uncensored)
    join_db(entrance, is_uncensored)

    entrance_html = downloader.get_html(entrance)
    next_page_url = pageparser.get_next_page_url(entrance, entrance_html)
    while True:
        if next_page_url:
            join_db(next_page_url, is_uncensored)
        logging.info('cur url:{}'.format(next_page_url))
        next_page_html = downloader.get_html(next_page_url)
        next_page_url = pageparser.get_next_page_url(entrance, next_page_html)
        if next_page_url is None:
            logging.info('next page is none')
            break


if __name__ == '__main__':
    op = 0
    if op == 0:
        main(const.BASEHTTPS)
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
