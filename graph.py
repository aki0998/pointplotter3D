import ast
import re
import pygame as pg
from models.point import Point
from models.line import Line
import math
import json
import os

from config import WINSIZE, WINCENTER
from utils import display_text

try:
    import tkinter as tk
    from tkinter import simpledialog
except (ImportError, ModuleNotFoundError):
    tk = None
    simpledialog = None



from models.interfaces.drawable import Drawable


class Graph(Drawable):
    def __init__(self, points = None, lines = None, width = 1000,height = 1000,pixels_per_unit = 10):
        self.points = points or []
        self.lines = lines or []
        self.screen= pg.display.set_mode((width,height))
        self.width = width
        self.height = height
        self.pixels_per_unit = pixels_per_unit #this represents how many pixels will be one unit in the graph
        self.selected_point = None
        self.tk_root = None  # Tk root for the dialog
        self.max_zoom = 10
        self.min_zoom = 0.1
        self.default_ppu = pixels_per_unit


    def draw_axes(self):
        pg.draw.line(self.screen, (0, 0, 0),(self.width/2 , 0), (self.width/2 , self.height))
        pg.draw.line(self.screen, (0, 0, 0),( 0,self.height/2), (self.width , self.height/2))
        # ---- dynamic X labels across screen at any zoom ----
        ppu = self.pixels_per_unit
        axis_y = self.height // 2

        # visible world range in x
        x_min = math.floor(-self.width / (2 * ppu))
        x_max = math.ceil(self.width / (2 * ppu))

        # keep labels ~80 pixels apart -> simple integer step
        min_px_gap = 80
        step_x = max(1, math.ceil(min_px_gap / ppu))

        for x in range(int(x_min), int(x_max) + 1, int(step_x)):
            x_pix, _ = self.coords_to_pos(x, 0)
            # small tick mark on the axis
            pg.draw.line(self.screen, (120, 120, 120), (x_pix, axis_y - 4), (x_pix, axis_y + 4), 1)
            # label just BELOW the x-axis so it doesn't sit on the line
            display_text(str(x), (x_pix, axis_y + 8), self.screen, size=14, bg=None, anchor="midtop")

        # ---- dynamic Y labels across screen at any zoom ----
        axis_x = self.width // 2

        # visible world range in y
        y_min = math.floor(-self.height / (2 * ppu))
        y_max = math.ceil(self.height / (2 * ppu))

        step_y = max(1, math.ceil(min_px_gap / ppu))

        for y in range(int(y_min), int(y_max) + 1, int(step_y)):
            _, y_pix = self.coords_to_pos(0, y)
            # small tick mark on the axis
            pg.draw.line(self.screen, (120, 120, 120), (axis_x - 4, y_pix), (axis_x + 4, y_pix), 1)
            # label just LEFT of the y-axis so it doesn't sit on the line
            display_text(str(y), (axis_x - 8, y_pix), self.screen, size=14, bg=None, anchor="midright")

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
                        for line in self.lines:
                            if line.start_point.mouse_intersection():
                                self.selected_point = line.start_point
                                # print("point ", point, " has been selected")
                            if line.end_point.mouse_intersection():
                                self.selected_point = line.end_point
                                # print("point ", point, " has been selected")

                elif e.type == pg.MOUSEBUTTONUP:
                    if e.button == 1:
                        self.selected_point = None
                elif e.type == pg.MOUSEWHEEL:
                    if e.y == 1:#
                        if self.pixels_per_unit < self.default_ppu*self.max_zoom:
                            self.pixels_per_unit *= 1.1
                    elif e.y == -1:
                        if self.pixels_per_unit > self.default_ppu*self.min_zoom:
                            self.pixels_per_unit *= 0.9
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_i:  # NEW
                        self.prompt_for_input()
                    elif e.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
                        print("pressed: CTRL + S")
                        self.save_graph()


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


    def to_json(self):
        return {"points":[point.to_json() for point in self.points], "lines":[line.to_json() for line in self.lines]}

    def save_graph(self):
        with open("graph.json", mode="w", encoding="utf-8") as write_file:
            json.dump(self.to_json(), write_file)
    @classmethod
    def load_graph(cls):
        if not os.path.exists("graph.json"):
            return Graph(width= WINSIZE[0], height = WINSIZE[1])
        with open("graph.json", mode="r", encoding="utf-8") as read_file:
            data = json.load(read_file)
            graph = Graph(width= WINSIZE[0], height = WINSIZE[1])
            graph.points = [Point.from_json(point,graph) for point in data['points']]
            graph.lines = [Line.from_json(line,graph) for line in data['lines']]

            return graph











