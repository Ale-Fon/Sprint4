import random

class Player:
    def __init__(self, color):
        self.color = color

    def is_computer(self):
        return False
    
class humanPlayer(Player):
    def __init__(self, color, get_letter_func):
        super().__init__(color)
        self.get_letter_func = get_letter_func

    def choose_letter(self):
        return self.get_letter_func()

class cpuPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def is_computer(self):
        return True

    def choose_letter(self):
        return random.choice(['S', 'O'])

    def choose_position(self, game):
        emptyChoice = [(r, c) for r in range(game.size) for c in range(game.size) if game.board[r][c] == '']
        if emptyChoice:
            return random.choice(emptyChoice)
        return None



class gameplay:
    def __init__(self, size, mode):
        self.size = size
        self.mode = mode
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.current_turn = random.choice(['Blue', 'Red'])
        self.moves = []
        self.scores = {'Blue': 0, 'Red': 0}
        print(f"Game initialized: Size {size}")
        print(f"Start player: {self.current_turn}")

    def letterPlace(self, row, col, letter):
        if self.board[row][col] != '':
            return None, None

        self.board[row][col] = letter
        self.moves.append((row, col, letter, self.current_turn))

        sosList = self.checkForSos(row, col, letter)

        if sosList:
            self.scores[self.current_turn] += len(sosList)
            return self.handle_sos(sosList)
            
        return None, sosList

    def switch_turn(self):
        self.current_turn = 'Red' if self.current_turn == 'Blue' else 'Blue'
        print(f"Turn is now {self.current_turn}")

    def is_full(self):
        full = all(self.board[r][c] != '' for r in range(self.size) for c in range(self.size))
        if full:
            print("The board is full.")
        return full

    def checkWinnerScore(self):
        if self.scores['Blue'] > self.scores['Red']:
            return 'Blue'
        elif self.scores['Red'] > self.scores['Blue']:
            return 'Red'
        else:
            print("The game is a draw.")
            return 'Draw'

    def checkForSos(self, row, col, letter):
        raise NotImplementedError("Subclasses must implement this method.")

    def handle_sos(self, sosList):
        raise NotImplementedError("Subclasses must implement this method.")
    
    def is_sos_in_direction(self, row, col, dr, dc):
        try:
            if self.board[row][col] == 'O':
                if (0 <= row + dr < self.size and 0 <= col + dc < self.size and
                    0 <= row - dr < self.size and 0 <= col - dc < self.size):

                    if (self.board[row + dr][col + dc] == 'S' and
                        self.board[row - dr][col - dc] == 'S'):
                        return True, [(row - dr, col - dc), (row, col), (row + dr, col + dc)]
            elif self.board[row][col] == 'S':
                if (0 <= row + dr < self.size and 0 <= col + dc < self.size and
                    0 <= row + 2 * dr < self.size and 0 <= col + 2 * dc < self.size):
                    if (self.board[row + dr][col + dc] == 'O' and
                        self.board[row + 2 * dr][col + 2 * dc] == 'S'):
                        return True, [(row, col), (row + dr, col + dc), (row + 2 * dr, col + 2 * dc)]
        except IndexError:
            pass
        return False, None


class SimpleGame(gameplay):
    def __init__(self, size):
        super().__init__(size, "Simple")

    def checkForSos(self, row, col, letter):
        sosFound, coordinates = self.is_sos(row, col)
        return [coordinates] if sosFound else []

    def handle_sos(self, sosList):
        print(f"{self.current_turn} has won the game in Simple mode")
        return self.current_turn, sosList

    def is_sos(self, row, col):
        directions = [(-1,0), (1,0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            sosFound, coordinates = self.is_sos_in_direction(row, col, dr, dc)
            if sosFound:
                return True, coordinates
        return False, None
        


class GeneralGame(gameplay):
    def __init__(self, size):
        super().__init__(size, "General")

    def checkForSos(self, row, col, letter):
        sosList = []
        checkedPositions = set()
        directions = [(-1,0), (1,0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        
        for dr, dc in directions:
            sosFound, coordinates = self.is_sos_in_direction(row, col, dr, dc)
            if sosFound:
                coordSet = frozenset(coordinates)
                if coordSet not in checkedPositions:
                    sosList.append(coordinates)
                    checkedPositions.add(coordSet)

        return sosList

    def handle_sos(self, sosList):
        if self.is_full():
            winner = self.checkWinnerScore()
            print(f"{winner} has won the game in general mode with a score of {self.scores[winner]}!")
            return winner, sosList
        if not sosList:
            self.switch_turn()

        return None, sosList