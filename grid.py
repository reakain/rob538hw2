import collections
import heapq
import random

class Agent:
    def __init__(self,position,bounds):
        self.score = 0
        self.id = (position[0]-1,position[1]-1)
        self.width = bounds[0]
        self.height = bounds[1]
        self.found_T = False

    def reward(self):
        if(self.found_T):
            self.score += 30
        else:
            self.score = self.score-1
        return self.score

    def move(self,target):
        if(not self.found_T):
            id = self.new_move()
            while(not self.in_bounds(id)):
                id = self.new_move()
            self.id = id
            self.found_T = (self.id == target)
            self.reward()

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
        
    def new_move(self):
        (x, y) = self.id
        x = x + random.randint(-1,1)
        y = y + random.randint(-1,1)
        return (x,y)
    
    def new_run(self,position):
        self.score = 0
        self.id = (position[0]-1,position[1]-1)
        self.found_T = False

class Target:
    def __init__(self,position,bounds):
        self.start_id = (position[0]-1,position[1]-1)
        self.id = (position[0]-1,position[1]-1)
        self.width = bounds[0]
        self.height = bounds[1]
    
    def move(self):
        id = self.new_move()
        while(not self.in_bounds(id)):
            id = self.new_move()
        self.id = id

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
        
    def new_move(self):
        (x, y) = self.id
        x = x + random.randint(-1,1)
        y = y + random.randint(-1,1)
        return (x,y)
    
    def new_run(self):
        self.id = self.start_id

'''
class SimpleGraph:
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, id):
        return self.edges[id]
		

class SquareGrid(object):
    def __init__(self, width, height, target, agents):
        self.width = width
        self.height = height
        self.walls = []
        self.target = (target[0]-1,target[1]-1)
        self.agents = agents
    
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def on_target(self, id):
        return self.target == id
    
    def passable(self, id):
        return id not in self.walls
    
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def move_target(self):
        id = self.new_move()
        while(not self.in_bounds(id)):
            id = self.new_move()
        self.target = id
        
    def new_move(self):
        (x, y) = self.target
        x = x + random.randint(-1,1)
        y = y + random.randint(-1,1)
        return (x,y)

    def get_agent_pos(self):
        pos = []
        for agent in self.agents:
            pos += {agent.id}
        return pos

    def found_T(self):
        for agent in self.agents:
            if(self.on_target(agent.id)):
                return True
        return False

    def move_agents(self):
        for agent in self.agents:
            id = agent.test_move()
            while(not self.in_bounds(id)):
                id = agent.test_move()
            agent.move(id)
'''