import random


class Supplies:
    """data object for storing supplies"""

    def __init__(self, supp):
        if isinstance(supp, list):
            self.food = supp[0]
            self.water = supp[1]
        else:
            self.food = supp
            self.water = supp

    def __str__(self):
        if self.food == self.water:
            return str(self.food)
        else:
            return "[{0},{1}]".format(self.food, self.water)


def random_building(size=10, equal_supplies=True):
    rooms = []
    for r in range(2 * size + 1):
        row = []
        for c in range(2 * size + 1):
            if equal_supplies:
                row.append(random.randint(0, 9))
            else:
                if random.choice([True, False]):
                    row.append([random.randint(0, 9), 0])
                else:
                    row.append([0, random.randint(0, 9)])
        rooms.append(row)
    return Building(rooms)


class Building:
    """data object for storing a (2n+1) by (2n+1) array of rooms"""

    def __init__(self, rooms):
        """rooms = 2D array of integers or pairs of integers"""
        if len(rooms) % 2 != 1 or len(rooms[0]) != len(rooms):
            raise ValueError("Illegal number of rooms: must be (2n+1) x (2n+1)")
        self.size = len(rooms) // 2
        self.rooms = [[Supplies(s) for s in row] for row in rooms]
        self.reset()

    def __str__(self):
        return "[[" + "],\n [".join([",".join([str(room) for room in row]) for row in self.rooms]) + "]]"

    def reset(self):
        """player starts in the center, without supplies"""
        self.player_row = self.size
        self.player_col = self.size
        self.player_food = 0
        self.player_water = 0

    def is_valid(self, row, col):
        """checks if (row,col) is a valid room location"""
        return 0 <= row <= 2 * self.size and 0 <= col <= 2 * self.size

    def is_collapsed(self, row, col):
        """checks if the room at position (row,col) is collapsed"""

        def is_after(start, x, end):
            return (start < end and x < end) or (start > end and x > end)

        return is_after(self.size, row, self.player_row) or is_after(self.size, col, self.player_col)

    def can_move(self):
        """check if the player is able to move in any direction"""
        return not (self.player_row in [0, 2 * self.size]) or not (self.player_col in [0, 2 * self.size])

    def move_player(self, delta_row, delta_col):
        """move player by (delta_row, delta_col) vector if possible; returns whether successful"""
        new_row = self.player_row + delta_row
        new_col = self.player_col + delta_col
        if not self.is_valid(new_row, new_col) or self.is_collapsed(new_row, new_col):
            return False
        else:
            self.player_row = new_row
            self.player_col = new_col
            self.player_food += self.rooms[self.player_row][self.player_col].food
            self.player_water += self.rooms[self.player_row][self.player_col].water
            return True
