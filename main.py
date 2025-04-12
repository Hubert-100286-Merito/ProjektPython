import pygame
import sys
import random
import pygame_gui

pygame.init()

SW, SH = 1024, 768
Rozmiar_Siatki = 32
Font = pygame.font.Font("font3.ttf", Rozmiar_Siatki * 2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Project: Snake")
manager = pygame_gui.UIManager((SW, SH))
clock = pygame.time.Clock()

# Tekstury węża
snake_head_img = pygame.image.load("snake.head.png").convert_alpha()
snake_tail_img = pygame.image.load("snake.tail.png").convert_alpha()
snake_body_img = pygame.image.load("snake.body.png").convert_alpha()
snake_body_corner_img = pygame.image.load("snake.body.corner.png").convert_alpha()
# Usunięto ładowanie tekstury skrętu ogona:
# snake_tail_corner_img = pygame.image.load("snake.tail.corner.png").convert_alpha()

# Skalowanie tekstur
snake_head_img = pygame.transform.scale(snake_head_img, (Rozmiar_Siatki, Rozmiar_Siatki))
snake_body_img = pygame.transform.scale(snake_body_img, (Rozmiar_Siatki, Rozmiar_Siatki))
snake_tail_img = pygame.transform.scale(snake_tail_img, (Rozmiar_Siatki, Rozmiar_Siatki))
snake_body_corner_img = pygame.transform.scale(snake_body_corner_img, (Rozmiar_Siatki, Rozmiar_Siatki))
# Usunięto skalowanie tekstury skrętu ogona:
# snake_tail_corner_img = pygame.transform.scale(snake_tail_corner_img, (Rozmiar_Siatki, Rozmiar_Siatki))

# Tekstura jabłka
apple_img = pygame.image.load("red apple.png").convert_alpha()
apple_img = pygame.transform.scale(apple_img, (Rozmiar_Siatki, Rozmiar_Siatki))

score = 0

# Nowe flagi gry: pauza i koniec gry
paused = False
game_over = False

# Referencje do nowych UI (panele i przyciski)
pause_panel = None
resume_button = None

death_panel = None
restart_button = None
quit_death_button = None

# Definicja klasy Snake
class Snake:
    def __init__(self):
        self.x = Rozmiar_Siatki
        self.y = Rozmiar_Siatki
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, Rozmiar_Siatki, Rozmiar_Siatki)
        self.body = [
            pygame.Rect(self.x - Rozmiar_Siatki * (i+1), self.y, Rozmiar_Siatki, Rozmiar_Siatki)
            for i in range(1)
        ]
        self.tail = pygame.Rect(self.x - Rozmiar_Siatki * 1, self.y, Rozmiar_Siatki, Rozmiar_Siatki)
        self.dead = False
        self.prev_directions = []
    
    def update(self):
        old_head_pos = (self.head.x, self.head.y)
        self.head.x += self.xdir * Rozmiar_Siatki
        self.head.y += self.ydir * Rozmiar_Siatki

        if len(self.body) > 0:
            old_last_body_pos = (self.body[-1].x, self.body[-1].y)
        
        if self.body:
            for i in range(len(self.body)-1, 0, -1):
                self.body[i].x = self.body[i-1].x
                self.body[i].y = self.body[i-1].y
            self.body[0].x = old_head_pos[0]
            self.body[0].y = old_head_pos[1]
        
        if len(self.body) > 0:
            self.tail.x = old_last_body_pos[0]
            self.tail.y = old_last_body_pos[1]

# Funkcja losująca jabłko
def losuj_jablko(snake):
    while True:
        x = random.randint(0, (SW - Rozmiar_Siatki) // Rozmiar_Siatki) * Rozmiar_Siatki
        y = random.randint(0, (SH - Rozmiar_Siatki) // Rozmiar_Siatki) * Rozmiar_Siatki
        new_rect = pygame.Rect(x, y, Rozmiar_Siatki, Rozmiar_Siatki)
        if new_rect.colliderect(snake.head) or any(b.colliderect(new_rect) for b in snake.body) or snake.tail.colliderect(new_rect):
            continue
        return new_rect

def Siatka():
    for x in range(0, SW, Rozmiar_Siatki):
        for y in range(0, SH, Rozmiar_Siatki):
            rect = pygame.Rect(x, y, Rozmiar_Siatki, Rozmiar_Siatki)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

def get_corner_angle(prev_dir, current_dir):
    direction_map = {
        (0, 1): 180,   # Góra -> Prawo
        (0, 3): 90,    # Góra -> Lewo
        (1, 0): 0,     # Prawo -> Góra
        (1, 2): 90,    # Prawo -> Dół
        (2, 1): 270,   # Dół -> Prawo
        (2, 3): 0,     # Dół -> Lewo
        (3, 0): 270,   # Lewo -> Góra
        (3, 2): 180    # Lewo -> Dół
    }
    return direction_map.get((prev_dir, current_dir), 0)

def get_direction(xdir, ydir):
    """Konwertuje xdir/ydir na indeks kierunku"""
    if ydir == -1: return 0   # Góra
    if xdir == 1: return 1    # Prawo
    if ydir == 1: return 2    # Dół
    if xdir == -1: return 3   # Lewo
    return 0

# Ustawienia przycisków w menu startowym
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((SW/2 - 60, SH/2 - 70), (120, 50)),
    text='Start',
    manager=manager
)

quit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((SW/2 - 60, SH/2 + 10), (120, 50)),
    text='Quit',
    manager=manager
)

