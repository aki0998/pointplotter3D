from models.interfaces.drawable import Drawable
import pygame as pg

from models.point import Point
from utils import display_text


class Line(Drawable):
    def __init__(self, graph, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.graph = graph


    def draw(self):
        pg.draw.line(self.graph.screen, (200, 0, 0), self.start_point.get_position(), self.end_point.get_position   (), 2)
        self.start_point.draw()
        self.end_point.draw()
        x,y = self.midpoint()
        display_text(str(round(self.length,1)), self.graph.coords_to_pos(x,y), self.graph.screen)



    def to_json(self):
        return [self.start_point.to_json(),self.end_point.to_json()]

    @classmethod
    def from_json(cls,line,graph):
        [start_point, end_point] = line
        return Line(graph,Point.from_json(start_point,graph), Point.from_json(end_point,graph))

    @property
    def length(self):
        dx = self.start_point.x - self.end_point.x
        dy = self.start_point.y - self.end_point.y
        dz = self.start_point.z - self.end_point.z
        return ((dx**2)+(dy**2)+(dz**2))**0.5

    def midpoint(self):
        x_midpoint = (self.start_point.x + self.end_point.x)/2
        y_midpoint = (self.start_point.y + self.end_point.y) / 2
        return x_midpoint,y_midpoint

