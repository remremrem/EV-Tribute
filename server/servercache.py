

class ServerCache:
    def __init__(self):
        self.sysdict = {}
        self.linkdict = {}
        self.aidict = {}
        self.govdict = {}
        self.playerdict = {}
        self.playingdict = {}
        self.passdict = {"Rane":"tribute", "Sam":"tribe", "guest":"password"}
        self.accountdict = {}
        self.crucialdict = {}  #crucialdict contains a subset of player data that includes movement and other info that is constantly changing
        self.noncrucialdict = {}  #noncrucialdict contains information like player name, ship, stats, things that aren't changing constantly
        
    def makePlayerDict(self):
        playersfile = open("players/players.list","r")
        playerlist = playersfile.readlines()
        playersfile.close()
        for x in playerlist:
            playerfile = open(("players/"+x.strip()+".player"),"r")
            playerlines = playerfile.readlines()
            playerfile.close()
            properties = []
            values = []
            for a in playerlines:
                if a.startswith("["):
                    properties.append(a.strip())
                elif a.startswith(" "):
                    pass
                else:
                    values.append(a.strip())
            player = dict(zip(properties,values))
            self.playerdict[x.strip()] = player
        print "playerdict:"
        print self.playerdict
