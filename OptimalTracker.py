import pdb
import pygame

from pygame.locals import *
from threading import Thread

import time
import Astarsearch

from pygame.locals import*
import random

class optimaltracker:
    colors=[(0,0,0),(192,192,192),(255,255,0),(0,153,0),(255,51,51)]
    answer=[]
    def init(self,w,h):
        self.mapd=[]

        self.mapw=w

        self.maph=h

	self.maplmtx=w
	self.maplmty=h
        self.startpoint=[w/2-random.randint(-10,10),1]

        self.endpoint=[w/2,h-7]
        self.reachpoint=[w-random.randint(2,39),h-random.randint(2,29)]
        size=w*h;
        for i in range(size):
            self.mapd.append(1)
        self.mapd[(self.startpoint[1]*w)+self.startpoint[0]] = 2
        self.mapd[(self.endpoint[1]*w)+self.endpoint[0]] = 3
	for i in range(size):
		if i>=243 and i<=275:

			self.mapd[i]=-1
		if i>= 1160:
			self.mapd[i]=-1
		if i>=770 and i<=788:
			self.mapd[i]=-1
		if i>=963 and i<=995:

			self.mapd[i]=-1
		#print i
	for i in range(size):
		#print i
		if  i <= 8:
			self.mapd[243+(40*i)] = -1
			self.mapd[275+(40*i)] = -1
		if i <= 5:
			self.mapd[723+(40*i)] = -1
			self.mapd[755+(40*i)] = -1

		if  i <= 10:
			self.mapd[379+(40*i)] = -1
                if  i <= 6:
			self.mapd[370+(40*i)] = -1
			self.mapd[388+(40*i)] = -1

	self.mapd[(self.reachpoint[1]*w)+self.reachpoint[0]] = 4
        self.maprect = Rect(0,0,w*24,h*24)
	#print w,h

    def draw(self):
        x = 0
        y = 0
        rect = [0,0,24,24]
       

	for p in self.mapd:
            if p == -1 :
                p = 0
            rect[0] = x*24
            rect[1] = y*24
	    
            self.screendata.fill(self.colors[p],rect)
            x+=1
            if x>=self.mapw:
                x=0
                y+=1
	#print x,y

    def update(self,x,y,v):
        index=(y*self.mapw)+x
        if v==2: # startpoint
            if self.mapd[index] != 2 and self.mapd[index] != 3 and self.mapd[index] != -1:
                self.mapd[(self.startpoint[1]*self.mapw)+self.startpoint[0]] = 1

                self.screendata.fill(self.colors[1],(self.startpoint[0]*24,self.startpoint[1]*24,24,24))
                self.startpoint = [x,y]

                self.mapd[index] = 2
                self.screendata.fill(self.colors[2],(x*24,y*24,24,24))     

	              
        elif v == 3: # endpoint
             if self.mapd[index] != 2 and self.mapd[index] != 3 and self.mapd[index] != -1 and x < self.mapw and y < self.maph-1 and x >= 0 and y >= 0:
                self.mapd[(self.endpoint[1]*self.mapw)+self.endpoint[0]] = 1
                self.screendata.fill(self.colors[1],(self.endpoint[0]*24,self.endpoint[1]*24,24,24))
                self.endpoint = [x,y]
                self.mapd[index] = 3

                self.screendata.fill(self.colors[3],(x*24,y*24,24,24))
        else:
            if self.mapd[index] != 2 and self.mapd[index] != 3:
                if v == 0:

                    self.mapd[index] = -1
                else:
                    self.mapd[index] = v

                self.screendata.fill(self.colors[v],(x*24,y*24,24,24))


    def findPath(self):
        a=Astarsearch.Astarsearch(Astarsearch.MapLayout(self.mapd,self.mapw,self.maph))

        s=Astarsearch.MapLocation(self.startpoint[0],self.startpoint[1])

        e=Astarsearch.MapLocation(self.endpoint[0],self.endpoint[1])
        p = a.findPath(s,e)
        #e = time()
        if not p:

            print "no path exists!"
        else:
            self.answer = []
	    self.path = []

            self.answer.append((s.x*24+12,s.y*24+12))
	    self.path.append((s.x,s.y))
            for n in p.nodes:

                self.answer.append((n.location.x*24+12,n.location.y*24+12))
		self.path.append((n.location.x,n.location.y))
            self.answer.append((e.x*24+12,e.y*24+12))
	    self.path.append((e.x,e.y))
	#print e.x
	
    def loop(self):
	i=0
	q = len(self.answer)-2	
	while 1:   
	    self.update(self.path[i][0], self.path[i][1], 2)                  
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
          
                    if event.key == K_UP:

                       	if len(self.answer):
                        	self.answer=[]
				self.draw()

			x = self.endpoint[0] 
			y = self.endpoint[1] - 1

			self.update(x,y,3)

			self.findPath()

			i = 0
			self.update(self.path[i][0], self.path[i][1], 2)
			if len(self.answer):
                                pygame.draw.lines(self.screendata, (255,255,255,255), 0, self.answer)

			q = len(self.answer)-2
			
		    elif event.key == K_DOWN:

                       	if len(self.answer):
				self.answer=[]

				self.draw()
			x = self.endpoint[0] 
			y = self.endpoint[1] + 1
			self.update(x,y,3)
			self.findPath()
			i = 0
			self.update(self.path[i][0], self.path[i][1], 2)
                        if len(self.answer):
                                pygame.draw.lines(self.screendata, (255,255,255,255), 0, self.answer)
			q = len(self.answer)-2
		    elif event.key == K_LEFT:
                       	if len(self.answer):
                        	self.answer=[]
				self.draw()
			x = self.endpoint[0] - 1 
			y = self.endpoint[1]
			self.update(x,y,3)
			self.findPath()
			i = 0
			self.update(self.path[i][0], self.path[i][1], 2)
                        if len(self.answer):
                                pygame.draw.lines(self.screendata, (255,255,255,255), 0, self.answer)
			q = len(self.answer)-2
		    elif event.key == K_RIGHT:
                       	if len(self.answer):
                        	self.answer=[]
				self.draw()

			x = self.endpoint[0] + 1
			y = self.endpoint[1]

			self.update(x,y,3)

			self.findPath()
			i = 0

			self.update(self.path[i][0], self.path[i][1], 2)
                        if len(self.answer):
                                pygame.draw.lines(self.screendata, (255,255,255,255), 0, self.answer)
			q = len(self.answer)-2
		#time.sleep(.02)

	    if (self.startpoint[0] == self.endpoint[0] or self.startpoint[0] == self.endpoint[0]+1 or self.startpoint[0] == self.endpoint[0]-1) and (self.startpoint[1] == self.endpoint[1] or self.startpoint[1] == self.endpoint[1]+1 or self.startpoint[1] == self.endpoint[1]-1 ):
	    	img = pygame.image.load('over1.bmp')
		while 1:
			
			self.screendata.blit(img,(0,0))
			pygame.display.flip()
			for event in pygame.event.get():
				#self.update(self.path[i][0], self.path[i][1], 2)
				if event.type == QUIT:
				    return
				elif event.type == KEYDOWN:
			  	    if event.key == K_RETURN:
					self.run()
	    if (self.reachpoint[0] == self.endpoint[0] or self.reachpoint[0] == self.endpoint[0]+1 or self.reachpoint[0] == self.endpoint[0]-1) and (self.reachpoint[1] == self.endpoint[1] or self.reachpoint[1] == self.endpoint[1]+1 or self.reachpoint[1] == self.endpoint[1]-1 ):
		img = pygame.image.load('win1.bmp')
		while 1:
			self.screendata.blit(img,(0,0))
			pygame.display.flip()
			for event in pygame.event.get():
				#self.update(self.path[i][0], self.path[i][1], 2)
				if event.type == QUIT:
				    return
				elif event.type == KEYDOWN:
			  	    if event.key == K_RETURN:
					self.run()
		
            pygame.display.flip()
	    if i < len(self.answer)-1:
	    	i += 1
	    time.sleep(.09) 			
    def run(self):
        pygame.init()    
        self.screendata = pygame.display.set_mode((960, 800),HWSURFACE)
        pygame.display.set_caption('Optimal Tracker')
        self.screendata.fill((150,150,150))
        self.init(40,30)
        self.draw()
        self.editmode = 0

        #self.drawMenu()
	self.findPath()
	if len(self.answer):
                  pygame.draw.lines(self.screendata, (255,255,255,255), 0, self.answer)
	pygame.key.set_repeat(80,80)
	self.loop()
    	    

def main():
    optimaltracker().run()

main();
    
