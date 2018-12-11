import http.server
import os
import pprint
import socketserver
from sys import argv
import urllib.error
import urllib.parse
import urllib.request

def create_handler(base_directory, read_len=999):
    dir = os.path.abspath(base_directory)

    class Handler(http.server.CGIHTTPRequestHandler):

        def translate_path(self, path):
            print('PATH: ' + path)
            return path

        def do_HEAD(self):
            self.send_error(ERROR_CODE, explain='do_HEAD called')

        def do_POST(self):
            self.handle_call()

        def do_GET(self):
            self.handle_call()

        def handle_call(self):
            request_url = urllib.parse.urlparse(self.path)
            path = os.path.abspath(os.path.join(dir, request_url.path[1:]))
            if os.path.isfile(path):
                if path.endswith('.cgi'):
                    modified_path = os.path.split(os.path.relpath(path, os.getcwd()))
                    self.cgi_info = modified_path[0], '{}?{}'.format(modified_path[1], request_url.query)
                    if self.cgi_info[0] == '':
                        self.cgi_info = '.',self.cgi_info[1]
                    print(self.cgi_info)
                    self.run_cgi()
                else:
                    self.get_result(path)
            else:
                self.send_error(ERROR_CODE, explain='Súbor neexistuje')

        def get_result(self, full_path):
            file_size = os.path.getsize(full_path)
            self.send_response(200)
            self.send_header('Content-Length', str(file_size))
            self.end_headers()
            file = open(full_path, 'rb')
            read = 0

            while True:
                data = file.read(read_len)
                if data is None or data == b'' or file_size == read:
                    break
                else:
                    read = read + len(data)
                    self.wfile.write(data)

    return Handler


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


def main():
    global ERROR_CODE
    ERROR_CODE = 404
    port = int(argv[1])
    path = argv[2]


    if len(argv) != 3:
        print('give me 2 args')
        return

    httpd = ThreadedHTTPServer(('', port), create_handler(path))
    httpd.serve_forever()

main()
