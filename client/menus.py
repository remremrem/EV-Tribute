import math
import pyglet
import rabbyt
from pyglet.gl import *
from glart import *

class MainMenu:
    def __init__(self,window):   
        self.width = window[0]
        self.height = window[1]
        self.open = 0
        self.batch = pyglet.graphics.Batch()
        self.name = "Butch"
        
        self.labels = {"Title": (pyglet.text.Label('EV: TRIBUTE',
                                               font_name = 'verdana', font_size = 26,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'center', anchor_y = 'center', 
                                               x = self.width/2,
                                               y = self.height - 70, batch = self.batch)),
                       "Name": (pyglet.text.Label('Name',
                                               font_name = 'verdana', font_size = 14,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'right', anchor_y = 'center', 
                                               x = 300,
                                               y = self.height - 200, batch = self.batch)),
                       "Password": (pyglet.text.Label('Password',
                                               font_name = 'verdana', font_size = 14,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'right', anchor_y = 'center', 
                                               x = 300,
                                               y = self.height - 250, batch = self.batch)),
                       "Attempt": (pyglet.text.Label('',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'center', anchor_y = 'center', 
                                               x = self.width/2,
                                               y = self.height - 150, batch = self.batch))}
        
        self.textentry = {"Name": (OGLTextInput2(content="Rane", height=30, width=200, 
                          pos=(325 , self.height-200), anchor_x="left", anchor_y="center",
                          batch = self.batch)),
                          "Password": (OGLTextInput2(content="tribe", height=30, width=200, 
                          pos=(325 , self.height-250), anchor_x="left", anchor_y="center",
                          batch = self.batch))}
        
        self.buttons = {"LAUNCH": OGLButton(label="LAUNCH", height=50, width=140, 
                         center=(self.width/2, self.height - 350),batch = self.batch),
                        "OPTIONS": OGLButton(label="OPTIONS", height=40, width=100, 
                         center=(self.width-70, 300),batch = self.batch),
                        "CREDITS": OGLButton(label="CREDITS", height=40, width=100, 
                         center=(self.width-70, 240),batch = self.batch),
                        "JETTISON": OGLButton(label="JETTISON", height=40, width=100, 
                         center=(self.width-70, 60),batch = self.batch)}

        
        
    def draw(self):    
        glBegin(GL_QUADS) #start background
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(0, 0)
        glVertex2f(0, self.height)
        glVertex2f(self.width, self.height)
        glVertex2f(self.width, 0)
        glEnd()
        
        for entry in self.textentry:
            self.textentry.get(entry).draw()
        for button in self.buttons:
            self.buttons.get(button).draw()
        self.batch.draw()
    
    def buttonEvent(self, event):
        if event == "LAUNCH":
            print "LAUNCH"
            return "LAUNCH"
        if event == "OPTIONS":
            print "OPTIONS"
            return "OPTIONS"
        if event == "CREDITS":
            print "CREDITS"
            return "CREDITS"
        if event == "JETTISON":
            print "JETTISON"
            return "JETTISON"      
        
    def handleEvent(self, event, x, y):
        if event == "mouse_left":
            value = None
            for entry in self.textentry:
                self.textentry.get(entry).focused = 0
                self.textentry.get(entry).caret.visible = False
                self.textentry.get(entry).caret.mark = self.textentry.get(entry).caret.position = 0
            for button in self.buttons:
                if (x - self.buttons.get(button).center[0] in 
                    range((self.buttons.get(button).width / -2), (self.buttons.get(button).width / 2)) and
                    y - self.buttons.get(button).center[1] in 
                    range((self.buttons.get(button).height / -2), (self.buttons.get(button).height / 2))):
                    value = self.buttonEvent(button)
            for entry in self.textentry:
                if (x - self.textentry.get(entry).center[0] in 
                      range((self.textentry.get(entry).width / -2), (self.textentry.get(entry).width / 2)) and
                      y - self.textentry.get(entry).center[1] in 
                      range((self.textentry.get(entry).height / -2), (self.textentry.get(entry).height / 2))):
                    self.textentry.get(entry).focused = 1
                    self.textentry.get(entry).caret.visible = True
                    self.textentry.get(entry).caret.mark = len(self.textentry.get(entry).document.text)
                    self.textentry.get(entry).caret.position = len(self.textentry.get(entry).document.text)
                    return entry + " Focus"        
            if value == "LAUNCH":    
                return "LAUNCH"
            if value == "OPTIONS":
                return "OPTIONS"
            if value == "CREDITS":
                return "CREDITS"
            if value == "JETTISON":
                return "JETTISON"
                

