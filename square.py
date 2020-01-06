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
            # TODO better popup animation
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

    def showValue(self, screen, font, W):
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

    def checkTop(self, grid, can_merge):
        """
        Check for the top,right,bottom,left cells
        :param grid: list
        :param can_merge: bool
        :return: bool (True if we moved a cell)
        :return: bool (True if we merged a cell into another)
        :return: int  (points)
        """
        index = self.search_index(self.i, self.j - 1, grid)
        if index >= 0:
            top = grid[index]
            if self.value == top.value and top.value != 0 and can_merge:
                top.value *= 2
                top.new = True
                self.value = 0
                pygame.mixer.music.play()
                return True, True, top.value
            elif top.value == 0:
                top.value = self.value
                self.value = 0
                if top.value == 0:
                    return False, False, 0
                return True, False, 0
        return False, False, 0

    def checkRight(self, grid, can_merge):
        index = self.search_index(self.i + 1, self.j, grid)
        if index >= 0:
            right = grid[index]
            if self.value == right.value and right.value != 0 and can_merge:
                right.value *= 2
                right.new = True
                self.value = 0
                pygame.mixer.music.play()
                return True, True, right.value
            elif right.value == 0:
                right.value = self.value
                self.value = 0
                if right.value == 0:
                    return False, False, 0
                return True, False, 0
        return False, False, 0

    def checkLeft(self, grid, can_merge):
        index = self.search_index(self.i - 1, self.j, grid)
        if index >= 0:
            left = grid[index]
            if self.value == left.value and left.value != 0 and can_merge:
                left.value *= 2
                left.new = True
                self.value = 0
                pygame.mixer.music.play()
                return True, True, left.value
            elif left.value == 0:
                left.value = self.value
                self.value = 0
                if left.value == 0:
                    return False, False, 0
                return True, False, 0
        return False, False, 0

    def checkDown(self, grid, can_merge):
        index = self.search_index(self.i, self.j + 1, grid)
        if index >= 0:
            down = grid[index]
            if self.value == down.value and down.value != 0 and can_merge:
                down.value *= 2
                down.new = True
                self.value = 0
                pygame.mixer.music.play()
                return True, True, down.value
            elif down.value == 0:
                down.value = self.value
                self.value = 0
                if down.value == 0:
                    return False, False, 0
                return True, False, 0
        return False, False, 0
