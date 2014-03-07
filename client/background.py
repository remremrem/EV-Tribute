import random
import pyglet
import rabbyt
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from tools import *

class Background:
    def __init__(self, window, panel):
        self.x = (window[0] - panel[0])
        self.y = window[1]
        self.pos = [0, 0]       
        print "self x y", self.x, self.y
        amt = 26 * 4
        self.amount_stars = [amt / 3, amt / 4, amt / 7, amt / 13]
        
    def populate(self):
        self.stars = [[], [], [], []]  #these lists represent 4 starfields.  
        count = 0                      #the first moves 1 pixel for every pixel the player moves
        for each in self.amount_stars: #the second moves .5 and the third .33333 the fourth .25   
            for x in range(each):
                a = random.randint(-300, 950)
                b = random.randint(-300, 900)
                bright = random.randint(1, 5)
                #magnitude, angle = CalcVectorMagAngle(a, b)
                self.stars[count].append([a, b, bright, count, 0, 0])
            count += 1
    
        
    def calc_visible(self, player):    #figure out which stars are now visible, erase those that are out of bounds, create new ones
        movement = [player[0] - self.pos[0], player[1] - self.pos[1]]
        self.pos = [self.pos[0] + movement[0], self.pos[1] + movement[1]]
        divisor = 0.0
        for slist in self.stars:
            divisor += 1.0
            for star in slist:
                flag = 0
                if star[3] > -1:    # for all stars that don't move pixel for pixel against the ship
                    x = movement[0] / divisor
                    if -1.0 < x < 1.0:
                        if (x + star[4] / divisor) >= 1.0 or (x + star[4] / divisor) <= -1.0:
                            star[0] -= int(x + star[4] / divisor)
                            star[4] = 0
                        else:
                            star[4] += movement[0]
                    elif x > 1.0 or x < -1.0:
                        star[0] -= int(x)
                        star[4] = 0
                               
                    y = movement[1] / divisor
                    if -1 < y < 1.0:
                        if (y + star[5] / divisor) >= 1.0 or (y + star[5] / divisor) <= -1.0:
                            star[1] -= int(y + star[5] / divisor)
                            star[5] = 0
                        else:
                            star[5] += movement[1]
                    elif y > 1.0 or y < -1.0:
                        star[1] -= int(y)
                        star[5] = 0

                #else:
                #    star[0] -= int(movement[0] / divisor)
                #    star[1] -= int(movement[1] / divisor)
                which_layer = star[3]    
                if star [0] < -300:
                    slist.remove(star)
                    x = 950
                    y = random.randint(-300,900)
                    flag = 1 
                elif star[0] > 950:
                    slist.remove(star)
                    x = -300
                    y = random.randint(-300,900)
                    flag = 1 
                elif star[1] < -300:
                    slist.remove(star)
                    y = 900
                    x = random.randint(-300,950)
                    flag = 1
                elif star [1] > 900:
                    slist.remove(star)
                    y = -300
                    x = random.randint(-300,950)
                    flag = 1
                if flag <> 0:
                    slist.append([x,y,random.randint(1, 5),which_layer,0,0])
        #print "SELF STARS"
        #print self.stars
        vis_stars = []
        for slist in self.stars:
            for star in slist:
                if (0 <= star[0] <= 650 and 0 <= star[1] <= 600):                
                    vis_stars.append(star)
        return vis_stars
            
    def draw(self,player, count):
        stars=self.calc_visible(player)
        glPointSize(1.0)
        glBegin(GL_POINTS)
        glColor3f(0.6, 0.6, 0.7)        
        verts = []  
        for star in stars: 
            if star[2] < 5:
                glVertex2f(star[0], star[1])
            else:
                glVertex2f(star[0], star[1])
                glVertex2f(star[0] + 1, star[1])
                glVertex2f(star[0] + 1, star[1] + 1)
                glVertex2f(star[0], star[1] + 1)
        glEnd()
