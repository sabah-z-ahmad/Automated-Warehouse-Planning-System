import pygame
from object import Object

# Color constants
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
BLUE       = (  0,   0, 255)
YELLOW     = (255, 255,   0)
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
PURPLE     = (128,   0, 128)
ORANGE     = (255, 165,   0)
DARK_GREY = ( 64,  64,  64)
GREY       = (128, 128, 128)
LIGHT_GREY  = (192, 192, 192)
TURQUOISE  = ( 64, 224, 208)

SHELF_COLOR = BLUE

class Shelf(Object):
    # Inherited variables:
    #   self.id
    #   self.pos
    #

    def get_type(self):
        return "S"

    # Draw to screen
    def draw(self, surface):
        print("test")
