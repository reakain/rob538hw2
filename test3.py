"""
Assignment 2 Reinforcement Learning

based on https://amunategui.github.io/reinforcement-learning/index.html
and https://www.redblobgames.com/pathfinding/grids/graphs.html
https://firsttimeprogrammer.blogspot.com/2016/09/getting-ai-smarter-with-q-learning.html
http://mnemstudio.org/path-finding-q-learning-tutorial.htm
https://github.com/harvitronix/reinforcement-learning-car
http://outlace.com/rlpart1.html
https://github.com/nikitasrivatsan/DeepLearningVideoGames
https://github.com/spragunr/deep_q_rl
https://blog.coast.ai/using-reinforcement-learning-in-python-to-teach-a-virtual-car-to-avoid-obstacles-6e782cc7d4c6

"""
import random	# For generating obstacles
import numpy as np
import pylab as plt
import networkx as nx


# Generating a point definition
class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.color = "White"
        self.discoveryTime = 0
        self.finishTime = 0
        self.predId = 0

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

    def setColor(self,nbr):
        self.color = nbr

    def getColor(self):
        return self.color

    def setDiscovery(self,nbr):
        self.discoveryTime = nbr

    def getDiscovery(self):
        return self.discoveryTime

    def setFinish(self,nbr):
        self.finishTime = nbr

    def getFinish(self):
        return self.finishTime

    def setPred(self,nbr):
        self.predId = nbr

    def getPred(self):
        return self.predId


# Graph class definition from a list of vertexess and edge connections
class Graph(object):
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

class GridGraph(Graph):
    def __init__(self,xdim,ydim,tid):
        super(GridGraph,self).__init__()
        for x in range(xdim):
            for y in range(ydim):
                nodeId = self.posToNodeId(x,y,xdim)
                newPositions = self.genNeighbors(x,y,xdim,ydim)
                for e in newPositions:
                    nid = self.posToNodeId(e[0],e[1],xdim)
                    self.addEdge(nodeId,nid)
        self.edgeList = self.getEdges()
        self.target = tid
        self.tStart = tid
        self.R = np.matrix(np.ones(shape=(self.numVertices,self.numVertices)))
        self.R *= -1000
        self.updateR()
        
    def reset(self):
        self.target = self.tStart
        self.updateR()

    def updateR(self):
        # assign -1 to paths and 30 to target-reaching point
        for edge in self.edgeList:
            if edge[1] == self.target:
                self.R[edge] = 30
            else:
                self.R[edge] = -1

            if edge[0] == self.target:
                self.R[edge[::-1]] = 30
            else:
                # reverse of point
                self.R[edge[::-1]]= -1
        # add goal point round trip
        self.R[self.target,self.target]= 30

    def moveTarget(self):
        choice = []
        neighbors = self.getVertex(self.target).getConnections()
        for n in neighbors:
            choice.append(n.id)
        self.target = random.choice(choice)

    def posToNodeId(self, x, y, xdim):
        return (y * xdim) + x

    def genNeighbors(self,x,y,xdim,ydim,blockCells=[]):
        newMoves = []
        moveOffsets = [(-1,0),(0,1),
                    (0,-1),(1,0)]
        for i in moveOffsets:
            newX = x + i[0]
            newY = y + i[1]
            if self.legalCoord(newX,xdim,blockCells) and \
                            self.legalCoord(newY,ydim,blockCells):
                newMoves.append((newX,newY))
        return newMoves

    def legalCoord(self, x,xdim,blockCells=[]):
        if x >= 0 and x < xdim and x not in blockCells:
            return True
        else:
            return False
    
    def getEdges(self):
        edgeList = []
        for n in self.vertList:
            for nn in self.vertList[n].getConnections():
                edge = (self.vertList[n].id,nn.id)
                if edge not in edgeList:
                    edgeList.append(edge)
        return edgeList

class QTraining:
    def __init__(self,xdim,ydim,tartgetStart,gamma):
        self.gGraph = GridGraph(xdim,ydim,tartgetStart)
        self.gamma = gamma
        self.Q = np.matrix(np.zeros([self.gGraph.numVertices,self.gGraph.numVertices]))
    
    def train(self,iterations):
        self.gGraph.reset()
        scores = []
        current_state = random.randint(0,self.gGraph.numVertices-1)
        for i in range(iterations):
            if(current_state == self.gGraph.target):
                self.gGraph.reset()
            else:
                self.gGraph.moveTarget()
                self.gGraph.updateR()
            current_state = random.randint(0,self.gGraph.numVertices-1)
            available_act = self.available_actions(current_state)
            action = self.sample_next_action(available_act)
            score = self.update(current_state, action)
            scores.append(score)
        return scores

    def run(self):
        self.gGraph.reset()
        current_state = random.randint(0,self.gGraph.numVertices-1)
        steps = [current_state]
        while current_state != self.gGraph.target:
            self.gGraph.moveTarget()
            self.gGraph.updateR()
            next_step_index = np.where(self.Q[current_state,] == np.max(self.Q[current_state,]))[1]
            
            if next_step_index.shape[0] > 1:
                next_step_index = int(np.random.choice(next_step_index, size = 1))
            else:
                next_step_index = int(next_step_index)
            
            steps.append(next_step_index)
            current_state = next_step_index
        return steps

    def available_actions(self,state):
        current_state_row = self.gGraph.R[state,]
        av_act = np.where(current_state_row >= -1)[1]
        return av_act

    def sample_next_action(self,available_actions_range):
        next_action = int(np.random.choice(available_actions_range,1))
        return next_action

    def update(self, current_state, action):
        
        max_index = np.where(self.Q[action,] == np.max(self.Q[action,]))[1]
        
        if max_index.shape[0] > 1:
            max_index = int(np.random.choice(max_index, size = 1))
        else:
            max_index = int(max_index)
        max_value = self.Q[action, max_index]
        
        self.Q[current_state, action] = self.gGraph.R[current_state, action] + self.gamma * max_value
        #print('max_value', self.gGraph.R[current_state, action] + self.gamma * max_value, flush=True)
        
        if (np.max(self.Q) > 0):
            return(np.sum(self.Q/np.max(self.Q)*100))
        else:
            return (0)


if __name__ == "__main__":
    try:
        training = QTraining(10,5,39,0.8)

        # Training
        scores = training.train(5)
            #print ('Score:', str(score), flush=True)
            
        print("Trained Q matrix:", flush=True)
        print(training.Q/np.max(training.Q)*100, flush=True)

        print("Most efficient path:", flush=True)
        print(training.run(), flush=True)

        plt.plot(scores)
        plt.show()

    except BaseException:
        import sys
        print(sys.exc_info()[0], flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)
    finally:
        print("Press Enter to continue ...")
        input()

