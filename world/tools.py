from math import *
import pyglet
import rabbyt
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *

def CalcRot(prev_time, rps, step, direction):
    time = rabbyt.get_time()
    rt = (1.0 / rps) / (360 / step)
    if time - prev_time >= rt:
        num_steps = int((time - prev_time) / rt)
        rotate = direction * num_steps * step
    else:
        rotate = 0
    return rotate
    
def CalcPos(last_pos, prev_time, speed, accel, velocity, heading): #Calculate Position Based on last know position, vector, and amount of time passed
    new_time = rabbyt.get_time()
    time = new_time - prev_time
    velocity = accel * time + velocity
    if velocity > speed:
        velocity = speed
    new_pos = [last_pos[0] + (velocity * time * sin(radians(heading*1))),
                last_pos[1] + (velocity * time * cos(radians(heading*1)))]
    #print "gopos",new_pos

    return new_pos, velocity
    
def SlowDown(last_pos, prev_time, speed, accel, velocity, heading): #Calculate Position Based on last know position, vector, and amount of time passed
    new_time = rabbyt.get_time()
    time = new_time - prev_time
    velocity = velocity - accel * time
    if velocity < 0:
        velocity = 0
    new_pos = [last_pos[0] + (velocity * time * sin(radians(heading*1))),
                last_pos[1] + (velocity * time * cos(radians(heading*1)))]
    #print "slowpos",new_pos

    return new_pos, velocity

def CalcHeading(last_pos, prev_time, speed, accel, velocity, direction, heading, rot, step):
    time = rabbyt.get_time() - prev_time
    a = accel * time
    #print "ACCEL DIRECTION VELOCITY HEADING ROTATION"
    #print a, direction, velocity, heading, rot
    vecx = sin(radians(direction)) * velocity
    vecy = cos(radians(direction)) * velocity
    thrustx = sin(radians(rot)) * a
    thrusty = cos(radians(rot)) * a
    #print "old velocity:", velocity
    #print "vecx:",vecx,"vecy:",vecy,"thrustx:",thrustx,"thrusty:",thrusty
    velocity = sqrt((vecx + thrustx)**2 + (vecy + thrusty)**2)
    new_direction = degrees(atan((vecx + thrustx)/(vecy + thrusty)))
    if vecy + thrusty < 0:
        new_direction += 180
        #new_heading = round(new_direction/10.0)*10 + 180
    new_heading = round(new_direction/float(step))*step
    #print "new velocity:",velocity
    #print "old_direction:", direction
    if new_heading < 0:
        new_heading = 360 + new_heading
    #print "new_direction:", new_direction
    #print "NEW HEADING",new_heading   
    
    if velocity > speed:
        velocity = speed
    new_pos = [last_pos[0] + (velocity * time * sin(radians(new_heading*1))),
                last_pos[1] + (velocity * time * cos(radians(new_heading*1)))]
    return new_heading, new_direction, velocity, new_pos
    
def CalcVectorMagAngle(a, b):
    c = (float(a)**2) * (float(b)**2)
    c = sqrt(c)
    angle = atan(float(b) / float(a))
    return c, angle
    
def CalcVisibleVector(x1, y1, x2, y2):
    shallow = atan(float(y1) / float(x1))
    wide = atan(float(y2) / float(x2))
    return (shallow,wide)
    
def CalcBodyPos(player,location,visible_size):
    #visible_area = [(player[0] - visible_size[0] / 2), (player[0] + visible_size[0] / 2), 
    #                (player[1] - visible_size[1] / 2), (player[1] + visible_size[1] / 2)]
    
    position = (location[0] - player[0], location[1] - player[1])
    distance = fabs(hypot(position[0],position[1]))
    pos_value = []
    for x in position:
        if x < 0:
            x *= -1
        pos_value.append(x)              
    if (pos_value [0] <= visible_size[0] / 2 + 200) and (pos_value [1] <= visible_size[1] / 2 + 200):
        return (int(position[0] + visible_size[0] / 2),int(position[1]) + visible_size[0] / 2), distance
    else:
        return (1000,1000), distance
        
def CalcSatPos(location,distance,angle):
    x = sin(radians(angle))*distance
    y = cos(radians(angle))*distance
    sat_loc = (location[0] + x, location[1] + y)
    return sat_loc
    
def CalcOtherPos(player,location,visible_size):
    #print "location"+str(location)
    #print player 
    position = (int(location[0]) - player[0], int(location[1]) - player[1])
    pos_value = []
    for x in position:
        if x < 0:
            x *= -1
        pos_value.append(x)              
    if (pos_value [0] <= visible_size[0] / 2 + 200) and (pos_value [1] <= visible_size[1] / 2 + 200):
        return (int(position[0] + visible_size[0] / 2),int(position[1]) + visible_size[0] / 2)
    else:
        return (1000,1000) 

def ParseLines(lines):
    comments = []
    properties = []
    values = []
    for x in lines:
        comment = x.find("#")
        if x.startswith("[") == 1:
            a = x.split("]")
            properties.append(a[0]+"]")
            if comment != -1:
                y = a[1].strip()
                comments.append(y)
        elif x.startswith("#") == 1:
            y = x.strip()
            comments.append(y)
        elif x.startswith(" "):
            pass
        else:
            y = x.strip()
            values.append(y)
    linedict = dict(zip(properties,values))
    print linedict
    return linedict
