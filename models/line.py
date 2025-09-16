from models.interfaces.drawable import Drawable
import pygame as pg

class Line(Drawable):
    def __init__(self, graph, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.graph = graph


    def draw(self):
        pg.draw.line(self.graph.screen, (200, 0, 0), self.start_point.get_position(), self.end_point.get_position(), 2)



