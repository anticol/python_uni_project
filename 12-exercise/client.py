from urllib import request
#from ttt import *
from sys import argv
import urllib
from time import sleep
import json
GAMES = {}

def parse_json_response(response):
    try:
        parsed_response = response.read().decode('utf-8')
        return json.loads(parsed_response)
    except Exception as e:
        print(e)
        return None

def get_list_of_the_games(server_address):
    response = request.urlopen(server_address + ("/list" ))
    list_of_games_json = parse_json_response(response)
    for game in list_of_games_json:
        GAMES[game] = str(list_of_games_json[game])
        print(str(list_of_games_json[game]) + ' ' + game )
    return GAMES

def play_new_game(server_address,name):
    response = request.urlopen(server_address + ("/start?name=%s" % (urllib.parse.quote(name),)))
    game_id = parse_json_response(response)['id']
    print_game(server_address,int(game_id))
    return int(game_id)

def print_game(server_address,game_id):
    response = request.urlopen(server_address + ("/status?game=%s" % (game_id)))
    parsed_response = parse_json_response(response)
    if 'board' in parsed_response:
        board = parsed_response['board']
    else:
        return

    for line in board:
        if line[0] == 1:
            print('x', end='')
        elif line[0] == 2:
            print('o', end='')
        else:
            print('_', end='')

        if line[1] == 1:
            print('x', end='')
        elif line[1] == 2:
            print('o', end='')
        else:
            print('_', end='')


        if line[2] == 1:
            print('x', end='')
        elif line[2] == 2:
            print('o', end='')
        else:
            print('_', end='')

        print('')


def play_game(server_address,game_id,player,coordinates):
    response = request.urlopen(server_address + ("/play?game=%d&player=%d&x=%d&y=%d" % (game_id,player,coordinates[0],coordinates[1])))
    parsed = parse_json_response(response)
    print_game(server_address,game_id)
    if parsed['status'] == 'bad':
        print(parsed['message'])
        make_turn(server_address,game_id,player)
        return
    if wait_for_player(server_address,game_id,player,False) == False:
        return

def get_status(server_address,game_id):
    response = request.urlopen(server_address + ("/status?game=%d" % (game_id)))
    return parse_json_response(response)

def wait_for_player(server_addres, game_id,player,printed):
    if printed == False:
        print('waiting for the other player')

    status = get_status(server_addres,game_id)
    #print(status)
    #print('player = ' + str(player) + 'game id = ' + str(game_id))
    if 'winner' in status:
        if int(status['winner']) == int(player):
            print('you win')
            exit()
        elif int(status['winner'] == 0):
            print('draw')
            exit(0)
        else:
            print('you lose')
            exit()
    if int(status['next']) == int(player):
        print_game(server_addres,game_id)
        make_turn(server_addres,game_id,status['next'])


    else:
        sleep(1)
        wait_for_player(server_addres,game_id,player,True)

def play_existing_game(server_address,game_id):
    game_exists = False
    for game in GAMES:
        if(GAMES[game] == game_id):
            game_exists = True
    if game_exists == False:
        print('Game does not exist')
        what_to_do(server_address)
        return
    game_id = int(game_id)
    wait_for_player(server_address,game_id,2,False)
    #make_turn(server_address,game_id,2)
    #response = request.urlopen(server_address + ("/status?game=%d" % (int(game_id))))
    #print(parse_json_response(response))

def parse_coordinates(coordinates):
    parsed_coordinates = coordinates.split(' ')
    if(len(parsed_coordinates)) != 2:
        return None
    elif (parsed_coordinates[0].strip().isdigit() and parsed_coordinates[1].isdigit()) is False:
        return None
    coordinates = int(parsed_coordinates[0].strip()), int(parsed_coordinates[1].strip())
    if (coordinates[0] < 0 or coordinates[0] > 2) or (coordinates[1] < 0 or coordinates[1] > 2):
        return None

    return coordinates

def make_turn(server_address,game_id,player):
        character = 'x' if player == 1 else 'o'
        coordinates = input('your turn (' + character + '): ')
        coordinates_tuple = parse_coordinates(coordinates)
        if coordinates_tuple is None:
            print('Wrong input')
            make_turn(server_address,game_id,player)
        play_game(server_address,game_id,player,coordinates_tuple)

def what_to_do(server_address):
    command = input('Enter <id> of the game you would like to play or type <new> for new game\n')
    if command == 'new':
        name = input('What will be the name of the game?\n')
        game_id = play_new_game(server_address, name)
        make_turn(server_address,game_id,1)
    elif command != '' and all(x.isdigit() for x in command):
        play_existing_game(server_address,command)
    elif command == 'exit':
        return
    else:
        print('Wrong command')
        what_to_do(server_address)

def main():
    if len(argv) != 3:
        print('You have to specify port and host')
        return

    host = argv[1]
    port = int(argv[2])
    server_address = 'http://' + host + ':'+ str(port)

    get_list_of_the_games(server_address)
    what_to_do(server_address)


main()
