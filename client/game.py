import pyglet
#pyglet.options['debug_gl'] = False
import rabbyt
import pygame.mixer
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
import time
try:    import cPickle as pickle
except: import pickle as pickle
from panel import Panel
from dialogues import *
import player
import others
from starsystem import *
from background import Background
from Net import *
import netclient
from menus import *
from sounds import *

pygame.mixer.init()
Name = "TestPlayer"
#cont = True
#while cont:
#    Name = raw_input("What is your pilot name?  ")
#    for char in Name:
#        if char != " ":
#            cont = False
#            break
class GameWindow(pyglet.window.Window):
    def __init__(self):
        global Name        
        
        super(GameWindow, self).__init__()
        self.textevents = 1
        self.set_size(800, 600)
        self.gamestate = 1  # 0 playing  1 main menu
        rabbyt.set_default_attribs()
        pyglet.clock.schedule(rabbyt.add_time)
        pyglet.clock.set_fps_limit(100)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.mainmenu = MainMenu((self.width, self.height))
        self.mainmenu.open = 1
        self.creditsmenu = CreditsMenu((self.width, self.height)) 
        self.optionsmenu = OptionsMenu((self.width, self.height))
        self.keymenu = KeyMenu((self.width, self.height))
        self.sounds = Sounds()
        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus = None  
        self.configuration = player.Configuration()
        self.controls = self.configuration.getControls()
        self.keys = self.configuration.pykeys 
        self.idnum = 0
        #self.image = pyglet.image.load('ship2.png')
        #music = pyglet.resource.media('sample.wav',streaming=False)
        #music.play()
        #self.push_handlers(pyglet.window.event.WindowEventLogger())
        
    def playerLogin(self):
        self.name = self.mainmenu.textentry.get("Name").document.text
        password = self.mainmenu.textentry.get("Password").document.text
        print "NAME: ",self.name
        print "password: ", password
        self.net_client = netclient.NetData(self.name)
        data = self.net_client.Connect("localhost",6317,password)  #doyle.is-a-geek.net
        print "connection", data
        self.idnum = data[4]
        self.startsystem = pickle.loads(data[1])
        print "self.startsystem",self.startsystem
        return data
           
    def startPlaying(self,data):
        self.mainmenu.open = 0
        self.textevents = 0        
        self.otherlist = {}
        self.playercount = 1
        safejump = 500
        self.mapsize = (13000 * 4, 13000 * 4)
        self.center = (13000 * 2, 13000 * 2)
        self.safejump = range(self.center[0] - safejump, self.center[0] + safejump)                    
        def entities(self):
            self.label = pyglet.text.Label('Hello, world',
                                           font_name = 'Times New Roman',
                                           font_size = 36,
                                           x = self.width/2, y = self.height/2,
                                           anchor_x = 'center', anchor_y = 'center')
            self.panel = Panel((self.width,self.height))
            self.background = Background((self.width,self.height),self.panel.size)
            self.background.pos = [self.mapsize[0] / 2, self.mapsize[1] / 2]
            self.background.populate()
            self.bgcheck = 1
            self.player = player.Player((self.width,self.height),self.panel.size)
            self.player.name = self.name
            self.player.idnum = self.idnum
            self.player.location[0] = self.startsystem
            self.spritelist = [self.player.sprite]
            self.visible_size = (self.background.x,self.background.y)
            self.systemdict = MakeSystemDict("data/systems/systems.list",self.player.pos,self.center,self.visible_size)
            self.systemdict.get(self.startsystem.name).update(self.startsystem)
            self.systemdict.get(self.startsystem.name).active = 1
            self.system = self.systemdict.get(self.startsystem.name)
            self.selectedsystem = None
            self.activesystem = self.system.name
            self.linkdict = MakeLinks(self.systemdict)
            print "LINKDICT: " + str(self.linkdict)
            self.menudialogue = MenuDialogue((self.width,self.height))
            self.optionsdialogue = OptionsDialogue((self.width,self.height))
            self.controlsdialogue = ControlsDialogue((self.width,self.height))
            self.dockdialogue = DockDialogue((self.width,self.height))           
            self.mapdialogue = MapDialogue((self.width, self.height))
            self.mapdialogue.active = self.activesystem
        entities(self)
        
        self.playerdict = {}
        otherdata = pickle.loads(data[2])
        print "OTHERDATA"
        for each in otherdata:
            print each, otherdata.get(each)
            self.playerdict[each] = others.Other((self.width,self.height),self.panel.size)
            self.playerdict.get(each).setNonCrucial(otherdata.get(each))
            
        otherdata = pickle.loads(data[3])
        for each in otherdata:
            self.playerdict.get(each).setCrucial(otherdata.get(each))
        
        def init_player(self):
            self.player_rot=(0,"CW")
            self.player_accel=(0,0,0)
            self.player_about=(0,0,0)
            self.player.pos = [self.mapsize[0] / 2, self.mapsize[1] / 2]
        init_player(self)
        self.net_client.sendData(["update", pickle.dumps({"pos":self.player.pos, "rot":self.player.rot, "velocity":self.player.velocity, 
            "heading":self.player.heading, "isfiring":self.player.isfiring, "isfiring2":self.player.isfiring2, "secondary":self.player.secondary})])


    """      BEGIN EVENT HANDLING MUMBO JUMBO      """

