BASEURL = 'www.cdnbus.one'
BASEHTTPS = 'https://' + BASEURL


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


class CodeState (object):
    none = 0
    normal = 1
    love = 2
    hate = 3


class AdaptorType(object):
    love = 1
    hate = 2
    dir = 3