class OptionsMenu:
    def __init__(self,window): 
        self.width = window[0]
        self.height = window[1]
        self.open = 0
        self.batch = pyglet.graphics.Batch()
        self.name = "stan"
        self.labels = {"OPTIONS": pyglet.text.Label('OPTIONS',
                                           font_name = 'verdana', font_size = 26,
                                           bold = 0, color = (200, 100, 100, 255),
                                           anchor_x = 'center', anchor_y = 'center', 
                                           x = self.width/2,
                                           y = self.height - 100, batch = self.batch),
                       "MODE": pyglet.text.Label('Screen Mode',
                                           font_name = 'verdana', font_size = 12,
                                           bold = 0, color = (200, 100, 100, 255),
                                           anchor_x = 'right', anchor_y = 'center', 
                                           x = self.width/2-100,
                                           y = self.height - 200, batch = self.batch),
                       "RESOLUTION": pyglet.text.Label('Resolution',
                                           font_name = 'verdana', font_size = 12,
                                           bold = 0, color = (200, 100, 100, 255),
                                           anchor_x = 'right', anchor_y = 'center', 
                                           x = self.width/2-100,
                                           y = self.height - 260, batch = self.batch),
                       "FX VOLUME": pyglet.text.Label('FX Volume',
                                           font_name = 'verdana', font_size = 12,
                                           bold = 0, color = (200, 100, 100, 255),
                                           anchor_x = 'right', anchor_y = 'center', 
                                           x = self.width/2-100,
                                           y = self.height - 320, batch = self.batch),
                       "FX VALUE": pyglet.text.Label('80',
                                           font_name = 'verdana', font_size = 12,
                                           bold = 0, color = (200, 100, 100, 255),
                                           anchor_x = 'center', anchor_y = 'center', 
                                           x = self.width/2,
                                           y = self.height - 320, batch = self.batch),
                       "MUSIC VOLUME": pyglet.text.Label('Music Volume',
                                           font_name = 'verdana', font_size = 12,
                                           bold = 0, color = (200, 100, 100, 255),
                                           anchor_x = 'right', anchor_y = 'center', 
                                           x = self.width/2-100,
                                           y = self.height - 380, batch = self.batch),
                       "MUSIC VALUE": pyglet.text.Label('80',
                                           font_name = 'verdana', font_size = 12,
                                           bold = 0, color = (200, 100, 100, 255),
                                           anchor_x = 'center', anchor_y = 'center', 
                                           x = self.width/2,
                                           y = self.height - 380, batch = self.batch)}
  
                                               
        self.buttons = {"FULLSCREEN": OGLButton(label="WINDOWED", height=34, width=100, 
                         center=(self.width/2 , self.height - 200), batch=self.batch),
                        "RESOLUTION": OGLButton(label="800x600", height=34, width=100, 
                         center=(self.width/2 , self.height - 260), batch=self.batch),
                        "FXUP": OGLButton(label="UP", height=30, width=40, 
                         center=(self.width/2+50 , self.height - 320), batch=self.batch),
                        "FXDOWN": OGLButton(label="DOWN", height=30, width=40, 
                         center=(self.width/2-50 , self.height - 320), batch=self.batch),                         
                        "FXMUTE": OGLButton(label="MUTE", height=24, width=40, 
                         center=(self.width/2+120 , self.height - 320), batch=self.batch),
                        "MUSICUP": OGLButton(label="UP", height=30, width=40, 
                         center=(self.width/2+50 , self.height - 380), batch=self.batch),
                        "MUSICDOWN": OGLButton(label="DOWN", height=30, width=40, 
                         center=(self.width/2-50 , self.height - 380), batch=self.batch),
                        "MUSICMUTE": OGLButton(label="MUTE", height=24, width=40, 
                         center=(self.width/2+120 , self.height - 380), batch=self.batch),
                        "CONTROLS": OGLButton(label="CONTROLS", height=34, width=100, 
                         center=(self.width/2 , self.height - 440), batch=self.batch),
                        "BACK": OGLButton(label="BACK", height=40, width=100, 
                         center=(self.width-80 , 40), batch=self.batch)}
    
    def draw(self):    
        glBegin(GL_QUADS) #start background
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(0, 0)
        glVertex2f(0, self.height)
        glVertex2f(self.width, self.height)
        glVertex2f(self.width, 0)
        glEnd()
        
        for button in self.buttons:
            self.buttons.get(button).draw()
        self.batch.draw()
    
    def buttonEvent(self, event):
        return event
        
    def handleEvent(self, event, x, y):
        if event == "mouse_left":
            value = None
            for button in self.buttons:
                if (x - self.buttons.get(button).center[0] in 
                      range((self.buttons.get(button).width / -2), (self.buttons.get(button).width / 2)) and
                      y - self.buttons.get(button).center[1] in 
                      range((self.buttons.get(button).height / -2), (self.buttons.get(button).height / 2))):
                    #value = self.buttonEvent(button) 
                    return button          