## KEY PRESS ##
    def on_key_press(self, symbol, modifiers):
        if symbol == self.keys.get(self.controls.get("[primary fire]")):
            if self.player.inspace == 1:
                self.sounds.weapon1.play(-1)
                self.player.isfiring = 1
                
        elif symbol == self.keys.get(self.controls.get("[secondary fire]")):
            if self.player.inspace == 1:
                self.sounds.weapon2.play(-1)
                self.player.isfiring2 = 1
       
        if self.mainmenu.open == 0: 
            if self.player.inspace == 1:
                if symbol == self.keys.get(self.controls.get("[left]")):
                    self.player_rot=(1, -1)
                    self.player.rot_time = rabbyt.get_time()
                elif symbol == self.keys.get(self.controls.get("[right]")):
                    self.player_rot=(1, 1)
                    self.player.rot_time = rabbyt.get_time()
                elif symbol == self.keys.get(self.controls.get("[up]")):
                    self.player_accel = 1
                    self.player.pos_time = rabbyt.get_time()
                elif symbol == self.keys.get(self.controls.get("[down]")):
                    self.player_about = 1
                    self.player.rot_time = rabbyt.get_time()

## KEY RELEASE ##     
    def on_key_release(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            if self.mainmenu.open == 0:
                if self.mapdialogue.open == 1:
                    self.mapdialogue.selected = self.selectedsystem
                    self.mapdialogue.open = 0
                elif self.controlsdialogue.open == 1:
                    self.controlsdialogue.open = 0
                elif self.optionsdialogue.open == 1:
                    self.optionsdialogue.open = 0
                elif self.menudialogue.open == 1:
                    self.menudialogue.open = 0
                elif self.menudialogue.open == 0:
                    self.menudialogue.open = 1
                    
        elif symbol == self.keys.get(self.controls.get("[jump]")):
            if self.mainmenu.open == 0:
                if self.player.inspace == 1:
                    if (self.selectedsystem and self.selectedsystem != self.activesystem and 
                        (int(self.player.pos[0]) not in self.safejump or
                        int(self.player.pos[1]) not in self.safejump)):
                        print "POS" + str(self.player.pos)
                        data = self.net_client.checkData(self.player)
                        print data
                        self.net_client.sendData(["jump",self.selectedsystem])
                        print self.selectedsystem                        
                        data = self.net_client.waitData(self.player)
                        print data
                        if data[0] == "system":
                            self.sounds.jump.play()
                            name = data[1].name
                            self.systemdict.get(name).update(data[1])
                            self.systemdict.get(name).active = 1
                            self.system.active = 0
                            self.system = self.systemdict.get(name)
                            self.activesystem = name
                            self.background.populate()
                            self.player.planet = None
                            self.panel.planet.text = str(self.player.planet)
                        else:
                            pass
            
        elif symbol == self.keys.get(self.controls.get("[land]")):
            if self.mainmenu.open == 0:
                if self.player.inspace == 1:
                    if self.player.planet == None:
                        self.sounds.toggle1.play()
                        bodies = []
                        for x in self.system.bodies:
                            bodies.append([self.system.bodies.get(x).pdistance, x])
                            print self.system.bodies.get(x).name
                            print self.system.bodies.get(x).location
                        bodies.sort()
                        if len(bodies) > 0:
                            self.player.planet = bodies[0][1]
                            self.panel.planet.text = str(self.player.planet)
                        return 0
                    if self.system.bodies.get(self.player.planet).pdistance < 90:
                        self.net_client.checkData()
                        self.net_client.sendData(["land",self.player.planet])
                        print self.player.planet
                        data = self.net_client.waitData(self.player)
                        print "landing data",data
                        if data[0] == "granted":
                            self.dockdialogue.open = 1
                            self.optionsdialogue.docked = 1
                            self.menudialogue.docked = 1
                            self.controlsdialogue.docked = 1
                            self.player.docked = 1
                            self.player.inspace = 0
                            self.player.velocity = 0
                            #self.player.pos = data[1]
                            self.player.location[1] = self.player.planet
                            print "granted landing"
                        elif data[0] == "denied":
                            print "denied landing"
                    
        elif symbol == self.keys.get(self.controls.get("[map]")):
            if self.mainmenu.open == 0:
                if self.mapdialogue.open == 0:
                    self.sounds.menu1.play()
                    self.mapdialogue.selected = self.selectedsystem
                    self.mapdialogue.highlightLinks(self.linkdict, self.activesystem)
                    self.mapdialogue.open = 1
                else:
                    self.selectedsystem = self.mapdialogue.selected
                    self.panel.destination.text = str(self.selectedsystem)
                    self.mapdialogue.open = 0
                
        elif symbol == self.keys.get(self.controls.get("[target nearest]")):
            print 'Select nearest target.'        
        elif symbol == self.keys.get(self.controls.get("[primary fire]")):
            print 'Halt Primary.'
            self.sounds.weapon1.fadeout(int(self.sounds.weapon1.get_length()*500))
            self.player.isfiring = 0
        elif symbol == self.keys.get(self.controls.get("[secondary fire]")):
            print 'Halt secondary.'
            self.sounds.weapon2.fadeout(int(self.sounds.weapon2.get_length()*1000))
            self.player.isfiring2 = 0
        elif symbol == self.keys.get(self.controls.get("[cycle secondary]")):
            print 'Cycle secondary weapon.'
        elif symbol == self.keys.get(self.controls.get("[global chat]")):
            print 'Initiate global chat.'
        elif symbol == self.keys.get(self.controls.get("[target]")):
            print 'Target ships.'        
                    
        elif symbol == self.keys.get(self.controls.get("[cycle planets]")):
            if self.mainmenu.open == 0:
                if self.player.inspace == 1:
                    try: 
                        self.sounds.toggle1.play()
                        p = self.system.bodynames.index(self.player.planet)+1
                    except:
                        print "OH NOES!"
                    if p <= len(self.system.bodynames)-1:
                        self.player.planet = self.system.bodynames[p]
                    else:
                        self.player.planet = self.system.bodynames[0]
                    self.panel.planet.text = str(self.player.planet)
                    print self.player.planet

        elif symbol == self.keys.get(self.controls.get("[left]")):
            self.player_rot = (0, -1)
        elif symbol == self.keys.get(self.controls.get("[right]")):
            self.player_rot = (0, 1)
        elif symbol == self.keys.get(self.controls.get("[up]")):
            self.player_accel = 0
        elif symbol == self.keys.get(self.controls.get("[down]")):
            self.player_about = 0     

## TEXT EVENTS ##
    def on_text(self, text):
        if self.textevents == 1:
            #if self.optionsmenu.open == 1:
            #    for entry in self.optionsmenu.textentry:
            #        if self.optionsmenu.textentry.get(entry).focused == 1:
            #            self.optionsmenu.textentry.get(entry).caret.on_text(text)
            if self.mainmenu.open == 1:
                for entry in self.mainmenu.textentry:
                    if self.mainmenu.textentry.get(entry).focused == 1:
                        self.mainmenu.textentry.get(entry).caret.on_text(text)
            print "on_text: " + text

    def on_text_motion(self, motion):
        if self.textevents == 1:
            if self.optionsmenu.open == 1:
                for entry in self.optionsmenu.textentry:
                    if self.optionsmenu.textentry.get(entry).focused == 1:
                        self.optionsmenu.textentry.get(entry).caret.on_text_motion(motion)
            elif self.mainmenu.open == 1:
                for entry in self.mainmenu.textentry:
                    if self.mainmenu.textentry.get(entry).focused == 1:
                        self.mainmenu.textentry.get(entry).caret.on_text_motion(motion)
            print "on_text_motion: " + str(motion)
      
    def on_text_motion_select(self, motion):
        if self.textevents == 1:
            if self.optionsmenu.open == 1:
                for entry in self.optionsmenu.textentry:
                    if self.optionsmenu.textentry.get(entry).focused == 1:
                        self.optionsmenu.textentry.get(entry).caret.on_text_motion_select(motion)
            elif self.mainmenu.open == 1:
                for entry in self.mainmenu.textentry:
                    if self.mainmenu.textentry.get(entry).focused == 1:
                        self.mainmenu.textentry.get(entry).caret.on_text_motion_select(motion)
            print "on_text_motion_select: " + str(motion)
 
## MOUSE PRESS ##        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if self.mainmenu.open == 0:
                if self.mapdialogue.open == 1:
                    self.selectedsystem = self.mapdialogue.handleEvent("mouse_left", self.systemdict, 
                                                                        self.selectedsystem, self.activesystem, 
                                                                        self.linkdict, x, y, self.sounds)
                    self.panel.destination.text = str(self.selectedsystem)
                elif self.dockdialogue.open == 1 and self.menudialogue.open == 0:
                    event = self.dockdialogue.handleEvent("mouse_left", x, y, self.sounds)
                    if event == "EMBARK":
                        print "EMBARK!"
                        self.net_client.sendData(["embark",self.player.planet])
                        data = self.net_client.waitData(self.player)
                        if data[0] == "granted":
                            self.dockdialogue.open = 0
                            self.player.inspace = 1
                            self.player.docked = 0
                            self.menudialogue.docked = 0
                            self.optionsdialogue.docked = 0
                            self.controlsdialogue.docked = 0
                            print "granted launch"
                        elif data[0] == "denied":
                            print "denied launch"
                elif self.controlsdialogue.open == 1:
                    event = self.controlsdialogue.handleEvent("mouse_left", x, y, self.sounds)
                    if event == "BACK":
                        self.controlsdialogue.open = 0
                elif self.optionsdialogue.open == 1:
                    event = self.optionsdialogue.handleEvent("mouse_left", x, y, self.sounds)
                    if event == "BACK":
                        self.optionsdialogue.open = 0
                    elif event == "CONTROLS":
                        self.controlsdialogue.open = 1
                elif self.menudialogue.open == 1:
                    event = self.menudialogue.handleEvent("mouse_left", x, y, self.sounds)
                    if event == "BACK":
                        self.menudialogue.open = 0
                    elif event == "OPTIONS":
                        self.optionsdialogue.open = 1
                    elif event == "QUIT":
                        exit()
            else:
                if self.optionsmenu.open == 1:
                    event = self.optionsmenu.handleEvent("mouse_left", x, y)
                    if event == "CONTROLS":
                        self.sounds.menu1.play()
                        self.keymenu.open = 1
                        self.optionsmenu.open = 0                       
                    elif event == "FULLSCREEN":
                        self.sounds.menu1.play()
                    elif event == "FXUP":
                        self.sounds.menu1.play()
                    elif event == "FXDOWN":
                        self.sounds.menu1.play()
                    elif event == "FXMUTE":
                        self.sounds.menu1.play()
                    elif event == "MUSICUP":
                        self.sounds.menu1.play()
                    elif event == "MUSICDOWN":
                        self.sounds.menu1.play()
                    elif event == "MUSICMUTE":
                        self.sounds.menu1.play()
                    elif event == "RESOLUTION":
                        self.sounds.menu1.play()
                    elif event == "BACK":
                        self.sounds.menu1.play()
                        self.optionsmenu.open = 0
                elif self.keymenu.open == 1:
                    event = self.keymenu.handleEvent("mouse_left", x, y)
                    if event == "BACK":
                        self.sounds.menu1.play()
                        self.keymenu.open = 0
                        self.optionsmenu.open = 1
                elif self.creditsmenu.open == 1:
                    event = self.creditsmenu.handleEvent("mouse_left", x, y)
                    if event == "BACK":
                        self.sounds.menu1.play()
                        self.creditsmenu.open = 0
                else:
                    event = self.mainmenu.handleEvent("mouse_left", x, y)
                    if event == "LAUNCH":
                        self.sounds.menu1.play()
                        attempt = self.playerLogin()
                        if attempt == 0:
                            self.mainmenu.labels.get("Attempt").text = "Invalid player name OR password"
                        else:
                            self.mainmenu.labels.get("Attempt").text = ""
                            self.startPlaying(attempt)
                    elif event == "OPTIONS":
                        self.sounds.menu1.play()
                        self.optionsmenu.open = 1
                        #self.set_focus(self.optionsmenu.nameentry)
                    elif event == "CREDITS":
                        self.sounds.menu1.play()
                        self.creditsmenu.open = 1
                    elif event == "JETTISON":
                        self.sounds.menu1.play()
                        exit()
                    
                print "EVENT: " + str(event)
                    
                        
## MOUSE RELEASE ##            
    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            pass
 
## MOUSE SCROLL ##            
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            print "scrolled forward"
        if scroll_y < 0:
            print "scrolled backward"

## MOUSE DRAG ##            
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons and mouse.LEFT:
            #print 'Dragging Left Mouse'
            pass


    """       END EVENT HANDLING MUMBO JUMBO        """




            
    def check_player(self):
        if self.player.inspace == 0:
            self.player.velocity = 0
        if self.player_rot[0] == 1:
            self.player.rotate(self.player_rot[1])
        if self.player_accel == 1:
            self.player.accelerate(self.mapsize)
        if self.player_accel == 0 and self.player.velocity > 0:
            self.player.glide(self.mapsize)
        if self.player_about == 1:
            self.player.about()
        
                    
    def on_draw(self):
        global Name
        glClear(GL_COLOR_BUFFER_BIT)
        if self.mainmenu.open == 0:        
            self.check_player()
            if self.player.inspace == 1:
                netinfo = self.net_client.netUpdate(self.player)
                if self.bgcheck == 1 or self.bgcheck == -1:
                    self.background.draw(self.player.pos, self.bgcheck)
                self.bgcheck *= -1
            
                addplayer = 0
                if netinfo[0] == "update":
                    crucial = pickle.loads(netinfo[1])
                    print "crucial data 3", crucial
                    for x in crucial:
                        if x != self.idnum:
                            if x in self.otherlist:
                                self.otherlist.get(x).setCrucial(crucial.get(x))
                            else:
                                self.playercount += 1
                                self.otherlist[x] = others.Other((self.width,self.height),self.panel.size)
                                self.otherlist.get(x).setCrucial(crucial.get(x))
                            
                    if len(self.otherlist) > len(crucial):
                        for x in self.otherlist:
                            if self.otherlist.get(x).name not in plist:
                                self.otherlist.pop(x)
                                break
                othersprites = []            
                for x in self.otherlist:
                    sprite = self.otherlist.get(x).draw(self.player.pos,self.visible_size,self.net_client.average_ping,self.player.name)
                    if sprite != None:
                        othersprites.append(sprite)
                sys_sprites = self.system.draw(self.player.pos)
                rabbyt.render_unsorted(sys_sprites)

                if len(othersprites) > 0:
                    #print "OTHER", othersprites
                    rabbyt.render_unsorted(othersprites)
                rabbyt.render_unsorted(self.spritelist)
                #print "PLAYER SPRITE: " + str(self.player.sprite.xy)
            
                
            #glColor3f(0.5, 0.5, 0.2)
            glDisable(GL_TEXTURE_2D)
            glLoadIdentity()
            self.panel.draw(self.system.bodies, self.otherlist, self.player.pos, self.center)

            if self.controlsdialogue.open == 1:
                self.controlsdialogue.draw()
            elif self.optionsdialogue.open == 1:
                self.optionsdialogue.draw()
            elif self.menudialogue.open == 1:
                self.menudialogue.draw()
            elif self.mapdialogue.open == 1:
                self.mapdialogue.draw(self.systemdict, self.linkdict)
            elif self.dockdialogue.open == 1 and self.player.docked == 1:
                self.dockdialogue.draw()
                            
        else:
            if self.creditsmenu.open == 1:
                glDisable(GL_TEXTURE_2D)
                glLoadIdentity()
                self.creditsmenu.draw()
            elif self.optionsmenu.open == 1:
                glDisable(GL_TEXTURE_2D)
                glLoadIdentity()
                self.optionsmenu.draw()
            elif self.keymenu.open == 1:
                glDisable(GL_TEXTURE_2D)
                glLoadIdentity()
                self.keymenu.draw()
            else:
                glDisable(GL_TEXTURE_2D)
                glLoadIdentity()
                self.mainmenu.draw()
            
        self.fps_display.draw()
        
        
if __name__ == '__main__':
    gamewindow = GameWindow()
    pyglet.app.run()


