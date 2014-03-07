

class Player:
    def __init__(self, name="new player", idnum=0 ):
        self.isai = 0
        self.name = name
        self.idnum = idnum
        self.inspace = 1
        self.ship = "Civilian Fighter"
        self.shipname = "Scruffy"
        self.speed = 300
        self.accel = 300
        self.velocity = 0
        self.movement = 0
        self.pos = [0, 0]
        self.pos_time = 0
        self.rps = .8
        self.rot = 0
        #self.rot_step = 1
        #self.rot_time = 0
        self.direction = 0
        self.heading = 0
        self.isfiring = 0
        self.isfiring2 = 0
        self.secondary = 0
        self.olddata = {}
        self.average_ping = 0
        self.pinglist = [100,100,100,100,100]
        self.send_time = 0
        self.receive_time = 0
        self.system = 0
        self.docked = 0
        self.body = 0
        self.outfit = []
        self.destination = 0
        
        def check_db():
            try:
                f = open("players/"+self.name+".player","r")
                playerlist = []
                for line in f:
                    l = line.rstrip("\n")
                    playerlist.append(l)
                f.close()
                count = 0
                for x in playerlist:
                    if x == "[shipname]":
                        self.shipname = playerlist[count+1]
                        count += 1
                        continue
                    if x == "[shiptype]":
                        self.ship = playerlist[count+1]
                        count += 1
                        continue
                    if x == "[speed]":
                        self.speed = int(playerlist[count+1])
                        count += 1
                        continue
                    if x == "[accel]":
                        self.accel = int(playerlist[count+1])
                        count += 1
                        continue
                    if x == "[rps]":
                        self.rps = int(playerlist[count+1])
                        count += 1
                        continue
                    count += 1
            except:
                f = open("players/players.list","a")
                f.writelines(self.name+"\n")
                f.close()
                self.ship = "Shuttle Craft"
                self.speed = 150
                self.accel = 150
                self.rps = .6
                lines = ["[player]\n", "[name]\n", str(self.name), "\n[shipname]\n", str(self.shipname), 
                         "\n[shiptype]\n", str(self.ship), "\n[speed]\n", str(self.speed), "\n[accel]\n", 
                         str(self.accel), "\n[rps]\n", str(self.rps)+"\n"]
                f = open("players/"+self.name+".player","w")
                f.writelines(lines)
        
    def update(self, newdata):
        for x in newdata:
            try:
                if newdata.get(x) != self.olddata.get(x):
                    data = newdata.get(x)
                    if x == velocity:
                        self.velocity = data
                        continue
                    if x == pos:
                        self.pos = data
                        continue
                    if x == direction:
                        self.direction = data
                        continue
                    if x == heading:
                        self.heading = data
                        continue
                    if x == isfiring:
                        self.isfiring = data
                        continue
            except:
                continue
        self.olddata = newdata

    def setCrucial(self,crucial):
        #print "crucial",crucial
        self.velocity = crucial.get("velocity")
        self.heading = crucial.get("heading")
        self.pos = crucial.get("pos")
        self.rot = crucial.get("rot")
        self.isfiring = crucial.get("isfiring")
        self.isfiring2 = crucial.get("isfiring2")
        self.secondary = crucial.get("secondary")
       
    def updateCrucial(self):
        return {"velocity":self.velocity,"heading":self.heading,"pos":self.pos,"rot":self.rot,"isfiring":self.isfiring,"isfiring2":self.isfiring2,"secondary":self.secondary}
        
    def updateNonCrucial(self):
        return {"name":self.name,"shipname":self.shipname,"isai":self.isai,"ship":self.ship,"speed":self.speed,"accel":self.accel,
                "rps":self.rps,"average_ping":self.average_ping,"outfit":self.outfit}
        
def connectPlayer(name,idnum,system):
    player = Player(name,idnum)
    player.system = system
    return player
                    

