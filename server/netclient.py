import os,sys,time
sys.path.append(os.path.split(sys.path[0])[0])
from Net import *
class NetData:
    def __init__(self, name="name"):
       self.oldpos = 0
       self.pos = 0
       self.rot = 0
       self.name = name
       self.send_time = 0
       self.receive_time = 0
       self.pinglist = [100,100,100,100,100]
       self.average_ping = 0
       
    def sendData(self, client, player, data):
        client.send_data(data)
        self.send_time = time.time()
        
    def checkData(self, client, player):
        data = client.check_for_data()
        if data:
            self.receive_time = time.time()
            del(self.pinglist[0])
            self.pinglist.append((self.receive_time - self.send_time) * 1000)
            self.average_ping = (int((self.pinglist[0]+self.pinglist[1]+
                                       self.pinglist[2]+self.pinglist[3]+self.pinglist[4])/5.0))
            print "PING: " + str(self.average_ping)
            return data
            
    def waitData(self, client, player):
        data = client.wait_for_data()
        if data:
            self.receive_time = time.time()
            del(self.pinglist[0])
            self.pinglist.append((self.receive_time - self.send_time) * 1000)
            self.average_ping = (int((self.pinglist[0]+self.pinglist[1]+
                                       self.pinglist[2]+self.pinglist[3]+self.pinglist[4])/5.0))
            print "PING: " + str(self.average_ping)
            return data
            
    def netUpdate(self, client, player):
        data = client.check_for_data()
        if data:
            self.receive_time = time.time()
            del(self.pinglist[0])
            self.pinglist.append((self.receive_time - self.send_time) * 1000)
            self.average_ping = (int((self.pinglist[0]+self.pinglist[1]+
                                       self.pinglist[2]+self.pinglist[3]+self.pinglist[4])/5.0))
            print "PING: " + str(self.average_ping)
            if self.oldpos != player.pos:
                self.oldpos = player.pos
                sendingdata = [player.idnum, "pos", [player.pos, player.sprite.rot, player.velocity, player.heading]]
            else: 
                sendingdata = [player.idnum, None]            client.send_data(sendingdata)
            self.send_time = time.time()
            return data
        else:
            #print "NO DATA RECIEVED"
            return [0]
