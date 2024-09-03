# Введение в работу с pygame - https://habr.com/ru/articles/588605/
# Основы pygame - https://python-course.readthedocs.io/projects/elementary/en/latest/lessons/18-pygame.html
# Pygame шпаргалка для использования -
# https://waksoft.susu.ru/2019/04/24/pygame-shpargalka-dlja-ispolzovanija/


import pygame
pygame.init()
setting_screen = (800, 600)
screen = pygame.display.set_mode(setting_screen)
pygame.display.set_caption("My game")


image = pygame.image.load("kolobok.png")
image_rect = image.get_rect()

speed = 1


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT] and image_rect.x > 0:
    #     image_rect.x -= speed
    # if keys[pygame.K_RIGHT] and image_rect.x < setting_screen[0] - image_rect.width:
    #     image_rect.x += speed
    # if keys[pygame.K_UP] and image_rect.y > 0:
    #     image_rect.y -= speed
    # if keys[pygame.K_DOWN] and image_rect.y < setting_screen[1] - image_rect.height:
    #     image_rect.y += speed

    # для следования за мышкой:
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = pygame.mouse.get_pos()
            image_rect.x = mouseX - image_rect.width / 2
            image_rect.y = mouseY - image_rect.height / 2


    screen.fill((255, 155, 133))
    screen.blit(image, image_rect)
    pygame.display.update() # либо pygame.display.flip()

pygame.quit()


