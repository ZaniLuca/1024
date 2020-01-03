#!/usr/local/bin/python3.8
import pygame
import random
import os

WIDTH = 400
HEIGHT = 500
W = 100
FPS = 30

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

Sqr2 = (245, 245, 245)
Sqr4 = (245, 245, 220)
Sqr8 = (255, 160, 122)
Sqr16 = (255, 127, 80)
Sqr32 = (255, 99, 71)
Sqr64 = (255, 0, 0)
Sqr128 = (255, 250, 96)
Sqr256 = (240, 224, 80)
Sqr512 = (240, 224, 16)
Sqr1024 = (250, 208, 0)

BG = (205,192,180)
BORDER = (187,173,160)
TEXT_COLOR1 = (119,110,101)
TEXT_COLOR2 = (249,246,242)

grid = []
score = 0

pygame.init()
pygame.mixer.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

logo = pygame.image.load(os.path.join(os.path.dirname(__file__),'Logo.ico'))

pygame.display.set_icon(logo)
pygame.display.set_caption("1024 in python")

clock = pygame.time.Clock()

font = pygame.font.Font(os.path.join(os.path.dirname(__file__),'ClearSans.ttf'),38)

def creaGriglia():
    for i in range(4):
        for j in range(4):
            square = Square(i,j)
            grid.append(square)
def pickRandomSquare():
    random_i = int(random.randrange(0,4))
    random_j = int(random.randrange(0,4))
    return random_i,random_j
def cercaIndice(i,j):
    for square in range(len(grid)):
        if grid[square].i == i and grid[square].j == j:
            return square
    return -1
def random2():
    tentativi = 0
    trovato = 0
    while trovato == 0 and tentativi < 1000:
        i,j = pickRandomSquare()
        for cell in range(len(grid)):
            if grid[cell].i == i and grid[cell].j == j and grid[cell].value == 0:
                trovato = 1
                grid[cell].value = 2
            else:
                tentativi += 1
def contaPunti(punti):
    punti = 1
    for cell in range(len(grid)):
        punti += 2*grid[cell].value
    return punti-1
class Square:
    def __init__(self,i,j):
        self.i = i
        self.j = j
        self.value = 0
    def show(self):
        x = self.i * W
        y = self.j * W
        rect = pygame.Rect(x,y,W,W)
        pygame.draw.rect(screen,BG,rect)
        if self.value == 2:
            pygame.draw.rect(screen,Sqr2,rect)
        elif self.value == 4:
            pygame.draw.rect(screen,Sqr4,rect)
        elif self.value == 8:
            pygame.draw.rect(screen,Sqr8,rect)
        elif self.value == 16:
            pygame.draw.rect(screen,Sqr16,rect)
        elif self.value == 32:
            pygame.draw.rect(screen,Sqr32,rect)
        elif self.value == 64:
            pygame.draw.rect(screen,Sqr64,rect)
        elif self.value == 128:
            pygame.draw.rect(screen,Sqr128,rect)
        elif self.value == 256:
            pygame.draw.rect(screen,Sqr256,rect)
        elif self.value == 512:
            pygame.draw.rect(screen,Sqr512,rect)
        elif self.value == 1024:
            pygame.draw.rect(screen,Sqr1024,rect)
        pygame.draw.rect(screen,BORDER,rect,10)
    def showValue(self):
        if self.value > 0:
            textsurface = font.render(str(self.value), True, TEXT_COLOR1)
            if self.value > 4:
                textsurface = font.render(str(self.value), True, TEXT_COLOR2)
            text_rect = textsurface.get_rect(center=(W*self.i+1//2+50, W*self.j+1//2+50))
            screen.blit(textsurface, text_rect)
    def checkTop(self):
        index = cercaIndice(self.i,self.j-1)
        if index >= 0:
            top = grid[index]
            if self.value == top.value:
                #---- Set Value
                top.value *= 2
                self.value = 0
            elif top.value == 0:
                #---- Merge
                top.value = self.value
                self.value = 0
    def checkRight(self):
        index = cercaIndice(self.i+1,self.j)
        if index >= 0:
            right = grid[index]
            if self.value == right.value:
                #---- Set Value
                right.value *= 2
                self.value = 0
            elif right.value == 0:
                #---- Merge
                right.value = self.value
                self.value = 0
    def checkLeft(self):
        index = cercaIndice(self.i-1,self.j)
        if index >= 0:
            left = grid[index]
            if self.value == left.value:
                #---- Set Value
                left.value *= 2
                self.value = 0
            elif left.value == 0:
                #---- Merge
                left.value = self.value
                self.value = 0
    def checkDown(self):
        index = cercaIndice(self.i,self.j+1)
        if index >= 0:
            down = grid[index]
            if self.value == down.value:
                #---- Set Value
                down.value *= 2
                self.value = 0
            elif down.value == 0:
                #---- Merge
                down.value = self.value
                self.value = 0
creaGriglia()
random2()

run = True
while run:
    clock.tick(FPS)
    newscore = contaPunti(score)
    score = newscore
    score_text = font.render('Score:', True, TEXT_COLOR1)
    points_text = font.render(str(score), True, TEXT_COLOR1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                for square in range(len(grid)):
                    for square in range(len(grid)):
                        grid[square].checkTop()
                random2()
            elif event.key == pygame.K_RIGHT:
                for square in range(len(grid)):
                    for square in range(len(grid)):
                        grid[square].checkRight()
                random2()
            elif event.key == pygame.K_DOWN:
                for square in range(len(grid)):
                    for square in range(len(grid)):
                        grid[square].checkDown()
                random2()
            elif event.key == pygame.K_LEFT:
                for square in range(len(grid)):
                    for square in range(len(grid)):
                        grid[square].checkLeft()
                random2()
    screen.fill(Sqr2)
    for i in range(len(grid)):
        grid[i].show()
        grid[i].showValue()
    screen.blit(logo,(335,435))
    screen.blit(score_text,(30,425))
    screen.blit(points_text,(150,425))
    pygame.display.flip()
pygame.quit()
