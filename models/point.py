class Point:
    def __init__(self, x: float, y: float, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def draw(self, screen):
        import pygame
        pygame.draw.circle(screen, (0,0,0), self.get_position(), 4)

    def get_position(self):
        from config import WINSIZE, WINCENTER
        center_x = WINCENTER[0]
        center_y = WINCENTER[1]
        PIXELS_PER_UNIT = 50
        return (center_x+self.x * PIXELS_PER_UNIT, center_y-self.y * PIXELS_PER_UNIT)




