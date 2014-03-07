import pyglet
import rabbyt
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
import tools

class Player:
    def __init__(self,window,panel):
        self.isai = 0
        self.name = "howard"
        self.sprite = rabbyt.Sprite(texture = "data/ships/Rebelfighterblank.png")
        self.sprite.xy = ((window[0]-panel[0])/2, window[1]/2)
        print "CHECK IT"
        print self.sprite.xy
        print window
        print panel
        print "/CHECK IT"
        self.speed = 250
        self.accel = 175
        self.velocity = 0
        self.movement = 0
        self.pos = [0, 0]
        self.pos_time = 0
        self.rps = .6
        self.rot = 0
        self.rot2 = self.sprite.rot
        self.rot_step = 1
        self.rot_time = 0
        self.direction = 0
        self.heading = 0
        self.time = rabbyt.get_time()
        self.isfiring = 0
        self.isfiring2 = 0
        self.secondary = "space bomb"
        self.outfit = []
        self.inspace = 1
        self.docked = 0
        self.system  = None
        self.destination = None
        self.idnum = None
        self.planet = None
        self.location = ["system","body"]
        
    def rotate(self,direction):
        rot_amt = tools.CalcRot(self.rot_time, self.rps, self.rot_step, direction)
        if rot_amt > 0 and self.rot == (360 - rot_amt):
            self.rot = 0
        elif rot_amt < 0 and self.rot == (0):
            self.rot = 360 - self.rot_step
        else:
            self.rot += rot_amt
        self.sprite.rot = self.rot * -1
        if rot_amt <> 0:
            self.rot_time = rabbyt.get_time()
        if self.velocity == 0:
            self.heading, self.direction = self.rot, self.rot
        #print "selfrot",self.rot,"sprite rot",self.sprite.rot
        #print "self.heading",self.heading   
        return None
        
    def instaRotate(self,direction):
        pass
    def accelerate(self,mapsize):
        if self.rot == self.heading:
            self.pos, self.velocity = tools.CalcPos(self.pos, self.pos_time, self.speed, 
                                               self.accel, self.velocity, self.heading)
        elif (self.rot == self.heading - 180) or (self.rot == self.heading + 180):
            self.pos, self.velocity = tools.SlowDown(self.pos, self.pos_time, self.speed, 
                                               self.accel, self.velocity, self.heading)
        else:
            self.heading, self.direction, self.velocity, self.pos = tools.CalcHeading(self.pos, self.pos_time, 
                                                                       self.speed, self.accel, 
                                                                       self.velocity, self.direction, 
                                                                               self.heading, self.rot, self.rot_step)

        if self.velocity == 0:
            self.heading, self.direction = self.rot, self.rot
        self.pos_time = rabbyt.get_time()
        #print "VEC ROT",self.direction,self.rot       
        return None
   
    def glide(self,mapsize):
        self.pos, self.velocity = tools.CalcPos(self.pos, self.pos_time, self.speed, 0, self.velocity, self.heading)
        self.pos_time = rabbyt.get_time()
        
    def about(self):
        if (self.rot == self.heading - 180) or (self.rot == self.heading + 180):
            return None
        if (self.heading >= self.rot):
            if (self.heading - self.rot < 180):
                self.rotate(-1)
            else:
                self.rotate(1)
            return None
        if (self.heading < self.rot):
            if (self.rot - self.heading > 180):
                self.rotate(-1)
            else:
                self.rotate (1)
            return None
            
    def jump(self, system):
        pass
        
        
    def setCrucial(self,crucial):
        self.velocity = crucial.get("velocity")
        self.heading = crucial.get("heading")
        self.pos = crucial.get("pos")
        self.rot = crucial.get("rot")
        self.isfiring = crucial.get("isfiring")
        self.isfiring2 = crucial.get("isfiring2")
        self.secondary = crucial.get("secondary")
       
    def updateCrucial(self):
        return {"velocity":self.velocity,"heading":self.heading,"pos":self.pos,"rot":self.rot,"isfiring":self.isfiring,"isfiring2":self.isfiring2, "secondary":self.player.secondary}
        
    def updateNonCrucial(self):
        return {"name":self.name,"shipname":self.shipname,"isai":self.isai,"ship":self.ship,"speed":self.speed,"accel":self.accel,
                "rps":self.rps,"average_ping":self.average_ping,"average_ping":self.average_ping,"outfit":self.outfit}
        
        
        
