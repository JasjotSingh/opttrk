import math
import pdb

class Astarsearch:

    def __init__(self,maphandler):
        self.Mhandler = maphandler
    
    def PathTrace(self,n):
        nodes = []
	nodes.insert(0,n) 
	p = n.previuosNode
        totalCost = n.movecost
	#print p      
        while 1:
            if p.previuosNode is None:
		#print p.previuosNode
                break
	    nodes.insert(0,p)
            p=p.previuosNode
            #print p.previuosNode
        return mapPath(totalCost,nodes)
           
    def getOpenNode(self):
        OpenNode = None        
        for n in self.onlist:
            if not OpenNode:
                OpenNode = n
            elif n.score<=OpenNode.score:
                OpenNode = n
        return OpenNode

    def findPath(self,begningNode,destinationNode):
        self.openlist = []
        self.onlist = []
        self.closelist = []

        end = destinationNode
        fnode = self.Mhandler.getNode(begningNode)
	nextNode = fnode 
        self.onlist.append(fnode)
        self.openlist.append(fnode.locationID)
               
        while nextNode is not None: 
            done = self.NodeHandlerAStar(nextNode,end)
            if done:                
                return self.PathTrace(done)
            nextNode=self.getOpenNode()
                
        return None

    def NodeHandlerAStar(self,node,end):        
        i = self.openlist.index(node.locationID)
        self.closelist.append(node.locationID)
	self.openlist.pop(i)
	self.onlist.pop(i)
        nodes = self.Mhandler.neighbouringNodes(node,end)
        for n in nodes:
            if n.locationID in self.openlist:
                i = self.openlist.index(n.locationID)
                onlist = self.onlist[i]
                if n.movecost<onlist.movecost:
                    self.openlist.pop(i)
		    self.onlist.pop(i)
                    self.onlist.append(n)
                    self.openlist.append(n.locationID)
	    elif n.locationID in self.closelist:
                continue
	    elif n.location == end:
                return n
            else:
                self.onlist.append(n)        
                self.openlist.append(n.locationID)
        return None


class nodeClass:
    def __init__(self,locationID,location,movecost,previuosNode=None):
        self.locationID = locationID 
	self.location = location 
        self.movecost = movecost 
        self.previuosNode = previuosNode 
        self.score = 0 
        
    def __eq__(self, n):
        if n.locationID == self.locationID:
            return 1
        else:
            return 0
class mapPath:
    def __init__(self,tCost,nodes):
        self.tCost = tCost
	self.nodes = nodes
      
class MapLocation:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, l):
        if l.x == self.x and l.y == self.y:
            return 1
        else:
            return 0

class MapLayout:
    def __init__(self,mapdata,width,height):
        self.w = width
        self.h = height
	self.m = mapdata

    def neighbouringNodes(self, currentNode, destination):   
        result = []
        currentLocation = currentNode.location
        destinationLocation = destination
        
        n = self.NodeCal(currentLocation.x+1,currentLocation.y,currentNode,destinationLocation.x,destinationLocation.y)
        if n: result.append(n)
        n = self.NodeCal(currentLocation.x-1,currentLocation.y,currentNode,destinationLocation.x,destinationLocation.y)
        if n: result.append(n)
        n = self.NodeCal(currentLocation.x,currentLocation.y+1,currentNode,destinationLocation.x,destinationLocation.y)
        if n: result.append(n)
        n = self.NodeCal(currentLocation.x,currentLocation.y-1,currentNode,destinationLocation.x,destinationLocation.y)
        if n: result.append(n)
	n = self.NodeCal(currentLocation.x+1,currentLocation.y+1,currentNode,destinationLocation.x,destinationLocation.y)
        if n: result.append(n)
        n = self.NodeCal(currentLocation.x-1,currentLocation.y-1,currentNode,destinationLocation.x,destinationLocation.y)
        if n: result.append(n)
	n = self.NodeCal(currentLocation.x+1,currentLocation.y-1,currentNode,destinationLocation.x,destinationLocation.y)
        if n: result.append(n)
        n = self.NodeCal(currentLocation.x-1,currentLocation.y+1,currentNode,destinationLocation.x,destinationLocation.y)
        if n: result.append(n)
	                
        return result

    def getNode(self, location):
        x = location.x
        y = location.y
        if x<0 or x>=self.w or y<0 or y>=self.h:
            return None
        stepCost = self.m[(y*self.w)+x]
        if stepCost == -1 or stepCost == 4:
            return None
        return nodeClass(((y*self.w)+x),location,stepCost)                

    def NodeCal(self,x,y,fromnode,x_destination,y_destination):
        n = self.getNode(MapLocation(x,y))
        if n:
            dx = max(x,x_destination) - min(x,x_destination)
            dy = max(y,y_destination) - min(y,y_destination)
            heuristic = math.sqrt((dx*dx)+(dy*dy))
            n.movecost += fromnode.movecost                                   
            n.score = n.movecost+heuristic
            n.previuosNode=fromnode
            return n
        return None    
