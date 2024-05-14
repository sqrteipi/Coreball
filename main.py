from data import Data
import pygame  # type: ignore
import random
import requests
from math import sin, cos, pi, dist
import sys

# initialization
class HTTPRequestError(Exception):
    pass

URL = "http://localhost:5000"
pygame.init()

# pygame setup
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h
SCREEN_MIDDLE = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    ### Settings
    WHITE = (255, 255, 255)
    font = pygame.font.Font(None, 80)
    db = Data("data.db")

    ### Parameters
    core_ang = 0.0
    core_speed = 2
    core_radii = 50
    line_len = 300
    snipe_radii = 30
    snipes = []
    pressed = False

    ### Variations
    RANDOM_REVERSE = True
    REVERSED = True
    SPEED_UP = True
    SPEED_ADD = True

    ### Info
    round = 0
    username = ""

    ### Typing Player Username
    running = True

    while running:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: ### Press Esc -> Quit
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN: ### Press Return -> Finish typing
                    running = False
                elif event.key == pygame.K_BACKSPACE: ### Delete char
                    username = username[:-1]
                else:
                    username += event.unicode ### Add char

        ### Show Current Name
        name_surface = font.render(username, True, WHITE)
        name_rect = name_surface.get_rect()
        name_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(name_surface, name_rect)

        ### Text: "Please Type Your Name"
        text_surface = font.render("Please Type Your Name: ", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80) ### A bit higher than the centre of the screen
        screen.blit(text_surface, text_rect)
        
        ### Update
        pygame.display.update()

    ### Running the Game
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: ### Press Esc -> Quit
                    pygame.quit()
                    sys.exit()

        ### Background
        screen.fill("black")

        ### Showing Score
        text = font.render(f"SCORE: {len(snipes)}", True, WHITE)
        screen.blit(text, (0, 0))

        ### Core "turning"
        core_ang += core_speed
        core_ang %= 360

        ### Check if Spacebar pressed -> Snipe one shot
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not pressed:
                pressed = True ### Avoid errors caused by long press

                ### Action for the snipe shoot towards the video
                k = SCREEN_MIDDLE[1] + line_len + 300 # A bit lower than the core
                while k > SCREEN_MIDDLE[1] + line_len:
                    k -= 100 # The snipe goes up
                    
                    ##### DRAWS EVERYTHING WHILE ACTION #####

                    ### Background
                    screen.fill("black")

                    ### Previous snipes
                    for i in range(len(snipes)):
                        angle = snipes[i]
                        x = sin(angle * pi / 180) * line_len
                        y = cos(angle * pi / 180) * line_len
                        pygame.draw.line(
                            screen,
                            WHITE, [SCREEN_MIDDLE[0], SCREEN_MIDDLE[1]],
                            [SCREEN_MIDDLE[0] + x, SCREEN_MIDDLE[1] + y],
                            width=5)
                        pygame.draw.circle(
                            screen,
                            WHITE,
                            [SCREEN_MIDDLE[0] + x, SCREEN_MIDDLE[1] + y],
                            radius=snipe_radii)

                    pygame.draw.circle(screen, WHITE,
                                       [SCREEN_MIDDLE[0], SCREEN_MIDDLE[1]],
                                       core_radii)

                    pygame.draw.line(screen,
                                     WHITE, [SCREEN_MIDDLE[0], k - line_len],
                                     [SCREEN_MIDDLE[0], k],
                                     width=5)
                    pygame.draw.circle(screen, WHITE, [SCREEN_MIDDLE[0], k],
                                       snipe_radii)
                    
                    screen.blit(text, (0, 0))

                    ### Update the screen
                    pygame.display.flip()
                    pygame.display.update()

                    clock.tick(60)

                ### Add the snipe
                snipes.append(0.0)

                ### REVERSED -> Reverse the direction of core
                if REVERSED:
                    core_speed = -core_speed
        else:
            pressed = False

        ### Retry Button -> R
        if keys[pygame.K_r]:
            main()

        ### Previous shots
        loc = []
        for i in range(len(snipes)):
            angle = snipes[i]
            x = sin(angle * pi / 180) * line_len
            y = cos(angle * pi / 180) * line_len
            pygame.draw.line(screen,
                             WHITE, [SCREEN_MIDDLE[0], SCREEN_MIDDLE[1]],
                             [SCREEN_MIDDLE[0] + x, SCREEN_MIDDLE[1] + y],
                             width=5)
            pygame.draw.circle(screen,
                               WHITE,
                               [SCREEN_MIDDLE[0] + x, SCREEN_MIDDLE[1] + y],
                               radius=snipe_radii)
            snipes[i] += core_speed
            snipes[i] %= 360
            loc.append([x, y])

        pygame.draw.circle(screen, WHITE, [SCREEN_MIDDLE[0], SCREEN_MIDDLE[1]],
                           core_radii)

        pygame.draw.line(
            screen,
            WHITE, [SCREEN_MIDDLE[0], SCREEN_MIDDLE[1] + 300],
            [SCREEN_MIDDLE[0], SCREEN_MIDDLE[1] + 300 + (line_len - 180)],
            width=5)
        pygame.draw.circle(
            screen, WHITE,
            [SCREEN_MIDDLE[0], SCREEN_MIDDLE[1] + 300 + (line_len - 180)],
            snipe_radii)
        
        ### SPEED_UP -> Increases the speed of core for a short period
        if SPEED_UP:
            if round % 100 == 1:
                if core_speed >= 0:
                    core_speed += 4.5
                else:
                    core_speed -= 4.5
            elif round % 100 == 30:
                if core_speed >= 0:
                    core_speed -= 4.5
                else:
                    core_speed += 4.5

        ### SPEED_ADD -> Increases the speed of core (Without decreasing) until it reaches a maximum speed of 10
        if SPEED_ADD:
            if core_speed >= 0 and core_speed < 10:
                core_speed += 0.003
            elif core_speed <= 0 and core_speed < -10:
                core_speed -= 0.003

        ### RANDOM_REVERSE -> Randomly reverse the direction of core
        if RANDOM_REVERSE and random.randint(1, 250) == 1:
            core_speed = -core_speed

        ### Update round info.
        round += 1

        ### Update the screen
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

        ### Check whether two shots collides
        collides = False
        for i in range(len(loc)):
            for j in range(i + 1, len(loc)):
                if dist(loc[i], loc[j]) <= 2 * snipe_radii: ### (Mathematical) Method to check whether two circle collides
                    collides = True

        ### Game Over
        if collides:
            db.insert((username, len(snipes)))
            data = db.fetch()
            response = requests.post(url=URL, json=data)
            if response.status_code != 200:
                raise HTTPRequestError(f"Error code: {response.status_code}")
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                
                ### Retry
                if keys[pygame.K_r]:
                    main()
                    running = False

    ### Quit After Game
    pygame.quit()
    sys.exit()


main()
