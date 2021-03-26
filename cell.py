import pygame

# Color constants
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
BLUE       = (  0,   0, 255)
YELLOW     = (255, 255,   0)
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
PURPLE     = (128,   0, 128)
ORANGE     = (255, 165,   0)
DARK_GREY  = ( 64,  64,  64)
GREY       = (128, 128, 128)
LIGHT_GREY = (192, 192, 192)
TURQUOISE  = ( 64, 224, 208)


## Cell class
class Cell:
    def __init__(self, row, col, size, num_cols):
        # [row][col] index in grid
        self.row = row
        self.col = col

        # Total number of columns in the grid (to calculate id)
        self.num_cols = num_cols

        # Size in pixels
        self.size = size

        # X,Y coordinate corresponding to clingo node
        self.pos_x = self.col + 1
        self.pos_y = self.row + 1

        # x,y coordinate on the screen (top left)
        self.pixel_x = (self.col * self.size) + (self.pos_x * 10)
        self.pixel_y = (self.row * self.size) + (self.pos_y * 10)

        # Color
        self.color = ORANGE

        # ID corresponding to node 'N' in clingo
        self.id = self.pos_x + ((self.pos_y - 1) * self.num_cols)

        # Initialize font for drawing
        self.font = pygame.font.SysFont('Arial', 10)

        # Cell properties
        self._is_passable = True
        self._is_highway = False
        self._is_picking_station = False

        # Object list
#        self.__objects = []



    def get_pos(self):
        return self.row, self.col

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pixel_x, self.pixel_y, self.size, self.size))
        surface.blit(self.font.render(str(self.id) + ":" + str(self.pos_x) + "," + str(self.pos_y), True, (255,0,0)), (self.pixel_x+5, self.pixel_y+5))
#        shift = 10
#        for o in self.__objects:
#            surface.blit(self.font.render(o.get_type() + str(o.get_id()) + ": " + str(o.get_pos()), True, (255,0,0)), (self.pixel_x+5, self.pixel_y+5+shift))
#            shift += 10

#    def add_object(self, o):
#        self.__objects.append(o)
