import random
from settings import *
from timer import Timer


class Game:
    def __init__(self):
        # general setup
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        # tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        init_shape = random.choice(list(TETROMINOS.keys()))
        self.tetromino = Tetromino(init_shape,
                                   self.sprites,
                                   self.create_new_tetromino,
                                   self.field_data)

        # timers
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, repeated=True, func=self.move_tetromino_down),
            'horizontal move': Timer(MOVE_WAIT_TIME, repeated=False)
        }
        self.timers['vertical move'].activate()
        self.timers['horizontal move'].activate()

    def create_new_tetromino(self):
        random_shape = random.choice(list(TETROMINOS.keys()))
        self.tetromino = Tetromino(random_shape,
                                   self.sprites,
                                   self.create_new_tetromino,
                                   self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_tetromino_down(self):
        self.tetromino.move_down(1)

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), width=1)
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), width=1)

        self.surface.blit(self.line_surface, (0, 0))

    def input(self):
        if not self.timers['horizontal move'].active:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

    def run(self):
        # update
        self.input()
        self.timer_update()
        self.sprites.update()

        # drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))

        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, width=2)


class Tetromino():
    def __init__(self, shape, group, create_new_tetromino, field_data):
        # setup
        self.field_data = field_data
        self.create_new_tetromino = create_new_tetromino
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']

        # create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    def move_down(self, offset):
        if not self.next_move_vertical_collides(self.blocks, offset):
            for block in self.blocks:
                block.pos.y += offset
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    def move_horizontal(self, offset):
        if not self.next_move_horizontal_collides(self.blocks, offset):
            for block in self.blocks:
                block.pos.x += offset

    # collisions
    def next_move_horizontal_collides(self, blocks, offset):
        collision_list = [block.horizontal_collide(int(block.pos.x + offset), self.field_data) for block in blocks]
        return any(collision_list)

    def next_move_vertical_collides(self, blocks, offset):
        collision_list = [block.vertical_collide(int(block.pos.y + offset), self.field_data) for block in blocks]
        return any(collision_list)


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=self.pos * CELL_SIZE)

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE

    def horizontal_collide(self, x_pos, field_data):
        if not 0 <= x_pos < COLUMNS:
            return True
        if field_data[int(self.pos.y)][x_pos]:
            return True
        return False

    def vertical_collide(self, y_pos, field_data):
        if y_pos >= ROWS:
            return True

        if y_pos >= 0 and field_data[y_pos][int(self.pos.x)]:
            return True
        return False
