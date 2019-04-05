import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from random import random, seed
import csv
from Utilities import random_circle, normalize
from SFModel import SF_Model
import numpy as np
from tqdm import tqdm
import time



plt.figure(figsize=(5,5))

plt.style.use("ggplot")
cmap = matplotlib.cm.get_cmap('brg')

# Dark color maps gist_stern, brg, 
seed(5432345)
FRAMES = 400
dt = 0.1
AGENT_RADIUS = 0.15
BN_width = 2


sim = SF_Model()

sim.add_wall(-10,-5, -10, 5)

sim.add_wall(-10,5, 5, 5)
sim.add_wall(-10,-5, 5, -5)

sim.add_wall(5,5, 5, BN_width/2)
sim.add_wall(5,-5, 5, -BN_width/2)

sim.add_wall(5,BN_width/2, 8, BN_width/2)
sim.add_wall(5,-BN_width/2, 8, -BN_width/2)

alpha = 2* np.pi *random()
r = 3*np.sqrt(random())

N_GROUPS = 5


for i in range(N_GROUPS):
    sim.add_group(np.random.randint(2,5), [np.random.randint(-9,0), np.random.randint(-4,4)], [4,0], cmap(random()))



########## ANIMATE ############
def plt_axis(x):
    plt.ylim(-x, x)
    plt.xlim(-x, x)

fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)

def animate(i):
    print(str(i)+"/"+str(FRAMES), end="\r")
    sim.step(dt)
    
    #plt.subplot(121)
    plt.cla()
    plt.title(str(sim.amount_agents)+" Agents - "+str(N_GROUPS)+" Groups")
    plt_axis(18)
    plt.scatter(15, 0, marker="*", color="orange", s=50)

    display_text = "Frame: " + str(i) + "/" + str(FRAMES) +"\n"+ "       "+str(round(i*dt,2)) + " s"
    plt.text(-3, -12, display_text, bbox=dict(facecolor='red', alpha=0.5))

    for wall in sim.get_walls():
        plt.plot(wall.get_x(), wall.get_y(), color="black")

    for group in sim.get_groups():    

        #Group Radius
        plt.gcf().gca().add_artist(plt.Circle(
            (group.center_mass()[0], group.center_mass()[1]), group.radius(), color=group.color, alpha = 0.1))

    
    for agent in sim.get_agents():

            if abs(agent.position[1]) < 0.55 or agent.position[0] > 5.6:
                    agent.destination = [50, 0]
            else:
                agent.destination = [4,0]
            #Agent Trails
            ax.plot(agent.x_trail[:i+2], agent.y_trail[:i+2], linewidth=1, color = agent.color, alpha = 0.2)

            #Agent Head
            plt.gcf().gca().add_artist(plt.Circle(
                (agent.position[0], agent.position[1]), agent.radius, color=agent.color))

            #Agent Direction
            plt.arrow(agent.position[0], agent.position[1],agent.direction[0]/2,agent.direction[1]/2,fc=agent.color, ec=agent.color)





ani = animation.FuncAnimation(
    fig, animate, frames=FRAMES, interval=1, repeat=False)

#ani.save(str(sim.amount_agents)+"A_"+str(N_GROUPS)+"G"+str(np.random.randint(1,5000))+".gif", writer='imagemagick')

plt.show()
