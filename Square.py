import pygame
from Colors import *


class Square:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.value = 0
        self.new = False

    def show(self, w, screen):
        """
        Displays the square with its specific color
        :param w: int
        :param screen: surface
        :return: None
        """
        x = self.i * w
        y = self.j * w
        rect = pygame.Rect(x, y, w, w)
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

    def display_value(self, screen, font, w):
        """
        Display the value of the square
        :param screen: surface
        :param font: font
        :param w: int
        :return: None
        """
        if self.value > 0:
            textsurface = font.render(str(self.value), True, TEXT_COLOR1)
            if self.value > 4:
                textsurface = font.render(str(self.value), True, TEXT_COLOR2)
            text_rect = textsurface.get_rect(center=(w * self.i + 1 // 2 + 50, w * self.j + 1 // 2 + 50))
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

    def move(self, grid, move_dir):
        """
        moves every cell to the given destination,
        can merge cells into each others
        :param grid: list
        :param move_dir: tuple
        :return: bool (True if we moved a cell)
        :return: int  (points)
        """
        index = self.search_index(self.i + move_dir[0], self.j + move_dir[1], grid)
        if index >= 0:
            cell = grid[index]
            if self.value == cell.value and cell.value != 0 and not self.new:
                cell.value *= 2
                cell.new = True
                self.value = 0
                pygame.mixer.music.play()
                return True, cell.value
            elif cell.value == 0:
                cell.value = self.value
                self.value = 0
                if cell.value == 0:
                    return False, 0
                return True, 0
        return False, 0
