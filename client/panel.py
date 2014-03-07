import math
import pyglet
import rabbyt
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *

class Panel:
    def __init__(self,window):
        self.window = window    
        self.width = 150
        self.height = self.window[1]
        self.size = [self.width,self.height]
        self.batch = pyglet.graphics.Batch()
        self.weapon_label = pyglet.text.Label('Weapon',
                                               font_name = 'verdana', font_size = 11,
                                               bold = 0, color = (70, 200, 200, 255),
                                               anchor_x = 'center', anchor_y = 'center', 
                                               x = self.window[0]-self.width/2,
                                               y = self.height - 160, batch = self.batch)
        self.weapon = pyglet.text.Label('Blaster',
                                               font_name = 'verdana', font_size = 11,
                                               bold = 0, color = (70, 200, 200, 255),
                                               anchor_x = 'center', anchor_y = 'center', 
                                               x = self.window[0]-self.width/2,
                                               y = self.height - 180, batch = self.batch)
        self.destination_label = pyglet.text.Label('Destination',
                                               font_name = 'verdana', font_size = 11,
                                               bold = 0, color = (70, 200, 200, 255),
                                               anchor_x = 'center', anchor_y = 'center', 
                                               x = self.window[0]-self.width/2,
                                               y = self.height - 210, batch = self.batch)
        self.destination = pyglet.text.Label('-', font_name = 'verdana', font_size = 11,
                                             bold = 0, color = (70, 200, 200, 255),
                                             anchor_x = 'center', anchor_y = 'center', 
                                             x = self.window[0]-self.width/2,
                                             y = self.height - 230, batch = self.batch)                                       
        self.planet_label = pyglet.text.Label('Planet',
                                               font_name = 'verdana', font_size = 11,
                                               bold = 0, color = (70, 200, 200, 255),
                                               anchor_x = 'center', anchor_y = 'center', 
                                               x = self.window[0]-self.width/2,
                                               y = self.height - 260, batch = self.batch)
        self.planet = pyglet.text.Label('-', font_name = 'verdana', font_size = 11,
                                        bold = 0, color = (70, 200, 200, 255),
                                        anchor_x = 'center', anchor_y = 'center', 
                                        x = self.window[0]-self.width/2,
                                        y = self.height - 280, batch = self.batch)
        self.bodies = []
        self.others = []
    
        def radar(self):
            self.center = (self.window[0] - 75, self.height - 75)
            self.fov = 20
            num_sides = 32
            angle = math.radians(360.0/num_sides)
            diameter = 140
            self.radius = diameter/2
            self.radrange = range((-diameter/2+4), (diameter/2-4))
            print "SELF.RADRANGE" + str(self.radrange)
            x = self.center[0]
            y = self.center[1]
            self.sides = []
            count = 0
            for item in range(num_sides):
                self.sides.append([x + math.sin(angle*count) * self.radius, y + math.cos(angle*count) * self.radius])
                count += 1
        radar(self)
        
    def updadar(self, bodies, others, player, syscenter):
        nearbodylist = []
        center = False
        farbodylist = []
        otherlist = []
        for x in bodies:
            a = bodies.get(x).location
            distance = int(math.hypot(a[0] - player[0], a[1] - player[1])/self.fov)
            if math.fabs(distance) <= self.radius-4:
                pos = (int(a[0] - player[0])/self.fov, int(a[1] - player[1])/self.fov)
                nearbodylist.append((self.center[0] + pos[0], self.center[1] + pos[1]))
        fromcenter = int(math.hypot(syscenter[0] - player [0], syscenter[1] - player [1])/self.fov)
        if math.fabs(fromcenter) > self.radius+10:
            angle = math.atan2(syscenter[0]-player[0],syscenter[1]-player[1])
            center = ((int(self.center[0] + (math.sin(angle)*(self.radius+3))),
                       int(self.center[1] + (math.cos(angle)*(self.radius+3)))))
        return nearbodylist,farbodylist,otherlist,center
        
    def draw(self, bodies, others, player, syscenter):    
        nbd,fbd,otherlist,center = self.updadar(bodies, others, player, syscenter)        
        ww = self.window[0]
        wh = self.window[1]
        w = self.size[0]
        h = self.size[1]
        width = self.window[0]
        height = self.window[1]
        thick = 2
        
        
        glBegin(GL_QUADS)  #start border
        glColor3f(0.4, 0.5, 0.2)
        glVertex2f(ww-w, 0)
        glVertex2f(ww-w, h)
        glVertex2f(ww, h)
        glVertex2f(ww, 0)
        glEnd()
        
        glBegin(GL_QUADS) #start gradient background
        glColor3f(0.1, 0.1, 0.1)
        glVertex2f(ww-w+thick, h-thick)
        glVertex2f(ww-thick, h-thick)
        glColor3f(0.2, 0.3, 0.2)
        glVertex2f(ww-thick, thick)
        glVertex2f(ww-w+thick, thick)
        glEnd()
        
        #self.weapon_label.draw()
        #self.weapon.draw()
        #self.destination_label.draw()
        if self.destination.text == "None":
            self.destination.text = "-"
        #self.destination.draw()
        #self.planet_label.draw()
        if self.planet.text == "None":
            self.planet.text = "-"
        #self.planet.draw()
        self.batch.draw()
        glBegin(GL_TRIANGLE_FAN)  #start weapon label
        glColor3f(0.0, 0.0, 0.0)
        for item in self.sides:
            glVertex2f(item[0], item[1])
        glEnd()
        
        glColor3f(0.9, 0.9, 0.0)
        glPointSize(6.0)
        glBegin(GL_POINTS)
        for x in nbd:
            glVertex2f(x[0],x[1])                
        glEnd()
        
        if center:
            glPointSize(4.0)
            glBegin(GL_POINTS)
            glVertex2f(center[0],center[1])                
            glEnd()
        
        glColor3f(0.0, 0.0, 0.0)
        glPointSize(4.0)
        glBegin(GL_POINTS)
        for x in nbd:
            glVertex2f(x[0],x[1])
        glEnd()
        
        glColor3f(0.0, 0.5, 1.0)
        glPointSize(2.0)
        glBegin(GL_POINTS)
        glVertex2f(self.center[0],self.center[1])
        glEnd()

