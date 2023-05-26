import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir las dimensiones de la ventana del juego
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# Definir los colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


# Crear la ventana del juego
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Definir el título de la ventana del juego
pygame.display.set_caption("Pacman")

# Definir la posición y el tamaño del jugador
player_x = 300
player_y = 600
player_width = 30
player_height = 30

# Definir la velocidad del jugador
player_speed = 5

# Definir la posición y el tamaño del enemigo
enemy_x = random.randint(0, WINDOW_WIDTH - player_width)
enemy_y = random.randint(50, 250)
enemy_width = 30
enemy_height = 30

# Definir la velocidad del enemigo
enemy_speed = 3

# Definir la puntuación del jugador
score = 0

# Definir la fuente y el tamaño del texto de la puntuación
font = pygame.font.SysFont(None, 30)

# Función para dibujar al jugador
def draw_player():
    pygame.draw.rect(game_window, YELLOW, [player_x, player_y, player_width, player_height])

# Función para dibujar al enemigo
def draw_enemy():
    pygame.draw.rect(game_window, BLUE, [enemy_x, enemy_y, enemy_width, enemy_height])

# Función para mostrar la puntuación del jugador
def show_score(score):
    score_text = font.render("Score: " + str(score), True, WHITE)
    game_window.blit(score_text, [10, 10])

# Bucle principal del juego
running = True
while running:

    # Manejar eventos de teclado y de cierre de la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player_x += player_speed
            elif event.key == pygame.K_UP:
                player_y -= player_speed
            elif event.key == pygame.K_DOWN:
                player_y += player_speed

    # Mover al enemigo
    enemy_y += enemy_speed
    if enemy_y > WINDOW_HEIGHT:
        enemy_x = random.randint(0, WINDOW_WIDTH - player_width)
        enemy_y = random.randint(50, 250)

    # Detectar colisión entre el jugador y el enemigo
    if player_x < enemy_x + enemy_width and player_x + player_width > enemy_x and player_y < enemy_y + enemy_height and player_y + player_height > enemy_y:
        score += 1
        enemy_x = random.randint(0, WINDOW_WIDTH - player_width)
        enemy_y = random.randint(50, 250)

    # Dibujar la ventana del juego
    game_window.fill(BLACK)
    draw_player()
    draw_enemy()
    show_score(score)
    pygame.display.update()

# Salir del juego
pygame
