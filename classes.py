from random import choice

class Game:
    def __init__(self):
        self.tiles = [[0]*4, [0]*4, [0]*4, [0]*4]
        self.history = []
        self.add_tile(2)

    def __str__(self):
        return '\n'.join(str(self.tiles[i]) for i in range(4))

    def give_zeros(self):
        """updates where the zeros are; returns list of coord tuples of zeros"""
        return [(i, j) for i in range(4) for j in range(4) if self.tiles[i][j] == 0]

    def add_tile(self, num=1):
        """make a num amount of 2s appear in a random empty spot"""
        for _ in range(num):
            (i, j) = choice(self.give_zeros())
            self.tiles[i][j] = 2

    def record(self):
        """adds current state to self.history"""
        # makes sure all the lists are copies
        self.history.append([row.copy() for row in self.tiles])

    def merge(self):
        """merges tiles of same number together horizontally"""
        for row in self.tiles:
            # looks at each row individually, starting from the left
            i = 0
            while i < len(row) - 1:
                if row[i] == row[i+1]:
                    # if the ith and i+1th are the same, double ith, remove i+1th
                    # moving on after that means you won't merge an already-merged tile
                    row[i] *= 2
                    row.pop(i+1)
                i += 1

    def check_prev_valid(self):
        """checks if the previous move did anything. if yes, returns true, removes last self.history entry"""
        if self.history[-1] == self.tiles:
            self.history.pop(-1)
            return False
        return True

    def left(self):
        """shifts everything to the left, merging if necessary, by removing all zeros, and re-adding them on right"""
        for (i, j) in self.give_zeros()[::-1]:
            self.tiles[i].pop(j)
        self.merge()
        for row in self.tiles:
            while len(row) < 4:
                row.append(0)

    def right(self):
        """shifts everything to the right, merging if necessary"""
        # reverse all rows, shift left, before reversing again
        self.tiles = [row[::-1] for row in self.tiles]
        self.left()
        self.tiles = [row[::-1] for row in self.tiles]

    def up(self):
        """shifts everything up, merging if necessary"""
        # transposes self.tiles, shift left, before transposing again
        self.tiles = list(map(list, zip(*self.tiles)))
        self.left()
        self.tiles = list(map(list, zip(*self.tiles)))

    def down(self):
        """shifts everything down, merging if necessary"""
        # transposes self.tiles, shifts right, before transposing again
        self.tiles = list(map(list, zip(*self.tiles)))
        self.right()
        self.tiles = list(map(list, zip(*self.tiles)))

    def back(self):
        """reverts to previous position"""
        if self.history:
            self.tiles = self.history[-1].copy()
            self.history.pop(-1)


if __name__ == '__main__':
    a = Game()
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
            a.add_tile()
