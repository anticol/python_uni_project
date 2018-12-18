from game import Game
from sys import argv
import urllib
import json
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler

COUNTER = 0
GAMES = {}


class TTTHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super(TTTHandler, self).__init__(*args, **kwargs)

    def send_response_to_client(self, code, response_json):

        res_content = bytes(json.dumps(response_json,
                                       indent=4,
                                       sort_keys=False,
                                       ensure_ascii=False), 'utf-8')

        self.send_response(code)
        self.send_header('Connection', 'close')
        self.send_header('Content-Type', 'text/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(res_content)

    def do_GET(self):
        global GAMES
        global COUNTER

        parsed_url = urllib.parse.urlparse(self.path)
        request_parameters = urllib.parse.parse_qs(parsed_url.query)
        request_path = parsed_url.path.strip('/')

        res_json = {}

        if request_path == 'start':

            name = request_parameters['name'][0] if 'name' in request_parameters else ''
            game = Game(name, COUNTER)
            GAMES[COUNTER] = game
            res_json['id'] = COUNTER

            COUNTER += 1

        else:
            if request_path == 'list':
                for x in GAMES:
                    if all(y == 0 for y in [i for j in GAMES[x].board for i in j]):
                        print('name')
                        print(GAMES[x].name)
                        res_json[GAMES[x].name] = GAMES[x].get_id()

            elif 'game' not in request_parameters:
                self.send_response_to_client(400,{'status':'bad', 'message':'Game not in parameters'})
                return


            elif all(x.isdigit() for x in request_parameters['game'][0]) is False:
                self.send_response_to_client(400,{'status':'bad', 'message':'Game ID is not a number'})
                return

            elif int(request_parameters['game'][0]) not in GAMES:
                self.send_response_to_client(400,{'status':'bad', 'message':'Game with selected ID does not exists'})
                return

            elif request_path == 'status':

                game_id = int(request_parameters['game'][0])
                game = GAMES[game_id]

                if game.get_status() == 0 and game.isDraw is False:
                    res_json['board'] = game.board
                    res_json['next'] = game.next
                elif game.isDraw and game.winner == 0:
                    res_json['winner'] = 0
                else:
                    res_json['winner'] = game.winner

            elif request_path == 'play':

                game_id = int(request_parameters['game'][0]) if 'game' in request_parameters else None
                player = request_parameters['player'][0] if 'player' in request_parameters else None
                x = request_parameters['x'][0] if 'x' in request_parameters else None
                y = request_parameters['y'][0] if 'y' in request_parameters else None

                if game_id is None or player is None or x is None or y is None:
                    res_json['status'] = 'bad'
                    res_json['message'] = 'Missing parameter'

                elif player != '1' and player != '2':
                    res_json['status'] = 'bad'
                    res_json['message'] = 'Invalid parameter - player'


                elif x not in ['0', '1', '2'] or y not in ['0', '1', '2']:
                    res_json['status'] = 'bad'
                    res_json['message'] = 'Invalid parameter - x or y'

                else:
                    game = GAMES[game_id]
                    player = int(player)
                    x = int(x)
                    y = int(y)
                    status, message = game.make_turn(player, x, y)


                    res_json['status'] = status
                    if status is not message:
                        res_json['message'] = message

            else:
                res_json['status'] = 'bad'
                res_json['message'] = 'Invalid action (start|status|play|list)'

        self.send_response_to_client(200, res_json)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    if len(argv) != 2:
        print('You have to specify port')
        return

    port = int(argv[1])

    httpd = ThreadedHTTPServer(('', port), TTTHandler)
    httpd.serve_forever()


main()
