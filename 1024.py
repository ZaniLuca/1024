"""
1024 game by Luca Zani
https://github.com/ZaniLuca/1024

1024 è un videogioco libero a giocatore singolo il cui obiettivo è quello di far scorrere le piastrelle su una griglia,
unirle e creare una tessera con il numero 1024 i controlli sono molto semplici e intuitivi:
si utilizzano le frecce direzionali per far "scivolare" i blocchi che,
qualora vengano a contatto con blocchi dello stesso valore si uniranno.
"""

import pygame

pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()

from Square import *
import random


class Game:
    def __init__(self):
        self.width = 400
        self.height = 500
        self.w = 100
        self.fps = 15
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.logo = pygame.image.load('assets/Logo.ico')
        self.font_38 = pygame.font.Font('assets/ClearSans.ttf', 38)
        self.font_24 = pygame.font.Font('assets/ClearSans.ttf', 24)
        self.clak = pygame.mixer.music.load('assets/clak.wav')
        self.grid = []
        self.score = 0
        self.highscore = 0
        self.lost = False

        pygame.display.set_caption('1024 in python')
        pygame.display.set_icon(self.logo)

    def run(self):
        self.create_grid()
        self.random2()
        self.random2()
        clock = pygame.time.Clock()
        run = True
        while run:
            moved_list = []
            clock.tick(self.fps)
            # TODO implement highscore
            score_text = self.font_38.render('Score:', True, TEXT_COLOR1)
            points_text = self.font_38.render(str(self.score), True, TEXT_COLOR1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if not self.lost:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            for line in range(3):
                                for square in range(len(self.grid)):
                                    move_dir = (0, -1)
                                    moved, points = self.grid[square].move(self.grid, move_dir)
                                    moved_list.append(moved)
                                    self.score += points
                            if True in moved_list:
                                self.random2()
                            self.check_lost()
                        elif event.key == pygame.K_RIGHT:
                            for line in range(3):
                                for square in range(len(self.grid) - 1, -1, -1):
                                    move_dir = (1, 0)
                                    moved, points = self.grid[square].move(self.grid, move_dir)
                                    moved_list.append(moved)
                                    self.score += points
                            if True in moved_list:
                                self.random2()
                            self.check_lost()
                        elif event.key == pygame.K_DOWN:
                            for line in range(3):
                                for square in range(len(self.grid) - 1, -1, -1):
                                    move_dir = (0, 1)
                                    moved, points = self.grid[square].move(self.grid, move_dir)
                                    moved_list.append(moved)
                                    self.score += points
                            if True in moved_list:
                                self.random2()
                            self.check_lost()
                        elif event.key == pygame.K_LEFT:
                            for line in range(3):
                                for square in range(len(self.grid)):
                                    move_dir = (-1, 0)
                                    moved, points = self.grid[square].move(self.grid, move_dir)
                                    moved_list.append(moved)
                                    self.score += points
                            if True in moved_list:
                                self.random2()
                            self.check_lost()
                else:
                    mouse_pressed = pygame.mouse.get_pressed()
                    pos = pygame.mouse.get_pos()
                    left_click = mouse_pressed[0]
                    if left_click == 1:
                        if 142 < pos[0] < 262:
                            if 230 < pos[1] < 270:
                                self.restart()
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
            self.grid[i].display_value(self.screen, self.font_38, self.w)
        if self.lost:
            transp_fg = pygame.Surface((400, 400))
            transp_fg.fill((240, 192, 0))
            transp_fg.set_alpha(128)
            # Lost Text
            lost_text = self.font_38.render('You Lost', True, TEXT_COLOR2)
            lost_text_rect = lost_text.get_rect(center=(400 // 2, 400 // 2 - 30))
            # Retry box
            retry_rect = pygame.Rect(400 // 2 - 57, 400 // 2 + 30, 120, 40)
            retry_text = self.font_24.render('Retry', True, TEXT_COLOR2)
            retry_text_rect = retry_text.get_rect(center=(400 // 2 + 4, 400 // 2 + 48))
            # Blitting
            self.screen.blit(transp_fg, (0, 0))
            self.screen.blit(lost_text, lost_text_rect)
            pygame.draw.rect(self.screen, TEXT_COLOR1, retry_rect)
            self.screen.blit(retry_text, retry_text_rect)
        self.screen.blit(self.logo, (335, 435))
        self.screen.blit(score_text, (30, 425))
        self.screen.blit(points_text, (150, 425))
        pygame.display.flip()

    def create_grid(self):
        """
        Creates the whole grid
        :return: None
        """
        for i in range(4):
            for j in range(4):
                square = Square(i, j)
                self.grid.append(square)

    def random2(self):
        """
        Tries 1000 times to place a 2 in the grid
        :return: None
        """
        tries = 0
        found = 0
        while found == 0 and tries < 1000:
            i = int(random.randrange(0, 4))
            j = int(random.randrange(0, 4))
            for cell in range(len(self.grid)):
                if self.grid[cell].i == i and self.grid[cell].j == j and self.grid[cell].value == 0:
                    found = 1
                    self.grid[cell].value = 2
                    self.grid[cell].new = True
                else:
                    tries += 1

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

    def restart(self):
        self.grid = []
        self.lost = False
        self.score = 0
        self.create_grid()
        self.random2()
        self.random2()


game = Game()
game.run()
