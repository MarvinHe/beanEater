import os
import pygame
from pygame.locals import *

data_path = "data"


class Color:
    BLACK = (0, 0, 0)
    WHITE = (244, 244, 244)


def load_image(name, colorkey=None):
    fullname = os.path.join(data_path, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join(data_path, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound:', name)
        raise SystemExit
    return sound
