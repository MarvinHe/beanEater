"""
the real game body
"""
import pygame
from pygame.locals import QUIT, K_RIGHT, K_LEFT, K_UP, K_DOWN, KEYDOWN
import numpy as np
from utils import load_image, Color


def generate_matrix(rows, cols):
    # np.ndarray((rows, cols), bool)
    return np.random.rand(rows, cols)


class BeanEater(pygame.sprite.Sprite):
    """
    the eater
    """
    def __init__(self, pos, window_size):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("monster.png")
        self.pos = np.array(pos)
        self.window_size = np.array(window_size)

    def get_ab_pos(self):
        return self.window_size * self.pos + self.window_size//2

    def update(self):
        # print("in the update, pos is: ", self.pos)
        self.rect.center = self.get_ab_pos()


class AreaType:
    WALL = -1
    EMPTY = 0
    COIN = 1


class Stats(object):
    def __init__(self):
        self.score = 0
        self.step = 0


class BeanEaterGame(object):
    """
    the game obj, hold all states
    """
    def __init__(self, screen, board_screen):
        self.screen = screen
        self.board_screen = board_screen
        self.screen.fill(Color.BLACK)
        self.board_screen.fill(Color.WHITE)

        self.stats = Stats()
        self.eater = None
        # 如何裁剪图片到 40*40, 目前是人工预处理
        wall, wall_rect = load_image("brick_wall_xs.png")
        coin, coin_rect = load_image("coin.png")
        self.rows, self.cols = screen.get_width() // wall_rect.width, screen.get_height() // wall_rect.height
        matrix = generate_matrix(self.rows, self.cols)
        self.matrix = np.zeros((self.rows, self.cols), int)
        self.matrix[matrix < 0.5] = AreaType.WALL
        self.matrix[matrix > 0.6] = AreaType.COIN
        # initial background

        self.black = pygame.Surface(wall_rect.size)
        self.black.fill(Color.BLACK)
        self.black_rect = self.black.get_rect()
        self.coin_num = 0
        self.state = 1
        for i, row in enumerate(self.matrix):
            for j, val in enumerate(row):
                if val == -1:
                    screen.blit(wall, (wall_rect.width*i, wall_rect.height*j))
                elif val == 1:
                    center = (wall_rect.width*i+wall_rect.width//2, wall_rect.height*j+wall_rect.height//2)
                    if not self.eater:
                        self.eater = BeanEater((i, j), (wall_rect.width, wall_rect.height))
                        self.matrix[(i, j)] = 0
                    else:
                        self.coin_num += 1
                        coin_rect.center = center
                        screen.blit(coin, coin_rect)
        self.allsprites = pygame.sprite.RenderPlain(self.eater)
        self.board_group = pygame.sprite.RenderPlain(ScoreBoard(self.stats))
        self.update()

    def update(self):
        self.allsprites.update()
        self.allsprites.draw(self.screen)
        self.board_screen.fill((244, 244, 244))
        self.board_group.update()
        self.board_group.draw(self.board_screen)

    def move(self, key):
        if key == K_LEFT:
            move = (-1, 0)
        elif key == K_RIGHT:
            move = (1, 0)
        elif key == K_UP:
            move = (0, -1)
        elif key == K_DOWN:
            move = (0, 1)
        else:
            print("invalid key: ", key)
            return
        new_pos = self.eater.pos + move
        # print("new _pos", new_pos, "new pos value is", self.matrix[tuple(new_pos)], "self matrix", self.matrix)
        area_type = self.matrix[tuple(new_pos)]
        if self.stats.score >= 2 or area_type != AreaType.WALL:
            self.stats.step += 1
            self.black_rect.center = self.eater.get_ab_pos()
            self.screen.blit(self.black, self.black_rect)
            self.eater.pos = new_pos
            self.black_rect.center = self.eater.get_ab_pos()
            self.screen.blit(self.black, self.black_rect)
            if self.matrix[tuple(new_pos)] == 1:
                self.coin_num -= 1
                self.stats.score += 1
                if self.coin_num < 1:
                    self.state = 0
            elif area_type == AreaType.WALL:
                self.stats.score -= 2
            self.matrix[tuple(new_pos)] = 0


class ScoreBoard(pygame.sprite.Sprite):
    pattern = "Score: {:d}     Step: {:d}"

    def __init__(self, game_state):
        self.font = pygame.font.Font(None, 36)
        pygame.sprite.Sprite.__init__(self)
        self.state = game_state
        self.image = self.font.render(self.pattern.format(self.state.score, self.state.step), 1, (10, 10, 10))
        self.rect = self.image.get_rect()

    def update(self):
        self.image = self.font.render(self.pattern.format(self.state.score, self.state.step), 1, (10, 10, 10))
