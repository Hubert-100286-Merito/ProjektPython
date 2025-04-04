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

# Tekstury Węża
snake_head_img = pygame.image.load("snake.head.png").convert_alpha()
snake_tail_img = pygame.image.load("snake.tail.png").convert_alpha()
snake_body_img = pygame.image.load("snake.body.gif").convert_alpha()
snake_body_corner_img = pygame.image.load("snake.body.corner.png").convert_alpha()
snake_tail_corner_img = pygame.image.load("snake.tail.corner.png").convert_alpha()

# Skalowanie tekstur
snake_head_img = pygame.transform.scale(snake_head_img, (Rozmiar_Siatki, Rozmiar_Siatki))
snake_body_img = pygame.transform.scale(snake_body_img, (Rozmiar_Siatki, Rozmiar_Siatki))
snake_tail_img = pygame.transform.scale(snake_tail_img, (Rozmiar_Siatki, Rozmiar_Siatki))
snake_body_corner_img = pygame.transform.scale(snake_body_corner_img, (Rozmiar_Siatki, Rozmiar_Siatki))
snake_tail_corner_img = pygame.transform.scale(snake_tail_corner_img, (Rozmiar_Siatki, Rozmiar_Siatki))

class Snake:
    def __init__(self):
        self.x = Rozmiar_Siatki
        self.y = Rozmiar_Siatki
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, Rozmiar_Siatki, Rozmiar_Siatki)
        # 4 segmenty ciała + oddzielny ogon
        self.body = [
            pygame.Rect(self.x - Rozmiar_Siatki * (i+1), self.y, Rozmiar_Siatki, Rozmiar_Siatki)
            for i in range(2)
        ]
        self.tail = pygame.Rect(self.x - Rozmiar_Siatki * 5, self.y, Rozmiar_Siatki, Rozmiar_Siatki)
        self.dead = False
        self.prev_directions = []
    
    def update(self):
        # Zapamiętanie starej pozycji głowy
        old_head_pos = (self.head.x, self.head.y)
        
        # Przesunięcie głowy
        self.head.x += self.xdir * Rozmiar_Siatki
        self.head.y += self.ydir * Rozmiar_Siatki
        
        # Zapamiętanie starej pozycji ostatniego segmentu ciała
        if len(self.body) > 0:
            old_last_body_pos = (self.body[-1].x, self.body[-1].y)
        
        # Przesuwanie segmentów ciała (od tyłu)
        if self.body:
            for i in range(len(self.body)-1, 0, -1):
                self.body[i].x = self.body[i-1].x
                self.body[i].y = self.body[i-1].y
            
            # Pierwszy segment przejmuje starą pozycję głowy
            self.body[0].x = old_head_pos[0]
            self.body[0].y = old_head_pos[1]
        
        # Ogon przejmuje STARĄ pozycję ostatniego segmentu ciała
        if len(self.body) > 0:
            self.tail.x = old_last_body_pos[0]
            self.tail.y = old_last_body_pos[1]

def Siatka():
    for x in range(0, SW, Rozmiar_Siatki):
        for y in range(0, SH, Rozmiar_Siatki):
            rect = pygame.Rect(x, y, Rozmiar_Siatki, Rozmiar_Siatki)
            pygame.draw.rect(screen, (0,0,0), rect, 1)

def get_corner_angle(prev_dir, current_dir):
    """Oblicza kąt obrotu dla rogów"""
    direction_map = {
        (0, 1): 180,   # Góra -> Prawo
        (0, 3): 90,     # Góra -> Lewo
        (1, 0): 0,      # Prawo -> Góra
        (1, 2): 90,     # Prawo -> Dół
        (2, 1): 270,    # Dół -> Prawo
        (2, 3): 0,      # Dół -> Lewo
        (3, 0): 270,    # Lewo -> Góra
        (3, 2): 180     # Lewo -> Dół
    }
    return direction_map.get((prev_dir, current_dir), 0)

def get_direction(xdir, ydir):
    """Konwertuje xdir/ydir na indeks kierunku"""
    if ydir == -1: return 0   # Góra
    if xdir == 1: return 1    # Prawo
    if ydir == 1: return 2    # Dół
    if xdir == -1: return 3   # Lewo
    return 0

