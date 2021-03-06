import pyglet
import rabbyt
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from tools import *
import sys,os,random
        

class Body:
    def __init__(self):
        self.name = "Planet no. 1"
        self.type = "body"
        self.sprite = "null"
        self.dock = 0
        self.race = "human"
        self.faction = "rebel"
        self.wealth = 20  # in trillions
        self.population = 70    # in billions
        self.location = [0,0]
        self.distance = 0
        self.parent =  0
        self.angle = random.randint(0, 359)
        self.pdistance = 0
        
    def draw(self,player,bodies,visible_size):
        if self.type == "body":
            #print "VISIBLE_SIZE"
            #print visible_size
            position,self.pdistance = CalcBodyPos(player,self.location,visible_size)
            self.sprite.xy = position
            #print "PLANET SPRITE" + str(self.sprite.xy)
        elif self.type == "sattelite":
            #print self.name
            #print self.parent
            for x in bodies:
                #print x
                if bodies.get(x).name == self.parent:
                    position,self.pdistance,self.location = CalcSatPos(player, bodies.get(x).location, visible_size, self.distance, self.angle)
                    self.sprite.xy = position
        #print "TYPE" + self.type
        if position == (1000,1000):
            return None
        else:
            return self.sprite
                    
class StarSystem:
    def __init__(self,name="System",visible_size=(650,600)):
        self.name = name
        self.location =[0,0]
        self.icon = [0,0]
        self.num_bodies = 0
        self.bodies = {}
        self.bodynames = []
        self.links = []
        self.asteroids = 0
        self.visible_size = visible_size
        self.active = 0
        self.selected = 0
        self.plotted = 0
        self.discovered = 1
        self.visible = 1
        
    def load(self,player,center):
         f = open("data/systems/"+self.name+".system","r")
         system = 0
         body = 0
         sattelite = 0
         syslist = []
         for line in f:
             l = line.rstrip("\n")
             syslist.append(l)
         f.close()
         #print syslist
         bodycount = -1
         count = 0
         for x in syslist:
             if x == "[system]":
                 system = 1
                 newbody = 0
                 sattelite = 0
                 count += 1
                 continue
             if x == "[body]":
                 system = 0
                 newbody = 1
                 sattelite = 0
                 bodycount += 1
                 count += 1
                 continue
             if x == "[sattelite]":
                 system = 0
                 newbody = 0
                 sattelite = 1
                 bodycount += 1
                 count += 1
                 continue
             if x == "[links]":
                 links = syslist[count+1].split(",")
                 for y in links:
                     self.links.append(y)
                 count += 1
                 continue
             if x == "[bodies]":
                 self.num_bodies = int(syslist[count+1])
                 count += 1
                 continue
             if x == "[asteroids]":
                 self.asteroids = int(syslist[count+1])
                 count += 1
                 continue
             if x == "[name]":
                 if newbody == 1:
                     body = Body()
                     body.name = syslist[count+1]
                     body.type = "body"
                     self.bodies[body.name] = body
                     count += 1
                     continue
                 if sattelite == 1:
                     body = Body()
                     body.name = syslist[count+1]
                     body.type = "sattelite"
                     self.bodies[body.name] = body
                     count += 1
                     newbody == 1
                     continue
             if x == "[location]":
                 if system == 1:
                     print syslist[count+1]
                     location = syslist[count+1].split(",")
                     self.location = [int(location[0]),int(location[1])]
                     count += 1
                     continue
             if x == "[sprite]":
                 try:
                     self.bodies.get(body.name).sprite = rabbyt.Sprite(texture = "data/systems/"+syslist[count+1])
                 except:
                     self.bodies.get(body.name).sprite = rabbyt.Sprite(texture = "data/systems/earth.png")
                 count += 1
                 continue
             if x == "[dock]":
                 self.bodies.get(body.name).dock = int(syslist[count+1])
                 count += 1
                 continue
             if x == "[race]":
                 self.bodies.get(body.name).race = syslist[count+1]
                 count += 1
                 continue
             if x == "[faction]":
                 self.bodies.get(body.name).faction = syslist[count+1]
                 count += 1
                 continue
             if x == "[wealth]":
                 self.bodies.get(body.name).wealth = int(syslist[count+1])
                 count += 1
                 continue
             if x == "[population]":
                 self.bodies.get(body.name).population = int(syslist[count+1])
                 count += 1
                 continue
             if x == "[parent]":
                 #print "parent of " + body.name + " is " + str(syslist[count+1])
                 self.bodies.get(body.name).parent = syslist[count+1]
                 count += 1
                 continue
             count += 1
         self.bodynames = [None]
         for x in self.bodies:
             self.bodynames.append(x)  
     
    def update(self,updates):
        for x in updates.bodies:
            self.bodies.get(x).location = updates.bodies.get(x).location
            self.bodies.get(x).angle = updates.bodies.get(x).angle
            self.bodies.get(x).distance = updates.bodies.get(x).distance         
             
    def draw(self,player):
        spritelist = [] 
        for body in self.bodies:
            x = self.bodies.get(body).draw(player,self.bodies,self.visible_size)
            if x != None:
                spritelist.append(x)
        return spritelist
        
class StarLink:
    def __init__(self, name="name", start=(0,0), end=(0,0), visible=0):
        self.name = name
        self.start = start
        self.end = end
        self.active = 0
        self.plotted = 0
        self.visible = visible
        
                
def MakeSystemDict(path, player, center, visible_size):
    f = open(path)
    systemlist = []
    for line in f:
         systemlist.append(line.rstrip("\n"))
    f.close()
    systemdict = {}
    for x in systemlist:
        system = StarSystem(x, visible_size)
        system.load(player, center)
        systemdict[system.name] = (system)
    print "systemdict" + str(systemdict)
    return systemdict

    
def MakeLinks(systemdict):
    linkdict = {}
    print "SYSTEMDICT", systemdict
    for x in systemdict:
        print "systemname",x 
        for link in systemdict.get(x).links:
            if not x+link in linkdict and not link+x in linkdict:
                if systemdict.get(x).discovered == 1 or systemdict.get(link).discovered == 1:
                    visible = 1
                else: visible = 0
                linkdict[x+link] = StarLink(x+link, systemdict.get(x).location, systemdict.get(link).location, visible)
    return linkdict
