import pygame as pg


class Graph:
    def __init__(self, points,width,height):
        self.points=points
        self.screen= pg.display.set_mode((width,height))
        self.width = width
        self.height = height


    def draw_axes(self):
        from config import SCREEN_WIDTH, SCREEN_HEIGHT
        pg.draw.line(self.screen, (0, 0, 0),(SCREEN_WIDTH/2 , 0), (SCREEN_WIDTH/2 , SCREEN_HEIGHT))
        pg.draw.line(self.screen, (0, 0, 0),( 0,SCREEN_HEIGHT/2), (SCREEN_WIDTH , SCREEN_HEIGHT/2))

    def draw(self):
        for point in self.points:
            point.draw()
        self.draw_axes()

    def run(self):
        pg.display.set_caption("pygame Point Plotter 3D")
        white = 255, 240, 200
        black = 20, 20, 40
        self.screen.fill(white)

        clock = pg.time.Clock()
        # main game loop
        done = 0
        while not done:
            self.draw()
            pg.display.update()
            for e in pg.event.get():
                if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                    done = 1
                    break
            clock.tick(50)
        pg.quit()

    def add_point(self,x, y, z=0):
        from models.point import Point
        point = Point(x, y, z, self)
        self.points.append(point)


