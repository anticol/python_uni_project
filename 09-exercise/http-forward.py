import sys
import json
import asyncio
import ssl, socket
import aiohttp
from aiohttp import web

def get_info(host, port):

    context = ssl.create_default_context()
    with context.wrap_socket(socket.socket(), server_hostname=host) as s:

        try:
            s.connect((host, port))
        except ssl.CertificateError as e:
            return {'certificate valid': False, 'cert error': e.strerror}
        except ssl.SSLError as e:
            return {}

        peercert = s.getpeercert()['subjectAltName']
        hostname_list = [c[1] for c in peercert]
        return {'certificate valid': True, 'certificate for': hostname_list}


def get_response(r):

    json_nice_response = json.dumps(r, indent=2, ensure_ascii=False)
    return web.Response(text= json_nice_response)


async def get_handler(request):

    request = {
        'type': DEFAULT_TYPE,
        'url': UPSTREAM,
        'content': await request.text(),
        'headers': request.headers,
        'timeout': DEFAULT_TIMEOUT,
    }

    json_response = await send_request(request)
    return aiohttp.web.json_response(json_response)
    #return get_response(json_response)


async def post_handler(request: web.Request):

    try:
        req_json = await request.json()
    except json.decoder.JSONDecodeError as e:
        req_json = {}

    json_response = await send_request(req_json)
    return aiohttp.web.json_response(json_response)
    #return get_response(json_response)


async def send_request(request_to_send):

    request_to_send['timeout'] = 1 if 'timeout' not in request_to_send.keys() else float(request_to_send['timeout'])
    request_to_send['type'] = DEFAULT_TYPE if 'type' not in request_to_send.keys() else request_to_send['type'].upper()

    if 'url' not in request_to_send.keys() or request_to_send['type'] not in ['GET', 'POST'] or (request_to_send['type'] == 'POST' and 'content' not in request_to_send.keys()):
        return {'code': 'invalid json'}

    if not request_to_send['url'].startswith('http://') and not request_to_send['url'].startswith('http://'):
        request_to_send['url'] = 'http://%s' % request_to_send['url']

    #request_to_send['content'] = None if 'content' not in request_to_send.keys() else bytes(request_to_send['content'],'utf-8')
    #request_to_send['content'] = None if 'content' not in request_to_send.keys() else request_to_send['content']
    request_to_send['content'] = request_to_send['content'] if 'content' in request_to_send.keys() and request_to_send['type'] == 'POST' else None

    request_to_send['headers'] = None if 'headers' not in request_to_send.keys() else request_to_send['headers']
    #request_to_send['headers'].update({'Content-Type': 'text/plain'})
    #request_to_send['headers']['Content-Type'] = 'text/plain'
    #print(request_to_send['headers'])


    result = {}

    async with aiohttp.ClientSession() as session:

        try:
            async with session.request(
                    request_to_send['type'],
                    request_to_send['url'],
                    data=request_to_send['content'],
                    headers=request_to_send['headers'],
                    timeout=aiohttp.ClientTimeout(total=request_to_send['timeout']),
                    verify_ssl=False,
                    ) as response:

                headers = {}
                for k, v in response.headers.items():
                    headers[k] = ','.join(response.headers.getall(k))

                result['headers'] = headers

                result['code'] = response.status
                
                result.update(get_info(response.url.host, response.url.port))

                try:
                    result['json'] = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    result['content'] = await response.text()

                return result

        except asyncio.TimeoutError:
            return {'code': 'timeout'}


def lets_begin(p):

    app = web.Application()
    routes_arr = [web.get('/', get_handler), web.post('/', post_handler)]
    app.add_routes(routes_arr)
    web.run_app(app, port=p)


def main():

    if len(sys.argv) != 3:
        print('Wrong number of arguments')
        return

    global PORT,UPSTREAM,DEFAULT_TIMEOUT, DEFAULT_TYPE
    PORT = int(sys.argv[1])
    UPSTREAM = sys.argv[2]
    DEFAULT_TIMEOUT = 1
    DEFAULT_TYPE = 'GET'
    lets_begin(PORT)


if __name__ == "__main__":
    main()
