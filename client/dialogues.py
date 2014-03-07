import math
import pyglet
import rabbyt
from pyglet.gl import *
from glart import *
from sounds import *

class MapDialogue:
    def __init__(self,window):
        self.window = window    
        self.width = 500
        self.height = 500
        self.margin = [(window[0] - self.width) / 2 ,(window[1] - self.height) / 2]
        self.corners = [(self.margin[0], self.margin[1]), (self.margin[0], window[1] - self.margin[1]),
                        (window[0] - self.margin[0], window[1] -self.margin[1]), (window[0] - self.margin[0], self.margin[1])]
        self.center = (window[0]/2, window[1]/2)
        self.open = 0
        self.maplocation = [0,0]
        self.zoom = 3
        self.selected = None
        self.active = None
        self.activelinks = []
        self.batch = pyglet.graphics.Batch()
        self.buttons = {"ZOOM": OGLButton(label="ZOOM", height=20, width=62, 
                         center=(self.corners[0][0]+50,self.corners[0][1]+20),batch = self.batch, font_size=10),
                        "OUT": OGLButton(label="OUT", height=20, width=62, 
                         center=(self.corners[0][0]+125,self.corners[0][1]+20),batch = self.batch, font_size=10),
                        "CONFIRM": OGLButton(label="CONFIRM", height=20, width=70, 
                         center=(self.corners[0][0]+300,self.corners[0][1]+20),batch = self.batch, font_size=10),
                        "ABORT": OGLButton(label="ABORT", height=20, width=70, 
                         center=(self.corners[0][0]+375,self.corners[0][1]+20),batch = self.batch, font_size=10)}
      
    def draw(self,systemdict,linkdict):    
        thick=2
        glBegin(GL_QUADS)
        #glColor3f(0.0, 0.0, 0.0)
        #glVertex2f(self.corners[0][0], self.corners[0][1])
        #glVertex2f(self.corners[1][0], self.corners[1][1])
        #glVertex2f(self.corners[2][0], self.corners[2][1])
        #glVertex2f(self.corners[3][0], self.corners[3][1])
       
        glColor3f(0.1, 0.1, 0.1)  #start border
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[1][0] + thick, self.corners[1][1])
        glVertex2f(self.corners[0][0] + thick, self.corners[0][1])
        
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[2][0], self.corners[2][1] - thick)
        glVertex2f(self.corners[1][0], self.corners[1][1] - thick)
        
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[3][0] - thick, self.corners[3][1])
        glVertex2f(self.corners[2][0] - thick, self.corners[2][1])
        
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[0][0], self.corners[0][1] + thick)
        glVertex2f(self.corners[3][0], self.corners[3][1] + thick)
        glEnd()
        
        glPointSize(7.0)
        glBegin(GL_POINTS)
        glColor3f(0.247, 0.463, 0.682)
        for item in systemdict:
            system = systemdict.get(item)
            x = self.maplocation[0] + self.center[0] + system.location[0]*self.zoom
            y = self.maplocation[1] + self.center[1] + system.location[1]*self.zoom
            system.icon = [x,y]
            #print "SYSTEM" + system
            if system.active == 1:
                glColor3f(1.0, 0.678, 1.0)
            elif item == self.selected:
                glColor3f(0.463, 0.678, 1.0)
            glVertex2f(x, y)
            glColor3f(0.247, 0.463, 0.682)
        glEnd()
        glLineWidth(1.0)
        glBegin(GL_LINES)
        glColor3f(0.25, 0.468, 0.69)        
        for item in linkdict:
            link = linkdict.get(item)
            ax = self.maplocation[0] + self.center[0] + link.start[0] * self.zoom
            ay = self.maplocation[1] + self.center[1] + link.start[1] * self.zoom
            bx = self.maplocation[0] + self.center[0] + link.end[0] * self.zoom
            by = self.maplocation[1] + self.center[1] + link.end[1] * self.zoom
            if link.active == 1:
                glColor3f(0.4196, 0.1373, 0.5569)
            elif link.plotted == 1:
                glColor3f(0.0, 1.0, 0.498)
            glVertex2f(ax, ay)
            glVertex2f(bx, by)
            glColor3f(0.25, 0.468, 0.69)
        glEnd()
        for button in self.buttons:
            self.buttons.get(button).draw()
        self.batch.draw()
    
    def buttonEvent(self, event):
        if event == "ZOOM":
            pass
        if event == "OUT":
            pass
        if event == "CONFIRM":
            self.open = 0
            return 1
        if event == "ABORT":
            self.open = 0
            return None
    
    def highlightLinks(self, linkdict, activesystem):
        for link in linkdict:
            if (linkdict.get(link).name == str(self.selected)+activesystem or 
                linkdict.get(link).name == activesystem+str(self.selected)):
                linkdict.get(link).active = 1
            else: linkdict.get(link).active = 0      
        
    def handleEvent(self, event, systemdict, selectedsystem, activesystem, linkdict, x, y, sounds):
        if event == "mouse_left":
            value = None
            wasbutton = 0
            for button in self.buttons:
                if (x - self.buttons.get(button).center[0] in 
                    range(self.buttons.get(button).width * -1, self.buttons.get(button).width) and
                    y - self.buttons.get(button).center[1] in 
                    range(self.buttons.get(button).height * -1, self.buttons.get(button).height)):
                    value = self.buttonEvent(button)
                    wasbutton = 1
                    sounds.menu1.play()
            if wasbutton == 0:
                for system in systemdict:
                    if (x - systemdict.get(system).icon[0] in range(-7,7) and 
                       y - systemdict.get(system).icon[1] in range(-7,7)):                        
                        if system == self.selected:
                            self.selected = None
                            value = None
                        elif systemdict.get(system).selected != self.selected:
                            self.selected = system
                            value = None
                        break
            self.highlightLinks(linkdict, activesystem)
            if value == None:
                return selectedsystem
            if value == 1:
                return self.selected

            
