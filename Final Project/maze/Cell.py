from typing import Dict
from values.Direction import Direction


class Cell:

    """
    Dumb class representing each cell in the maze-grid by holding values needed when drawing and solving mazes.
    """

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y
        self.__walls: Dict[Direction: bool] = {Direction.LEFT: True, Direction.RIGHT: True, Direction.UP: True, Direction.DOWN: True}

        # Values used specifically for Recursive Walk Algorithm
        self.__visited_while_solving: bool = False

        # Values used specifically for A* algorithm
        self.__cost_from_start: int = 0
        self.__cost_to_end: int = 0
        self.__parent: Cell = None
    # __init__()

    def toggle_wall(self, direction: Direction):
        self.__walls[direction] = not self.__walls[direction]

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def walls(self):
        return self.__walls

    @property
    def visited_while_solving(self) -> bool:
        return self.__visited_while_solving

    @property
    def cost_from_start(self) -> int:
        return self.__cost_from_start

    @property
    def cost_to_end(self) -> int:
        return self.__cost_to_end

    @property
    def parent(self):
        return self.__parent

    @visited_while_solving.setter
    def visited_while_solving(self, visited: bool):
        self.__visited_while_solving = visited

    @cost_from_start.setter
    def cost_from_start(self, value):
        self.__cost_from_start = value

    @cost_to_end.setter
    def cost_to_end(self, value):
        self.__cost_to_end = value

    @parent.setter
    def parent(self, parent):
        self.__parent = parent
