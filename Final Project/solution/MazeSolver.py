from typing import Dict, List, Tuple

from maze.Cell import Cell
from maze.Grid import Grid
from utilities.DrawUtills import *
from solution.algorithms.AStar import AStar
from solution.algorithms.RecursiveWalk import RecursiveWalk
from values.SolutionType import SolutionType


class MazeSolver:

    __solutionSteps: List[Tuple[int, int]]
    __solutionType: SolutionType

    def __init__(self, screen: Union[Surface, SurfaceType], solution_type: SolutionType, solution_start: Tuple[int]):
        grid_instance: Grid = Grid.get_instance()

        self.__screen = screen
        self.__solutionType: SolutionType = solution_type
        self.__grid: Dict[Tuple[int, int], Cell] = grid_instance.grid
        self.__solutionStartX: int = solution_start[0]
        self.__solutionStartY: int = solution_start[1]
    # __init__()

    # ---------- General Solution Functions ---------- #

    def solve_maze(self) -> None:
        self.__solutionSteps = []
        self.__mark_start_exit()
        solution_start_coordinates: Tuple[int, int] = (self.__solutionStartX, self.__solutionStartY)

        if self.__solutionType == SolutionType.RECURSIVE_WALK:
            self.__solutionSteps = RecursiveWalk(solution_start_coordinates).solve_maze()

        if self.__solutionType == SolutionType.A_STAR:
            self.__solutionSteps = AStar(solution_start_coordinates).solve_maze()

        self.__draw_solution_cells()
    # solve_maze()

    def __mark_start_exit(self) -> None:
        """
        Convenience function for drawing the solution's start and exit positions as red and green cells, respectively.
        """

        draw_maze_cell(self.__solutionStartX, self.__solutionStartY, self.__screen, None, Colour.RED)
        draw_maze_cell(Constants.ROOT_X, Constants.ROOT_Y, self.__screen, None, Colour.GREEN)
    # mark_start_exit()

    def __draw_solution_cells(self, remove: bool = False) -> None:
        """
        Draws a red circle in the center of the cell at position (x, y).
        Used to draw individual steps in the solution path.

        :param remove: Indicate whether the function should be used to remove existing solution cells already drawn
                        on the canvas.
        """

        for step in self.__solutionSteps:
            # Add an offset to place the circle in the center of the cell
            x = step[0] + Constants.CELL_SIZE / 2
            y = step[1] + Constants.CELL_SIZE / 2

            if not remove:
                pygame.draw.circle(self.__screen, Colour.RED.value, (x, y), 3)
            else:
                pygame.draw.circle(self.__screen, Colour.WHITE.value, (x, y), 3)

            pygame.display.update()

            sleep_if_animation(.1)
    # draw_solution_cells()
