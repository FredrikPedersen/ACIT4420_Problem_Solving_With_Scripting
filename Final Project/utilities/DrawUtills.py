from typing import Union

import pygame
import time
import values.Constants as Constants
from pygame.surface import SurfaceType, Surface

from values.Colour import Colour
from values.Direction import Direction


def draw_maze_cell(x, y, screen: Union[Surface, SurfaceType], direction: Direction = None, colour: Colour = None) -> None:
    """
    Fills out a cell on the maze with a coloured rectangle to indicate part of the maze at coordinates (x, y).
    If a direction is given, the cell in the given direction is also filled out in addition to the cell at (x, y).

    :param x: X-coordinate of current cell.
    :param y: Y-coordinate of current cell.
    :param screen: Which screen the cell should be drawn on.
    :param direction: Which cell shall be drawn in addition to the current one.
    :param colour: What colour the drawn cell shall have.
    """

    # Offsets to make sure the maze's tile colour does not fill over the wall colour.
    rectangle_size: int = Constants.CELL_SIZE - 1
    x += 1
    y += 1

    if colour is None:
        colour_value = Colour.WHITE.value
    else:
        colour_value = colour.value

    if direction is None:
        pygame.draw.rect(screen, colour_value, (x, y, rectangle_size, rectangle_size), 0)

    if direction == Direction.LEFT:
        pygame.draw.rect(screen, colour_value, (x - Constants.CELL_SIZE, y, rectangle_size * 2, rectangle_size), 0)

    if direction == Direction.RIGHT:
        pygame.draw.rect(screen, colour_value, (x, y, rectangle_size * 2, rectangle_size), 0)

    if direction == Direction.DOWN:
        pygame.draw.rect(screen, colour_value, (x, y, rectangle_size, rectangle_size * 2), 0)

    if direction == Direction.UP:
        pygame.draw.rect(screen, colour_value, (x, y - Constants.CELL_SIZE, rectangle_size, rectangle_size * 2), 0)

    pygame.display.update()
    sleep_if_animation()
# draw_maze_cell()


def sleep_if_animation(timer: float = .05):
    """
    Convenience function for sleeping the program for a set time, if animations are enabled
    :param timer: Time in seconds the program should sleep
    """
    if Constants.ANIMATIONS_ENABLED:
        time.sleep(timer)
