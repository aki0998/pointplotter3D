#!/usr/bin/env python
"Creating a basic 2D environment for now to create a point "
import pygame as pg

from config import WINSIZE, WINCENTER
from graph import Graph
from models.point import Point



# constants


def main():
    "This is the base code for the environment"


    # initialize and prepare screen
    pg.init()
    graph = Graph(points=[], width= WINSIZE[0], height = WINSIZE[1])
    graph.add_point(0,0)
    graph.add_point(1,1)
    graph.run()





# So `python -m pygame.example.stars` will work.
if __name__ == "__main__":
    main()

