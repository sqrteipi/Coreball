import pygame # type: ignore
from math import sin, cos, pi, dist

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)

core_ang = 0.0
core_speed = 2.5
core_radii = 50
line_len = 300
snipe_radii = 30
snipes = []
pressing = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    screen.fill("black")

    core_ang += core_speed
    core_ang %= 360

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if not pressed:
            pressed = True
            snipes.append(0.0)
    else:
        pressed = False

    loc = []
    for i in range(len(snipes)):
        angle = snipes[i]
        x = sin(angle*pi/180)*line_len
        y = cos(angle*pi/180)*line_len
        pygame.draw.line(screen, WHITE, [500, 500], [500+x, 500+y], width=5)
        pygame.draw.circle(screen, WHITE, [500+x, 500+y], radius=snipe_radii)
        snipes[i] += core_speed
        snipes[i] %= 360
        loc.append([x, y])

    pygame.draw.circle(screen, WHITE, [500, 500], core_radii)

    pygame.display.flip()
    clock.tick(60)  

    collides = False
    for i in range(len(loc)):
        for j in range(i+1, len(loc)):
            if dist(loc[i], loc[j]) <= 2*snipe_radii:
                collides = True

    if collides:
        while True:
            if not running:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

pygame.quit()