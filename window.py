import pygame
import pygame_gui
from grid import Grid
from robot import Robot
from shelf import Shelf

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


EDIT_MAIN_PANEL_WIDTH = 400
INFO_MAIN_PANEL_HEIGHT = 100

# The Window class.....................
class Window:
    def __init__(self, screen_w, screen_h):
        self.__screen_w = screen_w
        self.__screen_h = screen_h

        self.__grid_w = None
        self.__grid_h = None

        self.____grid_centered_panel_pos_x = None
        self.____grid_centered_panel_pos_y = None

        ###########################################################
        #                  pygame Initialization
        ###########################################################

        # Initialize pygame display
        pygame.init()
        pygame.display.set_caption("Automated Warehouse Planner")

        # Create pygame surfaces
        self.__window_surface = pygame.display.set_mode((self.__screen_w, self.__screen_h))
        self.__background_surface = pygame.Surface((self.__screen_w, self.__screen_h))
        self.__centered_grid_surface = None


        ###########################################################
        #                pygame_gui Initialization
        ###########################################################

        # Create a pygame clock to track time
        self.__clock = pygame.time.Clock()

        # Create pygame_gui manager
        self.__ui_manager = pygame_gui.UIManager(
            (self.__screen_w, self.__screen_h),
             pygame_gui.PackageResource(package='data.themes',
                                        resource='test_theme2.json'))
        # Load Fonts
        self.__ui_manager.preload_fonts(
            [{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
             {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
             {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
             {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
             {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
             ])

        # Declare panels
        self.__grid_main_panel = None
        self.__grid_centered_panel = None
        self.__info_main_panel = None
        self.__edit_main_panel = None

        # Define grid objects
        self.__buttons_list = None
        self.__selected_button_id = None
        self.sizes = ['1','2','3','4','5','6','7','8','9','10']
        self.cell_sizes = ['50','60','70','80','90']

        # Define info objects


        # Define UI objects
        self.num_rows = 4
        self.num_cols = 4
        self.cell_size = 70
        self.rows_drop_down = None
        self.cols_drop_down = None
        self.size_drop_down = None
        self.info_text_box = None


        ###########################################################
        #                 Finalize Initialization
        ###########################################################

        # Declare grid
        self.__grid = None

        # Create screen and prepare to run
        self.create_ui()
        self.running = True


    # Creates...................
    def create_ui(self):
        # Reset pygame_gui manager
        self.__ui_manager.clear_and_reset()

        # Clear the screen
        self.__background_surface.fill(DARK_GREY)

        # Calculate grid size and position
        button_w = self.cell_size
        button_h = self.cell_size
        shift = 2

        self.__grid_w = (button_w * self.num_cols) + 10
        self.__grid_h = (button_h * self.num_rows) + 10

        self.__grid_centered_panel_pos_x = (self.__screen_w
                                            - EDIT_MAIN_PANEL_WIDTH
                                            - self.__grid_w) / 2
        self.__grid_centered_panel_pos_y = (self.__screen_h
                                            - INFO_MAIN_PANEL_HEIGHT
                                            - self.__grid_h) / 2

        # Initialize centered_grid surface
        self.__centered_grid_surface = pygame.Surface((self.__grid_w,
                                                       self.__grid_h),
                                                       pygame.SRCALPHA, 32)

        # Initialize grid cells
        self.__grid = Grid(self.num_rows, self.num_cols, self.cell_size)


        # Initialize pygame_gui panels
        self.__grid_main_panel = pygame_gui.elements.UIPanel(
            pygame.Rect(0, 0,
                        self.__screen_w - EDIT_MAIN_PANEL_WIDTH,
                        self.__screen_h - INFO_MAIN_PANEL_HEIGHT),
                        starting_layer_height=4, manager=self.__ui_manager)

        self.__grid_centered_panel = pygame_gui.elements.UIPanel(
            pygame.Rect(self.__grid_centered_panel_pos_x,
                        self.__grid_centered_panel_pos_y,
                        self.__grid_w,
                        self.__grid_h),
                        starting_layer_height=4, manager=self.__ui_manager,
                        container=self.__grid_main_panel)

        self.__info_main_panel = pygame_gui.elements.UIPanel(
            pygame.Rect(0, self.__screen_h - INFO_MAIN_PANEL_HEIGHT,
                        self.__screen_w - EDIT_MAIN_PANEL_WIDTH,
                        INFO_MAIN_PANEL_HEIGHT),
                        starting_layer_height=4, manager=self.__ui_manager)

        self.__edit_main_panel = pygame_gui.elements.UIPanel(
            pygame.Rect(self.__screen_w - EDIT_MAIN_PANEL_WIDTH, 0,
                        EDIT_MAIN_PANEL_WIDTH,
                        self.__screen_h),
                        starting_layer_height=4, manager=self.__ui_manager)

        # Initialize grid buttons
        self.__buttons_list = []
        self.__selected_button_id = 0

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.__buttons_list.append(pygame_gui.elements.UIButton(
                    pygame.Rect(((button_w * c) + shift, (button_h * r) + shift),
                                (button_w, button_h)),
                    '', self.__ui_manager,
                    container=self.__grid_centered_panel))

        self.rows_drop_down = pygame_gui.elements.UIDropDownMenu(
            self.sizes, str(self.num_rows), pygame.Rect((10, 10), (50, 25)),
            self.__ui_manager, container=self.__edit_main_panel)

        self.cols_drop_down = pygame_gui.elements.UIDropDownMenu(
            self.sizes, str(self.num_cols), pygame.Rect((10, 30), (50, 25)),
            self.__ui_manager, container=self.__edit_main_panel)

#        self.size_drop_down = pygame_gui.elements.UIDropDownMenu(
#            self.cell_sizes, str(self.cell_size), pygame.Rect((10, 10), (50, 25)),
#            self.__ui_manager, container=self.__info_main_panel)

        text=("<font face=fira_code color=normal_text size=2>"
                  "<b>Node:</b> #<br>"
                  "<b>Location:</b> (x,y)<br>"
                  "<b>Type:</b> Passable cell<br>"
                  "<b>Robot:</b> None<br>"
                  "<b>Shelf:</b> None<br>"
                  "<b>Picking Station:</b> None"
                  "</font>")

        self.info_text_box = pygame_gui.elements.UITextBox(
            html_text=text,
            relative_rect=pygame.Rect((5, 5), (200, INFO_MAIN_PANEL_HEIGHT - 15)),
            manager=self.__ui_manager,
            container=self.__info_main_panel)



        # TESTING!!!!!!!!!!
#        r = 2
#        c = 2
#        r1 = robot.Robot(1, (c,r))
#        s1 = shelf.Shelf(4, (c,r))
#        self.__grid[r-1][c-1].add_object(r1)
#        self.__grid[r-1][c-1].add_object(s1)



    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.__ui_manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if (event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
                        and (event.ui_element == self.rows_drop_down or event.ui_element == self.cols_drop_down)):
                    self.num_rows = int(self.rows_drop_down.selected_option)
                    self.num_cols = int(self.cols_drop_down.selected_option)
                    self.create_ui()

                if (event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
                        and event.ui_element == self.size_drop_down):
                    self.cell_size = int(self.size_drop_down.selected_option)
                    self.create_ui()

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    n = 0
                    for button in self.__buttons_list:
                        n += 1
                        if event.ui_element == button:
                            # If no button is selected, then select
                            if self.__selected_button_id == 0:
                                button.select()
                                self.__selected_button_id = n

                            # If some button is selected, check if it is
                            # 'button' and if so, unselect
                            elif self.__selected_button_id == n:
                                button.unselect()
                                self.__selected_button_id = 0

                            # Unselect selected button and select 'button'
                            else:
                                self.__buttons_list[self.__selected_button_id-1].unselect()
                                button.select()
                                self.__selected_button_id = n

                            print("selected button id: "+str(self.__selected_button_id))
                            break



    def run(self):
        image = pygame.image.load("data/images/robot.png")
#        robot_images = []
#        robot_images.append(pygame.transform.scale(image))


        while self.running:
            # Calculate time delta for pygame_gui and lock the frame rate
            time_delta = self.__clock.tick(60)/1000.0

            # Check for input events
            self.process_events()

            # Respond to input events
            self.__ui_manager.update(time_delta)

            # Clear window
            self.__window_surface.blit(self.__background_surface, (0, 0))

            # Draw graphics
            self.__ui_manager.draw_ui(self.__window_surface)
            self.__grid.draw(self.__centered_grid_surface)

            # Blit to display
            self.__window_surface.blit(self.__centered_grid_surface, (self.__grid_centered_panel_pos_x+3, self.__grid_centered_panel_pos_y+3))

            # Update the display
            pygame.display.update()

        pygame.quit()
