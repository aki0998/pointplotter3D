class Point:
    def __init__(self, x: float, y: float, z: float = 0, graph=None):
        self.x = x
        self.y = y
        self.z = z
        self.graph = graph




    def draw(self):
        import pygame
        pygame.draw.circle(self.graph.screen, (0,0,0), self.get_position(), 4)

    def get_position(self):
        center_x = self.graph.width//2
        center_y = self.graph.height//2
        PIXELS_PER_UNIT = 10
        return center_x + self.x * PIXELS_PER_UNIT, center_y - self.y * PIXELS_PER_UNIT




