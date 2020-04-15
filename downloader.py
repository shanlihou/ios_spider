#!/usr/bin/env python
#-*-coding:utf-8-*-

import requests
import os
import config

headers = {
    'User-Agent	': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
}


def get_html(url, Referer_url=None):
    '''get_html(url),download and return html'''
    if Referer_url:
        headers['Referer'] = Referer_url
    # print(url)
    req = requests.get(url, headers=headers)
    return req.content


def get_page_name(page):
    format_str = 'jpg_data_u_{}' if config.mcIns.get_config('is_u') else 'jpg_data_{}'
    return format_str.format(page)


def get_page_dir():
    save_page = config.mcIns.get_config('save_page', 1)
    page_name = get_page_name(save_page)
    if not os.path.exists(page_name):
        return page_name
        
    page_count = len(os.listdir(page_name))
    if page_count >= 100:
        return get_page_name(save_page + 1)
    else:
        return page_name


def get_page(page_name):
    page = page_name.split('_')[-1]
    return int(page)


def down_jpg(dic):
    code = dic['識別碼']
    url = dic['jpg_src']
    page_name = get_page_dir()
    try:
        os.mkdir(page_name)
        config.mcIns.set_config('save_page', get_page(page_name))
        config.mcIns.set_config('max_page', max(get_page(page_name),
                                                config.mcIns.get_config('max_page', 1)))
    except Exception as e:
        pass
    pic_name = os.path.join(page_name, code + '.jpg')
    if os.path.exists(pic_name):
        print('exist:', pic_name)
        return

    content = get_html(url)
    with open(pic_name, 'wb') as fw:
        fw.write(content)


if __name__ == '__main__':
    op = 0
    if op == 0:
        ret = get_html('https://www.cdnbus.one/prtd-026')
        print(ret)
        with open('example.html', 'wb') as fw:
            fw.write(ret)
    elif op == 1:
        url = 'https://pics.javcdn.pw/cover/7lld_b.jpg'
        ret = get_html(url)
        with open('test.jpg', 'wb') as fw:
            fw.write(ret)
    elif op == 2:
        print(get_page_dir())
