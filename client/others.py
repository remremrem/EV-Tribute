import pyglet
import rabbyt
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
import tools

class Other:
    def __init__(self,window,panel):
        self.isai = 0
        self.name = "player"
        self.sprite = rabbyt.Sprite(texture = "data/ships/reaper2.png")
        self.sprite.xy = ((window[0]-panel[0])/2, window[1]/2)
        self.speed = 300
        self.accel = 300
        self.velocity = 0
        self.movement = 0
        self.pos = [0, 0]
        self.net_pos = 0
        self.pos_time = 0
        self.rps = .8
        self.rot = 0
        self.rot_step = 1
        self.rot_time = 0
        self.direction = 0
        self.heading = 0
        self.isfiring = 0
        self.isfiring2 = 0
        self.secondary = "space bomb"
        self.outfit = []
        self.ping = 100
        self.location = ["system","body"]
        
    def setCrucial(self,crucial):
        self.velocity = crucial.get("velocity")
        self.heading = crucial.get("heading")
        self.pos = crucial.get("pos")
        self.rot = crucial.get("rot")
        self.isfiring = crucial.get("isfiring")
        self.isfiring2 = crucial.get("isfiring2")
        self.secondary = crucial.get("secondary")
        
    def setNonCrucial(self,crucial):
        self.name = crucial.get("name")
        self.shipname = crucial.get("shipname")
        self.isai = crucial.get("isai")
        self.ship = crucial.get("ship")
        self.speed = crucial.get("speed")
        self.accel = crucial.get("accel")
        self.rps = crucial.get("rps")
        self.average_ping = crucial.get("average_ping")
        self.outfit = crucial.get("outfit")

    def draw(self,player,visible_size,ping,name):
        #if self.net_pos != 0:
            #print "NET_POS"+str(self.net_pos)
            #if self.name > name:
                 #self.pos = tools.CalcOtherPosPlus(self,ping)
            #    print "PLUS" + str(self.pos)
            #else:
            #    self.pos = tools.CalcOtherPosMinus(self,ping)
            #    print "MINUS" + str(self.pos)
            #self.pos = self.net_pos
            #print "NET_POS: " + str(self.net_pos)
            #print "OTHER POS: " +str(self.pos)
            #self.pos = tools.CalcOtherPosPlus(self,ping)
            #self.pos = self.net_pos
            #self.net_pos = 0
            #print "SPRITE POS: " + str(self.sprite.xy)
        position = tools.CalcOtherPos(player,self,visible_size)
        self.sprite.xy = position
        self.sprite.rot = self.rot*-1.0
        if position == (1000,1000):
            return None
        else:
            return self.sprite
