
import pygame.mouse

from models.interfaces.drawable import Drawable
from utils import display_text

PIXELS_PER_UNIT = 10
class Point(Drawable):
    def __init__(self, x: float, y: float, z: float = 0, graph=None,radius = 4):
        self.x = x
        self.y = y
        self.z = z
        self.graph = graph
        self.radius = radius

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y


    def draw(self):
        import pygame
        pygame.draw.circle(self.graph.screen, (0,0,0), self.get_position(), self.radius)
        x, y = self.get_position()

        if self.mouse_intersection():
            display_text(f'{round(self.x, 2)},{round(self.y, 2)},{round(self.z, 2)}', (x - 20, y - 20),self.graph.screen)




    def get_position(self):
        center_x = self.graph.width//2
        center_y = self.graph.height//2
        return center_x + self.x *self.graph.pixels_per_unit, center_y - self.y * self.graph.pixels_per_unit

    def mouse_intersection(self):
        x,y = pygame.mouse.get_pos() #stores these x and y coordinates into a variable
        a,b = self.get_position()
        distance = ((a-x)**2 + (b-y)**2)**0.5
        return distance <= self.radius #tells if the mouse is on top of the point

    def to_json(self):
        return [self.x ,self.y ,self.z]

    @classmethod #not an object just for the class (decorator)
    def from_json(cls, coordinates, graph):
        [x, y, z] = coordinates
        return Point(x,y,z,graph=graph)














