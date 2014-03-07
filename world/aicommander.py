import time,math
from aiclasses import *
import aitools
#from aidatabase import *

class AICommander:
    def __init__(self):      
        f = open("npcs/governments")
        governments = []
        for line in f:
            governments.append(line.rstrip("\n"))
        f.close()
        print "GOVERNMENTS: " + str(governments)
        aiDict = {}
        for x in governments:
            aiDict[x] = {}
            f = open("npcs/" + x + "/" + x + ".gov")
            for line in f:
                aiDict.get(x)[line.rstrip("\n")] = NPC()
            f.close()
        print "aiDict"
        print aiDict
        #self.galaxy = LoadGalaxy()
        #self.npcs = aitools.loadNPCs()
        
        
    def update(self):
        pass
   
    
if __name__ == '__main__':
    commander = Commander()
