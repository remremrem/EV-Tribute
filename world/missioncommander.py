from aitools import *
import time

class MissionComputer:
    def __init__(self,planet="Earth",system="Sol"):
        self.planet = planet
        self.system = system
        self.missions = {}
        
class Mission:
    def __init__(self, data):
        self.idnum = data.get("idnum")
        self.title = data.get("title")
        self.mtype = data.get("mtype")
        self.start = data.get("start")
        self.finish = data.get("finish")
        self.agency = data.get("agency")
        self.filename = data.get("filename")
        self.source = data.get("source")
        self.description = data.get("description")
        self.start = data.get("start")
        self.finish = data.get("finish")
        self.time = data.get("time")
        self.cargo = data.get("cargo")
        self.camount = data.get("camount")
        self.passengers = data.get("passengers")
        self.pamount = data.get("pamount")
        self.target = data.get("target")
        self.tname = data.get("tname")
        self.tsystem = data.get("tsystem")
        self.shiptype = data.get("shiptype")
        self.escorts = data.get("escorts")
        self.objective = data.get("objective")
        self.payout = data.get("payout")
        self.string = data.get("string")
        self.stringfile = data.get("stringfile")
        self.dialogues = data.get("dialogues")
