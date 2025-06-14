#!/usr/bin/env python
"Creating a basic 2D environment for now to create a point "
import pygame as pg

from config import WINSIZE, WINCENTER
from graph import Graph
from models.point import Point

points = [Point(0,0), Point(1,1)]
new_graph = Graph(points)

# constants


def main():
    "This is the base code for the environment"
    # create our base

    # initialize and prepare screen
    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    pg.display.set_caption("pygame Point Plotter 3D")
    white = 255, 240, 200
    black = 20, 20, 40
    screen.fill(white)

    clock = pg.time.Clock()

    # main game loop
    done = 0
    while not done:
        # draw_stars(screen, stars, black) #
        # move_stars(stars)
        # draw_stars(screen, stars, white)
        for point in points:
            point.draw(screen)
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                WINCENTER[:] = list(e.pos)


        clock.tick(50)
    pg.quit()


# So `python -m pygame.example.stars` will work.
if __name__ == "__main__":
    main()

