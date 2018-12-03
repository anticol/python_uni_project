import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse, error
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import json


def make_json(code, headers, content):
    data = {'code': code}

    if headers:
        header_dictionary = dict()
        for idx, val in headers:
            header_dictionary[idx] = val
        data['headers'] = header_dictionary

    if content:
        try:
            data['json'] = json.loads(content)
        except ValueError:
            data['content'] = content

    return json.dumps(data, indent=2)


def HttpHandler(url):
    class Handler(BaseHTTPRequestHandler):
        def send(self, code, json_data):
            self.send_response(code)
            self.send_header('Content-Type', "application/json; charset=UTF-8")
            length = len(json_data)
            self.send_header('Content-Length', str(length))
            self.end_headers()
            self.wfile.write(bytes(json_data, ENCODING))

        def do_GET(self):
            path = self.path
            request_url = url
            parameters = parse.urlparse(path).query
            if parameters:
                request_url += '?' + parameters
            if 'Host' not in self.headers:
                pass
            else:
                del self.headers['Host']

            self.headers['Accept-Encoding'] = 'identity'
            request = Request(request_url, None, self.headers, method=GET_METHOD)
            try:
                with urlopen(request, timeout=DEFAULT_TIMEOUT) as result:
                    self.send(OK_STATUS, make_json(result.status, result.getheaders(), result.read().decode(ENCODING)))

            except error.HTTPError as http_error:
                self.send(OK_STATUS, make_json(http_error.code, None, None))
            except:
                self.send(OK_STATUS, make_json('timeout', None, None))

        def do_POST(self):
            try:
                content_length = int(self.headers.get('Content-Length'), 0)
                json_data = self.rfile.read(content_length)
                data = json.loads(json_data)
                if data.get('url') is None or (data.get('type') is not None and data.get('type') == POST_METHOD and data.get('content') is None):
                    raise Exception("Missing parameter")
            except:
                self.send(OK_STATUS, make_json('invalid json', None, None))
                return

            try:
                request_method = GET_METHOD if data.get('type') is None else data['type']
                request_content = data['content'] if request_method == POST_METHOD else None
                json_content = json.dumps(request_content).encode(ENCODING) if request_content else None
                request_timeout =  DEFAULT_TIMEOUT if data.get('timeout') is None else data['timeout']

                request_headers = dict() if data.get('headers') is None else data['headers']
                request_headers['Accept-Encoding'] = 'identity'

                if request_headers.get('Content-Type') is None:
                    request_headers['Content-Type'] = 'application/json; charset=utf-8'
                req = Request(data['url'], json_content, request_headers, method=request_method)

                with urlopen(req, timeout=request_timeout) as result:
                    self.send(OK_STATUS, make_json(result.status, result.getheaders(), result.read().decode(ENCODING)))
            except error.HTTPError as err:
                self.send(OK_STATUS, make_json(err.code, None, None))
            except:
                return self.send(OK_STATUS, make_json('timeout', None, None))

    return Handler


def main():
    global DEFAULT_TIMEOUT, GET_METHOD, POST_METHOD, ENCODING, OK_STATUS
    GET_METHOD = 'GET'
    POST_METHOD = 'POST'
    DEFAULT_TIMEOUT = 1
    ENCODING = "UTF-8"
    OK_STATUS = 200

    if len(sys.argv) != 3:
        print('Wrong number of arguments')
        return

    port = sys.argv[1]
    upstream = sys.argv[2]
    parsed_url = urlparse(upstream)

    if parsed_url.scheme != 'http':
        if parsed_url.scheme != 'https':
            upstream = 'http://' + upstream

    server = HTTPServer(('', int(port)), HttpHandler(upstream))
    server.serve_forever()



main()
