import pygame 
import sys
import random

pygame.init()

SW, SH = 800, 800

Font = pygame.font.Font("font.ttf", 100)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake Test nr.1")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(10)