import os,sys,time
try:    import cPickle as pickle
except: import pickle as pickle
sys.path.append(os.path.split(sys.path[0])[0])
from Net import *
class NetData:
    def __init__(self, name="name"):
       self.oldpos = 0
       self.pos = 0
       self.rot = 0
       self.name = name
       self.idnum = 0
       self.send_time = 0
       self.receive_time = 0
       self.pinglist = [60,60,60,60,60,60,60,60,60,60,
                        60,60,60,60,60,60,60,60,60,60]
       self.reportping = 0
       self.average_ping = 0
       self.updated = 0
       self.updata = 0
       self.client = TCPClient()
       
    def Connect(self, address, port, password):
        print "connect"
        self.client.connect(address,port)
        self.client.send_data(["credentials", self.name, password])
        data = self.client.wait_for_data()
        print "connect data",data
        if data[0] == "identity":
            if data[1] == "confirmed":
                data = self.client.wait_for_data()
                if data[0] == "startdict":
                    startsystem = data[1]
                    self.idnum = pickle.loads(data[2])
            elif data[1] == "invalid":
                print "Invalid player name OR password."
                return 0
        else: return 0
        self.client.send_data(["hi server",self.idnum])
        return data
    
    def sendData(self, data):
        self.client.send_data(data)
        self.send_time = time.time()
        
    def checkData(self):
        data = self.client.check_for_data()
        if data:
            self.receive_time = time.time()
            pingtime = (self.receive_time - self.send_time) * 1000
            self.pinglist.append(pingtime)
            average = 0
            del(self.pinglist[0])
            for x in self.pinglist:
                average = average + x
            self.average_ping = int(average/len(self.pinglist))
            if data[0] == "update":
                self.updata = data
            if self.reportping < 500:
                self.reportping += pingtime
            else:
                self.reportping = 0
                print "ping:",self.average_ping
            return data
            
    def waitData(self, player):
        data = self.client.wait_for_data()
        if data:
            self.receive_time = time.time()
            self.pinglist.append((self.receive_time - self.send_time) * 1000)
            average = 0
            del(self.pinglist[0])
            for x in self.pinglist:
                average = average + x
            self.average_ping = int(average/len(self.pinglist))
            if data[0] == "update":
                self.updata = data
            return data
            
    def netUpdate(self, player):
        self.checkData()
        if self.updata != 0:
            self.oldpos = player.pos
            sendingdata = ["update", pickle.dumps({"pos":player.pos, "rot":player.rot, "velocity":player.velocity, 
            "heading":player.heading, "isfiring":player.isfiring, "isfiring2":player.isfiring2, "secondary":player.secondary})]
            self.sendData(sendingdata)
            data = self.updata
            self.updata = 0
            return data
        else:
            return [0]
            
    def Jump(self,system):
        self.client.check_for_data()
        self.client.send_data(["jump",system])
        data = self.client.wait_for_data()
        return data
