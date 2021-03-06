import time,math
import systemcommander
import aicommander
from Net import *
from worldnetclient import NetData
try:    import cPickle as pickle
except: import pickle as pickle
import zlib

class WorldCommander:
    def __init__(self):
        self.sysComm = systemcommander.SystemCommander()
        #self.aiComm = aicommander.AICommander()      
        self.client = TCPClient()
        self.client.connect("localhost",6317)
        self.client.send_data(["WORLD","init","initialisation crap"])
        self.netdata = self.client.wait_for_data()
        print "self.netdata", str(self.netdata)
        self.client.send_data(["WORLD","update",None])
        for name in self.sysComm.systemdict:
            value = self.sysComm.systemdict.get(name)
            print value 
            self.client.send_data(["WORLD","sysdict", name, pickle.dumps(value)],1)
        print "GLAXY"
        self.netdata = NetData("GaLaXy")
        print self.netdata
        
        def main():
            #self.aiComm.update()
            self.sysComm.update()
            data_type = "WORLD"
            data = None
            ackcount = 0
            while 1 == 1:
                netinfo = self.netdata.NetUpdate(self.client, data_type, ["hi"])
                if netinfo == "none":
                    time.sleep(.01)
                    self.client.send_data(["WORLD","ack"+str(ackcount),None],1)
                    ackcount += 1
                    #print "NONEY"
                else:
                    pass
                    #print str(netinfo)
                
        main()
        
        
        
        
if __name__ == '__main__':
    commander = WorldCommander()
