#!/usr/local/bin/python3.8
import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

from square import *
import random
import os


class Game:
    def __init__(self):
        self.width = 400
        self.height = 500
        self.w = 100
        self.fps = 30
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.logo = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Logo.ico'))
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), 'ClearSans.ttf'), 38)
        self.clak = pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'clak.wav'))
        self.grid = []
        self.score = 0
        self.lost = False

        pygame.display.set_caption('1024 in python')
        pygame.display.set_icon(self.logo)

    def run(self):
        self.createGrid()
        # Generate 2 cells
        self.random2()
        self.random2()
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.fps)

            self.getPoints()
            score_text = self.font.render('Score:', True, TEXT_COLOR1)
            points_text = self.font.render(str(self.score), True, TEXT_COLOR1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if not self.lost:
                    if event.type == pygame.KEYDOWN:
                        # TODO rewrite loop
                        if event.key == pygame.K_UP:
                            for square in range(len(self.grid)):
                                for square2 in range(len(self.grid)):
                                    moved = self.grid[square2].checkTop(self.grid)
                            if moved:
                                self.random2()
                            self.check_lost()
                        elif event.key == pygame.K_RIGHT:
                            for square in range(len(self.grid)):
                                for square2 in range(len(self.grid)):
                                    moved = self.grid[square2].checkRight(self.grid)
                            if moved:
                                self.random2()
                            self.check_lost()
                        elif event.key == pygame.K_DOWN:
                            for square in range(len(self.grid)):
                                for square2 in range(len(self.grid)):
                                    moved = self.grid[square2].checkDown(self.grid)
                            if moved:
                                self.random2()
                            self.check_lost()
                        elif event.key == pygame.K_LEFT:
                            for square in range(len(self.grid)):
                                for square2 in range(len(self.grid)):
                                    moved = self.grid[square2].checkLeft(self.grid)
                            if moved:
                                self.random2()
                            self.check_lost()
            self.update(score_text, points_text)
        pygame.quit()

    def update(self, score_text, points_text):
        """
        Updates the game grid,places the score text,
        the point text and the logo
        :param score_text: font-surface
        :param points_text: font-surface
        :return: None
        """
        self.screen.fill((255, 255, 255))
        for i in range(len(self.grid)):
            self.grid[i].show(self.w, self.screen)
            self.grid[i].showValue(self.screen, self.font, self.w)
        self.screen.blit(self.logo, (335, 435))
        self.screen.blit(score_text, (30, 425))
        self.screen.blit(points_text, (150, 425))
        pygame.display.flip()

    def createGrid(self):
        """
        Creates the whole grid
        :return: None
        """
        for i in range(4):
            for j in range(4):
                square = Square(i, j)
                self.grid.append(square)

    def pickRandomSquare(self):
        """
        Gets a random square to place the new cell
        containing 2
        :return: 2 random integers between 0 and 4
        """
        random_i = int(random.randrange(0, 4))
        random_j = int(random.randrange(0, 4))

        return random_i, random_j

    def random2(self):
        """
        Tries 1000 times to place a 2 in the grid
        :return: None
        """
        tries = 0
        found = 0
        while found == 0 and tries < 1000:
            i, j = self.pickRandomSquare()
            for cell in range(len(self.grid)):
                if self.grid[cell].i == i and self.grid[cell].j == j and self.grid[cell].value == 0:
                    found = 1
                    self.grid[cell].value = 2
                else:
                    tries += 1

    def getPoints(self):
        """
        Calculate the score
        :return: None
        """
        self.score = 0
        for cell in range(len(self.grid)):
            self.score += 2 * self.grid[cell].value

    def check_lost(self):
        """
        Checks if the player loses
        :return: None
        """
        filled_cells = 0
        for square in range(len(self.grid)):
            if self.grid[square].value > 0:
                filled_cells += 1
            if filled_cells == 16:
                self.lost = True


game = Game()
game.run()
