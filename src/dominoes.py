# 28 available tiles with smallest value first
available_tiles = ((0, 0),
                   (0, 1), (1, 1),
                   (0, 2), (1, 2), (2, 2),
                   (0, 3), (1, 3), (2, 3), (3, 3),
                   (0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
                   (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6))


class DominoTile:
    def __init__(self, tile, is_spinner, placed_by_player):
        self.__data = [available_tiles[tile][0], available_tiles[tile][1], is_spinner, placed_by_player]

    def face_values(self):
        return self.__data[0], self.__data[1]

    def is_spinner(self):
        return self.__data[2]

    def placed_by_player(self):
        return self.__data[3]

    def to_list(self):
        return self.__data


class DominoesGameBase:
    empty_tile = DominoTile(0, 0, 0).to_list()
    axis_length = len(available_tiles)
    max_element = axis_length - 1
    first_position = int(max_element / 2)

    def zero_axis(self, axis):
        self.__game_axes[axis] = []
        empty_axis = []
        for axis_element in range(self.axis_length):
            empty_axis.append(self.empty_tile)
        self.__game_axes[axis] = empty_axis

    def zero_axes(self):
        self.__game_axes = []
        empty_axis = []
        for axis_element in range(self.axis_length):
            empty_axis.append(self.empty_tile)
        # make a copy of the axis array so that the axes array doesn't contain two references to the same axis array
        self.__game_axes = [empty_axis, empty_axis.copy()]

    def reset(self):
        self.zero_axes()
        self.__spinner_locations = [0, 0]

    def __init__(self):
        self.__game_axes = []
        self.zero_axes()
        self.__spinner_locations = [0, 0]

    def has_spinner(self):
        return self.__spinner_locations != [0, 0]

    def update_spinner_locations(self):
        for first_axis_element in range(self.axis_length):
            if self.__game_axes[0][first_axis_element][2] == 1:
                self.__spinner_locations[0] = first_axis_element
                break
        for second_axis_element in range(self.axis_length):
            if self.__game_axes[1][second_axis_element][2] == 1:
                self.__spinner_locations[1] = second_axis_element
                break

    def axis_needs_recenter(self, axis):
        return self.__game_axes[axis][0] != self.empty_tile or \
               self.__game_axes[axis][self.axis_length - 1] != self.empty_tile
    
    def recenter_axis(self, axis):
        old_start_position = 0
        for old_axis_element in range(self.axis_length):
            if self.__game_axes[axis][old_axis_element] != self.empty_tile:
                old_start_position = old_axis_element
                break
        empty_tiles = self.__game_axes[axis].count(self.empty_tile)
        new_start_position = int(empty_tiles / 2)

        axis_copy = self.__game_axes[axis]
        self.zero_axis(axis)
        for new_axis_element in range(self.axis_length - empty_tiles):
            self.__game_axes[axis][new_start_position + new_axis_element] = \
                axis_copy[old_start_position + new_axis_element]

        self.update_spinner_locations()

    def insert_tile(self, domino_tile, axis, location):
        tile_list = domino_tile.to_list()
        if domino_tile.is_spinner() == 0:
            self.__game_axes[axis][location] = tile_list
        elif not self.has_spinner():
            self.__game_axes[axis][location] = tile_list
            self.__game_axes[1][self.first_position] = tile_list
            self.__spinner_locations = [location, self.first_position]

    def print_game(self):
        for y_var in range(self.axis_length):
            print_str = ''
            for x_var in range(self.axis_length):
                if self.has_spinner():
                    if (x_var != self.__spinner_locations[0] and y_var != self.__spinner_locations[1]) or \
                            self.__game_axes[0][x_var] == self.empty_tile or \
                            self.__game_axes[1][y_var] == self.empty_tile:
                        print_str += '-----'
                    else:
                        if y_var == self.__spinner_locations[1]:
                            print_str += '[' + str(self.__game_axes[0][x_var][0]) + '|' + \
                                         str(self.__game_axes[0][x_var][1]) + ']'
                        else:
                            print_str += '[' + str(self.__game_axes[1][y_var][0]) + '|' + \
                                         str(self.__game_axes[1][y_var][1]) + ']'
                else:
                    if y_var != self.first_position or self.__game_axes[0][x_var] == self.empty_tile:
                        print_str += '-----'
                    else:
                        print_str += '[' + str(self.__game_axes[0][x_var][0]) + '|' + \
                                     str(self.__game_axes[0][x_var][1]) + ']'
            print(print_str)

    def to_list(self):
        return self.__game_axes


test_game = DominoesGameBase()
test_game.insert_tile(DominoTile(1, 0, 2), 0, 5)
test_game.insert_tile(DominoTile(2, 0, 1), 0, 6)
test_game.insert_tile(DominoTile(3, 1, 2), 0, 7)
test_game.insert_tile(DominoTile(4, 0, 1), 1, 12)
test_game.insert_tile(DominoTile(5, 0, 2), 1, 14)

test_game.recenter_axis(0)

test_game.print_game()
