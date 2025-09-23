# utils.py
import pygame as pg

def display_text(text, pos, screen, size=14, color=(0,0,0), bg=None, anchor="center"):
    # small, reusable text helper
    font = pg.font.Font(pg.font.get_default_font(), size)
    surf = font.render(text, True, color, bg)   # bg=None => transparent
    rect = surf.get_rect()
    setattr(rect, anchor, pos)                  # e.g. "midtop", "midright"
    screen.blit(surf, rect)

