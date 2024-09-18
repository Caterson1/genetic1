import pygame as p
import sys  # most commonly used to turn the interpreter off (shut down your game)
from classism import *
from contants import *

# Constants - sets the size of the window
window_bounds = WIDTH, HEIGHT, scale = 600, 600, .75
origin = x0, y0 = 10, HEIGHT-HEIGHT/2  # This is the new origin


def ball_xy(ball):
    return origin[0] + ball.pos.x*scale, origin[1] - ball.pos.y*scale - 10


screen = p.display.set_mode((WIDTH, HEIGHT))


def pygame_init():
    # Screen or whatever you want to call it is your best friend - it's a canvas
    # or surface where you can draw - generally you'll have one large canvas and
    # additional surfaces on top - effectively breaking things up and giving
    # you the ability to have multiples scenes in one window
    p.init()
    screen.fill((180, 210, 255))
    p.display.set_caption('Fireworks')


def drawer(object_list, place_to_draw_stuff=screen):
    for i in object_list:
        p.draw.circle(place_to_draw_stuff, i.color.color(), ball_xy(i), 1)


population = Population(100, 20, Ball(45, speed=330, wind = Vec(-15, 2, 0)))
# populations = [Population(1000, .000001, Ball(Vec(), 45, 10)) for x in range(10)]

running = False
while True:
    # screen.fill((150, 210, 255))
    #keystroke example
    for event in p.event.get():

        if event.type == p.QUIT:  # this refers to clicking on the "x"-close
            p.quit()
            sys.exit()

        elif event.type == p.KEYDOWN:  # there's a separate system built in
            # for multiple key presses or presses
            # that result in changes of state - tba
            if event.key == p.K_g:
                print("n")

            if event.key == p.K_a:
                print("goodbye")

            if event.key == p.K_SPACE:
                if running is False:
                    running = True
                    print("START")
                elif running is True:
                    running = False
                    print("PAUSE")

    if running:
        #background
        for x in range(200):
            if population.step():
                screen.fill((0,0,0))
            # for x in populations:
            #     x.step()
        drawer(population.population)
        # for x in populations:
        #     drawer(x.population)

        p.draw.rect(screen, (50, 200, 100), (0, y0, WIDTH, HEIGHT))
        p.display.flip()

    # This sets an upper limit on the frame rate (here 100 frames per second)
    # often you won't be able
    # p.time.Clock().tick(100)
