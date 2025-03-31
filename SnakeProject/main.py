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

snake_head_img = pygame.image.load("snake.head.png").convert_alpha()
snake_tail_img = pygame.image.load("snake.tail.png").convert_alpha()
snake_body_img = pygame.image.load("snake.body.gif").convert_alpha()

snake_head_img = pygame.transform.scale(snake_head_img, (Rozmiar_Siatki, Rozmiar_Siatki))
snake_body_img = pygame.transform.scale(snake_body_img, (Rozmiar_Siatki, Rozmiar_Siatki))
snake_tail_img = pygame.transform.scale(snake_tail_img, (Rozmiar_Siatki, Rozmiar_Siatki))



class Snake:
    def __init__(self):
        self.x = Rozmiar_Siatki
        self.y = Rozmiar_Siatki
        self.xdir = 1
        self.ydir = 0
        self.angle = 270
        self.head = pygame.Rect(self.x, self.y, Rozmiar_Siatki, Rozmiar_Siatki)
        self.body = [
            pygame.Rect(self.x-Rozmiar_Siatki, self.y, Rozmiar_Siatki, Rozmiar_Siatki)
            for i in range(1,3)
            ]
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
            pygame.draw.rect(screen, (0,0,0), rect, 1)

Siatka()
snake = Snake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake.xdir = -1 
                snake.angle = 90
                snake.ydir = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake.xdir = 1
                snake.angle = 270
                snake.ydir = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                snake.xdir = 0
                snake.ydir = -1
                snake.angle = 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake.xdir = 0
                snake.ydir = 1
                snake.angle = 180
    snake.update()

    screen.fill('black')
    Siatka()

    rotacja_t = pygame.transform.rotate(snake_tail_img, snake.angle)
    rotacja_b = pygame.transform.rotate(snake_body_img, snake.angle)
    rotacja_g = pygame.transform.rotate(snake_head_img, snake.angle)
    screen.blit(rotacja_g, snake.head)

    for cialo  in snake.body[:-1]:
        screen.blit(rotacja_b, cialo)
        
    if snake.body:
        screen.blit(rotacja_t, snake.body[-1])

    pygame.display.update()
    clock.tick(10)