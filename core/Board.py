class Board:
    def __init__(self):
        """making a 2D matrix with board"""
        self.board_rows_2D_list = []  # 2d list which store board look

    def board_making(self):
        """
        Creating an empty board for Tic Tac Toe
        Filling row to append them to matrix, and clear row and agine until done
        :return: matrix of board
        """
        board_list_row = []  # 1d list for row of board
        for i in range(0, 12):
            for j in range(0, 12):    # i mean rows, j mean columns
                if i == 0:  # in 1st row I want to show names of columns
                    if j == 2:
                        board_list_row.append('A')
                    elif j == 6:
                        board_list_row.append('B')
                    elif j == 10:
                        board_list_row.append('C')
                    else:  # filling rest of 1st row with spacebars
                        board_list_row.append(' ')
                elif i == 2 and j == 0:  # in 1st column I want to show names of rows
                    board_list_row.append('1')
                elif i == 6 and j == 0:
                    board_list_row.append('2')
                elif i == 10 and j == 0:
                    board_list_row.append('3')
                elif (j == 4 and i == 4) or (j == 4 and i == 8) or (j == 8 and i == 4) or (j == 8 and i == 8):
                    board_list_row.append('+')  # crosses of rows and columns
                elif j == 4 or j == 8:
                    board_list_row.append('|')  # fill columns where should be "break"
                elif i == 4 or i == 8:
                    board_list_row.append('-')  # fill rows where should be "break"
                else:
                    board_list_row.append(' ')  # filling rest of board with spacebars
            self.board_rows_2D_list.append(board_list_row)  # addind 1d rows to 2d board
            # cleaning of board_list[] to get ready for another row
            board_list_row = []
        return self.board_rows_2D_list

    @staticmethod
    def print_board(board):
        """
        printing out board from argument, where there are changes (moves/ lane of win)
        :param board: board changed when played
        :return: none
        """
        for row in board:
            for element in row:
                print(element, end="")
            print()

    def board_from_file(self):
        """
        Creating an empty board from File txt
        :return: matrix of board
        """
        board_list_row = []
        try:  # This works perfectly (if .txt is good), but I want to overwrite it, just to make sure, game will work ;)
            file = open("../TicTacToe_board.txt", encoding='utf-8')
            for lane in file:
                lane = lane.rstrip("\n")  # removing EoL from right side
                for char in lane:
                    board_list_row.append(char)  # adding every charakter to row
                self.board_rows_2D_list.append(board_list_row)  # addind this row to 2d board list
                board_list_row = []  # crealring row before next iteration
            file.close()  # closing file
            return self.board_rows_2D_list
        except IOError:  # chatching if there is no file
            pass
        finally:  # I don't trust anyone ;) so it's better to load board from code above, than file which is changeable
            self.board_rows_2D_list = []
            self.board_rows_2D_list = self.board_making()
            return self.board_rows_2D_list

    @staticmethod
    def showing_vitory_lane_on_board(board_rows_2d_list, winning_type, winning_pos):
        """
        changing board to add lane, that show win result
        char is acronym of character - class(chr)
        :param board_rows_2d_list: Current board matrix to be "fixed" with winning lane
        board_rows_2d_list - 2d list of board, to get changes; winning_type/pos - two variables that
        :param winning_type: Which type (horizontal/ diagonal / vertical)
        clearly shows which of ten result are done   type: 1-4 (1 diagonal left top \\ 2 diagonal right top /
         3 - rows -  4- cols | )
        :param winning_pos: Which lane was filled with same character
        pos 2/6/10 (2 - highest/ leftest 6 middle 10 lowest/rightest
        :return: none
        """
        x, y = -1, -1
        length = len(board_rows_2d_list[0])  # I need lenght of list to know positions

        diagonal_left = [[i]*2 for i in range(0, length) if i % 2 == 1]  # [i]*2 is same as [i, i] 1:1 3:3..
        diagonal_lefttop_char = '\\'   # char for left top diagonal

        diagonal_right = [[i, length-i] for i in range(0, length) if i % 2 == 1]  # 1:11 9:3...
        diagonal_righttop_char = '/'   # char for right top diagonal
        if winning_type:  # if winning type is exists I check and set values for rows / colums number
            if 3 in winning_type and 4 in winning_type:  # if there is two lane win
                x = winning_pos[0]  # like in math X mean row
                y = winning_pos[1]  # like in math Y mean column
            elif 3 in winning_type:  # if there is single lane or + diagonal win
                x = winning_pos[0]
            elif 4 in winning_type:  # if there is single lane or + diagonal win
                y = winning_pos[0]

        if 1 in winning_type:  # type 1-4 (1 diagonal left top \, 2 diagonal right top /,3 - rows -.  4- cols|
            for each in diagonal_left:
                board_rows_2d_list[each[0]][each[1]] = diagonal_lefttop_char
        if 2 in winning_type:
            for each in diagonal_right:
                board_rows_2d_list[each[0]][each[1]] = diagonal_righttop_char
        if 3 in winning_type:
            row_lane = [[x, i] for i in range(0, length) if i % 2 == 1]  # 2/6/10 : 1, 3 ...
            row_char = '-'  # char for column lane
            for each in row_lane:
                board_rows_2d_list[each[0]][each[1]] = row_char  # changing row into lane
        if 4 in winning_type:
            column_lane = [[i, y] for i in range(0, length) if i % 2 == 1]  # 1, 3 ... : 2/6/10
            column_char = '|'  # char for row lane
            for each in column_lane:
                board_rows_2d_list[each[0]][each[1]] = column_char  # changing column into lane
