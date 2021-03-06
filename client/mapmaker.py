import Tkinter,tkFileDialog,os,math,Pmw

class System:
    def __init__(self, name="Unnamed"):
        self.location = (0,0)
        self.name = name
        self.idnum = 0
        self.textid = 0
        self.bodies = {}
        self.bodynames = []
        self.asteroids = 0
        self.nebula = 0
        self.description = "This system is a system within a system within a system."
        self.governments = []
        self.races = []
        self.links = []

class Body:
    def __init__(self,name="unnamed",sattelite=0):
        self.location = (0,0)
        self.sattelite = sattelite
        self.parent = ""
        self.name = name
        self.system = ""
        self.distance = 0
        self.description = "A beautiful planet with lots of cheese."
        self.government = ""
        self.race = ""
        self.faction = ""
        self.population = 0
        self.sprite = "sprite1.png"
        self.techlevel=0
        self.dock=0
        self.wealth=0

class Link:
    def __init__(self,name=None):
        self.systems = []
        self.idnum = 0
        self.name = name
        self.coords = [(0,0),(0,0)]

class MapMaker:
    def __init__(self,master):
        self.master = master
        self.lastactive = "booty"
        self.activesystem = "booty"
        self.selectedsystem = None
        self.movingsystem = None
        self.systemnames = []
        self.starteventcoord = []
        self.lasteventcoord = []
        self.movedistance = [0,0]
        self.center=[250,250]
        self.width = 500
        self.height = 500
        self.focus=[250,250]
        self.wasx = 250
        self.wasy= 250
        
        
        self.systemlist = []
        f = open("data/systems/systems.list")
        for line in f:
            self.systemlist.append(line.rstrip("\n"))
        f.close()
        self.systems = {}
        
        self.races = []
        f = open("data/races/races.list")
        for line in f:
            self.races.append(line.rstrip("\n"))
        f.close()
        self.races.sort()
        
        self.factions = []
        f = open("data/factions/factions.list")
        for line in f:
            self.factions.append(line.rstrip("\n"))
        f.close()
        self.factions.sort()
        
        self.governments = []
        f = open("data/governments/governments.list")
        for line in f:
            self.governments.append(line.rstrip("\n"))
        f.close()
        self.governments.sort()
                      
        def makeSystem(system):  #MAKESYSTEM
            lines = []
            f = open("data/systems/" + system + ".system")
            self.systems[system] = System(system)
            for line in f:
                lines.append(line.rstrip("\n"))
            f.close()
            issystem = 0
            isbody = 0
            linecount = 0
            isbody = 0
            body = None
            issattelite = 0
            for x in lines:
                if x == "[system]":
                    issystem = 1
                    isbody = 0
                    issattelite = 0
                elif x == "[location]":
                    location = lines[linecount+1].split(",")
                    if issystem == 1:
                        self.systems.get(system).location = [int(location[0]),int(location[1])]
                    elif isbody == 1:
                        self.systems.get(system).bodies.get(body).location = [int(location[0]),int(location[1])]
                elif x == "[links]":
                    links = lines[linecount+1].split(",")
                    self.systems.get(system).links = links
                elif x == "[asteroids]":
                    self.systems.get(system).asteroids = int(lines[linecount+1])
                elif x == "[nebula]":
                    self.systems.get(system).nebula = int(lines[linecount+1])
                elif x == "[body]":
                    isbody = 1
                    issattelite = 0
                    issystem = 0
                elif x == "[sattelite]":
                    issattelite = 1 
                    isbody = 0
                    issystem = 0
                elif x == "[name]":
                    if isbody == 1:
                        self.systems.get(system).bodies[lines[linecount+1]] = Body(lines[linecount+1],0)
                        body = lines[linecount+1]
                        self.systems.get(system).bodynames.append(body)
                    elif issattelite == 1:
                        self.systems.get(system).bodies[lines[linecount+1]] = Body(lines[linecount+1],1)
                        body = lines[linecount+1]
                        self.systems.get(system).bodynames.append(body)
                elif x == "[sprite]":
                    self.systems.get(system).bodies.get(body).sprite = lines[linecount+1]
                elif x == "[dock]":
                    self.systems.get(system).bodies.get(body).dock = lines[linecount+1]
                elif x == "[race]":
                    self.systems.get(system).bodies.get(body).race = lines[linecount+1]
                elif x == "[faction]":
                    self.systems.get(system).bodies.get(body).faction = lines[linecount+1]
                elif x == "[government]":
                    self.systems.get(system).bodies.get(body).government = lines[linecount+1]
                elif x == "[wealth]":
                    self.systems.get(system).bodies.get(body).wealth = lines[linecount+1]
                elif x == "[population]":
                    self.systems.get(system).bodies.get(body).population = int(lines[linecount+1])
                elif x == "[description]":
                    self.systems.get(system).bodies.get(body).description = lines[linecount+1]
                elif x == "[tech level]":
                    self.systems.get(system).bodies.get(body).techlevel = lines[linecount+1]
                    print body
                    print "tech"
                    print lines[linecount+1]
                elif x == "[parent]":
                    self.systems.get(system).bodies.get(body).parent = lines[linecount+1]
                elif x == "[distance]":
                    self.systems.get(system).bodies.get(body).distance = lines[linecount+1]
                linecount += 1
       
        for x in self.systemlist:
            makeSystem(x)
        
        print "SYSTEMS"    
        print self.systems
        
        def makeLinks(): #MAKELINKS
            links = {}
            for x in self.systems:
                if x:
                    for l in self.systems.get(x).links:
                        if l:
                            if l+self.systems.get(x).name in links:
                                pass
                            else:
                                a = self.systems.get(x).name+l
                                print a
                                print x
                                print l
                                links[a] = Link(a)
                                links.get(a).coords = [self.systems.get(x).location,self.systems.get(l).location]
            return links
            
        self.links = makeLinks()

        print "LINKS"
        print self.links
        self.systemnames = []
        for x in self.systems:
            self.systemnames.append(self.systems.get(x).name)
        self.systemnames.sort()
        self.zoom = 6

        def quit():
            saveSystem(self.activesystem)
            print "I AM DONECUS!"
            master.destroy()
            
        ##### FUNCTIONS #####
        def sysSelect(event,idnum,button): #SYSSELECT
            print "sysSelect()"
            if button == '1':
                self.messagebar.message('help','Ctrl + left click to drag/move the currently active system (yellow one)')
                for x in self.systems:
                    if self.systems.get(x).idnum == idnum:
                        updateAll(0,0)
                        saveSystem(self.activesystem)
                        updateSystem(x)
                    elif self.systems.get(x).idnum != idnum and self.selectedsystem != self.systems.get(x).name:
                        self.map.component('canvas').itemconfigure(self.systems.get(x).idnum, fill='black')
            if button == '3':
                self.messagebar.message('help','Shift + right click to create a new system.')
                for x in self.systems:
                    if self.systems.get(x).idnum == idnum and self.activesystem != self.systems.get(x).name:
                        self.map.component('canvas').itemconfigure(idnum, fill='blue')
                        if self.systems.get(x).name == self.selectedsystem:
                            self.selectedsystem=None
                            self.map.component('canvas').itemconfigure(self.systems.get(x).idnum, fill='black')
                        else:
                            self.selectedsystem = self.systems.get(x).name                       
                    elif self.systems.get(x).idnum != idnum and self.activesystem != self.systems.get(x).name:
                        self.map.component('canvas').itemconfigure(self.systems.get(x).idnum, fill='black')
            if button == 'C1':
                self.lasteventcoords = (event.x,event.y)
                for x in self.systems:
                    if self.systems.get(x).idnum == idnum:
                        updateSystem(x)
                    elif self.systems.get(x).idnum != idnum and self.selectedsystem != self.systems.get(x).name:
                        self.map.component('canvas').itemconfigure(self.systems.get(x).idnum, fill='black')
            if button == 'C1M':
                if self.systems[self.activesystem].idnum == idnum:
                    movement = [0,0]
                    self.movedistance[0] += (event.x-self.lasteventcoords[0])/float(self.zoom)
                    self.movedistance[1] += (self.lasteventcoords[1]-event.y)/float(self.zoom)
                    if self.movedistance[0] >= 1:
                        movement[0] = int(self.movedistance[0]/1)
                        self.movedistance[0] -= int(self.movedistance[0])
                    if self.movedistance[0] <= -1:
                        movement[0] = int(self.movedistance[0]/1)
                        self.movedistance[0] += abs(int(self.movedistance[0]))
                        
                    if self.movedistance[1] >= 1:
                        movement[1] = int(self.movedistance[1]/1)
                        self.movedistance[1] -= int(self.movedistance[1])
                    if self.movedistance[1] <= -1:
                        movement[1] = int(self.movedistance[1]/1)
                        self.movedistance[1] += abs(int(self.movedistance[1]))
                    self.lasteventcoords = (event.x,event.y)
                    oldloc = (self.systems[self.activesystem].location[0],self.systems[self.activesystem].location[1])
                    self.systems[self.activesystem].location = (self.systems[self.activesystem].location[0]+movement[0],self.systems[self.activesystem].location[1]+movement[1])
                    for x in self.links:
                        if self.systems[self.activesystem].name in x:
                            if (self.links.get(x).coords[0][0] == oldloc[0] and
                                self.links.get(x).coords[0][1] == oldloc[1]):
                                self.links.get(x).coords[0] = self.systems[self.activesystem].location
                            elif (self.links.get(x).coords[1][0] == oldloc[0] and
                                self.links.get(x).coords[1][1] == oldloc[1]):
                                self.links.get(x).coords[1] = self.systems[self.activesystem].location
                    moveSystem()
            if button == "AKR":
                resizeMap()
            
        def addText(x,y,name): #ADDTEXT
            print "addText()"
            c=self.center
            p1=(c[0]+x*self.zoom,c[1]+12-y*self.zoom)
            text = self.map.create_text(p1[0],p1[1],fill="white",font=("Verdana",8),justify='center',state="disabled",text=name)
            return text
            
        def addText2(event,name): #ADDTEXT
            print "addText2()"
            p1=(event.x,event.y+12)
            text = self.map.create_text(p1[0],p1[1],fill="white",font=("Verdana",8),justify='center',state="disabled",text=name)
            return text
            
        def addCircle(x,y): #ADDCIRCLE
            print "addCircle()"
            if self.zoom < 1:
                dia = 2
            elif self.zoom < 3:
                dia = 3
            else:
                dia = 4
            c = self.center
            oval = self.map.create_oval(c[0]+x*self.zoom-dia, c[1]-y*self.zoom-dia, c[0]+x*self.zoom+dia, c[1]-y*self.zoom+dia, fill="black", outline="blue", width=2)
            self.map.component('canvas').tag_bind(oval,'<Control-B1-Motion>', lambda o:sysSelect(o,oval,'C1M'))
            self.map.component('canvas').tag_bind(oval,'<Control-Button-1>', lambda o:sysSelect(o,oval,'C1'))
            self.map.component('canvas').tag_bind(oval,'<Button-1>', lambda o:sysSelect(o,oval,'1'))
            self.map.component('canvas').tag_bind(oval,'<Button-3>', lambda o:sysSelect(o,oval,'3'))
            self.map.component('canvas').tag_bind(oval,'<ButtonRelease>', lambda o:sysSelect(o,oval,'AKR'))
            return oval
            
        def addCircle2(event): #ADDCIRCLE2
            print "addCircle2()"
            if self.zoom < 1:
                dia = 2
            elif self.zoom < 3:
                dia = 3
            else:
                dia = 4
            #c = self.center
            oval = self.map.create_oval(event.x-dia, event.y-dia, event.x+dia, event.y+dia, fill="black", outline="blue", width=2)
            self.map.component('canvas').tag_bind(oval,'<Control-B1-Motion>', lambda o:sysSelect(o,oval,'C1M'))
            self.map.component('canvas').tag_bind(oval,'<Control-Button-1>', lambda o:sysSelect(o,oval,'C1'))
            self.map.component('canvas').tag_bind(oval,'<Button-1>', lambda o:sysSelect(o,oval,'1'))
            self.map.component('canvas').tag_bind(oval,'<Button-3>', lambda o:sysSelect(o,oval,'3'))
            self.map.component('canvas').tag_bind(oval,'<ButtonRelease>', lambda o:sysSelect(o,oval,'AKR'))
            return oval

        def addLine(coords): #ADDLINE
            print "addLine()"
            c=self.center
            p1=(int(c[0]+coords[0][0]*self.zoom),int(c[1]-coords[0][1]*self.zoom))
            p2=(int(c[0]+coords[1][0]*self.zoom),int(c[1]-coords[1][1]*self.zoom))
            line = self.map.create_line(p1[0],p1[1],p2[0],p2[1], fill="blue", width=1)
            return line
       
        def drawSystems(): #DRAWSYSTEMS
            print "drawSystems()"
            for x in self.systems:
                self.systems.get(x).idnum=addCircle(int(self.systems.get(x).location[0]),int(self.systems.get(x).location[1]))
                self.systems.get(x).textid=addText(int(self.systems.get(x).location[0]),int(self.systems.get(x).location[1]),self.systems.get(x).name)
                pop = 0
                for y in self.systems[x].bodies:
                    #print "Y: "+str(y)
                    if y:
                        try:
                            pop += self.systems[x].bodies[y].population
                            print "add population amount: "+str(pop)
                        except:
                            pass
                    else:
                        pop = -1
                if len(self.systems[x].bodies) == 0:
                    pop = -1
                if pop == 0:
                    self.map.itemconfigure(self.systems[x].idnum,outline="#5BB9E8")
                if pop == -1:
                    self.map.itemconfigure(self.systems[x].idnum,outline="white")
            self.map.component('canvas').itemconfigure(self.systems[self.activesystem].idnum, fill='yellow')
            
                
        def drawLinks(): #DRAWLINKS
            print "drawLinks()"
            for x in self.links:
                self.links.get(x).idnum=addLine(self.links.get(x).coords)
        
        def moveSystem(): #MOVESYSTEM
            print "moveSystem()"
            c=self.center
            print "C MOVE: " + str(self.center)
            if self.zoom < 1:
                dia = 2
                fontsize = 6
            elif self.zoom < 3:
                dia = 3
                fontsize = 6
            else:
                dia = 4
                fontsize = int(self.zoom*2)
            if self.zoom >= 7:
                fontsize = 14
                
            x=self.systems[self.activesystem].location[0]
            y=self.systems[self.activesystem].location[1]
            c1=c[0]+x*self.zoom-dia
            c2=c[1]-y*self.zoom-dia
            c3=c[0]+x*self.zoom+dia
            c4=c[1]-y*self.zoom+dia
            self.map.coords(self.systems[self.activesystem].idnum,c1,c2,c3,c4)
            p1=(c[0]+x*self.zoom,c[1]+12-y*self.zoom)
            self.map.coords(self.systems[self.activesystem].textid,p1[0],p1[1])
            self.map.itemconfigure(self.systems[self.activesystem].textid,font=("Verdana",fontsize))
            
            co = self.map.coords(self.systems[self.activesystem].idnum)
            xc = (co[2]-co[0])+co[0]
            yc = (co[3]-co[1])+co[1]
            if xc > self.width:
                difference = xc-self.width
                self.width=self.width+difference*2
            if xc < 0:
                self.width=self.width+xc*2
            if yc > self.height:
                difference = yc-self.height
                self.height=self.height+difference*2
            if yc < 0:
                self.height=self.height+yc*2
            #resizeMap()         
            for s in self.systems:
                if self.systems.get(s).name != self.activesystem:
                    x=self.systems.get(s).location[0]
                    y=self.systems.get(s).location[1]
                    c1=c[0]+x*self.zoom-dia
                    c2=c[1]-y*self.zoom-dia
                    c3=c[0]+x*self.zoom+dia
                    c4=c[1]-y*self.zoom+dia
                    self.map.coords(self.systems.get(s).idnum,c1,c2,c3,c4)
                    p1=(c[0]+x*self.zoom,c[1]+12-y*self.zoom)
                    self.map.coords(self.systems.get(s).textid,p1[0],p1[1])                
            for l in self.links:
                coords = self.links.get(l).coords
                p1=(c[0]+coords[0][0]*self.zoom,c[1]-coords[0][1]*self.zoom)
                p2=(c[0]+coords[1][0]*self.zoom,c[1]-coords[1][1]*self.zoom)
                self.map.coords(self.links.get(l).idnum, p1[0],p1[1],p2[0],p2[1])
            updateSystem(self.activesystem)

        def updateSystem(system): #UPDATESYSTEM
            print "updateSystem()"
            bodies = []
            self.systemmenu.setvalue(system)
            for x in self.systems.get(system).bodies:
                if x:
                    try:
                        bodies.append(self.systems.get(system).bodies.get(x).name)
                    except:
                        pass
            bodies.sort()
            self.bodymenu.setitems(bodies)
            self.linkbox.setlist(self.systems.get(system).links)
            self.location.clear()
            self.location.insert(0,str(self.systems.get(system).location[0])+","+str(self.systems.get(system).location[1]))
            if self.systems.get(system).asteroids == 1:
                self.asteroids.select()
            else:
                self.asteroids.deselect()
            if self.systems.get(system).nebula == 1:
                self.nebula.select()
            else:
                self.nebula.deselect()
            self.lastactive = self.activesystem
            self.activesystem = system
            if self.bodymenu.getvalue():
                updateBody(self.bodymenu.getvalue())
            else:
                updateBody('')
            locDist()
            self.map.component('canvas').itemconfigure(self.systems.get(self.lastactive).idnum, fill='black')
            self.map.component('canvas').itemconfigure(self.systems[self.activesystem].idnum, fill='yellow')
            
        def updateBody(body): #UPDATEBODY
            print "updateBody()"
            print body
            if body:
                b = self.systems[self.activesystem].bodies.get(body)
                print b.techlevel
                self.bodylocation.clear()
                self.bodylocation.insert(0,str(b.location[0])+","+str(b.location[1]))
                if int(b.population) <= 10000 and int(b.population) >= 0:
                    self.population.delete(0,5)
                    self.population.insert(0,str(b.population))
                if int(b.techlevel) <= 100 and int(b.techlevel) >= 0:
                    self.techlevel.delete(0,5)
                    self.techlevel.insert(0,str(b.techlevel))
                if b.race in self.races:
                    self.race.setvalue(b.race)
                if b.faction in self.factions:
                    self.faction.setvalue(b.faction)
                if b.government in self.governments:
                    self.government.setvalue(b.government)
                if b.sattelite == 1:
                    self.sattelite.select()
                    locDist()
                    parents = []
                    for x in self.systems[self.activesystem].bodies:
                        if self.systems[self.activesystem].bodies.get(x).sattelite == 0:
                            parents.append(self.systems[self.activesystem].bodies.get(x).name)
                    self.parents.setitems(parents)
                    try:
                        self.parents.setvalue(b.parent)
                    except: pass
                else:
                    self.sattelite.deselect()
                    locDist()
                    self.parents.setitems([""])
                try:
                    self.description.delete('1.0','end')
                    self.description.insert('1.0',b.description)
                except:
                    pass
            else:
                self.bodylocation.clear()
                self.bodylocation.insert(0,0)
                self.population.delete(0,5)
                self.population.insert(0,0)
                self.techlevel.delete(0,5)
                self.techlevel.insert(0,0)
                self.sattelite.deselect()
                self.parents.setitems('')
                self.parents.setvalue('')
                self.description.delete('1.0','end')
                
        def updateAll(event,name): #UPDATEALL
            print "updateAll()"
            sys = self.systems.get(self.activesystem)
            location = self.location.getvalue()
            loc = location.split(",")
            sys.location = [int(loc[0]),int(loc[1])]
            sys.asteroids = self.astvar.get()
            sys.nebula = self.nebvar.get()
            
            body = sys.bodies.get(self.bodymenu.getvalue())            
            location = self.bodylocation.getvalue()
            loc = location.split(",")
            if body:
                body.location = [int(loc[0]),int(loc[1])]
                body.population = int(self.population.get())
                body.techlevel = int(self.techlevel.get())
                body.race = str(self.race.getvalue())
                body.faction = str(self.faction.getvalue())
                body.government = str(self.government.getvalue())
                body.sattelite = self.satvar.get()
                body.parent = self.parents.getvalue()
                body.description = self.description.get('1.0','end').rstrip("\n")
            
            self.systems[self.activesystem] = sys
            self.systems[self.activesystem].bodies[self.bodymenu.getvalue()] = body
            pop = 0
            for y in self.systems[self.activesystem].bodies:
                #print "Y: "+str(y)
                if y:
                    try:
                        pop += self.systems[self.activesystem].bodies[y].population
                        print "add population amount: "+str(pop)
                    except:
                        print "population exception"
                else:
                    print "population = -1"
                    pop = -1
            if len(self.systems[self.activesystem].bodies) == 0:
                pop = -1
            if pop == 0:
                self.map.itemconfigure(self.systems[self.activesystem].idnum,outline="#5BB9E8")
            elif pop == -1:
                self.map.itemconfigure(self.systems[self.activesystem].idnum,outline="white")
            elif pop > 0:
                self.map.itemconfigure(self.systems[self.activesystem].idnum,outline="blue")
            
            """for x in self.systems:
                pop = 0
                for y in self.systems[x].bodies:
                    #print "Y: "+str(y)
                    if y:
                        try:
                            pop += self.systems[x].bodies[y].population
                            print "add population amount: "+str(pop)
                        except:
                            pass
                    else:
                        pop = -1
                if len(self.systems[x].bodies) == 0:
                    pop = -1
                if pop == 0:
                    self.map.itemconfigure(self.systems[x].idnum,outline="#5BB9E8")
                if pop == -1:
                    self.map.itemconfigure(self.systems[x].idnum,outline="white")"""
        
        def addSystem(event): #ADDSYSTEM
            print "addSystem()"
            reference = self.systems[self.systems.keys()[0]]            
            x = self.map.canvasx(event.x)
            y = self.map.canvasy(event.y)           
            print x
            print y
            print x/self.zoom
            print y/self.zoom
            print reference.location
            print self.map.coords(reference.idnum)
            refc = self.map.coords(reference.idnum)
            refc = [(((refc[2]-refc[0])/2)+refc[0])/self.zoom ,(((refc[1]-refc[3])/2)+refc[3])/self.zoom]
            zero = [refc[0]-reference.location[0],refc[1]+reference.location[1]]
            new = [int((x/self.zoom)-zero[0]),int(zero[1]-(y/self.zoom))]
            def add(button):
                if button == "OK":
                    if dialog.get():
                        name=dialog.get()
                    else: 
                        name = "unnamed"+str(new[0])+str(new[1])                   
                    self.systems[name]=System(name)
                    self.systems[name].location = new
                    self.systems[name].idnum=addCircle2(event)
                    self.systems[name].textid=addText2(event,name)
                    self.activesystem=name
                    self.systemnames.append(name)
                    self.systemmenu.setitems(self.systemnames)
                    self.systemmenu.setvalue(name)
                    self.location.clear()
                    self.location.insert(0,str(new[0])+","+str(new[1]))
                    sysSelect(event,self.systems[name].idnum,'1')
                    updateSystem(name)
                    zoomMap()
                dialog.withdraw()
            dialog=Pmw.PromptDialog(master,
            title = 'Add New System',
            label_text = 'New System Name:',
            entryfield_labelpos = 'n',
            defaultbutton = 0,
            buttons = ('OK', 'Cancel'),
            command = add)  
            
        def saveSystem(system): #SAVESYSTEM
            print "saveSystem()"
            lines = []
            sys=self.systems.get(system)
            lines.append('[system]')
            lines.append('[name]')
            lines.append(str(sys.name))
            lines.append('[location]')
            lines.append(str(sys.location[0])+","+str(sys.location[1]))
            lines.append('[links]')
            links = ""
            count = 1
            for x in sys.links:
                links += x
                if count < len(sys.links):
                    links += ","
                count += 1
            lines.append(links)
            lines.append('[asteroids]')
            lines.append(str(sys.asteroids))
            lines.append('[nebula]')
            lines.append(str(sys.nebula))
            lines.append('[bodies]')
            lines.append(str(len(sys.bodies)))
            for x in sys.bodies:
                if x:
                    bod = sys.bodies.get(x)
                    try:
                        if bod.sattelite == 0:
                            lines.append('[body]')
                            lines.append('[name]')
                            lines.append(str(bod.name))
                            lines.append('[location]')
                            lines.append(str(bod.location[0])+","+str(bod.location[1]))
                            lines.append('[sprite]')
                            lines.append(str(bod.name)+".png")
                            lines.append('[dock]')
                            lines.append(str(bod.dock))
                            lines.append('[race]')
                            lines.append(str(bod.race))
                            lines.append('[faction]')
                            lines.append(str(bod.faction))
                            lines.append('[government]')
                            lines.append(str(bod.government))
                            lines.append('[wealth]')
                            lines.append(str(bod.wealth))
                            lines.append('[population]')
                            lines.append(str(bod.population))
                            lines.append('[tech level]')
                            lines.append(str(bod.techlevel))
                            lines.append('[description]')
                            lines.append(str(bod.description))
                            lines.append('[end body]')
                        elif bod.sattelite == 1:
                            lines.append('[sattelite]')
                            lines.append('[name]')
                            lines.append(str(bod.name))
                            lines.append('[distance]')
                            lines.append(str(bod.distance))
                            lines.append('[sprite]')
                            lines.append(str(bod.name)+".png")
                            lines.append('[parent]')
                            lines.append(str(bod.parent))
                            lines.append('[dock]')
                            lines.append(str(bod.dock))
                            lines.append('[race]')
                            lines.append(str(bod.race))
                            lines.append('[faction]')
                            lines.append(str(bod.faction))
                            lines.append('[government]')
                            lines.append(str(bod.government))
                            lines.append('[wealth]')
                            lines.append(str(bod.wealth))
                            lines.append('[population]')
                            lines.append(str(bod.population))
                            lines.append('[tech level]')
                            lines.append(str(bod.techlevel))
                            lines.append('[description]')
                            lines.append(str(bod.description))
                            lines.append('[end sattelite]')
                    except:
                        pass
            lines.append('[end system]') 
            f = open("data/systems/" + system + ".system",'w')
            for line in lines:
                f.write(line+"\n")
            f.close()
            
            lines = []
            f = open("data/systems/systems.list")
            for line in f:
                lines.append(line.rstrip("\n"))
            f.close()
            if sys.name in lines:
                print "sysname: "+str(sys.name)
            else:
                lines.append(sys.name)
            for x in lines:
                if x in self.systemnames:
                    continue
                else:
                    lines.remove(x)
                    try:
                        os.remove("data/systems/"+x+".system")
                    except:
                        print "no file"
            lines.sort()
            f = open("data/systems/systems.list","w")
            for line in lines:
                f.write(line+"\n")
            f.close()
            
        def delSystem(): #DELSYSTEM
            print "delSystem()"
            def delete(button):
                if button == "OK" and len(self.systems)>1:   
                    self.map.delete(self.systems[self.activesystem].idnum)   
                    self.map.delete(self.systems[self.activesystem].textid)  
                    for link in self.systems[self.activesystem].links:
                        print "LINK: "+str(link)
                        try:
                            name = self.activesystem+link
                            name2 = link+self.activesystem
                        except:
                            continue
                        if name in self.links or name2 in self.links:
                            print name
                            print name2
                            print self.systems[link].links
                            self.systems[link].links.remove(self.activesystem)  
                            print self.systems[link].links            
                            try:
                                self.map.delete(self.links.get(name).idnum)
                                del self.links[name]
                            except:
                                self.map.delete(self.links.get(name2).idnum)
                                del self.links[name2]    
                            saveSystem(link)                        
                    self.systemnames.remove(self.activesystem)
                    del self.systems[self.activesystem]
                    try:
                        os.remove("data/systems/"+self.activesystem+".system")
                    except:
                        print "no file"
                    self.systemmenu.setitems(self.systemnames)
                    self.systemmenu.setvalue(self.systemnames[0])
                    self.activesystem=self.systemnames[0]                   
                    self.bodymenu.setitems(self.systems[self.activesystem].bodynames)
                    updateSystem(self.activesystem)
                dialog.withdraw()
            dialog=Pmw.Dialog(master,
            title = 'Delete System',
            defaultbutton = 0,
            buttons = ('OK', 'Cancel'),
            command = delete,
            buttonbox_hull_bg="#373A36")
            dialog.component('buttonbox').configure(hull_borderwidth = 0, hull_relief = 'flat')
            dialog.component('buttonbox').button(0).configure(bd=0,relief='flat')
            dialog.component('buttonbox').button(1).configure(bd=0,relief='flat',highlightbackground="#667766")
            label = Tkinter.Label(dialog.component('dialogchildsite'),text='Are you sure you want to destroy the startsystem called\n' + self.systemmenu.getvalue()+', and any worlds therein?',relief='flat',bd=0)
            label.pack()   
        
        def renameSystem(): #RENAMESYSTEM
            print "renameSystem()"
            def rename(button):
                if button == "OK":
                    if dialog.get():
                        self.systems[self.activesystem].name = dialog.get()
                        oldname = self.activesystem
                        new = self.systems.pop(self.activesystem)
                        self.systems[dialog.get()]= new
                        self.systemnames.remove(self.activesystem)
                        self.activesystem=dialog.get()
                        print self.systems
                        for link in self.systems[self.activesystem].links:
                            print "LINK: "+str(link)
                            try:
                                name = oldname+link
                                name2 = link+oldname
                            except:
                                continue
                            if name in self.links or name2 in self.links:
                                print name
                                print name2
                                print self.systems[link].links
                                self.systems[link].links.remove(oldname)
                                self.systems[link].links.append(self.activesystem) 
                                print self.systems[link].links            
                                try:
                                    self.links[self.activesystem] = self.links.get(name)
                                    del self.links[name]
                                except:
                                    self.links[self.activesystem] = self.links.get(name2)
                                    del self.links[name2]    
                                saveSystem(link)                        
                        self.systemnames.append(self.activesystem)
                        self.systemmenu.setitems(self.systemnames)
                        self.systemmenu.setvalue(self.activesystem)
                        self.map.itemconfigure(self.systems[self.activesystem].textid,text=self.activesystem)
                dialog.withdraw()
            dialog=Pmw.PromptDialog(master,
            title = 'System Name',
            label_text = 'System Name:',
            entryfield_labelpos = 'n',
            defaultbutton = 0,
            buttons = ('OK', 'Cancel'),
            command = rename)
            
        def addBody(): #ADDBODY
            print "addBody()"
            def add(button):
                print self.bodymenu.components()
                if button == "OK":
                    if dialog.get():
                        name=dialog.get()
                    else: 
                        name = "unnamed"                   
                    self.systems[self.activesystem].bodynames.append(name)
                    self.systems[self.activesystem].bodies[name]=Body(name)
                    self.bodymenu.setitems(self.systems[self.activesystem].bodynames)
                    self.bodymenu.setvalue(name)
                    updateBody(name)
                dialog.withdraw()
            dialog=Pmw.PromptDialog(master,
            title = 'Add New Body',
            label_text = 'New Body Name:',
            entryfield_labelpos = 'n',
            defaultbutton = 0,
            buttons = ('OK', 'Cancel'),
            command = add)    
            
        def delBody(): #DELBODY
            print "delBody()"
            if self.bodymenu.getvalue():
                def delete(button):
                    print self.bodymenu.components()
                    if button == "OK":                       
                        self.systems[self.activesystem].bodynames.remove(self.bodymenu.getvalue())
                        del self.systems[self.activesystem].bodies[self.bodymenu.getvalue()]
                        self.bodymenu.setitems(self.systems[self.activesystem].bodynames)
                        try:
                            self.bodymenu.setvalue(self.systems[self.activesystem].bodynames[0])
                            updateBody(self.systems[self.activesystem].bodynames[0])
                        except:
                            updateBody('')
                    dialog.withdraw()
                dialog=Pmw.Dialog(master,
                title = 'Delete Body',
                defaultbutton = 0,
                buttons = ('OK', 'Cancel'),
                command = delete,
                buttonbox_hull_bg="#373A36")
                dialog.component('buttonbox').configure(hull_borderwidth = 0, hull_relief = 'flat')
                dialog.component('buttonbox').button(0).configure(bd=0,relief='flat')
                dialog.component('buttonbox').button(1).configure(bd=0,relief='flat',highlightbackground="#667766")
                label = Tkinter.Label(dialog.component('dialogchildsite'),text='Are you sure you want to utterly destroy the land of\n' + self.bodymenu.getvalue()+', including any inhabitants it may have?',relief='flat',bd=0)
                label.pack()    
            else: pass
            
        def renameBody(): #RENAMEBODY
            print "renameBody()"
            def rename(button):
                if button == "OK":
                    if dialog.get():
                        self.systems[self.activesystem].bodynames.remove(self.bodymenu.getvalue())
                        new = self.systems[self.activesystem].bodies.pop(self.bodymenu.getvalue())
                        new.name=dialog.get()
                        self.systems[self.activesystem].bodies[dialog.get()] = new
                        self.systems[self.activesystem].bodynames.append(dialog.get())
                        self.systems[self.activesystem].bodynames.sort()
                        self.bodymenu.setitems(self.systems[self.activesystem].bodynames)
                        self.bodymenu.setvalue(dialog.get())
                dialog.withdraw()
            dialog=Pmw.PromptDialog(master,
            title = 'Rename',
            label_text = "Body's new Name:",
            entryfield_labelpos = 'n',
            defaultbutton = 0,
            buttons = ('OK', 'Cancel'),
            command = rename)    

        def getBodies(system): #GETBODIES
            print "getBodies()"
            bodies = []
            for x in self.systems.get(system).bodies:
                bodies.append(self.systems.get(system).bodies.get(x).name)
            bodies.sort()
            return bodies
            
        def makeLink(): #MAKELLINK
            print "makeLink()"
            try:
                name = self.activesystem+self.selectedsystem
                name2 = self.selectedsystem+self.activesystem
            except:
                print "LINK NOT POSSIBLE!"
            if name in self.links or name2 in self.links:
                print 'Link already exists'
            else:
                print name + " / " + name2
                self.systems[self.activesystem].links.append(self.selectedsystem)
                self.systems[self.selectedsystem].links.append(self.activesystem)
                self.links[name]=Link(name)
                self.links.get(name).coords = [self.systems[self.activesystem].location,
                                               self.systems.get(self.selectedsystem).location]
                self.links.get(name).idnum = addLine(self.links.get(name).coords)
                zoomMap()
                print self.links
                self.map.tag_lower(self.links[name].idnum,self.systems[self.activesystem].idnum)
                self.map.tag_lower(self.links[name].idnum,self.systems[self.selectedsystem].idnum)
                self.linkbox.setlist(self.systems[self.activesystem].links)
                saveSystem(self.selectedsystem)
            
        def removeLink():#REMOVELINK
            print "removeLink()"
            try:
                name = self.activesystem+self.selectedsystem
                name2 = self.selectedsystem+self.activesystem
            except:
                return 0
            if name in self.links or name2 in self.links:
                self.systems[self.activesystem].links.remove(self.selectedsystem)
                self.systems.get(self.selectedsystem).links.remove(self.activesystem)              
                try:
                    self.map.delete(self.links.get(name).idnum)
                    del self.links[name]
                except:
                    self.map.delete(self.links.get(name2).idnum)
                    del self.links[name2]
                self.linkbox.setlist(self.systems[self.activesystem].links)
                saveSystem(self.selectedsystem)
            else:
                print "Link does not exist."
                
        def setPopulation(): #SETPOPULATION
            print "setPopulation()"
            self.systems[self.activesystem].bodies[self.bodymenu.getvalue()].population = self.population.get()
            pop = 0
            for y in self.systems[self.activesystem].bodies:
                #print "Y: "+str(y)
                if y:
                    try:
                        pop += self.systems[self.activesystem].bodies[y].population
                        print "add population amount: "+str(pop)
                    except:
                        print "population exception"
                else:
                    print "population = -1"
                    pop = -1
            if len(self.systems[self.activesystem].bodies) == 0:
                pop = -1
            if pop == 0:
                self.map.itemconfigure(self.systems[self.activesystem].idnum,outline="#5BB9E8")
            elif pop == -1:
                self.map.itemconfigure(self.systems[self.activesystem].idnum,outline="white")
            elif pop > 0:
                self.map.itemconfigure(self.systems[self.activesystem].idnum,outline="blue")

        def setTech(): #SETTECH
            print "setTech()"
            self.systems[self.activesystem].bodies[self.bodymenu.getvalue()].techlevel = self.techlevel.get()

        def setParent(event): #SETPARENT
            print "setParent()"
            self.systems[self.activesystem].bodies[self.bodymenu.getvalue()].parent = self.parents.getvalue()
        
        def getCanvasFocus(): #GETCANVASFOCUS
            print "getCanvasFocus()"
            self.wasx = self.map.xview()[0]
            self.wasy= self.map.yview()[0]
        
        def focusCanvas():
            print "focusCanvas()"
            self.map.xview_moveto(self.wasx)
            self.map.yview_moveto(self.wasy)
            
        def resizeMap(): #RESIZEMAP
            print "resizeMap()"
            getCanvasFocus()
            self.map.component('canvas')['width'] = self.width
            self.map.component('canvas')['height'] = self.height
            self.center = [int(self.width/2),int(self.height/2)]
            self.map.resizescrollregion()
            focusCanvas()
        
        def zoomMap(): #ZOOMMAP
            print "zoomMap()"
            #resizeMap()
            c=self.center
            print "C ZOOM: " + str(c)
            if self.zoom < 1:
                dia = 2
                fontsize = 6
            elif self.zoom < 3:
                dia = 3
                fontsize = 6
            else:
                dia = 4
                fontsize = int(self.zoom*2)
            if self.zoom >= 7:
                fontsize = 14
            for s in self.systems:
                co = self.map.coords(self.systems.get(s).idnum)
                xc = (co[2]-co[0])+co[0]
                yc = (co[3]-co[1])+co[1]
                #if xc > self.width:
                #    difference = xc-self.width
                #    self.width=self.width+difference*2
                #if xc < 0:
                #    self.width=self.width+xc*2
                #if yc > self.height:
                #    difference = yc-self.height
                #    self.height=self.height+difference*2
                #if yc < 0:
                #    self.height=self.height+yc*2    
                x=self.systems.get(s).location[0]
                y=self.systems.get(s).location[1]
                c1=c[0]+x*self.zoom-dia
                c2=c[1]-y*self.zoom-dia
                c3=c[0]+x*self.zoom+dia
                c4=c[1]-y*self.zoom+dia
                """print s
                print x
                print y
                print c1
                print c2
                print c3
                print c4
                print self.map.coords(self.systems.get(s).idnum)"""
                self.map.coords(self.systems.get(s).idnum,c1,c2,c3,c4)
                p1=(c[0]+x*self.zoom,c[1]+12-y*self.zoom)
                self.map.coords(self.systems.get(s).textid,p1[0],p1[1])
                self.map.itemconfigure(self.systems.get(s).textid,font=("Verdana",fontsize))               
            for l in self.links:
                coords = self.links.get(l).coords
                p1=(c[0]+coords[0][0]*self.zoom,c[1]-coords[0][1]*self.zoom)
                p2=(c[0]+coords[1][0]*self.zoom,c[1]-coords[1][1]*self.zoom)
                self.map.coords(self.links.get(l).idnum, p1[0],p1[1],p2[0],p2[1])
            resizeMap()
                
        def canvasEvent(event):
            print event.type
        def canvasEvent2(event):
            print event.num
            print event.state
            print event.type
            print event.x
            print event.y
        def canvasEvent3(event):
            print event.num
            print event.state
            print event.type
            print event.x
            print event.y
            
        def zoomIn(): #ZOOMIN
            if self.zoom < 10 and self.zoom > .75:
                self.zoom += 1
                zoomMap()
            elif self.zoom >= .25 and self.zoom < 1:
                self.zoom += .25
                zoomMap()
            print "Zoom: " + str(self.zoom)
        def zoomOut(): #ZOOMOUT
            if self.zoom > .25 and self.zoom < 2:
                self.zoom -= .25
                zoomMap()
            elif self.zoom > 1 and self.zoom <=10:
                self.zoom -= 1
                zoomMap()
            print "Zoom: " + str(self.zoom)
        def canvasZoom(event): #CANVASZOOM
            print "canvasZoom()"
            print self.map.canvasx(0)
            print self.map.canvasx(500)
            print self.map.canvasy(0)
            print self.map.canvasy(500)
            self.wasx = self.map.canvasx(0)+250
            self.wasy= self.map.canvasy(0)+250
            if event.num == 4:
                zoomIn()
                edges = self.map.interior().cget('scrollregion').split()
                print edges
                self.width = int(edges[2])-int(edges[0])
                self.height = int(edges[3])-int(edges[1])
            if event.num == 5:
                zoomOut()
                edges = self.map.interior().cget('scrollregion').split()
                print edges
                self.width = int(edges[2])-int(edges[0])
                self.height = int(edges[3])-int(edges[1])
            self.messagebar.message('help','Ctrl + wheel to scroll vertical.  Shift + wheel to scroll horizontal.')
                
        def canvasScroll(event,idnum):
            if idnum == 'CB4':
                self.map.yview("scroll",-1,"unit")
            if idnum == 'CB5':
                self.map.yview("scroll",1,"unit")
            if idnum == 'SB5':
                self.map.xview("scroll",1,"unit")
            if idnum == 'SB4':
                self.map.xview("scroll",-1,"unit")
                
        def switchSystem(system):
            print "switchSystem()"
            print system
            updateAll(0,0)
            saveSystem(self.activesystem)
            updateSystem(system)

