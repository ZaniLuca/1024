#!/usr/local/bin/python3.8
import pygame

from colors import *


class Square:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.value = 0

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
        if self.value == 2:
            pygame.draw.rect(screen, Sqr2, rect)
        elif self.value == 4:
            pygame.draw.rect(screen, Sqr4, rect)
        elif self.value == 8:
            pygame.draw.rect(screen, Sqr8, rect)
        elif self.value == 16:
            pygame.draw.rect(screen, Sqr16, rect)
        elif self.value == 32:
            pygame.draw.rect(screen, Sqr32, rect)
        elif self.value == 64:
            pygame.draw.rect(screen, Sqr64, rect)
        elif self.value == 128:
            pygame.draw.rect(screen, Sqr128, rect)
        elif self.value == 256:
            pygame.draw.rect(screen, Sqr256, rect)
        elif self.value == 512:
            pygame.draw.rect(screen, Sqr512, rect)
        elif self.value == 1024:
            pygame.draw.rect(screen, Sqr1024, rect)
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

    def searchIndex(self, i, j, grid):
        """
        Search the cell's index in the vector
        based on the given parameters
        :param i: int
        :param j: int
        :param grid: vector
        :return: int
        """
        for square in range(len(grid)):
            if grid[square].i == i and grid[square].j == j:
                return square
        return -1

    def checkTop(self, grid):
        """
        Check for the top,right,bottom,left cells
        :param grid: vector
        :return: None
        """
        index = self.searchIndex(self.i, self.j - 1, grid)
        if index >= 0:
            top = grid[index]
            if self.value == top.value:
                # Set Value
                top.value *= 2
                self.value = 0
            elif top.value == 0:
                # Merge
                top.value = self.value
                self.value = 0

    def checkRight(self, grid):
        index = self.searchIndex(self.i + 1, self.j, grid)
        if index >= 0:
            right = grid[index]
            if self.value == right.value:
                right.value *= 2
                self.value = 0
            elif right.value == 0:
                right.value = self.value
                self.value = 0

    def checkLeft(self, grid):
        index = self.searchIndex(self.i - 1, self.j, grid)
        if index >= 0:
            left = grid[index]
            if self.value == left.value:
                left.value *= 2
                self.value = 0
            elif left.value == 0:
                left.value = self.value
                self.value = 0

    def checkDown(self, grid):
        index = self.searchIndex(self.i, self.j + 1, grid)
        if index >= 0:
            down = grid[index]
            if self.value == down.value:
                down.value *= 2
                self.value = 0
            elif down.value == 0:
                down.value = self.value
                self.value = 0
