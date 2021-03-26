from cell import Cell

class Grid:
    def __init__(self, num_rows, num_cols, cell_size):
        # Initialize grid dimensions
        self.num_rows = num_rows
        self.num_cols = num_cols

        # Declare list/dicts for grid cell/objects
        self.cell_layer = []
        self.robot_dict = {}
        self.shelf_dict = {}

        # Initialize each cell in the grid
        self.cell_size = cell_size
        for i in range(self.num_rows):
            self.cell_layer.append([])
            for j in range(self.num_cols):
                c = Cell(i, j, self.cell_size-10, self.num_cols)
                self.cell_layer[i].append(c)

    def draw(self, surface):
        # Draw
        for row in self.cell_layer:
            for cell in row:
                cell.draw(surface)

    def set_cell_size(self, size):
        self.__cell_size = size

    def get_cell_size(self):
        return self.__cell_size


    # TODO: CHECK FOR DUPLICATES/NON-EXISTING?
    def add_robot(self, r):
        self.robot_dict[str(r.get_id)] = r

    def get_robot(self, id):
        return self.robot_dict[str(id)]

    def add_shelf(self, s):
        self.shelf_dict[str(s.get_id)] = s

    def get_shelf(self, id):
        return self.shelf_dict[str(id)]
