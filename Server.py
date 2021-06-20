import cgi
import urllib
import sys
import threading
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from Adb_Handler import Adb_Handler as AdbHandler

class Server(BaseHTTPRequestHandler):
    key = ''
    deviceId = ''
    adbHandler = AdbHandler

    def start(self, host, port, key, deviceId):
        self.key = key
        self.deviceId = deviceId
        print('Starting server...')
        server_address = (host, port)
        self.httpd = HTTPServer(server_address, Server)
        # if using https
        # httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='', keyfile='', ssl_version=ssl.PROTOCOL_TLS)
        thread = threading.Thread(target = self.httpd.serve_forever)
        thread.daemon = True
        thread.start()        
        print('Server started on: ' + host + ':' + str(port))

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        print('Server stopped')

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers() 

        ctype, pdict = cgi.parse_header(self.headers['content-type'])

        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postVars = urllib.parse.parse_qs(self.rfile.read(length))
        else:
            postVars = {}

        message = ''

        if bytes('key', 'utf8') in postVars:
            try:
                key = postVars[bytes('key', 'utf8')][0].decode('utf-8')
                msg = postVars[bytes('msg', 'utf8')][0].decode('utf-8')
                rec = postVars[bytes('rec', 'utf8')][0].decode('utf-8')
            except:
                message = '{ "status":"error_decoding_params" }'         
        else:
            message = '{ "status":"no_auth" }'

        if len(message) > 0:
            self.wfile.write(bytes(message, 'utf8'))
            return

        if key == self.key:
            if len(msg) == 0:
                message = '{ "status":"EMPTY_MESSAGE" }'
            elif len(msg) > 160:
                message = '{ "status":"MESSAGE_EXCEEDS_160_CHAR_LIMIT" }'
            else:
                if (self.adbHandler.sendSms(AdbHandler, self.deviceId, rec, msg)):
                    message = '{ "status":"REQUEST_PROCESSED" }'
                else:
                    message = '{ "status":"ERROR_PROCESSING_REQUEST" }'
        else:
            message = '{ "status":"WRONG_AUTH" }'

        self.wfile.write(bytes(message, 'utf8'))