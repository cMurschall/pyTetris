import os

from settings import *

class Score:

    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(bottomright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.display_surface = pygame.display.get_surface()

        path = os.path.join(os.path.dirname(__file__), '..', 'graphics', 'Russo_One.ttf')
        self.font = pygame.font.Font(path, 30)

        self.score = [0,0,0]


    def run(self):

        self.surface.fill(GRAY)
        increment = self.surface.get_height() / 3
        for i , text in enumerate(['Score: ', 'Level: ', 'Lines: ']):
            x = self.surface.get_width() / 2
            y = (increment / 2) + i * increment
            self.display_text(text + str(self.score[i]), (x, y))

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, width=2, border_radius=2)

    def display_text(self, text, pos):
        text_surface = self.font.render(text, True, 'white')
        rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, rect)

    def update_score(self, current_score, current_lines, current_level):
        self.score[0] = current_score
        self.score[1] = current_level
        self.score[2] = current_lines