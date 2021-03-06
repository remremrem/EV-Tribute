import time
import math
from starsystem import *

class SystemCommander:
    def __init__(self):
        self.systemdict = {}
        print "SYSTEMDICT", str(self.systemdict)
        self.linkdict = {}
        print "linkdict", str(self.linkdict)
        
        self.systemdict = MakeSystemDict("data/systems/systems.list", (13000 * 2, 13000 * 2))
        for x in self.systemdict:
            for y in self.systemdict.get(x).bodies:
                if self.systemdict.get(x).bodies.get(y).type == "sattelite":
                    self.systemdict.get(x).bodies.get(y).locate(self.systemdict.get(x).bodies)
        self.linkdict = MakeLinks(self.systemdict)
        
    def update(self):
        pass