class Configuration:
    def __init__(self):
        self.keymap = {}
        self.resolution = 0
        self.fxvolume = 0.8
        self.musicvolume = 0.8
        self.pykeys = {   	 
        "MOD_SHIFT" : 1,
      	"MOD_CTRL" : 2,
      	"MOD_ALT" : 4,
      	"MOD_CAPSLOCK" : 8,
      	"MOD_NUMLOCK" : 16,
      	"MOD_WINDOWS" : 32,
      	"MOD_COMMAND" : 64,
      	"MOD_OPTION" : 128,
      	"MOD_SCROLLLOCK" : 256,
      	"MOD_ACCEL" : 2,
      	"BACKSPACE" : 65288,
      	"TAB" : 65289,
      	"LINEFEED" : 65290,
      	"CLEAR" : 65291,
      	"RETURN" : 65293,
      	"ENTER" : 65293,
      	"PAUSE" : 65299,
      	"SCROLLLOCK" : 65300,
      	"SYSREQ" : 65301,
      	"ESCAPE" : 65307,
      	"HOME" : 65360,
      	"LEFT" : 65361,
      	"UP" : 65362,
      	"RIGHT" : 65363,
      	"DOWN" : 65364,
      	"PAGEUP" : 65365,
      	"PAGEDOWN" : 65366,
      	"END" : 65367,
      	"BEGIN" : 65368,
      	"DELETE" : 65535,
      	"SELECT" : 65376,
      	"PRINT" : 65377,
      	"EXECUTE" : 65378,
      	"INSERT" : 65379,
      	"UNDO" : 65381,
      	"REDO" : 65382,
      	"MENU" : 65383,
      	"FIND" : 65384,
      	"CANCEL" : 65385,
      	"HELP" : 65386,
      	"BREAK" : 65387,
      	"MODESWITCH" : 65406,
      	"SCRIPTSWITCH" : 65406,
      	"MOTION_UP" : 65362,
      	"MOTION_RIGHT" : 65363,
      	"MOTION_DOWN" : 65364,
      	"MOTION_LEFT" : 65361,
      	"MOTION_NEXT_WORD" : 1,
      	"MOTION_PREVIOUS_WORD" : 2,
      	"MOTION_BEGINNING_OF_LINE" : 3,
      	"MOTION_END_OF_LINE" : 4,
      	"MOTION_NEXT_PAGE" : 65366,
      	"MOTION_PREVIOUS_PAGE" : 65365,
      	"MOTION_BEGINNING_OF_FILE" : 5,
      	"MOTION_END_OF_FILE" : 6,
      	"MOTION_BACKSPACE" : 65288,
      	"MOTION_DELETE" : 65535,
      	"NUMLOCK" : 65407,
      	"NUM_SPACE" : 65408,
      	"NUM_TAB" : 65417,
      	"NUM_ENTER" : 65421,
      	"NUM_F1" : 65425,
      	"NUM_F2" : 65426,
      	"NUM_F3" : 65427,
      	"NUM_F4" : 65428,
      	"NUM_HOME" : 65429,
      	"NUM_LEFT" : 65430,
      	"NUM_UP" : 65431,
      	"NUM_RIGHT" : 65432,
      	"NUM_DOWN" : 65433,
      	"NUM_PRIOR" : 65434,
      	"NUM_PAGE_UP" : 65434,
      	"NUM_NEXT" : 65435,
      	"NUM_PAGE_DOWN" : 65435,
      	"NUM_END" : 65436,
      	"NUM_BEGIN" : 65437,
      	"NUM_INSERT" : 65438,
      	"NUM_DELETE" : 65439,
      	"NUM_EQUAL" : 65469,
      	"NUM_MULTIPLY" : 65450,
      	"NUM_ADD" : 65451,
      	"NUM_SEPARATOR" : 65452,
      	"NUM_SUBTRACT" : 65453,
      	"NUM_DECIMAL" : 65454,
      	"NUM_DIVIDE" : 65455,
      	"NUM_0" : 65456,
      	"NUM_1" : 65457,
      	"NUM_2" : 65458,
      	"NUM_3" : 65459,
      	"NUM_4" : 65460,
      	"NUM_5" : 65461,
      	"NUM_6" : 65462,
      	"NUM_7" : 65463,
      	"NUM_8" : 65464,
      	"NUM_9" : 65465,
      	"F1" : 65470,
      	"F2" : 65471,
      	"F3" : 65472,
      	"F4" : 65473,
      	"F5" : 65474,
      	"F6" : 65475,
      	"F7" : 65476,
      	"F8" : 65477,
      	"F9" : 65478,
      	"F10" : 65479,
      	"F11" : 65480,
      	"F12" : 65481,
      	"F13" : 65482,
      	"F14" : 65483,
      	"F15" : 65484,
      	"F16" : 65485,
      	"LSHIFT" : 65505,
      	"RSHIFT" : 65506,
      	"LCTRL" : 65507,
      	"RCTRL" : 65508,
      	"CAPSLOCK" : 65509,
      	"LMETA" : 65511,
      	"RMETA" : 65512,
      	"LALT" : 65513,
      	"RALT" : 65514,
      	"LWINDOWS" : 65515,
      	"RWINDOWS" : 65516,
      	"LCOMMAND" : 65517,
      	"RCOMMAND" : 65518,
      	"LOPTION" : 65488,
      	"ROPTION" : 65489,
      	"SPACE" : 32,
      	"EXCLAMATION" : 33,
      	"DOUBLEQUOTE" : 34,
      	"HASH" : 35,
      	"POUND" : 35,
      	"DOLLAR" : 36,
      	"PERCENT" : 37,
      	"AMPERSAND" : 38,
      	"APOSTROPHE" : 39,
      	"PARENLEFT" : 40,
      	"PARENRIGHT" : 41,
      	"ASTERISK" : 42,
      	"PLUS" : 43,
      	"COMMA" : 44,
        "MINUS" : 45,
      	"PERIOD" : 46,
      	"SLASH" : 47,
      	"COLON" : 58,
      	"SEMICOLON" : 59,
      	"LESS" : 60,
      	"EQUAL" : 61,
      	"GREATER" : 62,
      	"QUESTION" : 63,
      	"AT" : 64,
      	"BRACKETLEFT" : 91,
      	"BACKSLASH" : 92,
      	"BRACKETRIGHT" : 93,
      	"ASCIICIRCUM" : 94,
      	"UNDERSCORE" : 95,
      	"GRAVE" : 96,
      	"QUOTELEFT" : 96,
      	"A" : 97,
      	"B" : 98,
      	"C" : 99,
      	"D" : 100,
      	"E" : 101,
      	"F" : 102,
      	"G" : 103,
      	"H" : 104,
      	"I" : 105,
      	"J" : 106,
      	"K" : 107,
      	"L" : 108,
      	"M" : 109,
      	"N" : 110,
      	"O" : 111,
      	"P" : 112,
      	"Q" : 113,
      	"R" : 114,
      	"S" : 115,
      	"T" : 116,
      	"U" : 117,
      	"V" : 118,
      	"W" : 119,
      	"X" : 120,
      	"Y" : 121,
      	"Z" : 122,
      	"BRACELEFT" : 123,
      	"BAR" : 124,
      	"BRACERIGHT" : 125,
      	"ASCIITILDE" : 126}
      	

    def getControls(self, filename="data/players/default/default.key"):
        keyfile = open(filename,"r")
        keylines = keyfile.readlines()
        keys = tools.ParseLines(keylines)
        return keys
