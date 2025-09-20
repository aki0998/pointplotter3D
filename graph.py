import ast
import re
import pygame as pg
from models.point import Point
from models.line import Line

try:
    import tkinter as tk
    from tkinter import simpledialog
except (ImportError, ModuleNotFoundError):
    tk = None
    simpledialog = None



from models.interfaces.drawable import Drawable


class Graph(Drawable):
    def __init__(self, points = None,width = 1000,height = 1000,pixels_per_unit = 10):
        self.points=points
        self.screen= pg.display.set_mode((width,height))
        self.width = width
        self.height = height
        self.pixels_per_unit = pixels_per_unit #this represents how many pixels will be one unit in the graph
        self.selected_point = None
        self.lines = []  # store ((x1,y1),(x2,y2)) segments
        self.tk_root = None  # Tk root for the dialog

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

        self.screen.fill(white)

        clock = pg.time.Clock()
        # main game loop
        done = 0
        while not done:
            self.update_selected_point()

            self.screen.fill(white)
            self.draw()

            self.draw_lines()  # draw segments
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
                elif e.type == pg.MOUSEWHEEL:
                    if e.y == 1:
                        self.pixels_per_unit = self.pixels_per_unit * 1.1
                    elif e.y == -1:
                        self.pixels_per_unit *= 0.90
                elif e.type == pg.KEYDOWN and e.key == pg.K_i:  # NEW
                        self.prompt_for_input()


            clock.tick(50)
        pg.quit()

    def update_selected_point(self):
        if self.selected_point:
            self.selected_point.set_coordinates(*self.convert_pos_to_coords(*pg.mouse.get_pos()))
            print(self.selected_point.x, self.selected_point.y)

    def add_point(self,x, y, z=0):
        point = Point(x, y, z, self)
        self.points.append(point)

    def convert_pos_to_coords(self, a, b):
        x = (a - self.width/2)/self.pixels_per_unit
        y = (self.height/2 - b)/self.pixels_per_unit
        return x,y

    def coords_to_pos(self, x, y):
        return self.width // 2 + x * self.pixels_per_unit, self.height // 2 - y * self.pixels_per_unit

    def add_line_segment(self, x1, y1, x2, y2):
        start_point = Point(x1, y1, 0, self)
        end_point = Point(x2, y2, 0, self)
        self.lines.append(Line(self, start_point, end_point))
        self.points.append(start_point)
        self.points.append(end_point)


    def draw_lines(self):
        for line in self.lines:
            line.draw()

    def _parse_coord(self, text):
        tup = ast.literal_eval(text)  # safe literal parse
        if not (isinstance(tup, tuple) and len(tup) == 2):
            raise ValueError("Not a 2-tuple")
        return float(tup[0]), float(tup[1])

    def parse_input_string_simple(self, s: str):
        blocks = re.findall(r"\([^()]*\)", s)  # ["(2,3)", "(4,5)"] etc.
        try:
            if len(blocks) == 1:
                x, y = self._parse_coord(blocks[0])

                self.add_point(x, y)
                return f"Point added: ({x},{y})"
            elif len(blocks) == 2:
                x1, y1 = self._parse_coord(blocks[0])
                x2, y2 = self._parse_coord(blocks[1])
                self.add_line_segment(x1, y1, x2, y2)
                return f"Line added: ({x1},{y1})–({x2},{y2})"
            else:
                return "Use (x,y) or (x1,y1) (x2,y2)."
        except (SyntaxError, ValueError):
            return "Invalid coordinates. Example: (2,3) or (0,0) (4,2)."

    def prompt_for_input(self):
        if simpledialog is None:
            print("Tkinter not available.")
            return
        if self.tk_root is None:
            self.tk_root = tk.Tk()
            self.tk_root.withdraw()
        s = simpledialog.askstring("Add point/line", "Enter (x,y) - Coordinate  or  (x1,y1) (x2,y2) - A line will connect between those two points")
        if s: print(self.parse_input_string_simple(s))












