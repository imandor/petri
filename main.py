import numpy as np
import matplotlib.pyplot as plt


class bot:
    def __init__(self,  pos_x, pos_y,max_pos_x,max_pos_y,type):
        self.pos_x = pos_x # starting position of the bot
        self.pos_y = pos_y # not elegant, we should use a vector
        # if the vector is written as y;x then why pass x first?
        self.type = type # numerical identifier
        self.max_pos_x = max_pos_x # this should be taken from mapping instead?
        self.max_pos_y = max_pos_y # does that mean it has to be passed explicitly?
        self.food = 10.0 # bots have 10 food stored in beginning

    def move(self,delta_x,delta_y):
        if delta_x > 0 and self.pos_x < self.max_pos_x: # way too complicated
            self.pos_x = self.pos_x + 1
        if delta_x < 0 and self.pos_x > 0:
            self.pos_x = self.pos_x - 1
        if delta_y > 0 and self.pos_y < self.max_pos_y:
            self.pos_y = self.pos_y + 1
        if delta_y < 0 and self.pos_y > 0:
            self.pos_y = self.pos_y - 1
        self.food = self.food - 1 # energy expenditure

    def eat(self,food):
        self.food += food * (1 - self.pos_x /self.max_pos_y) #further away from the surface there is less light
        # why += and then * ?
        # why is food level not reduced by bot consumption? is this photoysnthesis instead of simple ingestion?

class mapping:
    def __init__(self,max_pos_x,max_pos_y):
        self.food_level = np.zeros((max_pos_y,max_pos_x)) # no food everywhere
        self.time = 0 # starting time
        self.max_pos_x = max_pos_x # two useless variables
        self.max_pos_y = max_pos_y

    def update(self,new_food): # apply gravity: food settles one layer
        top_layer = np.zeros((1,self.max_pos_x))
        if new_food > 0: # fill a new top layer with food
            top_layer = np.random.dirichlet(np.ones(self.max_pos_x), size = 1) * new_food
        new_levels = np.zeros((self.max_pos_y + 1, self.max_pos_x))
        new_levels[0] = top_layer # this is equivalent to [0;:]? when to transpose and when not?
        new_levels[1:,:] = self.food_level # move entire table one down
        new_levels[-2] = self.food_level[-2] + self.food_level[-1] # bottom accumulates raining food
        self.food_level = new_levels[:-1,:] # copy all except for last

    def plot_map(self):
        fig, ax = plt.subplots()
        ax.axis('off')
        fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0.01, wspace=0.01)
        Y = self.food_level
        Y -= np.min(Y) # normalize plot to range 0-1
        Y /= np.max(Y)
        Y *= 255 # 16 bit grayscale ?
        Y *= 255
        ax.imshow(Y, cmap="gray", interpolation='none')
        plt.show()


environment = mapping(30,80) # initialize a mapping called "environment"

environment.update(10) # add 10 food thrice
environment.update(10)
environment.update(10)

for i in range(0,70):
    environment.update(0) # move 70 steps ahead without adding food

environment.plot_map()

# for phase in np.linspace(0, 10*np.pi, 500):
#     line1.set_ydata(np.sin(x + phase))
#     fig.canvas.draw()
#     fig.canvas.flush_events()

print("fin") # goodbye and thanks for all the food
