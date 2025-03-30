import pygame 
import sys
import random

pygame.init()

SW, SH = 800, 800

Rozmiar_Siatki = 50
Font = pygame.font.Font("font.ttf", Rozmiar_Siatki*2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake Test nr.1")
clock = pygame.time.Clock()

def Siatka():
    for x in range(0, SW, Rozmiar_Siatki):
        for y in range(0, SH, Rozmiar_Siatki):
            rect = pygame.Rect(x, y, Rozmiar_Siatki, Rozmiar_Siatki)
            pygame.draw.rect(screen, (157, 157, 157), rect, 1)

Siatka()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(10)