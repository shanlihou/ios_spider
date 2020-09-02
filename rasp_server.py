#!/usr/bin/env python
# --coding:utf-8 --

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse
import controler
import json
import const
import magnet
import functools
import config


curdir = path.dirname(path.realpath(__file__))
sep = '/'

# MIME-TYPE
mimedic = [
    ('.html', 'text/html'),
    ('.htm', 'text/html'),
    ('.js', 'application/javascript'),
    ('.css', 'text/css'),
    ('.json', 'application/json'),
    ('.png', 'image/png'),
    ('.jpg', 'image/jpeg'),
    ('.gif', 'image/gif'),
    ('.txt', 'text/plain'),
    ('.avi', 'video/x-msvideo'),
]

@functools.lru_cache(maxsize=1024)
def get_mag_list(code):
    return [{'mag': mag, 'size': size, 'name': name} for mag, size, name in magnet.getAllMagnet(code)]

class CmdHandler(object):
    @classmethod
    def do(cls, data):
        try:
            cmd = data['cmd']
            ret = getattr(cls, cmd)(data)
            return json.dumps(ret)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'Err': const.ErrCode.internalError}

    @classmethod
    def exit_self(cls, data):
        print('will exit')
        exit(0)
        
    @classmethod
    def get_data_by_id(cls, data):
        config.mcIns.set_config('last_watch_id', data['id'])
        ret = controler.get_data_by_id(data['id'])
        return {
            'Err': const.ErrCode.success,
            'cmd': data['cmd'],
            'id': data['id'],
            'retData': ret,
        }

    @classmethod
    def get_last_watch_id(cls, data):
        last_watch_id = config.mcIns.get_config('last_watch_id')
        return {
            'Err': const.ErrCode.success,
            'cmd': data['cmd'],
            'retData': last_watch_id,
        }


    @classmethod
    def get_data_by_code(cls, data):
        data_list = get_mag_list(data['code'])
        return {
            'Err': const.ErrCode.success,
            'cmd': data['cmd'],
            'code': data['code'],
            'retData': data_list
        }



class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        querypath = urlparse(self.path)
        filepath, _ = querypath.path, querypath.query
        print(filepath, _)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('{"hello": 123}'.encode('utf-8'))

    def do_POST(self):
        print(self.headers)
        print(self.command)
        req_datas = self.rfile.read(
            int(self.headers['content-length']))  # 重点在此步!

        data = req_datas.decode()
        data = json.loads(data)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(CmdHandler.do(data)).encode('utf-8'))

    def _do_GET_(self):
        sendReply = False
        querypath = urlparse(self.path)
        filepath, _ = querypath.path, querypath.query

        if filepath.endswith('/'):
            filepath += 'index.html'
        _, fileext = path.splitext(filepath)
        for e in mimedic:
            if e[0] == fileext:
                mimetype = e[1]
                sendReply = True

        if sendReply:
            try:
                with open(path.realpath(curdir + sep + filepath), 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)


def run():
    port = 8000
    print('starting server, port', port)

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
