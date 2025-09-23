from models.interfaces.drawable import Drawable
import pygame as pg

from models.point import Point


class Line(Drawable):
    def __init__(self, graph, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.graph = graph


    def draw(self):
        pg.draw.line(self.graph.screen, (200, 0, 0), self.start_point.get_position(), self.end_point.get_position   (), 2)
        self.start_point.draw()
        self.end_point.draw()

    def to_json(self):
        return [self.start_point.to_json(),self.end_point.to_json()]

    @classmethod
    def from_json(cls,line,graph):
        [start_point, end_point] = line
        return Line(graph,Point.from_json(start_point,graph), Point.from_json(end_point,graph))




