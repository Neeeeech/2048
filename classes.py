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

    # zeros: coords of where the zeros are; shifted_board: copy of board to work with
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
        """cost function for """
        pass

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


if __name__ == '__main__':
    state = GameState([[0,0,2,2],[0,2,0,2],[0,0,0,2],[2,2,2,2]])
    print()
    """a = Game()
    while True:
        print(a)
        b = input()
        if b == 'a':
            a.record()
            a.left()
        elif b == 'd':
            a.record()
            a.right()
        elif b == 'w':
            a.record()
            a.up()
        elif b == 's':
            a.record()
            a.down()
        elif b == 'q':
            a.back()
        else:
            a.record()
            a.add_tile()"""
