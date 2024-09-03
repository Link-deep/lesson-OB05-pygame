import pygame
import sys

# Инициализация Pygame
pygame.init()

# Основные параметры окна
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Арканоид")

# Параметры кирпичей
brick_rows = 5
brick_cols = 10
brick_width = 50  # Фиксированная ширина кирпича
brick_height = 20
brick_gap = 5  # Промежуток между кирпичами

# Вычисление отступа слева и промежутков между кирпичами
total_bricks_width = brick_cols * brick_width + (brick_cols - 1) * brick_gap
side_padding = (screen_width - total_bricks_width) // 2  # Вычисление отступа слева и справа

# Список кирпичей с учетом отступа слева
bricks = [(side_padding + col * (brick_width + brick_gap), row * (brick_height + brick_gap)) for row in range(brick_rows) for col in range(brick_cols)]

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# ФПС
clock = pygame.time.Clock()
fps = 60

# Параметры платформы
paddle_width, paddle_height = 100, 10
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 20
paddle_speed = 6

# Параметры мяча
ball_radius = 8
ball_x = paddle_x + paddle_width // 2
ball_y = paddle_y - ball_radius
ball_speed_x = 4
ball_speed_y = -6
ball_moving = False  # Флаг для проверки, началось ли движение мяча

# Параметры жизней
lives = 3
heart_image = pygame.Surface((20, 20))
pygame.draw.polygon(heart_image, RED, [(10, 0), (20, 10), (10, 20), (0, 10)])  # Простейшее изображение сердца

# Флаг окончания игры
game_over = False

# Шрифт для отображения текста
font = pygame.font.SysFont(None, 55)

# Функция для отображения сообщения на экране
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Функция для отображения жизней
def draw_lives(surface, lives, x, y, heart_image):
    for i in range(lives):
        surface.blit(heart_image, (x + 30 * i, y))

# Запуск основного цикла игры
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_moving and not game_over:
                ball_moving = True  # Начать движение мяча при нажатии на пробел

    # Движение платформы
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

    # Обновление позиции мяча на платформе до начала движения
    if not ball_moving:
        ball_x = paddle_x + paddle_width // 2

    # Движение мяча
    if ball_moving and not game_over:
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Столкновение с краями экрана
        if ball_x <= 0 or ball_x >= screen_width:
            ball_speed_x = -ball_speed_x

        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        if ball_y >= screen_height:
            # Сброс мяча
            ball_moving = False
            ball_x = paddle_x + paddle_width // 2
            ball_y = paddle_y - ball_radius
            ball_speed_y = -6  # Устанавливаем начальную скорость вверх
            lives -= 1  # Уменьшение количества жизней
            if lives <= 0:
                game_over = True  # Если жизней больше нет, игра окончена

        brick_rects = [pygame.Rect(brick[0], brick[1], brick_width, brick_height) for brick in bricks]

        for i, brick_rect in enumerate(brick_rects):
            if brick_rect.collidepoint(ball_x, ball_y):
                bricks.pop(i)  # Удаление кирпича
                ball_speed_y = -ball_speed_y  # Изменение направления мяча
                break  # Выход после уничтожения одного кирпича, чтобы не удалять несколько за один кадр

        # Проверка на столкновение с платформой
        if paddle_x <= ball_x <= paddle_x + paddle_width and paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height:
            ball_speed_y = -abs(ball_speed_y)  # Убедитесь, что мяч отскакивает вверх

    # Проверка на окончание игры
    if not bricks and not game_over:
        game_over = True
        draw_text("Игра закончилась. Ты победил!", font, WHITE, screen, screen_width // 2, screen_height // 2)

    # Очистка экрана
    screen.fill(BLACK)

    # Отрисовка кирпичей
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, pygame.Rect(brick[0], brick[1], brick_width, brick_height))

    # Рисование объектов
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)

    # Отображение жизней
    draw_lives(screen, lives, 10, 10, heart_image)

    # Отображение сообщения, если игра закончена
    if game_over:
        if lives <= 0:
            draw_text("Ты проиграл. Игра закончилась.", font, WHITE, screen, screen_width // 2, screen_height // 2)
        else:
            draw_text("Игра закончилась. Ты победил!", font, WHITE, screen, screen_width // 2, screen_height // 2)

    # Обновление экрана
    pygame.display.flip()

    # Контроль ФПС
    clock.tick(fps)

pygame.quit()
sys.exit()