class DockDialogue:
    def __init__(self,window):
        self.window = window    
        self.width = 400
        self.height = 400
        self.margin = [(window[0] - self.width) / 2 ,(window[1] - self.height) / 2]
        self.corners = [(self.margin[0], self.margin[1]), (self.margin[0], window[1] - self.margin[1]),
                        (window[0] - self.margin[0], window[1] -self.margin[1]), (window[0] - self.margin[0], self.margin[1])]
        self.center = (window[0]/2, window[1]/2)
        self.open = 0
        self.batch = pyglet.graphics.Batch()
        self.buttons = {"ANTIMATTER": OGLButton(label="ANTIMATTER", height=20, width=50, 
                         center=(self.corners[2][0]-50,self.corners[2][1]-150),batch = self.batch),
                        "JOBS": OGLButton(label="JOBS", height=20, width=50, 
                         center=(self.corners[2][0]-50,self.corners[2][1]-180),batch = self.batch),
                        "OUTFIT": OGLButton(label="OUTFIT", height=20, width=50, 
                         center=(self.corners[2][0]-50,self.corners[2][1]-210),batch = self.batch),
                        "EMBARK": OGLButton(label="EMBARK", height=20, width=50, 
                         center=(self.corners[2][0]-50,self.corners[2][1]-240),batch = self.batch)}

        
        
    def draw(self):    
        thick=2
        glBegin(GL_QUADS) #start background
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[3][0], self.corners[3][1])
       
        glColor3f(0.4, 0.5, 0.2)  #start border
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[1][0] + thick, self.corners[1][1])
        glVertex2f(self.corners[0][0] + thick, self.corners[0][1])
        
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[2][0], self.corners[2][1] - thick)
        glVertex2f(self.corners[1][0], self.corners[1][1] - thick)
        
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[3][0] - thick, self.corners[3][1])
        glVertex2f(self.corners[2][0] - thick, self.corners[2][1])
        
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[0][0], self.corners[0][1] + thick)
        glVertex2f(self.corners[3][0], self.corners[3][1] + thick)
        glEnd()
        
        for button in self.buttons:
            self.buttons.get(button).draw()
        self.batch.draw()  
        
    def handleEvent(self, event, x, y, sounds):
        if event == "mouse_left":
            for button in self.buttons:
                if (x - self.buttons.get(button).center[0] in 
                    range(self.buttons.get(button).width * -1, self.buttons.get(button).width) and
                    y - self.buttons.get(button).center[1] in 
                    range(self.buttons.get(button).height * -1, self.buttons.get(button).height)):
                    sounds.menu1.play()
                    return button
                    
