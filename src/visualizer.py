import pygame as pg
import numpy as np
import sys
import time


class DrawParams:
    def __init__(self, sequence_length: int, grid_row_length: int) -> None:
        self.execution_time = 25  # in seconds
        self.screen_size = 600  # in pixels
        self.margin_to_cell_ratio = 0.1
        self.border_to_cell_ratio = 0.03
        self.font_to_cell_ratio = 0.4
        self.dashed_to_solid_line_ratio = 0.03

        self.cell_size = self.screen_size / \
            (grid_row_length + self.margin_to_cell_ratio * (grid_row_length + 1))
        self.margin = self.margin_to_cell_ratio * self.cell_size
        self.border_width = int(self.border_to_cell_ratio * self.cell_size)
        self.font_size = int(self.font_to_cell_ratio * self.cell_size)
        self.dashed_line_interval = self.dashed_to_solid_line_ratio * self.cell_size

        self.sleep_time = min(self.execution_time /
                              sequence_length, 1)  # in seconds

        self.background_color = (255, 255, 255)
        self.cell_in_correct_position = (144, 238, 144)
        self.cell_in_wrong_position = (240, 128, 128)
        self.cell_in_motion_color = (135, 206, 250)

        self.solid_border_color = (169, 169, 169)
        self.dashed_border_color = (211, 211, 211)

        self.font_type = 'helveticaneue'
        self.font_color_for_value_cell = (15, 15, 15)
        self.font_color_for_empty_cell = (125, 125, 125)


def draw_dashed_border(surface: pg.Surface, params: DrawParams, x: int, y: int) -> None:
    border_width = params.border_width
    border_color = params.dashed_border_color
    cell_size = params.cell_size

    for curr_x in np.arange(x, x + cell_size + border_width // 2 + 1, params.dashed_line_interval * 2):
        pg.draw.line(surface, border_color, (curr_x, y),
                     (curr_x + params.dashed_line_interval, y), border_width)
    for curr_y in np.arange(y, y + cell_size + border_width // 2, params.dashed_line_interval * 2):
        pg.draw.line(surface, border_color, (x + cell_size, curr_y), (x +
                     cell_size, curr_y + params.dashed_line_interval), border_width)
    for curr_x in np.arange(x + cell_size, x - border_width // 2, -params.dashed_line_interval * 2):
        pg.draw.line(surface, border_color, (curr_x, y + cell_size),
                     (curr_x - params.dashed_line_interval, y + cell_size), border_width)
    for curr_y in np.arange(y + cell_size, y - border_width // 2, -params.dashed_line_interval * 2):
        pg.draw.line(surface, border_color, (x, curr_y),
                     (x, curr_y - params.dashed_line_interval), border_width)


def draw_cell(surface: pg.Surface, params: DrawParams, x: int, y: int, cell_color: tuple[int], font_color: tuple[int], value: int, is_empty_cell: bool) -> None:
    rect = pg.draw.rect(surface, cell_color, (x, y,
                        params.cell_size, params.cell_size))
    text_surface_object = pg.font.SysFont(
        params.font_type, params.font_size, False, is_empty_cell).render(str(value), True, font_color)
    text_rect = text_surface_object.get_rect(center=rect.center)
    surface.blit(text_surface_object, text_rect)


def get_swapped_cell_position(current_grid: tuple[int], next_grid: tuple[int]) -> None:
    for i in range(len(current_grid)):
        if current_grid[i] != 0 and current_grid[i] != next_grid[i]:
            return i
    raise KeyError("Same grid!")


def draw_grid(surface: pg.Surface, params: DrawParams, current_grid: tuple[int], next_grid: tuple[int], target_grid: tuple[int]) -> None:
    idx = 0
    swapped_cell_idx = get_swapped_cell_position(
        current_grid, next_grid) if next_grid else -1

    surface.fill(params.background_color)

    for y in np.arange(params.margin, params.screen_size - params.margin, params.cell_size + params.margin):
        for x in np.arange(params.margin, params.screen_size - params.margin, params.cell_size + params.margin):
            # leave empty cell without border if grid is final
            if current_grid[idx] == 0 and swapped_cell_idx == -1:
                pass
            elif current_grid[idx] == 0:
                draw_cell(surface, params, x, y,
                          params.background_color, params.font_color_for_empty_cell, current_grid[swapped_cell_idx] if swapped_cell_idx >= 0 else 0, True)
                draw_dashed_border(surface, params, x, y)
            else:
                if swapped_cell_idx == idx:  # cell in motion
                    draw_cell(surface, params, x, y,
                              params.cell_in_motion_color, params.font_color_for_value_cell, current_grid[idx], False)
                elif current_grid[idx] == target_grid[idx]:  # cell in correct position
                    draw_cell(surface, params, x, y,
                              params.cell_in_correct_position, params.font_color_for_value_cell, current_grid[idx], False)
                elif current_grid[idx] != target_grid[idx]:  # cell in wrong position
                    draw_cell(surface, params, x, y, params.cell_in_wrong_position,
                              params.font_color_for_value_cell, current_grid[idx], False)
                else:
                    raise ValueError("Strange cell")

            idx += 1


def run_visualizer(sequence: list[tuple[int]]) -> None:
    pg.init()
    pg.display.set_caption('n-puzzle @ crendeha')
    params = DrawParams(len(sequence), int(len(sequence[0]) ** 0.5))
    surface = pg.display.set_mode(
        (params.screen_size, params.screen_size))

    for i in range(len(sequence)):
        draw_grid(surface, params, sequence[i], sequence[i + 1]
                  if i + 1 < len(sequence) else None, sequence[-1])
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        time.sleep(params.sleep_time if i + 1 <
                   len(sequence) else 2 * params.sleep_time)
