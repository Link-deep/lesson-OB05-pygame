import pygame
import sys
import random

pygame.init()
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Пинг-Понг")

# ФПС
clock = pygame.time.Clock()
fps = 60

# Параметры платформы № 1
paddle_width_1, paddle_height_1 = 10, 100
paddle_x_1 = (paddle_width_1 + 20)
paddle_y_1 = (screen_height - paddle_height_1) // 2
paddle_speed_1 = 6

# Параметры платформы № 2
paddle_width_2, paddle_height_2 = 10, 100
paddle_x_2 = (screen_width - 20 - paddle_width_2)
paddle_y_2 = (screen_height - paddle_height_2) // 2
paddle_speed_2 = 6

# Параметры мяча
ball_width, ball_height = 10, 10
ball_x = screen_width // 2 - ball_width // 2
ball_y = screen_height // 2 - ball_height // 2
ball_speed_x = 0
ball_speed_y = 0
ball_speed = 5

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Очки (сердца) игроков
score_player_1 = 0
score_player_2 = 0
max_score = 5

# Шрифт для отображения счета и текста
font = pygame.font.SysFont(None, 55)
font_large = pygame.font.SysFont(None, 75)

def draw_score():
    score_text = font.render(f"{score_player_1} : {score_player_2}", True, WHITE)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 20))

def draw_winner(winner_text):
    winner_display = font_large.render(winner_text, True, WHITE)
    screen.blit(winner_display, (screen_width // 2 - winner_display.get_width() // 2, screen_height // 2 - winner_display.get_height() // 2))

running = True
ball_moving = False
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_moving and not game_over:
                # Задаем случайное начальное направление мяча
                ball_speed_x = random.choice([-ball_speed, ball_speed])
                ball_speed_y = random.choice([-ball_speed, ball_speed])
                ball_moving = True

    # Движение платформ только если игра не окончена
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and paddle_y_1 > 0:
            paddle_y_1 -= paddle_speed_1
        if keys[pygame.K_DOWN] and paddle_y_1 < screen_height - paddle_height_1:
            paddle_y_1 += paddle_speed_1

        if keys[pygame.K_w] and paddle_y_2 > 0:
            paddle_y_2 -= paddle_speed_2
        if keys[pygame.K_s] and paddle_y_2 < screen_height - paddle_height_2:
            paddle_y_2 += paddle_speed_2

        # Движение мяча
        if ball_moving:
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Проверка столкновения мяча с верхней и нижней границами
            if ball_y <= 0 or ball_y >= screen_height - ball_height:
                ball_speed_y = -ball_speed_y

            # Проверка столкновения мяча с платформами
            if (ball_x <= paddle_x_1 + paddle_width_1 and paddle_y_1 < ball_y < paddle_y_1 + paddle_height_1) or \
               (ball_x + ball_width >= paddle_x_2 and paddle_y_2 < ball_y < paddle_y_2 + paddle_height_2):
                ball_speed_x = -ball_speed_x

            # Проверка выхода мяча за пределы экрана (игроки промахнулись)
            if ball_x < 0:
                score_player_2 += 1
                ball_moving = False
                ball_x = screen_width // 2 - ball_width // 2
                ball_y = screen_height // 2 - ball_height // 2
                ball_speed_x = 0
                ball_speed_y = 0

            elif ball_x > screen_width:
                score_player_1 += 1
                ball_moving = False
                ball_x = screen_width // 2 - ball_width // 2
                ball_y = screen_height // 2 - ball_height // 2
                ball_speed_x = 0
                ball_speed_y = 0

            # Проверка на победителя
            if score_player_1 >= max_score:
                game_over = True
                winner_text = "Игрок 1 выиграл!"
            elif score_player_2 >= max_score:
                game_over = True
                winner_text = "Игрок 2 выиграл!"

    # Очистка экрана
    screen.fill(BLACK)

    # Рисование объектов
    pygame.draw.rect(screen, WHITE, (paddle_x_1, paddle_y_1, paddle_width_1, paddle_height_1))
    pygame.draw.rect(screen, WHITE, (paddle_x_2, paddle_y_2, paddle_width_2, paddle_height_2))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_width, ball_height))
    draw_score()  # Отображение счета

    # Если игра окончена, выводим победителя
    if game_over:
        draw_winner(winner_text)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
