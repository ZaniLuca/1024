#!/usr/local/bin/python3.8
import pygame

from colors import *


class Square:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.value = 0
        self.new = False

    def show(self, W, screen):
        """
        Displays the square with its specific color
        :param W: int
        :param screen: surface
        :return: None
        """
        x = self.i * W
        y = self.j * W
        rect = pygame.Rect(x, y, W, W)
        pygame.draw.rect(screen, BG, rect)
        if self.new:
            if self.value > 0:
                rect.inflate(-50, -50)
                pygame.draw.rect(screen, SqrColors[self.value], rect)
                rect.inflate(10, 10)
                pygame.draw.rect(screen, SqrColors[self.value], rect)
            self.new = False
        else:
            if self.value > 0:
                pygame.draw.rect(screen, SqrColors[self.value], rect)
            pygame.draw.rect(screen, BORDER, rect, 10)

    def display_value(self, screen, font, W):
        """
        Display the value of the square
        :param screen: surface
        :param font: font
        :param W: int
        :return: None
        """
        if self.value > 0:
            textsurface = font.render(str(self.value), True, TEXT_COLOR1)
            if self.value > 4:
                textsurface = font.render(str(self.value), True, TEXT_COLOR2)
            text_rect = textsurface.get_rect(center=(W * self.i + 1 // 2 + 50, W * self.j + 1 // 2 + 50))
            screen.blit(textsurface, text_rect)

    def search_index(self, i, j, grid):
        """
        Search the cell's index in the vector
        based on the given parameters
        :param i: int
        :param j: int
        :param grid: list
        :return: int
        """
        for square in range(len(grid)):
            if grid[square].i == i and grid[square].j == j:
                return square
        return -1

    def move(self, grid, can_merge, move_dir):
        """
        moves every cell to the given destination,
        can merge cells into each others
        :param grid: list
        :param can_merge: bool
        :param move_dir: tuple
        :return: bool (True if we moved a cell)
        :return: bool (True if we merged a cell into another)
        :return: int  (points)
        """
        index = self.search_index(self.i + move_dir[0], self.j + move_dir[1], grid)
        if index >= 0:
            cell = grid[index]
            if self.value == cell.value and cell.value != 0 and can_merge and not self.new:
                cell.value *= 2
                cell.new = True
                self.value = 0
                pygame.mixer.music.play()
                return True, True, cell.value
            elif cell.value == 0:
                cell.value = self.value
                self.value = 0
                if cell.value == 0:
                    return False, False, 0
                return True, False, 0
        return False, False, 0
