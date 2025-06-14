class Point:
    def __init__(self, x: float, y: float, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def draw(self, screen):
        import pygame
        pygame.draw.circle(screen, (0,0,0), (self.x*50,self.y*50), 4)



