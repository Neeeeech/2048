from random import choice

def give_zeros(board):
    """updates where the zeros are; returns list of coord tuples of zeros"""
    return [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]

def merge(board):
    """merges tiles of same number together horizontally"""
    for row in board:
        # looks at each row individually, starting from the left
        i = 0
        while i < len(row) - 1:
            if row[i] == row[i + 1]:
                # if the ith and i+1th are the same, double ith, remove i+1th
                # moving on after that means you won't merge an already-merged tile
                row[i] *= 2
                row.pop(i + 1)
            i += 1

def shift_left(board):
    """shifts everything to the left, merging if necessary, by removing all zeros, and re-adding them on right"""
    # not within the class, so all 4 move functions can make use of this one

    # zeros: co-ords of where the zeros are; shifted_board: copy of board to work with
    zeros = give_zeros(board)
    shifted_board = [row.copy() for row in board]

    # removes all zeros from shifted_board
    for (i, j) in zeros[::-1]:
        shifted_board[i].pop(j)

    # merges horizontally
    merge(shifted_board)

    # replaces all the zeros on the right
    for row in shifted_board:
        while len(row) < 4:
            row.append(0)

    return shifted_board


class GameState:
    def __init__(self, board):
        self.board = board

    def __str__(self):
        return '\n'.join(str(self.board[i]) for i in range(4))

    def cost(self):
        """cost function for self GameState"""
        pass

    def add_tile(self, num=1):
        """make a num amount of 2s appear in a random empty spot and return new GameState"""
        shifted_board = [row.copy() for row in self.board]
        for _ in range(num):
            (i, j) = choice(give_zeros(shifted_board))
            shifted_board[i][j] = 2
        return GameState(shifted_board)

    def give_left(self):
        """shifts left and returns new GameState"""
        return GameState(shift_left(self.board))

    def give_right(self):
        """shifts right and returns new GameState"""
        # reverse all rows, shift left, before reversing again
        shifted_board = shift_left([row[::-1] for row in self.board])
        return GameState([row[::-1] for row in shifted_board])

    def give_up(self):
        """shifts up and returns new GameState"""
        # transposes self.tiles, shift left
        shifted_board = shift_left(list(map(list, zip(*self.board))))
        # transposes again and places in new GameState
        return GameState(list(map(list, zip(*shifted_board))))

    def give_down(self):
        """shifts down and returns new GameState"""
        # transposes self.tiles, reverses horizontally, shifts left
        shifted_board = shift_left([row[::-1] for row in list(map(list, zip(*self.board)))])
        # reverses
        shifted_board = [row[::-1] for row in shifted_board]
        # transposes and places in new GameState
        return GameState(list(map(list, zip(*shifted_board))))


# constants for Game
LEFT, RIGHT, UP, DOWN = 0, 1, 2, 3
MOVE_LIST = (GameState.give_left, GameState.give_right, GameState.give_up, GameState.give_down)

class Game:
    def __init__(self, board=None):
        if board is None:
            board = [[0]*4, [0]*4, [0]*4, [0]*4]
        self.current_state = GameState(board).add_tile(2)
        self.prev_state = None

    def __str__(self):
        return str(self.current_state)

    def reset(self):
        """runs init without needing to create a new object"""
        self.__init__()

    def check_valid(self, next_state):
        """checks if the next state is different i.e. the move that caused next state is valid"""
        return self.current_state.board != next_state.board

    def shift(self, func):
        """shifts direction given by func if possible, returns whether possible"""
        potential_next = func(self.current_state)
        if self.check_valid(potential_next):
            # updates states, while adding a new tile to current_state
            self.prev_state = self.current_state
            self.current_state = potential_next.add_tile()
            return True
        return False

    def left(self):
        """shifts left"""
        return self.shift(GameState.give_left)

    def right(self):
        """shifts right"""
        return self.shift(GameState.give_right)

    def up(self):
        """shifts up"""
        return self.shift(GameState.give_up)

    def down(self):
        """shifts down"""
        return self.shift(GameState.give_down)

    def back(self):
        """goes back"""
        if self.prev_state is None:
            return False
        self.current_state = self.prev_state
        self.prev_state = None
        return True

    def lost(self):
        """if no more moves, returns True, else False"""
        board = self.current_state.board
        for i in range(4):
            for j in range(3):
                if board[i][j] == board[i][j+1] or board[j][i] == board[j][i+1]:
                    return False
        return True


if __name__ == '__main__':
    # game = Game([[0,0,2,2],[0,2,0,2],[0,0,0,2],[2,2,2,2]])
    # print()
    a = Game()
    while True:
        print(a)
        b = input()
        if b == 'a':
            a.left()
        elif b == 'd':
            a.right()
        elif b == 'w':
            a.up()
        elif b == 's':
            a.down()
        elif b == 'q':
            a.back()
