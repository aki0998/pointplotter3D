import pygame as pg


class Graph:
    def __init__(self, points = None,width = 1000,height = 1000,pixels_per_unit = 10):
        self.points=points
        self.screen= pg.display.set_mode((width,height))
        self.width = width
        self.height = height
        self.pixels_per_unit = pixels_per_unit #this represents how many pixels will be one unit in the graph
        self.selected_point = None


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
            self.update_selected_point()

            self.screen.fill(white)
            self.draw()
            pg.display.update()
            for e in pg.event.get():
                if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                    done = 1
                    break
                elif e.type == pg.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        for point in self.points:
                            if point.mouse_intersection():


                                self.selected_point = point
                                print("point ",point," has been selected")
                                break
                elif e.type == pg.MOUSEBUTTONUP:
                    if e.button == 1:
                        self.selected_point = None



            clock.tick(50)
        pg.quit()

    def update_selected_point(self):
        if self.selected_point:
            self.selected_point.set_coordinates(*self.convert_pos_to_coords(*pg.mouse.get_pos()))
            print(self.selected_point.x, self.selected_point.y)

    def add_point(self,x, y, z=0):
        from models.point import Point
        point = Point(x, y, z, self)
        self.points.append(point)

    def convert_pos_to_coords(self, a, b):
        x = (a - self.width/2)/self.pixels_per_unit
        y = (self.height/2 - b)/self.pixels_per_unit
        return x,y






