import pygame.image
import os

from settings import *


class Preview:

    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        self.rect = self.surface.get_rect(topright=(WINDOW_WIDTH - PADDING, PADDING))
        self.display_surface = pygame.display.get_surface()

        self.shape_surfaces = {shape: pygame.image.load(
            os.path.join(os.path.dirname(__file__), '..', 'graphics', f'{shape}.png')).convert_alpha() for shape in
                               TETROMINOS.keys()}

    def run(self, next_shapes):
        self.surface.fill(GRAY)

        self.display_pieces(next_shapes)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, width=2, border_radius=2)

    def display_pieces(self, next_shapes):
        fragment_height = self.surface.get_height() / 3

        for i, shape in enumerate(next_shapes):
            shape_surface = self.shape_surfaces[shape]
            x = self.surface.get_width() / 2
            y = (fragment_height / 2) + i * fragment_height
            rect = shape_surface.get_rect(center=(x, y))
            self.surface.blit(shape_surface, rect)