Siatka()
snake = Snake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            old_xdir, old_ydir = snake.xdir, snake.ydir
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if snake.xdir != 1:  # Zapobiega zawracaniu o 180°
                    snake.xdir = -1 
                    snake.ydir = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if snake.xdir != -1:
                    snake.xdir = 1
                    snake.ydir = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if snake.ydir != 1:
                    snake.xdir = 0
                    snake.ydir = -1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if snake.ydir != -1:
                    snake.xdir = 0
                    snake.ydir = 1
            
            # Jeżeli wąż skręca to zapisuje zmianę kierunku
            if (snake.xdir != old_xdir) or (snake.ydir != old_ydir):
                snake.prev_directions.append((old_xdir, old_ydir, snake.xdir, snake.ydir))
    
    snake.update()

    screen.fill('black')
    Siatka()

    # Rotacja głowy
    if snake.xdir == 1:
        head_angle = 270
    elif snake.xdir == -1:
        head_angle = 90
    elif snake.ydir == -1:
        head_angle = 0
    else:
        head_angle = 180
    
    rotacja_g = pygame.transform.rotate(snake_head_img, head_angle)
    screen.blit(rotacja_g, snake.head)

    # Renderowanie segmentów ciała
    for i in range(len(snake.body)):
        current_img = snake_body_img
        rotation = 0
        is_corner = False
        corner_angle = 0
        
        if i < len(snake.body)-1:  # Bez ostatniego segment
            # Oblicz kierunki dla obecnego segmentu
            if i == 0:  # Segment za głową
                dx_prev = snake.body[i].x - snake.head.x
                dy_prev = snake.body[i].y - snake.head.y
            else:
                dx_prev = snake.body[i].x - snake.body[i-1].x
                dy_prev = snake.body[i].y - snake.body[i-1].y
            
            dx_next = snake.body[i+1].x - snake.body[i].x
            dy_next = snake.body[i+1].y - snake.body[i].y
            
            prev_dir = get_direction(
                1 if dx_prev > 0 else (-1 if dx_prev < 0 else 0),
                1 if dy_prev > 0 else (-1 if dy_prev < 0 else 0)
            )
            next_dir = get_direction(
                1 if dx_next > 0 else (-1 if dx_next < 0 else 0),
                1 if dy_next > 0 else (-1 if dy_next < 0 else 0)
            )
            
            # Jeśli kierunki się różnią, użyj tekstury rogu
            if prev_dir != next_dir:
                is_corner = True
                current_img = snake_body_corner_img
                corner_angle = get_corner_angle(prev_dir, next_dir)
        
        if is_corner:
            rotacja_b = pygame.transform.rotate(current_img, corner_angle)
        else:
            # Dla prostych segmentów
            if i == 0:  # Segment za głową
                rotation = head_angle
            else:
                dx = snake.body[i].x - snake.body[i-1].x
                dy = snake.body[i].y - snake.body[i-1].y
                if dx > 0: rotation = 270
                elif dx < 0: rotation = 90
                elif dy > 0: rotation = 180
                else: rotation = 0
            rotacja_b = pygame.transform.rotate(current_img, rotation)
        
        screen.blit(rotacja_b, snake.body[i])
    
    # Renderowanie ogona
    if len(snake.body) > 0:
        # Sprawdzanie czy ogon powinien być prosty czy zakrzywiony
        if len(snake.body) > 1:
            dx = snake.tail.x - snake.body[-1].x
            dy = snake.tail.y - snake.body[-1].y
            tail_dir = get_direction(
                1 if dx > 0 else (-1 if dx < 0 else 0),
                1 if dy > 0 else (-1 if dy < 0 else 0)
            )
            
            # Sprawdź czy ogon jest na zakręcie
            if len(snake.prev_directions) > 1 and abs(snake.prev_directions[-1][1]) != abs(snake.prev_directions[-1][2]):
                prev_dir = get_direction(snake.prev_directions[-1][2], snake.prev_directions[-1][3])
                current_dir = get_direction(snake.prev_directions[-1][0], snake.prev_directions[-1][1])
                tail_angle = get_corner_angle(prev_dir, current_dir)
                rotacja_t = pygame.transform.rotate(snake_tail_corner_img, tail_angle)
                snake.prev_directions.pop()  # Usuwanie Skrętu
            else:
                # Prosty ogon
                if dx > 0: tail_angle = 90
                elif dx < 0: tail_angle = 270
                elif dy > 0: tail_angle = 0
                else: tail_angle = 180
                rotacja_t = pygame.transform.rotate(snake_tail_img, tail_angle)
        else:
            # Tylko jeden segment - ogon podąża za głową
            dx = snake.tail.x - snake.head.x
            dy = snake.tail.y - snake.head.y
            if dx > 0: tail_angle = 90
            elif dx < 0: tail_angle = 270
            elif dy > 0: tail_angle = 0
            else: tail_angle = 180
            rotacja_t = pygame.transform.rotate(snake_tail_img, tail_angle)
        
        screen.blit(rotacja_t, snake.tail)

    pygame.display.update()
    clock.tick(10)