class KeyMenu:
    def __init__(self, window):
        self.width = window[0]
        self.height = window[1]
        self.open = 0
        self.batch = pyglet.graphics.Batch()
        self.labels = {"[up]": (pyglet.text.Label('UP',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 60, batch = self.batch)),
                       "[down]": (pyglet.text.Label('DOWN',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 85, batch = self.batch)),
                       "[left]": (pyglet.text.Label('LEFT',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 110, batch = self.batch)),
                       "[right]": (pyglet.text.Label('RIGHT',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 135, batch = self.batch)),
                       "[primary fire]": (pyglet.text.Label('SPACE',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 160, batch = self.batch)),
                       "[secondary fire]": (pyglet.text.Label('LCTRL',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 185, batch = self.batch)),
                       "[cycle secondary]": (pyglet.text.Label('W',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 210, batch = self.batch)),
                       "[target]": (pyglet.text.Label('TAB',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 235, batch = self.batch)),
                       "[target nearest]": (pyglet.text.Label('Q',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 260, batch = self.batch)),
                       "[land]": (pyglet.text.Label('L',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 285, batch = self.batch)),
                       "[cycle planets]": (pyglet.text.Label('SEMICOLON',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 150,
                                               y = self.height - 310, batch = self.batch)),
                       "[map]": (pyglet.text.Label('M',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 500,
                                               y = self.height - 60, batch = self.batch)),
                       "[jump]": (pyglet.text.Label('J',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 500,
                                               y = self.height - 85, batch = self.batch)),
                       "[board]": (pyglet.text.Label('B',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 500,
                                               y = self.height - 110, batch = self.batch)),
                       "[booster]": (pyglet.text.Label('E',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 500,
                                               y = self.height - 135, batch = self.batch)),
                       "[stats]": (pyglet.text.Label('SLASH',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 500,
                                               y = self.height - 160, batch = self.batch)),
                       "[missions]": (pyglet.text.Label('I',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 500,
                                               y = self.height - 185, batch = self.batch)),
                       "[global chat]": (pyglet.text.Label('RETURN',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 500,
                                               y = self.height - 210, batch = self.batch)),
                       "[group chat]": (pyglet.text.Label('BACKSLASH',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 500,
                                               y = self.height - 235, batch = self.batch)),
                       "[gov chat]": (pyglet.text.Label('BRACKETLEFT',
                                               font_name = 'verdana', font_size = 12,
                                               bold = 1, color = (200, 100, 100, 255),
                                               anchor_x = 'left', anchor_y = 'center', 
                                               x = 500,
                                               y = self.height - 260, batch = self.batch))}
                                               
        self.buttons = {"BACK": OGLButton(label="Back", height=40, width=100, 
                         center=(self.width - 70 , 40), batch=self.batch),
                        "SAVE": OGLButton(label="Save", height=40, width=100, 
                         center=(70 , 40), batch=self.batch),
                        "[up]": OGLButton(label="Thrust", height=15, width=100, 
                         center=(70 , self.height - 60), batch=self.batch),
                        "[down]": OGLButton(label="180", height=15, width=100, 
                         center=(70 , self.height - 85), batch=self.batch),
                        "[left]": OGLButton(label="Left", height=15, width=100, 
                         center=(70 , self.height - 110), batch=self.batch),
                        "[right]": OGLButton(label="Right", height=15, width=100, 
                         center=(70 , self.height - 135), batch=self.batch),
                        "[primary fire]": OGLButton(label="Primary", height=15, width=100, 
                         center=(70 , self.height - 160), batch=self.batch),
                        "[secondary fire]": OGLButton(label="Secondary", height=15, width=100, 
                         center=(70 , self.height - 185), batch=self.batch),
                        "[cycle secondary]": OGLButton(label="Cycle Weapon", height=15, width=100, 
                         center=(70 , self.height - 210), batch=self.batch),
                        "[target]": OGLButton(label="Target", height=15, width=100, 
                         center=(70 , self.height - 235), batch=self.batch),
                        "[target nearest]": OGLButton(label="Target Nearest", height=15, width=100, 
                         center=(70 , self.height - 260), batch=self.batch),
                        "[land]": OGLButton(label="Land", height=15, width=100, 
                         center=(70 , self.height - 285), batch=self.batch),
                        "[cycle planets]": OGLButton(label="Cycle Planets", height=15, width=100, 
                         center=(70 , self.height - 310), batch=self.batch),
                        "[map]": OGLButton(label="Map", height=15, width=100, 
                         center=(420 , self.height - 60), batch=self.batch),
                        "[jump]": OGLButton(label="Jump", height=15, width=100, 
                         center=(420 , self.height - 85), batch=self.batch),
                        "[board]": OGLButton(label="Board", height=15, width=100, 
                         center=(420 , self.height - 110), batch=self.batch),
                        "[booster]": OGLButton(label="Booster", height=15, width=100, 
                         center=(420 , self.height - 135), batch=self.batch),
                        "[stats]": OGLButton(label="Player Stats", height=15, width=100, 
                         center=(420 , self.height - 160), batch=self.batch),
                        "[missions]": OGLButton(label="Mission Info", height=15, width=100, 
                         center=(420 , self.height - 185), batch=self.batch),
                        "[global chat]": OGLButton(label="Global Chat", height=15, width=100, 
                         center=(420 , self.height - 210), batch=self.batch),
                        "[group chat]": OGLButton(label="Group Chat", height=15, width=100, 
                         center=(420 , self.height - 235), batch=self.batch),
                        "[gov chat]": OGLButton(label="Gov Chat", height=15, width=100, 
                         center=(420 , self.height - 260), batch=self.batch)}
                         
    def draw(self):    
        glBegin(GL_QUADS) #start background
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(0, 0)
        glVertex2f(0, self.height)
        glVertex2f(self.width, self.height)
        glVertex2f(self.width, 0)
        glEnd()
        
        for button in self.buttons:
            self.buttons.get(button).draw()
        self.batch.draw()
    
   # def buttonEvent(self, event):
   #     if event == "BACK":
   #         print "BACK"
   #         return "BACK"    
        
    def handleEvent(self, event, x, y):
        if event == "mouse_left":
            value = None
            for button in self.buttons:
                if (x - self.buttons.get(button).center[0] in 
                    range((self.buttons.get(button).width / -2), (self.buttons.get(button).width / 2)) and
                    y - self.buttons.get(button).center[1] in 
                    range((self.buttons.get(button).height / -2), (self.buttons.get(button).height / 2))):       
                    return button


