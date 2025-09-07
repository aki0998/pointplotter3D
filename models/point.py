import pygame.mouse

PIXELS_PER_UNIT = 10
class Point:
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
        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font('freesansbold.ttf', 32)

        # create a text surface object,
        # on which text is drawn on it.
        text = font.render(f'{self.x},{self.y},{self.z}', True, (0,0,0), (255,255,255))

        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()

        # set the center of the rectangular object.
        x,y = self.get_position()
        textRect.center = (x-20, y-20)
        if self.mouse_intersection():
            self.graph.screen.blit(text, textRect)


    def get_position(self):
        center_x = self.graph.width//2
        center_y = self.graph.height//2
        return center_x + self.x *self.graph.pixels_per_unit , center_y - self.y * self.graph.pixels_per_unit

    def mouse_intersection(self):
        x,y = pygame.mouse.get_pos() #stores these x and y coordinates into a variable
        a,b = self.get_position()
        distance = ((a-x)**2 + (b-y)**2)**0.5
        return distance <= self.radius #tells if the mouse is on top of the point