# Zmienna stanu gry: False -> menu, True -> rozgrywka
game_active = False

# Przygotowanie obiektów gry (uruchamiamy je, gdy użytkownik kliknie "Start")
snake = None
apple = None

while True:
    time_delta = clock.tick(6) / 100.0  # Stała prędkość pętli

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Obsługa zdarzeń GUI
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Start z głównego menu
            if event.ui_element == start_button:
                game_active = True
                snake = Snake()
                apple = losuj_jablko(snake)
                start_button.hide()
                quit_button.hide()
            # Quit z głównego menu
            elif event.ui_element == quit_button:
                pygame.quit()
                sys.exit()
            # Resume przy pauzie
            elif resume_button is not None and event.ui_element == resume_button:
                paused = False
                if pause_panel is not None:
                    pause_panel.kill()  # Usuwamy panel pauzy razem z dziećmi
                    pause_panel = None
                    resume_button = None
            # Restart przy ekranie śmierci
            elif restart_button is not None and event.ui_element == restart_button:
                # Resetujemy grę
                game_active = True
                game_over = False
                score = 0
                snake = Snake()
                apple = losuj_jablko(snake)
                if death_panel is not None:
                    death_panel.kill()
                    death_panel = None
                    restart_button = None
                    quit_death_button = None
            # Quit z ekranu śmierci
            elif quit_death_button is not None and event.ui_element == quit_death_button:
                pygame.quit()
                sys.exit()
        
        # Obsługa klawisza P lub ESC do włączania/wyłączania pauzy (gdy gra trwa i nie ma game over)
        if game_active and not game_over and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_p, pygame.K_ESCAPE):
                paused = not paused
                if paused:
                    # Stwórz panel pauzy – przezroczysty overlay
                    pause_panel = pygame_gui.elements.UIPanel(
                        relative_rect=pygame.Rect(0, 0, SW, SH),
                        manager=manager,
                        object_id="#pause_panel"
                    )
                    # Ustawiamy kolor tła z przezroczystością
                    pause_panel.background_colour = pygame.Color(0, 0, 0, 150)
                    resume_button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((SW/2 - 60, SH/2 - 25), (120, 50)),
                        text='Resume',
                        manager=manager,
                        container=pause_panel
                    )
                else:
                    if pause_panel is not None:
                        pause_panel.kill()
                        pause_panel = None
                        resume_button = None
            # Sterowanie wężem gdy gra nie jest w pauzie
            elif not paused:
                old_xdir, old_ydir = snake.xdir, snake.ydir
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    if snake.xdir != 1:
                        snake.xdir = -1 
                        snake.ydir = 0
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if snake.xdir != -1:
                        snake.xdir = 1
                        snake.ydir = 0
                elif event.key in (pygame.K_UP, pygame.K_w):
                    if snake.ydir != 1:
                        snake.xdir = 0
                        snake.ydir = -1
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if snake.ydir != -1:
                        snake.xdir = 0
                        snake.ydir = 1

                if (snake.xdir != old_xdir) or (snake.ydir != old_ydir):
                    snake.prev_directions.append((old_xdir, old_ydir, snake.xdir, snake.ydir))
        
        manager.process_events(event)

    # Aktualizacja logiki gry tylko gdy gra trwa i nie jest pauzowana oraz nie ma game over
    if game_active and (not paused) and (not game_over):
        snake.update()

        # Sprawdzanie kolizji jabłka
        if snake.head.colliderect(apple):
            score += 1
            new_part = pygame.Rect(snake.tail.x, snake.tail.y, Rozmiar_Siatki, Rozmiar_Siatki)
            snake.body.append(new_part)
            apple = losuj_jablko(snake)
        
        # Sprawdzenie kolizji z końcami okna
        if snake.head.x < 0 or snake.head.x >= SW or snake.head.y < 0 or snake.head.y >= SH:
            snake.dead = True
        
        # Sprawdzenie kolizji z ciałem węża
        for segment in snake.body:
            if snake.head.colliderect(segment):
                snake.dead = True
                break
        
        # Jeśli wąż umarł, ustaw flagi i utwórz ekran śmierci
        if snake.dead:
            game_over = True
            game_active = False
            death_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(0, 0, SW, SH),
                manager=manager,
                object_id="#death_panel"
            )
            death_panel.background_colour = pygame.Color(0, 0, 0, 150)
            # Wyświetlanie punktacji po śmierci
            score_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((SW/2 - 100, SH/2 - 150), (200, 50)),
                text=f"Punkty: {score}",
                manager=manager,
                container=death_panel
            )    
            
            restart_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((SW/2 - 60, SH/2 - 50), (120, 50)),
                text='Restart',
                manager=manager,
                container=death_panel
            )
            quit_death_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((SW/2 - 60, SH/2 + 10), (120, 50)),
                text='Quit',
                manager=manager,
                container=death_panel
            )
    
    manager.update(time_delta)
    
    # Rysowanie ekranu
    screen.fill('black')
    Siatka()
    
    if game_active:
        # Rysujemy jabłko
        screen.blit(apple_img, apple)
        
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
            
            if i < len(snake.body) - 1:
                if i == 0:
                    dx_prev = snake.body[i].x - snake.head.x
                    dy_prev = snake.body[i].y - snake.head.y
                else:
                    dx_prev = snake.body[i].x - snake.body[i - 1].x
                    dy_prev = snake.body[i].y - snake.body[i - 1].y
                
                dx_next = snake.body[i + 1].x - snake.body[i].x
                dy_next = snake.body[i + 1].y - snake.body[i].y
                
                prev_dir = get_direction(
                    1 if dx_prev > 0 else (-1 if dx_prev < 0 else 0),
                    1 if dy_prev > 0 else (-1 if dy_prev < 0 else 0)
                )
                next_dir = get_direction(
                    1 if dx_next > 0 else (-1 if dx_next < 0 else 0),
                    1 if dy_next > 0 else (-1 if dy_next < 0 else 0)
                )
                
                if prev_dir != next_dir:
                    is_corner = True
                    current_img = snake_body_corner_img
                    corner_angle = get_corner_angle(prev_dir, next_dir)
            
            if is_corner:
                rotacja_b = pygame.transform.rotate(current_img, corner_angle)
            else:
                if i == 0:
                    rotation = head_angle
                else:
                    dx = snake.body[i].x - snake.body[i - 1].x
                    dy = snake.body[i].y - snake.body[i - 1].y
                    if dx > 0:
                        rotation = 270
                    elif dx < 0:
                        rotation = 90
                    elif dy > 0:
                        rotation = 180
                    else:
                        rotation = 0
                rotacja_b = pygame.transform.rotate(current_img, rotation)
            
            screen.blit(rotacja_b, snake.body[i])
        
        # Renderowanie ogona (bez skrętów)
        if len(snake.body) > 0:
            if len(snake.body) > 1:
                dx = snake.tail.x - snake.body[-1].x
                dy = snake.tail.y - snake.body[-1].y
                if dx > 0:
                    tail_angle = 90
                elif dx < 0:
                    tail_angle = 270
                elif dy > 0:
                    tail_angle = 0
                else:
                    tail_angle = 180
                rotacja_t = pygame.transform.rotate(snake_tail_img, tail_angle)
            else:
                dx = snake.tail.x - snake.head.x
                dy = snake.tail.y - snake.head.y
                if dx > 0:
                    tail_angle = 90
                elif dx < 0:
                    tail_angle = 270
                elif dy > 0:
                    tail_angle = 0
                else:
                    tail_angle = 180
                rotacja_t = pygame.transform.rotate(snake_tail_img, tail_angle)
            
            screen.blit(rotacja_t, snake.tail)
            score_text = Font.render(str(score), True, (255, 255, 255))
            screen.blit(score_text, (SW/2 - score_text.get_width() / 2, 20))
    else:
        # Ekran menu startowego lub w przypadku game over panele są rysowane przez manager
        if not game_over:
            title_text = Font.render("Project: Snake", True, (255, 255, 255))
            screen.blit(title_text, (SW/2 - title_text.get_width() / 2, SH/4))
    
    # Jeśli gra jest w pauzie, dodatkowo rysujemy przezroczysty overlay (na wypadek gdyby UI nie zajmowało całego ekranu)
    if paused and pause_panel is None:
        overlay = pygame.Surface((SW, SH), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
    
    manager.draw_ui(screen)
    
    pygame.display.update()
