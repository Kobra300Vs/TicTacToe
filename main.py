from random import randrange as rr

from core.Board import Board
from core.Logs import Logs
from core.player.PlayerCircle import PlayerCircle
from core.player.PlayerCross import PlayerCross

class Game(object):
    """
    Object of Game() is just a running game.
    Player are inputing thier names, answer the question about contiuning logs.
    Next there is coinflip to choice which player is moving next.
    """
    len_of_message_after_game = 40  # This var saying about minimum lenght of "winner" text and its lanes
    coinflip = rr(0, 2)  # As name say... make an coin flip, to make choice of 1st move
    # (i, j) Dict of allowed moves, that left in this game
    allowed_moves = {'a1': (2, 2),  'b1': (2, 6),  'c1': (2, 10),
                     'a2': (6, 2),  'b2': (6, 6),  'c2': (6, 10),
                     'a3': (10, 2), 'b3': (10, 6), 'c3': (10, 10)}

    def __init__(self):
        self.board_rows_2D_list = Board.board_from_file(Board())  # Taking an empty board from Board class
        """p_circe/ p_cross - listing moves of Player subclasses
        player_win_logs - listing logs of winners in rounds
        """
        self.p_circle_moves, self.p_cross_moves, self.player_win_logs = [], [], []
        # actual_player - after coin flip, I have to pass information, which player is moving... 0- Circle, 1 - Cross
        self.actual_player = -1
        """winning_type/ winning_pos - Helps to pass informations about lane to create - is it diagonal from left top,
                                    or left bottom or at 1/2/3 or a/b/c
        winning_type 1- \\ 2- / 3- - 4- |         winning_pos taking just 2/6/10 - which are ids` in-Board 
        """
        self.winning_type, self.winning_pos = [], []
        self.are_logs_loaded = ""  # Taking var from input (yes/no) - ask about contiunue/ start from scratch logs
        # Taking names from players
        self.name_of_player_one = " "  # empty placeholder
        self.player_circle = PlayerCircle(self.name_of_player_one)
        self.name_of_player_two = " "
        self.player_cross = PlayerCross(self.name_of_player_two)

        self.game_loop(True)  # Starting game and (take names plz)

    def game_loop(self, is_game_taking_names_logs_info):
        """
        Making a game loop that call other functions and count moves (Only one time in sesion You can give names)
        If players want rematch set every variable/ attribute to starting values.
        :param is_game_taking_names_logs_info: If game have 1st initialization I need to get names.
        In every next games in same session they use same names, so don't need for asking about names.
        :return: None
        """
        while is_game_taking_names_logs_info:  # if game have fresh start it need names and info what to to with logs
            print("Hello in my TicTacToe game")
            self.taking_logs_input()
            self.taking_names_input()
            is_game_taking_names_logs_info = False  # and in every game loop this shouldn't be asked
        are_we_still_playing = True  # if not exited, drawed or won
        does_player_said_exit = False  # does player said "exit" or not
        while are_we_still_playing:  # if there is no win/draw
            are_we_still_playing = not(self.is_victory())  # if there is no win, we're still playing
            if not are_we_still_playing:  # if we don't play, exit loop
                break
            count_moves = ((-1)*len(self.allowed_moves))+9  # getting number of moves i.e: when there are 3 moves -3+9=6
            if count_moves == 9:  # if there was 9 moves and was no winner -  round is draw and end loop of playing
                self.player_win_logs.append('d')  # "remembering" this is draw
                self.drawing_message()
                break
            else:
                Board.print_board(self.board_rows_2D_list)
                if self.taking_a_player_move():  # making move, and when player said "exit" there is no more playing
                    does_player_said_exit = True
                    break
        if does_player_said_exit:  # if there was "exit"... game should be stopped
            print("\nGame has no winners or tie.")  # print in new row and end game
            if self.are_logs_loaded == 'yes':  # from player answer about logs
                Logs.logs_with_load(Logs(self.name_of_player_one, self.name_of_player_two, self.player_win_logs))
            else:  # if they end any round I paste logs to .txt, coz I will overwrite it everytime
                Logs.logs_without_load(Logs(self.name_of_player_one, self.name_of_player_two, self.player_win_logs))
            return
        if self.player_win_logs[-1] != 'd':  # if in while we got "there is win", now I show text about it
            self.winning_message()
        are_you_want_rematch = input("Are you want to play agine? (yes/whatever) ").lower()  # asking about rematch
        if self.are_logs_loaded == 'yes':  # from player answer about logs
            if are_you_want_rematch != 'yes':  # if they stop playing, I'm pasting logs to .txt
                Logs.logs_with_load(Logs(self.name_of_player_one, self.name_of_player_two, self.player_win_logs))
        else:  # if they end any round I paste logs to .txt, coz I will overwrite it everytime
            Logs.logs_without_load(Logs(self.name_of_player_one, self.name_of_player_two, self.player_win_logs))

        if are_you_want_rematch == 'yes':  # When there is rematch, I want to reset every value to starting values
            self.board_rows_2D_list = Board.board_making(Board())
            self.allowed_moves = {'a1': (2, 2),  'b1': (2, 6),  'c1': (2, 10),
                                  'a2': (6, 2),  'b2': (6, 6),  'c2': (6, 10),
                                  'a3': (10, 2), 'b3': (10, 6), 'c3': (10, 10)}
            self.p_circle_moves, self.p_cross_moves = [], []
            self.winning_type, self.winning_pos = [], []
            # self.coinflip = rr(0, 2)  # if starter player should be more randomized, than only at begining
            self.len_of_message_after_game = 40
            self.game_loop(False)  # Starting game agine, but now don't ask about names agine

    def taking_logs_input(self):
        """
        This function ask main host about loading logs (if they are exists) or start them from scratch.
        :return: None
        """
        while True:  # ask about logs as many times, as answer will be "yes" or "no"
            self.are_logs_loaded = input("Do I have to load logs? (yes/no) ").lower()
            if self.are_logs_loaded == 'no' or self.are_logs_loaded == 'yes':  # if answer is good, break loop
                break

    def taking_names_input(self):
        """
        Taking names from both players and checking if they are have only letters in name.
        :return: None
        """
        self.name_of_player_one = ''
        while not self.name_of_player_one.isalpha():  # ask as many times, as answer will have only letters
            self.name_of_player_one = input("Give name of '" + self.player_circle.char + "' player: ").capitalize()
        self.player_circle = PlayerCircle(self.name_of_player_one)
        self.name_of_player_two = ''
        while not self.name_of_player_two.isalpha():  # ask as many times, as answer will have only letters
            self.name_of_player_two = input("Give name of '" + self.player_cross.char + "' player: ").capitalize()
        self.player_cross = PlayerCross(self.name_of_player_two)

    def is_victory(self):
        """
        Checking is anyone winner or not.
        :return: boolean values - True if someone winned game, False if noone is winner.
        """
        # Chacking only one of players with lastest move. If scored "win" adding it to logs and return "Game has won"
        if self.actual_player == 0:
            if self.win_rule(self.p_circle_moves):  # checking if it's won in single/multiple ways
                self.player_win_logs.append(self.player_circle.char)  # adding win information to logs
                return True
        elif self.actual_player == 1:
            if self.win_rule(self.p_cross_moves):
                self.player_win_logs.append(self.player_cross.char)
                return True
        return False  # False when game has no winner yet

    def win_rule(self, move_list):
        """
        Checking win rules   1- \\ 2- / 3- - 4- |
        Diadonals are checked first, coz 'now there are two of them!'
        Then are checked rows, and at last columns one by one.
        All checking is done by checking out move_list (down below) for only 1 player at same time from thier
        own move list.
        :param move_list: list of moves from last moving player, only 1 at the time.
        :return: True only if someone is winner
        """
        self.diagonals(move_list)  # checking diagonals first
        move_list = sorted(move_list)  # not necessary, it's only for one of player - for current one
        dic = {}  # i will put there pair of lane(row/col):how_many_of_them i.e.: "c":1, "c":1
        short_str = ""  # taking 'char' from dic, when its value == 3
        short_str_list = []  # taking 'char' from dic, when its value == 3 and putting it in list, to get all of them(2)
        for each in move_list:
            for cha in each:  # checking every char in every move
                counter = 1  # counting iterations
                if cha in dic:  # reverse checking
                    dic[cha] = dic.get(cha) + 1  # if char is in dic, incremente information of times they showed in
                    if dic[cha] > 2:  # if there is 3 of same chars, that mean we have winner and it's way of win
                        short_str = cha  # taking char form dic
                        short_str_list.append(short_str)  # putting this char into list to use it later
                else:
                    dic[cha] = counter  # if there is no char in dic, just add it with :value = 1

        if len(short_str_list) == 1:  # if there is only 1 win
            if short_str in ('1', '2', '3'):  # checking row number
                self.winning_pos.append(int(short_str)*4-2)  # getting good lane in middle of row
                self.winning_type.append(3)  # type 3 = row
            if short_str in ('a', 'b', 'c'):  # checking col letter
                self.winning_type.append(4)  # type 4 = column
                self.winning_pos.append(2 if (short_str == 'a') else 6 if (short_str == 'b') else 10)
            # ^ translate letter to good middle column of board, to make there a lane
        elif len(short_str_list) == 2:  # if there is 2 connected lanes
            if short_str_list[1] in ['1', '2', '3']:  # there was tuple, here is list.
                self.winning_pos.append(int(short_str_list[1])*4-2)  # same calculations as above
                self.winning_type.append(3)
                # ↓ with iformation about move - making right position on board to print lane↑
            if short_str_list[0] in ['a', 'b', 'c']:
                self.winning_type.append(4)
                self.winning_pos.append(2 if (short_str_list[0] == 'a') else 6
                                        if (short_str_list[0] == 'b') else 10)
        if self.winning_type:  # if there is any win lane - that's mean there is winner
            return True

    def diagonals(self, move_list):
        """
        Checking if player won by making diagonal lane
        :param move_list: list of moves from last moving player, only 1 at the time.
        :return: False if there is no diagonal winner, not important.
        """
        move_set = set(move_list)  # changing moves to set... just to use set operations
        tuple_a1_c3 = ('a1', 'b2', 'c3')  # \ diagonal
        tuple_a3_c1 = ('a3', 'b2', 'c1')  # / diagonal
        if set(tuple_a1_c3).issubset(move_set):  # if winner is by \
            self.winning_type.append(1)
        if set(tuple_a3_c1).issubset(move_set):  # if winner is by /
            self.winning_type.append(2)
        return False  # if there is no winner

    def name_of_next_player(self, is_not_finished):  # game is not finished  = change player, else dont.
        """
        This function is used to pick who make move if they are still playing or it don't change them
        if any of them is winner
        :param is_not_finished: boolean - True: change player to 2nd; False: giving name of player
        :return: ^ True: character of next player; False: name of the winner.
        """
        if is_not_finished:  # if players are playing
            self.coinflip += 1  # changing player to another to make him move
        # 0 = Circle, 1 = Cross
            if self.coinflip % 2 == 0:  # returning right name of Player
                self.actual_player = 0
                return self.player_circle.char
            else:
                self.actual_player = 1
                return self.player_cross.char

        if not is_not_finished:  # same stuff but without increasing coinflip so the players stay same = not change move
            if self.coinflip % 2 == 0:
                self.actual_player = 0
                return self.player_circle.name
            else:
                self.actual_player = 1
                return self.player_cross.name

    def taking_a_player_move(self):
        """
        Asking player about his move from input()
        :return: True - when player said "exit" -> quit current game
        """
        player_move = ""  # creating var
        choice = self.name_of_next_player(True)  # Allow to get charakter of next player
        is_valid = True  # just to call and end While loop
        while is_valid:
            player_move = input("Please " + choice + " give a coords (z0 / exit): ").lower()  # taking str
            if player_move == 'exit':  # exiting from game
                return True
            if player_move in self.allowed_moves.keys():  # checking if player can make this move
                is_valid = False  # if player make valid move, he cannot be ask agine for move
                if self.actual_player == 0:  # if Player is Circle
                    self.p_circle_moves.append(player_move)  # adding move to its moves list
                    coords = self.allowed_moves[player_move]  # taking coords from dict, by "key"
                    self.board_rows_2D_list[coords[0]][coords[1]] = self.player_circle.char  # changing value on board
                else:  # if Player is Cross
                    self.p_cross_moves.append(player_move)  # adding move to its moves list
                    coords = self.allowed_moves[player_move]  # taking coords from dict, by "key"
                    self.board_rows_2D_list[coords[0]][coords[1]] = self.player_cross.char  # changing value on board
            else:
                print("You are not allowed to make this move!")  # if move was done / is beyond board
        else:
            self.allowed_moves.pop(player_move)  # removing move from allowed, coz it's already done

    @staticmethod
    def adding_message_border(len_text=40):
        """
        Adding dashed border above end game messages.
        :param len_text: How log this border should be
        :return: None
        """
        empty_str = ""  # empty string which i will fill with - to make lane, 2nd "oneliner" way is down below
        print(empty_str.rjust(len_text, '-'))  # printing lane above Tie
        # empty_str = "".rjust(self.len_empty, '-')  # nicer way to implement same thing, than above

    def drawing_message(self):
        """
        This function is printing centered TIE text.
        :return: None
        """
        tie_str_text = 'Tie'
        len_of_text = len(tie_str_text)
        len_text = ((self.len_of_message_after_game - len_of_text) // 2 + len_of_text)  # centering Tie text

        self.adding_message_border(self.len_of_message_after_game)
        print(tie_str_text.rjust(len_text, ' '))  # printing "drawing" text
        self.adding_message_border(self.len_of_message_after_game)

        Board.print_board(self.board_rows_2D_list)  # printing Board to show last move

    def winning_message(self):
        """
        This function is printing centred WINNER text
        :return: None
        """
        winning_str_formating = f"And the winner is: {self.name_of_next_player(False)}"
        # ^taking name without changing player^
        len_of_text = len(winning_str_formating)  # variable taking lenght of "winner" text
        if len_of_text > self.len_of_message_after_game:  # if "winner" text is longer than base 40
            self.len_of_message_after_game = len_of_text
        len_text = ((self.len_of_message_after_game - len_of_text) // 2 + len_of_text)  # variable that calculate center

        self.adding_message_border(self.len_of_message_after_game)
        print(winning_str_formating.rjust(len_text, " "))  # printing out "winning" text in middle of lanes
        self.adding_message_border(self.len_of_message_after_game)

        Board.showing_vitory_lane_on_board(self.board_rows_2D_list, self.winning_type, self.winning_pos)  # drawing lane
        Board.print_board(self.board_rows_2D_list)  # Calling Board to print itself changed in game to show it last time


print(Logs.logs.__doc__)  # just showing docstring...

# start of Game 
if __name__ == "__main__":
    Game()
