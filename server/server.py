print "Tribe Venture Server"
import os,sys,time
try:    import cPickle as pickle
except: import pickle as pickle
sys.path.append(os.path.split(sys.path[0])[0])
from Net import *
import player
import servercache
import handle

########    BEGIN SERVER    #########


class GameServer(TCPServer):
    def __init__(self):
        TCPServer.__init__(self)
        self.Cache = servercache.ServerCache()
        self.Cache.makePlayerDict()
        self.average_ping = 0
        self.pinglist = [100,100,100,100,100]
        
    def connect_func(self,sock,host,port):
        print "Server successfully connected to %s on port %s!" % (host,port)
    def client_connect_func(self,sock,host,port,address):
        print "A client, (ip: %s, code: %s) connected on port %s!" % (address[0],address[1],port)
        self.newclient = [address[0], address[1]]
        print "NEWCLIENT: " + str(address[0]) + " and " + str(address[1])
        #print "self.newclient: "+str(self.newclient)
    def client_disconnect_func(self,sock,host,port,address):
        print "A client, (ip: %s, code: %s) disconnected from port %s!" % (address[0],address[1],port)
        print "ADDRESS", address
        for x in self.Cache.playingdict:
            print "X",x
            if x == address[1]:
                print "X DISCONNN"
                self.Cache.sysdict.get(self.Cache.playingdict.get(address[1]).system).players.remove(x)
                self.Cache.playingdict.pop(x)
                self.Cache.crucialdict.pop(x)
                self.Cache.noncrucialdict.pop(x)                
                break

    def handle_data(self, data, address):
        if data[0] == "WORLD":                  # WORLD DATA HANDLING
            #print "data"
            #print data
            if data[1] == "update":
                print "WORLD UPDATE"
                self.send_data("thanks")
                return None
            elif data[1] == "sysdict":
                print "SYSTEMS"
                self.Cache.sysdict[data[2]] = pickle.loads(data[3])
                print data[2]
                self.send_data("Nice System")
                return None
            elif data[1] == "init":
                print "INIT WORLD"
                self.send_data("Hello, World")
                return None                   # /WORLD DATA HANDLING

                
        elif data[0] == "update":                    # PLAYER DATA HANDLING
            self.Cache.playingdict.get(address[1]).setCrucial(pickle.loads(data[1]))
            self.Cache.crucialdict[address[1]] = self.Cache.playingdict.get(address[1]).updateCrucial()
            self.send_data(handle.update(self.Cache.crucialdict,self.Cache.playingdict,self.Cache.sysdict.get(self.Cache.playingdict.get(address[1]).system)),1)
            return 0
        elif data[0] == "pos_plus":
            pass
        elif data[0] == "jump":
            self.send_data(handle.jump(data,self.Cache.sysdict))
        elif data[0] == "sell":
            self.send_data(handle.sell(data))
        elif data[0] == "buy":
            self.send_data(handle.buy(data))
        elif data[0] == "command":
            self.send_data(handle.command(data))
        elif data[0] == "board":
            self.send_data(handle.board(data))
        elif data[0] == "target":
            self.send_data(handle.target(data))
        elif data[0] == "land":
            self.send_data(handle.land(data))
        elif data[0] == "embark":
            self.send_data(handle.embark(data))
        elif data[0] == "worldchat":
            self.send_data(handle.worldChat(data))
        elif data[0] == "systemchat":
            self.send_data(handle.systemChat(data))
        elif data[0] == "factionchat":
            self.send_data(handle.factionChat(data))
        elif data[0] == "whisper":
            self.send_data(handle.whisper(data))
        elif data[0] == "missioncomputer":
            self.send_data(handle.missionComputer(data))
        elif data[0] == "jettisoncargo":
            self.send_data(handle.jettisonCargo(data))
        elif data[0] == "credentials":
            confirmation = handle.credentials(data,self.Cache.playerdict)
            print "confirmation",confirmation
            self.send_data(confirmation[1])
            if confirmation[0] == 1:
                startsystem = "Sol"
                print "SYSDICT",self.Cache.sysdict
                system = self.Cache.sysdict.get(startsystem)
                print "system",system
                self.Cache.playingdict[self.newclient[1]] = player.connectPlayer(data[1],self.newclient[1],startsystem)
                print "playingdict: ",self.Cache.playingdict
                self.Cache.crucialdict[self.newclient[1]] = self.Cache.playingdict.get(self.newclient[1]).updateCrucial()
                self.Cache.noncrucialdict[self.newclient[1]] = self.Cache.playingdict.get(self.newclient[1]).updateNonCrucial()
                self.send_data(["startdict", pickle.dumps(system), 
                    pickle.dumps(system.getNonCrucial(self.Cache.playingdict, self.Cache.noncrucialdict)),
                        pickle.dumps(system.getCrucial(self.Cache.playingdict, self.Cache.crucialdict)),
                            self.newclient[1]],1)
                self.Cache.sysdict.get(startsystem).players.append(self.newclient[1])
                print "PLAYERS", self.Cache.sysdict.get(startsystem).players


########    END SERVER    ########

def main():
    gameserver = GameServer()
    gameserver.connect("localhost",6317)
    gameserver.serve_forever()
    gameserver.quit()
if __name__ == '__main__': main()
