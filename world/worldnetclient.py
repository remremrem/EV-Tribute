import os,sys
sys.path.append(os.path.split(sys.path[0])[0])
from Net import *

class NetData:
    def __init__(self, name="name"):
       self.name = name

    def NetUpdate(self, client, data_type, data_out):
        data_in = client.check_for_data()
        #print "DATA" + str(data)
        if data_in:            client.send_data([data_type, data_out])
            return data_in
        else:
            return "none"
