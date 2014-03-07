import pyglet
from pyglet.gl import *
import math

class OGLButton:
    def __init__(self, label="BUTTON!", height=20, width=50, center=(0,0), color=(.247, .463, .682, .2), border=3, border_color=0, font_color=(127,127,127,200), font_size=12, font_name="verdana", bold=1, batch=None):
        self.text = label
        self.height = height
        self.width = width
        self.center = center
        self.color = color
        self.border = border
        if border_color != 0:
            self.border_color = border_color
        else:
            self.border_color = color
        self.font_color = font_color
        self.font_size = font_size
        self.font_name = font_name
        self.bold = bold
        self.corners = {"SW": (self.center[0]-self.width/2, self.center[1]-self.height/2),
                       "NW": (self.center[0]-self.width/2, self.center[1]+self.height/2),
                       "NE": (self.center[0]+self.width/2, self.center[1]+self.height/2),
                       "SE": (self.center[0]+self.width/2, self.center[1]-self.height/2)}
        self.bounds = {"N": center[0]+self.height, "S": center[0]-self.height,
                       "E": center[1]+self.width, "W": center[1]-self.width}
        self.label = pyglet.text.Label(label, font_name = self.font_name, font_size = self.font_size,
                                       bold = self.bold, color = self.font_color,
                                       anchor_x = 'center', anchor_y = 'center',
                                       x = self.center[0], y = self.center[1], batch = batch)
                                       
    def draw(self):
        glBegin(GL_QUADS)
        glColor4f(self.border_color[0]+.075,self.border_color[1]+.075,self.border_color[2]+.075, .25)
        glVertex2f(self.corners.get("SW")[0], self.corners.get("SW")[1])
        glVertex2f(self.corners.get("NW")[0], self.corners.get("NW")[1])
        glColor4f(self.border_color[0]+.1,self.border_color[1]+.1,self.border_color[2]+.1, .35)
        glVertex2f(self.corners.get("NE")[0], self.corners.get("NE")[1])
        glVertex2f(self.corners.get("SE")[0], self.corners.get("SE")[1])
        
        glColor4f(self.color[0],self.color[1],self.color[2],self.color[3])
        glVertex2f(self.corners.get("SW")[0]+self.border, self.corners.get("SW")[1]+self.border)
        glVertex2f(self.corners.get("NW")[0]+self.border, self.corners.get("NW")[1]-self.border)
        glVertex2f(self.corners.get("NE")[0]-self.border, self.corners.get("NE")[1]-self.border)
        glVertex2f(self.corners.get("SE")[0]-self.border, self.corners.get("SE")[1]+self.border)
        
        glEnd()
        if self.label.batch == None:
            self.label.draw()
        
        
class OGLTextInput:
    def __init__(self, content="text", height=14, width=50, pos=(0,0), color=(.3,.3,.3), 
                   cursor=(2,8), anchor_x="center", anchor_y="center",batch=None):
        self.focused = 0
        self.column = 0
        self.line = 0
        self.cursor = cursor
        self.content = content
        self.height = height
        self.width = width
        self.pos = pos
        self.color = color
        if anchor_x == "left":
            self.left = 0
            self.right = 1
        elif anchor_x == "right":
            self.left = 1
            self.right = 0
        else: 
            self.left = .5
            self.right = .5
        if anchor_y == "top":
            self.top = 0
            self.bottom = 1
        elif anchor_y == "bottom":
            self.top = 1
            self.bottom = 0
        else: 
            self.top = .5
            self.bottom = .5
            
        self.bounds = {"N": self.pos[1]+self.height*self.top, "S": self.pos[1]-self.height*self.bottom,
                       "E": self.pos[0]+self.width*self.right, "W": self.pos[0]-self.width*self.left}
                       
        self.corners = {"SW": (self.bounds.get("W"), self.bounds.get("S")),
                         "NW": (self.bounds.get("W"), self.bounds.get("N")),
                         "NE": (self.bounds.get("E"), self.bounds.get("N")),
                         "SE": (self.bounds.get("E"), self.bounds.get("S"))}
                       
        self.center = (self.bounds.get("E")-self.width/2, self.bounds.get("N")-self.height/2)
        self.text = pyglet.text.Label(content, font_name = 'verdana', font_size = 10,
                                       bold = 0, color = (70, 200, 200, 255),
                                       anchor_x = 'left', anchor_y = 'center',
                                       x = self.pos[0], y = self.pos[1], batch = batch)
                                       
class OGLTextInput2(object):
    def __init__(self, content="text", height=14, width=50, pos=(0,0), color=(.5,.5,.5), 
                 cursor=(2,8), anchor_x="center", anchor_y="center",batch=None):
        self.focused = 0
        self.column = 0
        self.line = 0
        self.cursor = cursor
        self.content = content
        self.height = height
        self.width = width
        self.pos = pos
        self.color = color
        
        self.document = pyglet.text.document.UnformattedDocument(content)
        styles = {"color":(0,0,0,255),"font_size":18}
        self.document.set_style(0, len(self.document.text),styles)
        font = self.document.get_font()
        height2 = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, width, height2, 
                                                               multiline=False, batch=batch)
        self.layout.font_size = 16
        self.caret = pyglet.text.caret.Caret(self.layout)
        hobson = self.caret.get_style("font_size")
        print "hobson", hobson
        self.caret.set_style(styles)
        
        
        if anchor_x == "left":
            self.left = 0
            self.right = 1
        elif anchor_x == "right":
            self.left = 1
            self.right = 0
        else: 
            self.left = .5
            self.right = .5
        if anchor_y == "top":
            self.top = 0
            self.bottom = 1
        elif anchor_y == "bottom":
            self.top = 1
            self.bottom = 0
        else: 
            self.top = .5
            self.bottom = .5
            
        self.bounds = {"N": self.pos[1]+self.height*self.top, "S": self.pos[1]-self.height*self.bottom,
                       "E": self.pos[0]+self.width*self.right, "W": self.pos[0]-self.width*self.left}
                       
        self.corners = {"SW": (self.bounds.get("W"), self.bounds.get("S")),
                         "NW": (self.bounds.get("W"), self.bounds.get("N")),
                         "NE": (self.bounds.get("E"), self.bounds.get("N")),
                         "SE": (self.bounds.get("E"), self.bounds.get("S"))}
                       
        self.center = (self.bounds.get("E")-self.width/2, self.bounds.get("N")-self.height/2)
        self.layout.x = self.bounds.get("W")
        self.layout.y = self.bounds.get("S")
        
        #self.text = pyglet.text.Label(content, font_name = 'verdana', font_size = 10,
        #                               bold = 0, color = (70, 200, 200, 255),
        #                               anchor_x = 'left', anchor_y = 'center',
        #                               x = self.pos[0], y = self.pos[1], batch = batch)                                       
                                       
    def draw(self):
        glBegin(GL_QUADS)
        if self.focused == 1:
            glColor3f(self.color[0]+.2,self.color[1]+.2,self.color[2]+.2)
        else:
            glColor3f(self.color[0],self.color[1],self.color[2])
        glVertex2f(self.corners.get("SW")[0], self.corners.get("SW")[1])
        glVertex2f(self.corners.get("NW")[0], self.corners.get("NW")[1])
        glVertex2f(self.corners.get("NE")[0], self.corners.get("NE")[1])
        glVertex2f(self.corners.get("SE")[0], self.corners.get("SE")[1])
        glEnd()
        #if self.text.batch == None:        
        #    print "NOBATCH!"
        #    self.text.draw()
