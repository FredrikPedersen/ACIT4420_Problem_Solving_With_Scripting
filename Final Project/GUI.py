from tkinter import *
from typing import Union, List

import pygame
import values.Constants as Constants
from pygame.surface import SurfaceType, Surface

from maze.MazeDrawer import MazeDrawer
from solution.MazeSolver import MazeSolver
from values.SolutionType import SolutionType
from values.Colour import Colour


class Gui:

    __control_panel_width: int = 300
    __control_panel_height: int = 400
    __max_maze_width: int = int(Constants.WINDOW_WIDTH / Constants.CELL_SIZE - 2)
    __max_maze_height: int = int(Constants.WINDOW_HEIGHT / Constants.CELL_SIZE - 2)

    def __init__(self):
        self.__creationSteps = None
        self.__chosen_solution: SolutionType = SolutionType.BUILD_SOLUTION
        self.__solution_start: List[int, int] = [Constants.MAZE_WIDTH, Constants.MAZE_HEIGHT]
        self.__solved_once = False

        self.__root_window: Tk = self.__initialize_root_window()
        self.__screen: Union[Surface, SurfaceType] = self.__initialize_pygame()

    # ---------- Initializations ---------- #

    def __initialize_root_window(self) -> Tk:
        root_window: Tk = Tk()
        root_window.title("Control Panel")
        root_window.geometry(f"{self.__control_panel_width}x{self.__control_panel_height}")
        self.__initialize_inputs(root_window)

        return root_window

    def __initialize_pygame(self) -> Union[Surface, SurfaceType]:
        pygame.display.init()
        return pygame.display.set_mode((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))

    def __initialize_inputs(self, window: Tk) -> None:

        Label(window, text="Control Panel", font=("bold", 15)).grid(row=3, column=1, pady=10, columnspan=2)
        Label(window, text="Maze Width:", font=("bold", 10)).grid(row=4, column=1, pady=5)

        self.__width_scale = Scale(window, from_=5, to=self.__max_maze_width, orient=HORIZONTAL, command=self.__width_scale_callback)
        self.__width_scale.grid(row=4, column=2)

        Label(window, text="Maze Height:", font=("bold", 10)).grid(row=5, column=1, pady=10)

        self.__height_scale = Scale(window, from_=5, to=self.__max_maze_height, orient=HORIZONTAL, command=self.__height_scale_callback)
        self.__height_scale.grid(row=5, column=2)

        Label(window, text="Solution Algorithm:", font=("bold", 10)).grid(row=6, column=1, pady=10, padx=10)

        options = SolutionType.as_list()
        default_option = StringVar(window)
        default_option.set(options[0])

        self.__solution_option_menu = OptionMenu(window, default_option, *options, command=self.__option_menu_callback)
        self.__solution_option_menu.grid(row=6, column=2)

        Label(window, text="Solution start X:", font=("bold", 10)).grid(row=7, column=1, pady=5)

        self.__solution_start_x_scale = Scale(window, from_=5, to=self.__width_scale.get(), orient=HORIZONTAL, command=self.__solution_start_x_scale_callback)
        self.__solution_start_x_scale.grid(row=7, column=2)

        Label(window, text="Solution start Y:", font=("bold", 10)).grid(row=8, column=1, pady=10)

        self.__solution_start_y_scale = Scale(window, from_=5, to=self.__height_scale.get(), orient=HORIZONTAL, command=self.__solution_start_y_scale_callback)
        self.__solution_start_y_scale.grid(row=8, column=2)

        Label(window, text="Draw Animations:", font=("bold", 10)).grid(row=9, column=1, pady=10)

        self.__animations_checked = BooleanVar()
        self.__animations_checked.set(True)
        self.__animations_check_button = Checkbutton(window, variable=self.__animations_checked, command=self.__animations_check_callback).grid(row=9, column=2)

        Button(window, text="Draw and Solve Maze", font=("bold", 12), command=self.__draw_and_solve_maze).grid(row=11, column=1, pady=10, columnspan=2)

    # initialize_inputs()

    def run_gui_loop(self):
        while True:
            self.__root_window.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    # run_gui_loop()

    # ---------- Action Functions ---------- #

    def __draw_and_solve_maze(self) -> None:
        self.__clear_pygame_screen()
        maze_drawer: MazeDrawer = MazeDrawer(self.__screen)
        self.__creationSteps = maze_drawer.draw()
        maze_solver: MazeSolver = MazeSolver(self.__screen, self.__chosen_solution, self.__creationSteps, tuple(self.__solution_start))
        maze_solver.solve_maze()

    # ---------- Callback and Utility Functions ---------- #

    def __option_menu_callback(self, value):
        for solution_type in SolutionType:
            if value == solution_type.value:
                self.__chosen_solution = solution_type
                return

        raise Exception("A non-existing solution type has been selected. This should not be able to happen.")

    def __width_scale_callback(self, value: int):
        Constants.set_grid_width(int(value))
        self.__solution_start_x_scale.configure(to=value)

    def __height_scale_callback(self, value: int):
        Constants.set_grid_height(int(value))
        self.__solution_start_y_scale.configure(to=value)

    def __solution_start_x_scale_callback(self, value: int):
        self.__solution_start[0] = ((int(value) - 1) * Constants.CELL_SIZE) + Constants.ROOT_X

    def __solution_start_y_scale_callback(self, value: int):
        self.__solution_start[1] = ((int(value) - 1) * Constants.CELL_SIZE) + Constants.ROOT_Y

    def __animations_check_callback(self):
        Constants.ANIMATIONS_ENABLED = self.__animations_checked.get()

    def __clear_pygame_screen(self):
        self.__screen.fill(Colour.BLACK.value)
        pygame.display.update()
