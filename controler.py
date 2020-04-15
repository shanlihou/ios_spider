#!/usr/bin/env python
#-*-coding:utf-8-*-

import sqlite3
import const


# 用来处理用Python的sqlite3操作数据库要插入的字符串中含有中文字符的时候报错处理，配合map
def _decode_utf8(aStr):
    return aStr.encode('utf-8', 'ignore').decode('utf-8')


def create_db(dbname='javbus.sqlite3.db'):
    '''create a db and table if not exists'''
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JAVBUS_DATA(
            URL       TEXT PRIMARY KEY,
            識別碼    TEXT,
            發行日期  TEXT,
            長度      TEXT,
            導演      TEXT,
            製作商    TEXT,
            發行商    TEXT,
            系列      TEXT,
            演員      TEXT,
            類別      TEXT,
            磁力链接  TEXT,
            无码      INTEGER,
    state INTEGER);''')

    print("Table created successfully")
    cursor.close()
    conn.commit()
    conn.close()


def write_data(dict_jav, uncensored, state=CodeState.normal):
    '''write_data(dict_jav, uncensored)'''

    conn = sqlite3.connect("javbus.sqlite3.db")
    cursor = conn.cursor()
    # 对数据解码为unicode
    insert_data = list(map(_decode_utf8, (dict_jav['URL'], dict_jav['識別碼'], dict_jav['發行日期'], dict_jav['長度'], dict_jav['導演'],
                                          dict_jav['製作商'], dict_jav['發行商'], dict_jav['系列'], dict_jav['演員'], dict_jav['類別'], dict_jav['磁力链接'])))
    insert_data.append(uncensored)
    insert_data.append(state)
    # 插入数据
    cursor.execute('''
    INSERT INTO JAVBUS_DATA (URL, 識別碼, 發行日期, 長度, 導演, 製作商, 發行商, 系列, 演員, 類別, 磁力链接, 无码, state)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', insert_data)
    cursor.close()
    conn.commit()
    conn.close()


def check_url_not_in_table(url):
    """check_url_in_db(url),if the url isn't in the table it will return True, otherwise return False"""

    conn = sqlite3.connect("javbus.sqlite3.db")
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


def get_data():
    conn = sqlite3.connect("javbus.sqlite3.db")
    cursor = conn.cursor()
    c = cursor.execute('select * from JAVBUS_DATA')
    for row in c:
        pass
    cursor.close()
    conn.close()


def get_data_by_code(code):
    conn = sqlite3.connect("javbus.sqlite3.db")
    cursor = conn.cursor()
    c = cursor.execute(
        'select * from JAVBUS_DATA where 識別碼 = "{}"'.format(code))
    ret = None
    for row in c:
        ret = row
    cursor.close()
    conn.close()
    return ret


def old_to_new():
    create_db('javbus2.sqlite3.db')
    conn = sqlite3.connect("javbus.sqlite3.db")
    cursor = conn.cursor()
    c = cursor.execute('select * from JAVBUS_DATA')
    row_list = []
    for row in c:
        row_list.append(row)
    cursor.close()
    conn.close()

    conn = sqlite3.connect("javbus2.sqlite3.db")
    cursor = conn.cursor()
    # 对数据解码为unicode
    for row in row_list:

        insert_data = list(row)
        insert_data.append(CodeState.normal)
        # 插入数据
        cursor.execute('''
        INSERT INTO JAVBUS_DATA (URL, 識別碼, 發行日期, 長度, 導演, 製作商, 發行商, 系列, 演員, 類別, 磁力链接, 无码, state)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', insert_data)
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # ret = check_url_not_in_table('https://www.cdnbus.one/SSNI-754')
    # print(ret)
    # old_to_new()
    #get_data()
    url = ''.join((const.BASEHTTPS, '/KOSATSU104'))
    ret = check_url_not_in_table(url)
    print(ret)