class MenuDialogue:
    def __init__(self,window):
        self.docked = 0
        self.window = window    
        self.width = 250
        self.height = 300
        self.margin = [(window[0] - self.width) / 2 ,(window[1] - self.height) / 2]
        self.corners = [(self.margin[0], self.margin[1]), (self.margin[0], window[1] - self.margin[1]),
                        (window[0] - self.margin[0], window[1] -self.margin[1]), (window[0] - self.margin[0], self.margin[1])]
        self.center = (window[0]/2, window[1]/2)
        self.open = 0
        self.batch = pyglet.graphics.Batch()
        self.buttons = {"BACK": OGLButton(label="BACK", height=30, width=70, 
                         center=(self.center[0],self.center[1]+50),batch = self.batch),
                        "OPTIONS": OGLButton(label="OPTIONS", height=30, width=70, 
                         center=(self.center[0],self.center[1]),batch = self.batch),
                        "QUIT": OGLButton(label="QUIT", height=30, width=70, 
                         center=(self.center[0],self.center[1]-50),batch = self.batch)}
        
    def draw(self):    
        thick=2
        glBegin(GL_QUADS) #start background
        if self.docked == 1:
            glColor3f(0.0, 0.0, 0.0)
            glVertex2f(self.corners[0][0], self.corners[0][1])
            glVertex2f(self.corners[1][0], self.corners[1][1])
            glVertex2f(self.corners[2][0], self.corners[2][1])
            glVertex2f(self.corners[3][0], self.corners[3][1])
       
        glColor3f(0.4, 0.5, 0.2)  #start border
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[1][0] + thick, self.corners[1][1])
        glVertex2f(self.corners[0][0] + thick, self.corners[0][1])
        
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[2][0], self.corners[2][1] - thick)
        glVertex2f(self.corners[1][0], self.corners[1][1] - thick)
        
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[3][0] - thick, self.corners[3][1])
        glVertex2f(self.corners[2][0] - thick, self.corners[2][1])
        
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[0][0], self.corners[0][1] + thick)
        glVertex2f(self.corners[3][0], self.corners[3][1] + thick)
        glEnd()
        
        for button in self.buttons:
            self.buttons.get(button).draw()
        self.batch.draw()  
        
    def handleEvent(self, event, x, y, sounds):
        if event == "mouse_left":
            for button in self.buttons:
                if (x - self.buttons.get(button).center[0] in 
                    range(self.buttons.get(button).width * -1, self.buttons.get(button).width) and
                    y - self.buttons.get(button).center[1] in 
                    range(self.buttons.get(button).height * -1, self.buttons.get(button).height)):
                    sounds.menu1.play()
                    return button      
                    
                    
