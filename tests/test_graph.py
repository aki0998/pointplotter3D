import pygame

from graph import Graph


def test_screensize():
    graph = Graph(points=[], width=100, height=100)
    width, height = pygame.display.get_surface().get_size()
    assert width==100
    assert height==100
