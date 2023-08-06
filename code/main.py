import sys
import random
from settings import *

# components
from game import Game
from score import Score
from preview import Preview



class Main:
    def __init__(self):
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')


        # shapes
        self.next_shapes = [random.choice(list(TETROMINOS.keys())) for shape in range(3)]


        # components
        self.game = Game(self.get_next_shape)
        self.score = Score()
        self.preview = Preview()

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(random.choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            # display
            self.display_surface.fill(GRAY)

            self.game.run()

            self.update_score()
            self.score.run()
            self.preview.run(self.next_shapes)


            # update the game
            pygame.display.update()
            self.clock.tick()

    def update_score(self):
        self.score.update_score(self.game.current_score, self.game.current_lines, self.game.current_level)

if __name__ == '__main__':
    main = Main()
    main.run()
