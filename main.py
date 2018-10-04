import numpy as np
import matplotlib.pyplot as plt


class bot:
    def __init__(self,  pos_x, pos_y,max_pos_x,max_pos_y,type):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.type = type # numerical identifier
        self.max_pos_x = max_pos_x
        self.max_pos_y = max_pos_y
        self.food = 10.0

    def move(self,delta_x,delta_y):
        if delta_x > 0 and self.pos_x < self.max_pos_x:
            self.pos_x = self.pos_x + 1
        if delta_x < 0 and self.pos_x > 0:
            self.pos_x = self.pos_x - 1

        if delta_y > 0 and self.pos_y < self.max_pos_y:
            self.pos_y = self.pos_y + 1
        if delta_y < 0 and self.pos_y > 0:
            self.pos_y = self.pos_y - 1
        self.food = self.food - 1


    def eat(self,food):
        self.food += food* (1 - self.pos_x /self.max_pos_y) #further away from the surface there is less light


class mapping:
    def __init__(self,max_pos_x,max_pos_y):
        self.food_level = np.zeros((max_pos_y,max_pos_x))
        self.time = 0
        self.max_pos_x = max_pos_x
        self.max_pos_y = max_pos_y

    def update(self,new_food): # apply gravity
        top_layer = np.zeros((1,self.max_pos_x))
        if new_food > 0:
            top_layer = np.random.dirichlet(np.ones(self.max_pos_x),size=1)*new_food
        new_levels = np.zeros((self.max_pos_y + 1, self.max_pos_x))
        new_levels[0] = top_layer
        new_levels[1:,:] = self.food_level
        new_levels[-2] = self.food_level[-2] + self.food_level[-1]
        self.food_level = new_levels[:-1,:]


    def plot_map(self):
        fig, ax = plt.subplots()
        ax.axis('off')
        fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0.01, wspace=0.01)
        Y = self.food_level
        Y -= np.min(Y)
        Y /= np.max(Y)
        Y *= 255
        Y *= 255
        ax.imshow(Y, cmap="gray")
        plt.show()




environment = mapping(30,80)

environment.update(10)
environment.update(10)

environment.update(10)

for i in range(0,70):
    environment.update(0)
environment.plot_map()
# for phase in np.linspace(0, 10*np.pi, 500):
#     line1.set_ydata(np.sin(x + phase))
#     fig.canvas.draw()
#     fig.canvas.flush_events()
print("fin")