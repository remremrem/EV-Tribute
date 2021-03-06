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
        self.players = []
        self.npcs = []
        
                    
class StarSystem:
    def __init__(self,name="System"):
        self.name = name
        self.location =[0,0]
        self.icon = [0,0]
        self.num_bodies = 0
        self.bodies = {}
        self.links = []
        self.asteroids = 0
        #self.visible_size = visible_size
        self.active = 0
        self.selected = 0
        self.plotted = 0
        self.discovered = 1
        self.visible = 1
        self.players = []
        self.npcs = []
        
    def load(self,center):
        f = open("data/systems/"+self.name+".system","r")
        system = 0
        newbody = 0
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
                    continue
            if x == "[location]":
                if system == 1:
                    print syslist[count+1]
                    location = syslist[count+1].split(",")
                    self.location = [int(location[0]),int(location[1])]
                    count += 1
                    continue
                if newbody == 1:
                    if self.bodies.get(body.name).type == "body":
                        location = syslist[count+1].split(",")
                        self.bodies.get(body.name).location = [int(location[0]) + center[0], int(location[1]) + center[1]]
                    else:
                        self.bodies.get(body.name).location = 0
                    count += 1
                    continue
            #if x == "[sprite]":
            #    self.bodies[bodycount].sprite = rabbyt.Sprite(texture = "data/systems/"+syslist[count+1])
            #    count += 1
            #    continue
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
            if x == "[distance]":
                if self.bodies.get(body.name).type == "body":
                    self.bodies.get(body.name).distance = 0
                else:
                    self.bodies.get(body.name).distance = int(syslist[count+1])
                count += 1
                continue
            if x == "[parent]":
                if self.bodies.get(body.name).type == "body":
                    self.bodies.get(body.name).parent = 0
                else:
                    self.bodies.get(body.name).parent = syslist[count+1]
                count += 1
                continue
            count += 1

    def getCrucial(self, playingdict, crucialdict):
        crucialstats = {}
        for each in self.players:
            print playingdict.get(each)
            if playingdict.get(each).inspace == 1:
                crucialstats[each] = crucialdict.get(each)
        print self.name, "players", self.players
        print self.name, "crucialstats",crucialstats
        return crucialstats
        
    def getNonCrucial(self, playingdict, noncrucialdict):
        noncrucialstats = {}
        for each in self.players:
            if playingdict.get(each).inspace == 1:
                noncrucialstats[each] = noncrucialdict.get(each)
        return noncrucialstats
        
class StarLink:
    def __init__(self, name="name", start=(0,0), end=(0,0)):
        self.name = name
        self.start = start
        self.end = end
        self.active = 0
        self.plotted = 0
                     
def MakeSystemDict(path, center):
    f = open(path)
    systemlist = []
    for line in f:
         systemlist.append(line.rstrip("\n"))
    f.close()
    systemdict = {}
    for x in systemlist:
        system = StarSystem(x)
        system.load(center)
        systemdict[system.name] = (system)
    print "systemdict" + str(systemdict)
    return systemdict
    
def MakeLinks(systemdict):
    linkdict = {}
    for x in systemdict:
         for link in systemdict.get(x).links:
             if not x+link in linkdict and not link+x in linkdict:
                 linkdict[x+link] = StarLink(x+link, systemdict.get(x).location, systemdict.get(link).location)
    return linkdict
