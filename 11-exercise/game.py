import itertools

class Game:
    def __init__(self,name,id):
        self.id = id
        self.name = name
        self.next = 1
        self.winner = 0
        self.board  = [[0,0,0],[0,0,0],[0,0,0]]
        self.isDraw = False

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_status(self):
        self.winner = self.check_game()
        return self.winner


    def make_turn(self, player,coordinate_x,coordinate_y):
        if(self.winner != 0) or (self.isDraw and self.winner == 0):
            return 'bad','Game is over and the winner is player number ' + str(self.winner)

        if(player != self.next):
            return 'bad','Player number ' + str(self.next) + ' should make a turn'

        if self.board[coordinate_y][coordinate_x] != 0:
            return 'bad','This field is not empty' + '[' + str(coordinate_y) + '],[' + str(coordinate_x) + '] = ' + str(self.board[coordinate_y][coordinate_x])

        self.board[coordinate_y][coordinate_x] = player
        self.next = 1 if player == 2 else 2
        self.winner = self.check_game()

        return 'ok', 'ok'


    def check_game(self):

        winner = 0
        idx = 0
        while idx != 3:
            if self.board[idx][0] == self.board[idx][1] == self.board[idx][2] and self.board[idx][0] != 0:
                winner = self.board[idx][0]
                print('The winner is player ' +  str(winner))
            if self.board[0][idx] == self.board[1][idx] == self.board[2][idx] and self.board[0][idx] != 0:
                print('The winner is player ' +  str())
                winner = self.board[0][idx]
                print('The winner is player ' +  str(winner))
            idx += 1

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            winner = self.board[0][0]
            print('The winner is player ' +  str(winner))
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            winner = self.board[0][2]
            print('The winner is player ' +  str(winner))
        if all(x != 0 for x in itertools.chain.from_iterable(self.board)) and (winner != 1 and winner !=2):
            winner = 0
            self.isDraw = True
            print('The winner is player ' +  str(winner))
        return winner



    def print_game(self):
        for line in self.board:
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
        print('')
        print('')

