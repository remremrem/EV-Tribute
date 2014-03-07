import pyglet
import rabbyt
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from tools import *

class Asteroid:
    def __init__(self,window,panel):
        self.sprite = rabbyt.Sprite(texture = "asteroid.png")
        self.sprite.xy = (0,0)
        self.speed = 50
        self.pos = [0, 0]
        self.pos_time = 0
        self.rps = .5
        self.vector = 0
        self.time = rabbyt.get_time()
