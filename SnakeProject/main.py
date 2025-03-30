import pygame 
import sys
import random

pygame.init()

SW, SH = 768, 768

Rozmiar_Siatki = 32
Font = pygame.font.Font("font.ttf", Rozmiar_Siatki*2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake Test nr.1")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x = Rozmiar_Siatki
        self.y = Rozmiar_Siatki
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, Rozmiar_Siatki, Rozmiar_Siatki)
        self.body = [pygame.Rect(self.x-Rozmiar_Siatki, self.y, Rozmiar_Siatki, Rozmiar_Siatki)]
        self.dead = False
    def update(self):
        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x = self.body[i+1].x
            self.body[i].y = self.body[i+1].y
        self.head.x += self.xdir * Rozmiar_Siatki
        self.head.y += self.ydir * Rozmiar_Siatki
        self.body.remove(self.head)

def Siatka():
    for x in range(0, SW, Rozmiar_Siatki):
        for y in range(0, SH, Rozmiar_Siatki):
            rect = pygame.Rect(x, y, Rozmiar_Siatki, Rozmiar_Siatki)
            pygame.draw.rect(screen, (157, 157, 157), rect, 1)

Siatka()
snake = Snake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.xdir = -1
                snake.ydir = 0
            elif event.key == pygame.K_RIGHT:
                snake.xdir = 1
                snake.ydir = 0
            elif event.key == pygame.K_UP:
                snake.xdir = 0
                snake.ydir = -1
            elif event.key == pygame.K_DOWN:
                snake.xdir = 0
                snake.ydir = 1
    snake.update()

    screen.fill('black')
    Siatka()

    pygame.draw.rect(screen, "green", snake.head)

    for szescian in snake.body:
        pygame.draw.rect(screen, "green", szescian)

    pygame.display.update()
    clock.tick(10)