####### GUI ##########
        self.satvar=Tkinter.IntVar()
        self.astvar=Tkinter.IntVar()
        self.nebvar=Tkinter.IntVar()
        def locDist():
            print "locDist()"
            value=self.satvar.get()
            print value
            if value == 1:
                try:
                    self.bodylocation.grid_forget()
                    self.bodydistance.grid(row=0, column=0, columnspan=1, padx=10)
                    self.plocgroup.configure(tag_text="DISTANCE")
                    self.bodydistance.clear()
                    self.bodydistance.insert(0,self.systems[self.activesystem].bodies[self.bodymenu.getvalue()].distance)
                    self.systems[self.activesystem].bodies[self.bodymenu.getvalue()].sattelite=1
                    parents = []
                    for x in self.systems[self.activesystem].bodies:
                        if self.systems[self.activesystem].bodies[x].sattelite == 0:
                            parents.append(x)
                    self.parents.setitems(parents)
                    if self.systems[self.activesystem].bodies[self.bodymenu.getvalue()].parent:
                        self.parents.setvalue(self.systems[self.activesystem].bodies[self.bodymenu.getvalue()].parent)
                    else:
                        self.parents.setvalue(parents[0])
                        self.systems[self.activesystem].bodies[self.bodymenu.getvalue()].parent=parents[0]
                except:
                    self.bodydistance.grid_forget()
                    self.bodylocation.grid(row=0, column=0, columnspan=1, padx=10)
                    self.plocgroup.configure(tag_text="LOCATION")
            else:
                self.bodydistance.grid_forget()
                self.bodylocation.grid(row=0, column=0, columnspan=1, padx=10)
                self.plocgroup.configure(tag_text="LOCATION")
            
        def drawWindow(sc):
            print "drawWindow()"
            numrows=13
            self.sc=sc
            
            font8 = ("Helvetica",8)
            font10 = ("Helvetica",10)
            font11 = ("Helvetica",11)
            font12 = ("Helvetica",12)
            font13 = ("Helvetica",13)
            font14 = ("Helvetica",14)
            font16 = ("Helvetica",16)
            
            #####MAPCANVAS####
            self.canvassize = [500,500]
            self.map = Pmw.ScrolledCanvas(mapframe,
                    canvas_bg = "#000000",
                    borderframe = 1,
                    labelpos = 'n',
                    label_text = 'Venture Galaxy',
                    label_font = font14,
                    usehullsize = 1,
                    hull_width = 500,
                    hull_height = 500,
                    canvas_width=500,
                    canvas_height=500,
                    vscrollmode="static",
                    hscrollmode="static",
                    canvasmargin=250,
                    Scrollbar_troughcolor="#C4D7BF",
                    Scrollbar_activebackground="#667766")
            self.map.grid(row=0,column=0,columnspan=2,rowspan=1)
            self.map.component('canvas').bind('<1>', canvasEvent)
            self.map.component('canvas').bind('<3>', canvasEvent)
            self.map.component('canvas').bind('<Control-B1-Motion>', canvasEvent2)
            self.map.component('canvas').bind('<B3-Motion>', canvasEvent3)
            self.map.component('canvas').bind('<MouseWheel>', canvasScroll)
            self.map.component('canvas').bind('<Button-4>', canvasZoom)
            self.map.component('canvas').bind('<Button-5>', canvasZoom)
            self.map.component('canvas').bind('<Control-Button-4>', lambda o:canvasScroll(o,'CB4'))
            self.map.component('canvas').bind('<Control-Button-5>', lambda o:canvasScroll(o,'CB5'))
            self.map.component('canvas').bind('<Shift-Button-4>', lambda o:canvasScroll(o,'SB4'))
            self.map.component('canvas').bind('<Shift-Button-5>', lambda o:canvasScroll(o,'SB5'))
            self.map.component('canvas').bind('<Shift-Button-3>', addSystem)



            ###SYSTEMFRAME###
            sysgroup=Pmw.Group(optionframe,tag_text="SYSTEM",tag_font=font12)
            sysgroup.grid(row=0,column=0,sticky="n"+"w",pady=10)

            self.systemmenu = Pmw.OptionMenu(sysgroup.interior(),items=(self.systemnames),command=switchSystem,menubutton_highlightthickness=0)	
            self.systemmenu.grid(row=0, column=0, columnspan=1, padx=5)
            slocgroup = Pmw.Group(sysgroup.interior(),tag_text="LOCATION")
            slocgroup.grid(row=1, column=0, columnspan=1, sticky="w"+"e",padx=5,pady=5)
            
            self.location=Pmw.EntryField(slocgroup.interior(), entry_width=12)
            self.location.grid(row=0, column=0, columnspan=1, padx=10)
            self.location.insert(0,"0,0")
            self.location.bind('<FocusOut>', lambda o:updateAll(o,'systemlocation'))
            
            self.spacer11 = Tkinter.Label(sysgroup.interior(), text="      ", font=font12)	
            self.spacer11.grid(row=1, column=1, columnspan=1)
 
            linksgroup = Pmw.Group(sysgroup.interior(),tag_text="LINKS")
            linksgroup.grid(row=1, column=2, rowspan=2, sticky="w"+"e"+"s",padx=5,pady=5)

            self.linkbox=Pmw.ScrolledListBox(linksgroup.interior(), hull_height=36, hull_width=120, usehullsize=1,items=("Link 1","Link 2","Link 3"),Scrollbar_troughcolor="#C4D7BF")
            self.linkbox.grid(row=0, column=0, columnspan=1, padx=10)

            phenomenaframe = Tkinter.Frame(sysgroup.interior())
            phenomenaframe.grid(row=0, column=2, columnspan=1, rowspan=1, sticky="w")

            self.asteroidslabel = Tkinter.Label(phenomenaframe, text="Asteroids   ")	
            self.asteroidslabel.grid(row=0, column=0, columnspan=1, sticky="w")

            self.asteroids=Tkinter.Checkbutton(phenomenaframe,bd=0,highlightthickness=0,selectcolor="#C4D7BF",variable=self.astvar)
            self.asteroids.grid(row=0, column=1, columnspan=1, sticky="w")
            self.asteroids.bind('<FocusOut>', lambda o:updateAll(o,'asteroids'))

            self.nebulalabel = Tkinter.Label(phenomenaframe, text="Nebula     ")	
            self.nebulalabel.grid(row=1, column=0, columnspan=1, sticky="w")

            self.nebula=Tkinter.Checkbutton(phenomenaframe,bd=0,highlightthickness=0,selectcolor="#C4D7BF",variable=self.nebvar)
            self.nebula.grid(row=1, column=1, columnspan=1, sticky="w")
            self.nebula.bind('<FocusOut>', lambda o:updateAll(o,'nebula'))
            
            self.divider = Tkinter.Label(optionframe, text="  ")	
            self.divider.grid(row=0, column=1, columnspan=1)
            
            
            ###BODYFRAME###
            bodygroup=Pmw.Group(optionframe,tag_text="BODY",tag_font=font12)
            bodygroup.grid(row=1,column=0,sticky="w")
            
            self.bodymenu = Pmw.OptionMenu(bodygroup.interior(),command=updateBody,items=(getBodies(self.systemnames[0])),hull_width=40,menubutton_highlightthickness=0)	
            self.bodymenu.grid(row=0, column=0, columnspan=1, sticky="s"+"n")

            self.spacer0 = Tkinter.Label(bodygroup.interior(), text="      ", font=font12)	
            self.spacer0.grid(row=0, column=1, columnspan=1)

            self.plocgroup = Pmw.Group(bodygroup.interior(),tag_text="LOCATION")
            self.plocgroup.grid(row=1, column=0, columnspan=1, sticky="w"+"e"+"s",padx=5,pady=5)
            
            self.bodylocation=Pmw.EntryField(self.plocgroup.interior(), entry_width=12)
            self.bodylocation.grid(row=0, column=0, columnspan=1, padx=10)
            self.bodylocation.insert(0,"0,0")
            self.bodylocation.bind('<FocusOut>', lambda o:updateAll(o,'location'))
            
            self.bodydistance=Pmw.EntryField(self.plocgroup.interior(), entry_width=12)
            self.bodydistance.insert(0,"0")
            self.bodydistance.bind('<FocusOut>', lambda o:updateAll(o,'distance'))

            racegroup = Pmw.Group(bodygroup.interior(),tag_text="RACE")
            racegroup.grid(row=2, column=0, columnspan=1, sticky="w"+"e",padx=5,pady=5)
            
            self.race=Pmw.OptionMenu(racegroup.interior(), items=self.races, hull_width=200,menubutton_highlightthickness=0)
            self.race.grid(row=0, column=0, columnspan=1, padx=10)
            self.race.bind('<FocusOut>', lambda o:updateAll(o,'race'))
            
            
            satgroup = Pmw.Group(bodygroup.interior(),tag_text="SATTELITE",)
            satgroup.grid(row=3, column=0, columnspan=1, rowspan=2, sticky="w"+"e",padx=5,pady=5)
            
            self.sattelite=Tkinter.Checkbutton(satgroup.interior(),highlightthickness=0,selectcolor="#C4D7BF",command=locDist,variable=self.satvar)
            self.sattelite.grid(row=0, column=0, rowspan=1, padx=10)
            self.sattelite.bind('<FocusOut>', lambda o:updateAll(o,'sattelite'))
            
            self.parents=Pmw.OptionMenu(satgroup.interior(), items=("Body1","Body2"), labelpos="n", label_text="Parent       ",menubutton_highlightthickness=0,command=setParent)
            self.parents.grid(row=0, column=1, columnspan=1, sticky="e"+"w",padx=10,pady=2)
            self.parents.bind('<FocusOut>', lambda o:updateAll(o,'parents'))

            govgroup = Pmw.Group(bodygroup.interior(),tag_text="GOVERNMENT")
            govgroup.grid(row=3, column=2, columnspan=1, sticky="w"+"e"+"n",pady=5,padx=5)
            
            self.government=Pmw.OptionMenu(govgroup.interior(), items=("Gov2","Gov1","Gov3"), menubutton_highlightthickness=0)
            self.government.grid(row=0, column=0, columnspan=1, padx=10)
            self.government.bind('<FocusOut>', lambda o:updateAll(o,'government'))

            factiongroup = Pmw.Group(bodygroup.interior(),tag_text="FACTION")
            factiongroup.grid(row=2, column=2, columnspan=1, sticky="w"+"e",padx=5,pady=5)

            self.faction=Pmw.OptionMenu(factiongroup.interior(), items=("Fac2","Fac1","Fac3"), menubutton_highlightthickness=0)
            self.faction.grid(row=0, column=0, columnspan=1, padx=10)
            self.faction.bind('<FocusOut>', lambda o:updateAll(o,'faction'))


            popgroup = Pmw.Group(bodygroup.interior(),tag_text="POPULATION")
            popgroup.grid(row=0, column=2, columnspan=1, sticky="w"+"e",pady=5,padx=5)
            
            self.population=Tkinter.Spinbox(popgroup.interior(), from_=0,to_=10000,highlightthickness=0,repeatinterval=20,repeatdelay=200,width=5,command=setPopulation)
            self.population.grid(row=0, column=0, columnspan=1, padx=10)
            self.population.insert(500,"0")
            self.population.bind('<FocusOut>', lambda o:updateAll(o,'population'))
    
            techgroup = Pmw.Group(bodygroup.interior(),tag_text="TECH LEVEL")
            techgroup.grid(row=1, column=2, columnspan=1, sticky="w"+"e"+"s",pady=5,padx=5)
            
            self.techlevel=Tkinter.Spinbox(techgroup.interior(), from_=0,to_=100,highlightthickness=0,repeatinterval=20,repeatdelay=200,width=3,command=setTech)
            self.techlevel.grid(row=0, column=0, columnspan=1, padx=10)
            self.techlevel.insert(50,"0")
            self.techlevel.bind('<FocusOut>', lambda o:updateAll(o,'techlevel'))                     
            
            descriptiongroup = Pmw.Group(bodygroup.interior(),tag_text="DESCRIPTION")
            descriptiongroup.grid(row=5, column=0, columnspan=3, sticky="w"+"e",padx=5,pady=5)

            self.description=Tkinter.Text(descriptiongroup.interior(), width=42, height=5, wrap="word")
            self.description.grid(row=0, column=0, columnspan=1, sticky="w")
            self.description.bind('<FocusOut>', lambda o:updateAll(o,'description'))
            
            self.spacer1 = Tkinter.Label(bodygroup.interior(), text="                                  ", font=("Helvetica",12))	
            self.spacer1.grid(row=4, column=2, columnspan=1)
            
            ###BUTTONS###            
            self.addbody = Tkinter.Button(bodygroup.interior(), text="Add", command=lambda: addBody())
            self.addbody.grid(row=7,column=1,columnspan=1, sticky="n",ipadx=10)
            
            self.delbody = Tkinter.Button(bodygroup.interior(), text="Del", command=lambda: delBody())
            self.delbody.grid(row=7,column=2,columnspan=1, sticky="n"+"e",ipadx=10,padx=5)
            
            self.renamebody = Tkinter.Button(bodygroup.interior(), text="Rename", command=lambda: renameBody())
            self.renamebody.grid(row=7,column=0,columnspan=1, sticky="n",ipadx=10)
            
            #self.addsystem = Tkinter.Button(sysgroup.interior(), text="Add", command=lambda: addSystem())
            #self.addsystem.grid(row=3,column=1,columnspan=1, sticky="n",ipadx=10)
            addlabel = Tkinter.Label(sysgroup.interior(), text="          ",font=("Verdana",12))
            addlabel.grid(row=3,column=1,columnspan=1, sticky="n")
            
            self.delsystem = Tkinter.Button(sysgroup.interior(), text="Del", command=lambda: delSystem())
            self.delsystem.grid(row=3,column=2,columnspan=1, sticky="n"+"e",ipadx=10,padx=5)
            
            self.renamesystem = Tkinter.Button(sysgroup.interior(), text="Rename", command=lambda: renameSystem())
            self.renamesystem.grid(row=3,column=0,columnspan=1, sticky="n",ipadx=10)
            
            buttonframe = Tkinter.Frame(mapframe)
            buttonframe.grid(row=2,column=0,columnspan=2)
            
            self.zoomin = Tkinter.Button(buttonframe, text="Zoom In ", command=lambda: zoomIn())
            self.zoomin.grid(row=0,column=0,columnspan=1,padx=10,pady=5,sticky="e")
            
            self.zoomout = Tkinter.Button(buttonframe, text="Zoom Out", command=lambda: zoomOut())
            self.zoomout.grid(row=0,column=1,columnspan=1,padx=10,pady=5,sticky="w")
            
            self.link = Tkinter.Button(buttonframe, text=" Link ", command=lambda: makeLink())
            self.link.grid(row=0,column=2,columnspan=1,padx=10,pady=5,sticky="e")
            
            self.unlink = Tkinter.Button(buttonframe, text="Unlink", command=lambda: removeLink())
            self.unlink.grid(row=0,column=3,columnspan=1,padx=10,pady=5,sticky="w")
            
            mlabel = Tkinter.Label(mapframe,font=("Verdana",12),text="        ")
            mlabel.grid(row=3)
            
            messagetypes = { 'wait':(5,0,1,0),
                             'help':(1,10,0,0),
                             'state':(0,0,1,0)}
            
            self.messagebar = Pmw.MessageBar(mapframe,messagetypes=messagetypes,
                          hull_bg='blue',entry_readonlybackground='#667766',
                          entry_highlightbackground='#373A36',entry_highlightcolor='#373A36')
            self.messagebar.grid(row=4,column=0,columnspan=2,sticky="e"+"w"+'s',padx=1,pady=1)
            self.messagebar.message('state','This is a message bar.')

            print "End drawWindow"
        
        
        frame = Tkinter.Frame(master,width=800,height=600)
        frame.pack()

        mapframe=Tkinter.Frame(frame) #this is the frame that holds all the stock
        mapframe.grid(row=0,column=0,padx=1,pady=2,sticky="n"+"s")

        optionframe=Tkinter.Frame(frame) #this is the frame that hold the rest of the options
        optionframe.grid(row=0,column=1,padx=1,pady=2)


        drawWindow(1)
        w = int(self.map.component('canvas')['width'])
        h = int(self.map.component('canvas')['height'])
        self.center = [w/2,h/2]
        print self.center
        self.activesystem = self.lastactive = self.systemmenu.getvalue()
        print"LASTACTIVE"
        print self.lastactive
        updateSystem(self.lastactive)
        drawLinks()
        drawSystems()
        zoomMap()
        updateAll(0,0)
        
        master.protocol("WM_DELETE_WINDOW",quit)
        

    ###  END G.U.I  ###

root=Tkinter.Tk()
root.option_add ("*Frame*background", "#373A36",20 )
root.option_add ("*Button*background", "#667766",20 )
root.option_add ("*Entry*background", "#C4D7BF",20 )
root.option_add ("*Menubutton*background", "#667766",20 )
root.option_add ("*Menubutton*borderwidth", 0,20 )
root.option_add ("*Listbox*background", "#C4D7BF",20 )
root.option_add ("*Text*background", "#C4D7BF",20 )
#root.option_add ("*Scrollbar*background", "#5E6B5E",20 )
root.option_add ("*Spinbox*background", "#C4D7BF",20 )
root.option_add ("*Label*foreground", "#C4D7BF",20 )

Pmw.initialise(root)
app=MapMaker(root)
root.title("Map Maker of Destiny")
root.mainloop()
