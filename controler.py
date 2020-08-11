#!/usr/bin/env python
#-*-coding:utf-8-*-

import sqlite3
import const
import os
import utils
import psycopg2


KEY_LIST = ('URL', 'code', 'date', 'length', 'director', 'maker',
            'publish', 'series', 'actor', 'type', 'magnet', 'uncensored', 'state', 'save_path')

GET_KEYS = ('ID', 'URL', 'code', 'date', 'length', 'director', 'maker',
            'publish', 'series', 'actor', 'type', 'magnet', 'uncensored', 'state', 'save_path')

g_conn = None
if not g_conn:
    g_conn = psycopg2.connect(
        database="rasp_main", user="postgres", password="1", host="127.0.0.1", port="5432")


def _decode_utf8(aStr):
    return aStr.encode('utf-8', 'ignore').decode('utf-8')


def create_db():
    '''create a db and table if not exists'''
    cursor = g_conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS %s(
            ID        serial NOT NULL,
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
            save_path TEXT);''' % const.DB_NAME)

    print("Table created successfully")
    cursor.close()
    g_conn.commit()


def get_write_str():
    sql_str = '''
    INSERT INTO {} (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''.format(const.DB_NAME)
    values = """
    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, '{}')
    """
    return sql_str, values


def write_data(dict_jav, uncensored, save_path, state=const.CodeState.normal):
    '''write_data(dict_jav, uncensored)'''

    cursor = g_conn.cursor()
    insert_data = list(
        map(_decode_utf8, (dict_jav[key] for key in KEY_LIST[:-3])))
    insert_data.append(uncensored)
    insert_data.append(state)
    insert_data.append(save_path)
    sql_str, values = get_write_str()
    sql_str = sql_str % KEY_LIST
    values = values.format(*insert_data)

    sql_str = ' '.join((sql_str, values))

    cursor.execute(sql_str)
    cursor.close()
    g_conn.commit()


def check_url_not_in_table(url):
    """check_url_in_db(url),if the url isn't in the table it will return True, otherwise return False"""

    cursor = g_conn.cursor()
    if type(url) is not str:
        url = url.decode('utf-8')
    cursor.execute(
        "select URL from {} where URL='{}'".format(const.DB_NAME, url))
    check = cursor.fetchall()
    cursor.close()
    if check:
        return False
    return True


def change_state_by_code(code, state):
    cursor = g_conn.cursor()
    sql_str = "update JAVBUS_DATA set state = {} where code = '{}'".format(
        state, code)
    cursor.execute(sql_str)
    g_conn.commit()
    cursor.close()


def wrap_row(row):
    return {key: row[index] for index, key in enumerate(GET_KEYS)}


def get_data_by_id(ID):
    cursor = g_conn.cursor()
    keys = ','.join(GET_KEYS)
    cursor.execute('select {} from {} where ID = {}'.format(
        keys, const.DB_NAME, ID))
    ret = None
    for row in cursor:
        ret = row
    cursor.close()
    return wrap_row(row)


def get_data_by_code(code):
    cursor = g_conn.cursor()
    c = cursor.execute(
        'select * from JAVBUS_DATA where code = "{}"'.format(code))
    ret = None
    for row in c:
        ret = row
    cursor.close()
    return ret


def get_state_by_code(code):
    cursor = g_conn.cursor()
    c = cursor.execute(
        'select state from JAVBUS_DATA where code = "{}"'.format(code))
    ret = None
    for row in c:
        ret = row
    cursor.close()
    return ret[0] if ret else 0


def get_paths_by_state(state):
    cursor = g_conn.cursor()
    c = cursor.execute(
        'select save_path from JAVBUS_DATA where state = "{}"'.format(state))
    ret_list = []
    for row in c:
        ret_list.append(utils.fix_path(row[0]))
    cursor.close()
    return ret_list


def search_data(search_str):
    search_str = search_str.lower()
    cursor = g_conn.cursor()
    c = cursor.execute('select * from JAVBUS_DATA')
    ret_list = []
    for row in c:
        if search_str in row[const.CodeIndex.code].lower():
            ret_list.append(utils.fix_path(row[const.CodeIndex.save_path]))
    cursor.close()
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
    return


if __name__ == '__main__':
    # ret = check_url_not_in_table('https://www.cdnbus.one/SSNI-754')
    # print(ret)
    # old_to_new()
    #ret = search_data('hodv')
    # print(ret)
    # get_data()
    # url = ''.join((const.BASEHTTPS, '/KOSATSU104'))
    # ret = check_url_not_in_table(url)
    # print(ret)
    get_data_by_id(1)
    pass
