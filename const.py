#BASEURL = 'www.busfan.us'
#BASEURL = 'www.busfan.cloud'
BASEURL = 'www.busfan.pw'
BASEHTTPS = 'https://' + BASEURL
DB_NAME = 'CRAW_DATA'
RASP_URL = 'http://192.168.16.223:8000'


class CodeIndex(object):
    url = 0
    code = 1
    date = 2
    duration = 3
    director = 4
    name = 7
    actor = 8
    magnet = 10
    state = 12
    save_path = 13


class CodeState (object):
    none = 0
    normal = 1
    love = 2
    hate = 3


class AdaptorType(object):
    love = 1
    hate = 2
    dir = 3
    search = 4


class ErrCode(object):
    success = 0
    internalError = 1
