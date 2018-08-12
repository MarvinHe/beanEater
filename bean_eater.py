import sys
import pygame
from pygame.locals import QUIT, K_TAB, KEYDOWN
from utils import Color
from bean_eater_game import BeanEaterGame
import sqlite3


pygame.init()
db = None
# utils.data_path = ""

screen = pygame.display.set_mode((800, 640))

# how to split panel?
screen.fill(Color.BLACK)
board = pygame.Surface((800, 40))
board.fill((244, 244, 244))
mainframe = pygame.Surface((800, 600))
rect = pygame.Rect(0, 40, 800, 600)


def new_game():

    g = BeanEaterGame(mainframe, board)
    g.update()
    return g


def save_game_stats(g):
    """
    save game stats into sqlite
    """
    print(g.stats.score, g.stats.step)
    global db
    if not db:
        db = sqlite3.connect("bean_eater.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM sqlite_master where name='bean_eater_stats';")
    if not cur.fetchone():
        cur.execute("CREATE TABLE bean_eater_stats (`id` INTEGER primary key AUTOINCREMENT, "
                    "`score` INTEGER, `step` INTEGER, `create_at` datetime "
                    "DEFAULT CURRENT_TIMESTAMP);")
    cur.execute("insert into bean_eater_stats (`score`, `step`) values (?, ?)", (g.stats.score, g.stats.step))
    db.commit()
    cur.close()


def get_stats():
    global db
    if not db:
        db = sqlite3.connect("bean_eater.db")
    cur = db.cursor()
    cur.execute("select score, step, create_at from bean_eater_stats order by score desc limit 5;")
    scores = cur.fetchall()
    return scores


game = new_game()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_TAB:
                stats = get_stats()
                print(stats)
                continue
            game.move(event.key)
            game.update()
            if game.state == 0:
                save_game_stats(game)
                game = new_game()
    screen.blit(mainframe, rect)
    screen.blit(board, pygame.Rect(0, 0, 800, 10))
    pygame.display.flip()