class OptionsDialogue:
    def __init__(self,window):
        self.docked = 0
        self.window = window    
        self.width = window[0]-40
        self.height = window[1]-40
        self.margin = [(window[0] - self.width) / 2 ,(window[1] - self.height) / 2]
        self.corners = [(self.margin[0], self.margin[1]), (self.margin[0], window[1] - self.margin[1]),
                        (window[0] - self.margin[0], window[1] -self.margin[1]), (window[0] - self.margin[0], self.margin[1])]
        self.center = (window[0]/2, window[1]/2)
        self.open = 0
        self.batch = pyglet.graphics.Batch()
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
                         center=(self.width-80 , 60), batch=self.batch)}
        
    def draw(self):    
        thick=2
        glBegin(GL_QUADS) #start background
        if self.docked == 1:
            glColor3f(0.0, 0.0, 0.0)
            glVertex2f(self.corners[0][0], self.corners[0][1])
            glVertex2f(self.corners[1][0], self.corners[1][1])
            glVertex2f(self.corners[2][0], self.corners[2][1])
            glVertex2f(self.corners[3][0], self.corners[3][1])
       
        glColor3f(0.4, 0.5, 0.2)  #start border
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[1][0] + thick, self.corners[1][1])
        glVertex2f(self.corners[0][0] + thick, self.corners[0][1])
        
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[2][0], self.corners[2][1] - thick)
        glVertex2f(self.corners[1][0], self.corners[1][1] - thick)
        
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[3][0] - thick, self.corners[3][1])
        glVertex2f(self.corners[2][0] - thick, self.corners[2][1])
        
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[0][0], self.corners[0][1] + thick)
        glVertex2f(self.corners[3][0], self.corners[3][1] + thick)
        glEnd()
        
        for button in self.buttons:
            self.buttons.get(button).draw()
        self.batch.draw()   
        
    def handleEvent(self, event, x, y, sounds):
        if event == "mouse_left":
            for button in self.buttons:
                if (x - self.buttons.get(button).center[0] in 
                    range(self.buttons.get(button).width * -1, self.buttons.get(button).width) and
                    y - self.buttons.get(button).center[1] in 
                    range(self.buttons.get(button).height * -1, self.buttons.get(button).height)):
                    sounds.menu1.play()
                    return button              
                    
                    
class ControlsDialogue:
    def __init__(self,window):
        self.docked = 0
        self.window = window    
        self.width = window[0]-40
        self.height = window[1]-40
        self.margin = [(window[0] - self.width) / 2 ,(window[1] - self.height) / 2]
        self.corners = [(self.margin[0], self.margin[1]), (self.margin[0], window[1] - self.margin[1]),
                        (window[0] - self.margin[0], window[1] -self.margin[1]), (window[0] - self.margin[0], self.margin[1])]
        self.center = (window[0]/2, window[1]/2)
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
                         center=(self.width - 70 , 60), batch=self.batch),
                        "SAVE": OGLButton(label="Save", height=40, width=100, 
                         center=(70 , 60), batch=self.batch),
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
        thick=2
        glBegin(GL_QUADS) #start background
        if self.docked == 1:
            glColor3f(0.0, 0.0, 0.0)
            glVertex2f(self.corners[0][0], self.corners[0][1])
            glVertex2f(self.corners[1][0], self.corners[1][1])
            glVertex2f(self.corners[2][0], self.corners[2][1])
            glVertex2f(self.corners[3][0], self.corners[3][1])
       
        glColor3f(0.4, 0.5, 0.2)  #start border
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[1][0] + thick, self.corners[1][1])
        glVertex2f(self.corners[0][0] + thick, self.corners[0][1])
        
        glVertex2f(self.corners[1][0], self.corners[1][1])
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[2][0], self.corners[2][1] - thick)
        glVertex2f(self.corners[1][0], self.corners[1][1] - thick)
        
        glVertex2f(self.corners[2][0], self.corners[2][1])
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[3][0] - thick, self.corners[3][1])
        glVertex2f(self.corners[2][0] - thick, self.corners[2][1])
        
        glVertex2f(self.corners[3][0], self.corners[3][1])
        glVertex2f(self.corners[0][0], self.corners[0][1])
        glVertex2f(self.corners[0][0], self.corners[0][1] + thick)
        glVertex2f(self.corners[3][0], self.corners[3][1] + thick)
        glEnd()
        
        for button in self.buttons:
            self.buttons.get(button).draw()
        self.batch.draw()   
        
    def handleEvent(self, event, x, y, sounds):
        if event == "mouse_left":
            for button in self.buttons:
                if (x - self.buttons.get(button).center[0] in 
                    range(self.buttons.get(button).width * -1, self.buttons.get(button).width) and
                    y - self.buttons.get(button).center[1] in 
                    range(self.buttons.get(button).height * -1, self.buttons.get(button).height)):
                    sounds.menu1.play()
                    return button              
