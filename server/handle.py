import time
try:    import cPickle as pickle
except: import pickle as pickle

##The are all functions that handle requests issued by the clients

def board(data):
    return ["surrender ye' scurvy dogs!"]
    
def buy(data):
    return ["bought some crap"]

def command(data):
    return ["command acknowledged"]
    
def credentials(data, playerdict):
    print "player name " + data[1] + " requests permission to join,"
    print "using password: " + data[2]
    try:
        password = playerdict.get(data[1]).get("[password]")
        if password == data[2]:
            print "password confirmation: ", password, ", request granted."
            print "[SERVER:] ",data[1]," has joined at ",time.asctime()
            return [1,["identity", "confirmed", "Welcome!"]]
        else: 
            print "password invalid: ", password
            "request denied!"
            return [0,["identity", "invalid", "try again"]]
    except:
        print "invalid player name or password!"
        return [0,["identity", "invalid", "try again"]]

def embark(data):
    return ["granted"]

def factionChat(data):
    return ["command acknowledged"]

def jettisonCargo(data):
    return ["command acknowledged"]
                
def jump(data, sysdict):
    return ["system", sysdict.get(data[1])]
    
def land(data):
    return ["granted"]

def missionComputer(data):
    return ["command acknowledged"]
    
def sell(data):
    return ["sold some junk"]

def systemChat(data):
    return ["command acknowledged"]
    
def target(data):
    return ["locking on"]

def update(crucialdict, playingdict, system):
    print "crucialdict",crucialdict
    return ["update", pickle.dumps(system.getCrucial(playingdict,crucialdict))]
    
def whisper(data):
    return ["command acknowledged"]
    
def worldChat(data):
    return ["command acknowledged"]
