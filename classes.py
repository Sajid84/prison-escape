# Author : Sajid Mahmood

class game_map:
    def __init__(self, map_file, guard_file):

        # this part tries to open and read every line in the map text file
        # if the file doesn't exist in location, or can't be opened/read for some reason, the program exits

        try:
            self.map_open = open(map_file)
            map_lines_all = self.map_open.readlines()
            self.map_open.close()
        except IOError or IndexError:
            exit()

        # this part creates the 2D list/array for the grid, by taking each character in a line from the map text file
        # and appending it to a blank list, it repeats for every line, and all the lists are appended inside another
        # list to form a larger 2D list

        self.current_grid = []
        for i in map_lines_all:
            print(i.rstrip())
            self.current_row = []
            for m in i:
                if m == "\n":
                    continue
                self.current_row.append(m)
            self.current_grid.append(self.current_row)

        # this part tries to open and read every line in the guards text file
        # if the file doesn't exist in location, or can't be opened/read for some reason, the program exits

        try:
            self.guard_open = open(guard_file)
            guard_line_all = self.guard_open.readlines()
            self.guard_open.close()
        except IOError or IndexError:
            exit()

        # this part splits every line in the guards text file and creates a new object for every guard using the
        # guard class, and appends all the guard objects into a blank list

        self.guard_list = []
        for i in guard_line_all:
            guard_line = i.split()
            self.guard_list.append(guard(guard_line[0], guard_line[1], guard_line[2],
                                         guard_line[3:]))

        # this part just finds and stores the position (row & column) of the escape block ('E') on the map

        self.escape_row = 0
        self.escape_col = 0
        for x in self.current_grid:
            for y in x:
                if y == "E":

                    self.escape_row = self.current_grid.index(x)
                    self.escape_col = x.index(y)

    def get_grid(self):
        for i in range(len(self.guard_list)):
            self.current_grid[(guard.get_location(self.guard_list[i])[0])][(guard.get_location(self.guard_list[i])[1])]\
                = "G"
        return self.current_grid

    def get_guards(self):

        # returns the list of guard objects
        return self.guard_list

    def update_player(self, direction):
        check_bool = False

        # the next 6 lines finds and stores the row & column position of the player on the map
        for x in self.current_grid:
            for y in x:
                if y == "P":
                    row_position = self.current_grid.index(x)
                    col_position = x.index(y)

                    # this part below checks which direction input was given by user and updates the player's position
                    # accordingly, but only if within map boundary, and if it's an empty space or escape block ('E')

                    if direction == "U":
                        if (row_position - 1) >= 0 and \
                                (self.current_grid[row_position - 1][col_position] == " " or
                                 self.current_grid[row_position - 1][col_position] == "E"):
                            self.current_grid[row_position][col_position] = " "
                            row_position -= 1
                            self.current_grid[row_position][col_position] = "P"
                            break

                    elif direction == "D":
                        if (row_position + 1) < len(self.current_grid) and \
                                (self.current_grid[row_position + 1][col_position] == " " or
                                 self.current_grid[row_position + 1][col_position] == "E"):
                            self.current_grid[row_position][col_position] = " "
                            row_position += 1
                            self.current_grid[row_position][col_position] = "P"
                            check_bool = True
                            break

                    elif direction == "R":
                        if (col_position + 1) < len(self.current_grid[0]) and \
                                (self.current_grid[row_position][col_position + 1] == " " or
                                 self.current_grid[row_position][col_position + 1] == "E"):
                            self.current_grid[row_position][col_position] = " "
                            col_position += 1
                            self.current_grid[row_position][col_position] = "P"
                            break

                    elif direction == "L":
                        if (col_position - 1) >= 0 and \
                                (self.current_grid[row_position][col_position - 1] == " " or
                                 self.current_grid[row_position][col_position - 1] == "E"):
                            self.current_grid[row_position][col_position] = " "
                            col_position -= 1
                            self.current_grid[row_position][col_position] = "P"
                            break

                if check_bool:
                    break

    def update_guards(self):

        # loops for every guard in the guard text file
        for i in range(len(self.guard_list)):

            # edits the existing position of the guard on the grid to an empty space
            position_before = guard.get_location(self.guard_list[i])
            self.current_grid[position_before[0]][position_before[1]] = " "

            # places the guard in its new position on the grid
            position_after = guard.move(self.guard_list[i], self.current_grid)
            self.current_grid[position_after[0]][position_after[1]] = "G"

    def player_wins(self):

        # locates and stores the player's current grid position
        for x in self.current_grid:
            for y in x:
                if y == "P":
                    row_position = self.current_grid.index(x)
                    col_position = x.index(y)

                    # checks if the current position of the player is the same as the escape block on the grid
                    if row_position == self.escape_row and col_position == self.escape_col:
                        return True
                    else:
                        return False

    def player_loses(self):

        # loops for every guard in the guard list
        for f in range(len(self.guard_list)):
            for x in self.current_grid:
                for y in x:
                    if y == "P":
                        row_position = self.current_grid.index(x)
                        col_position = x.index(y)

                        # calls enemy_in_range function to check if player is in range of any guard
                        if guard.enemy_in_range(self.guard_list[f], row_position, col_position):
                            return True
        return False


class guard:
    def __init__(self, row, col, attack_range, movements):
        self.row = int(row)
        self.col = int(col)
        self.attack_range = int(attack_range)
        self.movements = movements
        self.counter = 0

    def get_location(self):

        # returns a tuple with the row and column of the guard's current position
        return int(self.row), int(self.col)

    def move(self, current_grid):
        self.current_grid = current_grid

        # resets movement counter once the end of movement list is reached, so it loops back from start
        if self.counter == len(self.movements):
            self.counter = 0

        # gets the movement direction from the movement list taken from the guards text file
        movement = self.movements[self.counter]

        # checks movement direction and updates the guard's position on the grid accordingly
        # but only if within map boundary, and if it's an empty space or escape block ('E')

        if movement == "L":
            if (self.col - 1) >= 0 and self.current_grid[self.row][self.col - 1] == " ":
                self.col -= 1
            self.counter += 1

        elif movement == "R":
            if (self.col + 1) < len(self.current_grid[0]) and self.current_grid[self.row][self.col + 1] == " ":
                self.col += 1
            self.counter += 1

        elif movement == "U":
            if (self.row - 1) >= 0 and self.current_grid[self.row - 1][self.col] == " ":
                self.row -= 1
            self.counter += 1

        elif movement == "D":
            if (self.row + 1) < len(self.current_grid) and self.current_grid[self.row + 1][self.col] == " ":
                self.row += 1
            self.counter += 1
        return self.row, self.col

    def enemy_in_range(self, enemy_row, enemy_col):

        # find how far apart the player is from the guard by the difference in row and column

        row_diff = abs(enemy_row - self.row)
        col_diff = abs(enemy_col - self.col)

        # if the sum of both difference are less than or equal to guard's attack range, then enemy is in range

        if row_diff + col_diff <= self.attack_range:
            return True
        else:
            return False
