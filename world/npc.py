import ai,aitools
import time

class NPC:
    def __init__(self,name="count shipula", ship="hellianattacker", seed):
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
        self.personality = ai.Personality(aitools.generatePersonality(seed))
        
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

class Merchant(NPC):
    def __init__(self, name="Merchant Ship", ship="hellianattacker", seed={"training":33,"experience":50,"bravery":60,"intelligence":50,"tenacity":40,
                            "morality":70,"loyalty":70,"honesty":70,"mercy":70,"faith":50,}):
        print "Merchant class NPC generated"
        
        
class Military(NPC):
    def __init__(self, name="Military Ship", ship="hellianattacker", seed={"training":75,"experience":75,"bravery":85,"intelligence":60,"tenacity":60,
                            "morality":40,"loyalty":99,"honesty":70,"mercy":30,"faith":20,}):
        print "Military class NPC generated"
        
class Pirate(NPC):
    def __init__(self, name="Pirate Ship", ship="hellianattacker", seed={"training":25,"experience":65,"bravery":50,"intelligence":40,"tenacity":80,
                            "morality":20,"loyalty":30,"honesty":30,"mercy":30,"faith":50,}):
        print "Pirate class NPC generated"
        
class Mercenary(NPC):
    def __init__(self, name="Mercenary Ship", ship="hellianattacker", seed={"training":75,"experience":80,"bravery":70,"intelligence":70,
                            "tenacity":80,"morality":30,"loyalty":85,"honesty":40,"mercy":50,"faith":50,}):
        print "Mercenary class NPC generated"
        
class Independant(NPC):
    def __init__(self, name="Independant Ship", ship="hellianattacker", seed={"training":40,"experience":60,"bravery":70,"intelligence":50,
                            "tenacity":60,"morality":80,"loyalty":70,"honesty":60,"mercy":70,"faith":50,}):
        print "Independant class NPC generated"
