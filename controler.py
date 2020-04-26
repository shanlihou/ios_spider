#!/usr/bin/env python
#-*-coding:utf-8-*-

import sqlite3
import const
import os
import utils


KEY_LIST = ('URL', 'code', 'date', 'length', 'director', 'maker',
            'publish', 'series', 'actor', 'type', 'magnet', 'uncensored', 'state', 'save_path')


def _decode_utf8(aStr):
    return aStr.encode('utf-8', 'ignore').decode('utf-8')


def create_db(dbname='crawler.sqlite3.db'):
    '''create a db and table if not exists'''
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JAVBUS_DATA(
            URL       TEXT PRIMARY KEY,
            code   TEXT,
            date TEXT,
            length      TEXT,
            director     TEXT,
            maker    TEXT,
            publish   TEXT,
            series     TEXT,
            actor     TEXT,
            type     TEXT,
            magnet TEXT,
            uncensored     INTEGER,
            state INTEGER,
            save_path TEXT);''')

    print("Table created successfully")
    cursor.close()
    conn.commit()
    conn.close()


def get_write_str():
    sql_str = '''
    INSERT INTO JAVBUS_DATA (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    return sql_str


def write_data(dict_jav, uncensored, save_path, state=const.CodeState.normal):
    '''write_data(dict_jav, uncensored)'''

    conn = sqlite3.connect("crawler.sqlite3.db")
    cursor = conn.cursor()
    insert_data = list(
        map(_decode_utf8, (dict_jav[key] for key in KEY_LIST[:-3])))
    insert_data.append(uncensored)
    insert_data.append(state)
    insert_data.append(save_path)
    sql_str = get_write_str()
    sql_str = sql_str % KEY_LIST
    cursor.execute(sql_str, insert_data)
    cursor.close()
    conn.commit()
    conn.close()


def check_url_not_in_table(url):
    """check_url_in_db(url),if the url isn't in the table it will return True, otherwise return False"""

    conn = sqlite3.connect("crawler.sqlite3.db")
    cursor = conn.cursor()
    if type(url) is not str:
        url = url.decode('utf-8')
    cursor.execute('select URL from JAVBUS_DATA where URL=?', (url,))
    check = cursor.fetchall()
    cursor.close()
    conn.close()
    if check:
        return False
    return True


def change_state_by_code(code, state):
    conn = sqlite3.connect("crawler.sqlite3.db")
    cursor = conn.cursor()
    sql_str = "update JAVBUS_DATA set state = {} where code = '{}'".format(
        state, code)
    cursor.execute(sql_str)
    conn.commit()
    cursor.close()
    conn.close()


def get_data():
    conn = sqlite3.connect("crawler.sqlite3.db")
    cursor = conn.cursor()
    c = cursor.execute('select * from JAVBUS_DATA')
    for row in c:
        print(row)
    cursor.close()
    conn.close()


def get_data_by_code(code):
    conn = sqlite3.connect("crawler.sqlite3.db")
    cursor = conn.cursor()
    c = cursor.execute(
        'select * from JAVBUS_DATA where code = "{}"'.format(code))
    ret = None
    for row in c:
        ret = row
    cursor.close()
    conn.close()
    return ret


def get_state_by_code(code):
    conn = sqlite3.connect("crawler.sqlite3.db")
    cursor = conn.cursor()
    c = cursor.execute(
        'select state from JAVBUS_DATA where code = "{}"'.format(code))
    ret = None
    for row in c:
        ret = row
    cursor.close()
    conn.close()
    return ret[0] if ret else 0


def get_paths_by_state(state):
    conn = sqlite3.connect("crawler.sqlite3.db")
    cursor = conn.cursor()
    c = cursor.execute(
        'select save_path from JAVBUS_DATA where state = "{}"'.format(state))
    ret_list = []
    for row in c:
        ret_list.append(utils.fix_path(row[0]))
    cursor.close()
    conn.close()
    return ret_list


def search_data(search_str):
    search_str = search_str.lower()
    conn = sqlite3.connect("crawler.sqlite3.db")
    cursor = conn.cursor()
    c = cursor.execute('select * from JAVBUS_DATA')
    ret_list = []
    for row in c:
        if search_str in row[const.CodeIndex.code].lower():
            ret_list.append(utils.fix_path(row[const.CodeIndex.save_path]))
    cursor.close()
    conn.close()
    return ret_list


def get_code_path(code):
    for dir in os.listdir('data'):
        dirname = os.path.join('data', dir)
        if not os.path.isdir(dirname):
            continue

        for filename in os.listdir(dirname):
            path = os.path.join(dirname, filename)
            if filename.split('.')[0] == code:
                return path

    return ''


def old_to_new():
    create_db('crawler2.sqlite3.db')
    conn = sqlite3.connect("crawler.sqlite3.db")
    cursor = conn.cursor()
    c = cursor.execute('select * from JAVBUS_DATA')
    row_list = []
    for row in c:
        row_list.append(row)
    cursor.close()
    conn.close()

    conn = sqlite3.connect("crawler2.sqlite3.db")
    cursor = conn.cursor()
    for row in row_list:

        insert_data = list(row)
        insert_data[-1] = get_code_path(row[const.CodeIndex.code])
        sql_str = get_write_str()
        sql_str = sql_str % KEY_LIST
        cursor.execute(sql_str, insert_data)
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # ret = check_url_not_in_table('https://www.cdnbus.one/SSNI-754')
    # print(ret)
    # old_to_new()
    #ret = search_data('hodv')
    #print(ret)
    get_data()
    # url = ''.join((const.BASEHTTPS, '/KOSATSU104'))
    # ret = check_url_not_in_table(url)
    # print(ret)
