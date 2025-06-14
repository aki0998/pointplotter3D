import pygame.draw


class Graph:
    def __init__(self, points,screen):
        self.points=points
        self.screen=screen


    def draw_axes(self):
        from config import SCREEN_WIDTH, SCREEN_HEIGHT
        pygame.draw.line(self.screen, (0, 0, 0),(SCREEN_WIDTH/2 , 0), (SCREEN_WIDTH/2 , SCREEN_HEIGHT))
        pygame.draw.line(self.screen, (0, 0, 0),( 0,SCREEN_HEIGHT/2), (SCREEN_WIDTH , SCREEN_HEIGHT/2))
    def draw(self):
        for point in self.points:
            point.draw(self.screen)
        self.draw_axes()
