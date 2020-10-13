from random import randint

class Agent:
    def __init__(self,position,bounds):
        self.score = 0
        self.id = (position[0]-1,position[1]-1)
        self.width = bounds[0]
        self.height = bounds[1]
        self.found_T = False
        self.fail = False

    def reward(self):
        if(self.found_T):
            self.score += 30
        elif(self.fail):
            self.score = self.score - 1000
        else:
            self.score = self.score-1
        return self.score

    def move(self,target):
        if(not self.found_T):
            id = self.act(action)
            self.id = id
            self.found_T = (self.id == target)
            self.fail = not self.in_bounds(self.id)
            self.reward()

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
        
    def act(self, action):
        (x, y) = self.id
        if(action == 'n'):
            return (x,y-1)
        elif(action == 's'):
            return (x,y+1)
        elif(action == 'e'):
            return (x+1,y)
        elif(action == 'w'):
            return (x-1,y)
        else:
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
        x = x + randint(-1,1)
        y = y + randint(-1,1)
        return (x,y)
    
    def new_run(self):
        self.id = self.start_id

class RLearning:
    def __init__(self, gridDim, num_agents, targetPos):
        self.gridDim = gridDim
        self.T_start = targetPos
        self.n_agents = num_agents
        self.T = Target(targetPos, gridDim)
        agent_id = (randint(1,gridDim[0]),randint(1,gridDim[1]))
        self.agents = []
        for a in range(num_agents):
            self.agents += {Agent(agent_id,gridDim)}

    def step_time(self):
        # iterate one time step
        self.T.move()
        for agent in self.agents:
            agent.move(self.T.id)
            if(agent.found_T):
                return True
        # assign reward
        return False
    
    def run(self, training=True):
        # initialize agents and target
        agent_id = (random.randint(1,gridDim[0]),random.randint(1,gridDim[1]))
        for agent in self.agents:
            agent.new_run(agent_id)
        self.T.new_run()
        # start run
        timestep = 0
        while(not self.step_time()):
            print('Running...')
            timestep += 1
        # if training:
        # update q map as you go
        return timestep
    
    def train(self,runs):
        count = 0
        for count in range(runs):
            self.run()
