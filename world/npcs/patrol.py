from aitools import *
#from state import *
import time

class Patrol:
    def __init__(self,ship="hellianattacker"):
        self.name = "Patrol"
        self.government = "nuetral"
        self.home = ["Sol","Earth"]
        self.job = "patrol"
        self.ship = ship
        self.type = "Shuttle Craft"
        self.speed = 300
        self.accel = 250
        self.velocity = 0
        self.movement = 0
        self.pos = [0, 0]
        self.pos_time = 0
        self.rps = .8
        self.rot = 0
        self.rot_step = 1
        self.rot_time = 0
        self.direction = 0
        self.heading = 0
        self.time = time.time()  
        self.isfiring = 0
        self.landed = 1
        self.state = "normal"
        self.prev_state = "none"
        self.target = "none"
        self.threat = 0
        self.threatened = 0
        #self.personality = generatePersonality(self.job)
        
        def loadShip(self):
            ship = open("data/ships/"+self.ship+".ship","r")
            lines = []
            for x in ship:
                lines.append(x.rstrip("\n"))
            ship.close()
            count = 0
            for x in lines:
                if x == "[name]":
                    self.type = lines[count+1]
                if x == "[speed]":
                    self.speed = lines[count+1]
                if x =="[accel]":
                    self.accel = lines[count+1]

                    
    def rotate(self,direction):
        rot_amt = CalcRot(self.rot_time, self.rps, self.rot_step, direction)
        if rot_amt > 0 and self.rot == (360 - rot_amt):
            self.rot = 0
        elif rot_amt < 0 and self.rot == (0):
            self.rot = 360 - self.rot_step
        else:
            self.rot += rot_amt
        self.sprite.rot = self.rot * -1
        if rot_amt <> 0:
            self.rot_time = rabbyt.get_time()
        if self.velocity == 0:
            self.heading, self.direction = self.rot, self.rot
        #print "selfrot",self.rot,"sprite rot",self.sprite.rot
        #print "self.heading",self.heading   
        return None
        
    def instaRotate(self,direction):
        pass
    def accelerate(self,mapsize):
        if self.rot == self.heading:
            self.pos, self.velocity = CalcPos(self.pos, self.pos_time, self.speed, 
                                               self.accel, self.velocity, self.heading)
        elif (self.rot == self.heading - 180) or (self.rot == self.heading + 180):
            self.pos, self.velocity = SlowDown(self.pos, self.pos_time, self.speed, 
                                               self.accel, self.velocity, self.heading)
        else:
            self.heading, self.direction, self.velocity, self.pos = CalcHeading(self.pos, self.pos_time, 
                                                                       self.speed, self.accel, 
                                                                       self.velocity, self.direction, 
                                                                               self.heading, self.rot, self.rot_step)

        if self.velocity == 0:
            self.heading, self.direction = self.rot, self.rot
        self.pos_time = rabbyt.get_time()
        #print "VEC ROT",self.direction,self.rot       
        return None
   
    def glide(self,mapsize):
        self.pos, self.velocity = CalcPos(self.pos, self.pos_time, self.speed, 0, self.velocity, self.heading)
        self.pos_time = rabbyt.get_time()
        

