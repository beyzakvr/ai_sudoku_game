from Field import Field


class Sudoku:

    def __init__(self, filename):
        self.board = self.read_sudoku(filename)

    def __str__(self):
        output = "╔═══════╦═══════╦═══════╗\n"
        # iterate through rows
        for i in range(9):
            if i == 3 or i == 6:
                output += "╠═══════╬═══════╬═══════╣\n"
            output += "║ "
            # iterate through columns
            for j in range(9):
                if j == 3 or j == 6:
                    output += "║ "
                output += str(self.board[i][j]) + " "
            output += "║\n"
        output += "╚═══════╩═══════╩═══════╝\n"
        return output

    @staticmethod
    def read_sudoku(filename):
        """
        Read in a sudoku file
        @param filename: Sudoku filename
        @return: A 9x9 grid of Fields where each field is initialized with all its neighbor fields
        """
        assert filename is not None and filename != "", "Invalid filename"
        # Setup 9x9 grid
        grid = [[Field for _ in range(9)] for _ in range(9)]

        try:
            with open(filename, "r") as file:
                for row, line in enumerate(file):
                    for col_index, char in enumerate(line):
                        if char == '\n':
                            continue
                        if int(char) == 0:
                            grid[row][col_index] = Field()
                        else:
                            grid[row][col_index] = Field(int(char))

        except FileNotFoundError:
            print("Error opening file: " + filename)

        Sudoku.add_neighbours(grid)
        return grid

    @staticmethod
    def add_neighbours(grid):
        """
        Adds a list of neighbors to each field
        @param grid: 9x9 list of Fields
        """

    # TODO: for each field, add its neighbors
        for rows in range(9): #looping through every field in the 9x9 grid
            for colums in range(9):
                neighbours = [] #creating empty list to later on store all the neighbours of that specific field

                for col in range(9): #adding all the fields in the same row
                    if col != colums: #except the current one
                        neighbours.append(grid[rows][col]) #adding these fields from the same row to the neighbours list

                for row in range(9): #adding all the fields in the same colum
                    if row != rows: #except the current one
                        neighbours.append(grid[row][colums])

                #adding all fields in the same three by three box
                three_by_three_box_row_start = (rows // 3) * 3 #find top-left corner of three by three by integer devision --> will give us which of the three boxes we are dealing with
                three_by_three_box_colum_start = (colums // 3) * 3 #multiply by three gives us than the exact coordinates

                for row in range(three_by_three_box_row_start, three_by_three_box_row_start + 3): #looping through all 9 fields in the three by three box
                    for col in range(three_by_three_box_colum_start, three_by_three_box_colum_start +3):

                        if (row != rows or col != colums) and grid[row][col] not in neighbours: #checking if not current field it self and if it is not already been added
                            neighbours.append(grid[row][col]) 
                
                grid[rows][colums].set_neighbours(neighbours) #assining the whole neighbour list to the current field, by using its coordinates (row  and colum)



    def board_to_string(self):

        output = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                output += self.board[row][col].get_value()
            output += "\n"
        return output

    def get_board(self):
        return self.board
