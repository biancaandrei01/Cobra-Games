# importarea tuturor functiilor si metodelor din biblioteca tkinter pentru instrumentele GUI
from tkinter import *
# importarea modulului numpy pentru lucrul cu matrici
import numpy as np

# dimensiunile tablei de X si 0
size_of_board = 800
# dimensiunile simbolurilor introduse pe tabla
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
# grosimea simbolurilor
symbol_thickness = 50
# culorile pentru fiecare simbol in parte
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


class Xsi0:
    # constructorul clasei, initializarea variabilelor
    def __init__(self):
        # initializare fereastra
        self.window = Tk()
        self.window.title('X si 0')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # preluarea pozitiei de insertie a simbolului de la utilizator sub forma de clicuri
        self.window.bind('<Button-1>', self.click)

        # initializare status tabla, jucatorul cu 'X' incepe primul
        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        # initializare status joc, 'X' incepe primul deci statusul lui este activ initial
        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        # initializare scoruri
        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    # desenarea liniilor verticale si orizontale ce formeaza tabla de X si 0
    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    # resetare joc
    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    # modulele necesare pentru a desena obiectul bazat pe joc pe tabela de joc
    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)  # valoarea grilei de pe tabla
        grid_position = self.convert_logical_to_grid_position(logical_position)  # valorile pozitiei din centrul grilei
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    # statusul jocului
    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'It\'s a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        # calculul scorului
        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)
        # calculul scorului obtinut de fiecare jucator si a situatiilor de egalitate
        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += '    Tie     : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True
        # la un click pe tabela jocul va reincepe pana cand este apasat exit
        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # modulele necesare pentru a realiza logica jocului
    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    # verificare statusului celulei
    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):
        player = -1 if player == 'X' else 1

        # cazul 1 in care sunt 3 la fel in linie
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # cazul 2 in care sunt 3 la fel pe diagonala
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    # cazul 3 in care niciun jucator nu castiga si este egalitate
    def is_tie(self):
        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True
        return tie

    # status joc cand castiga un jucator sau toate casutele sunt ocupate
    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        return gameover

    # preluarea pozitiilor oferite de click-urile efectuate de utilizator in fereastra
    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            # verificarea statusului jocului
            if self.is_gameover():
                self.display_gameover()

        else:  # reluarea jocului
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = Xsi0()
game_instance.mainloop()