class CreditsMenu:
    def __init__(self,window):   
        self.width = window[0]
        self.height = window[1]
        self.open = 0
        self.batch = pyglet.graphics.Batch()
        self.ninja_label = pyglet.text.Label('Farm Ninja  aka: Farm Ninja 23',
                                               font_name = 'verdana', font_size = 26,
                                               bold = 0, color = (200, 100, 100, 255),
                                               anchor_x = 'center', anchor_y = 'center', 
                                               x = self.width-self.width/2,
                                               y = self.height - 70, batch = self.batch)
                                               
        self.cosmo_label = pyglet.text.Label('Cosmonaut Assassin 7',
                                               font_name = 'verdana', font_size = 26,
                                               bold = 0, color = (200, 100, 100, 255),
                                               anchor_x = 'center', anchor_y = 'center', 
                                               x = self.width-self.width/2,
                                               y = self.height - 200, batch = self.batch)
        
        self.buttons = {"BACK": OGLButton(label="BACK", height=40, width=80, 
                         center=(self.width - 80 , 40),batch = self.batch)}

        
        
    def draw(self):    
        glBegin(GL_QUADS) #start background
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(0, 0)
        glVertex2f(0, self.height)
        glVertex2f(self.width, self.height)
        glVertex2f(self.width, 0)
        glEnd()
        
        for button in self.buttons:
            self.buttons.get(button).draw()
        self.batch.draw()
    
    def buttonEvent(self, event):
        if event == "BACK":
            print "BACK"
            return "BACK"    
        
    def handleEvent(self, event, x, y):
        if event == "mouse_left":
            value = None
            for button in self.buttons:
                if (x - self.buttons.get(button).center[0] in 
                    range((self.buttons.get(button).width / -2), (self.buttons.get(button).width / 2)) and
                    y - self.buttons.get(button).center[1] in 
                    range((self.buttons.get(button).height / -2), (self.buttons.get(button).height / 2))):
                    value = self.buttonEvent(button)        
            if value == "BACK":    
                return "BACK"
                
                
class MenuState:
    def __init__(self):
        pass
