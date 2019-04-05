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

plt.figure(figsize=(11,5))

#plt.figure(figsize=(5,5))

plt.style.use("ggplot")
cmap = matplotlib.cm.get_cmap('brg')

# Dark color maps gist_stern, brg, 
#seed(5432345)
FRAMES = 800
dt = 0.1
AGENT_RADIUS = 0.15

sim = SF_Model()


N_GROUPS = 4
RADIUS = 7
SCALE = 1.5


for i in range(N_GROUPS):
    circle = random_circle(RADIUS, SCALE)
    position = circle[0]
    destination = circle[1]
    sim.add_group(np.random.randint(2,5), position, destination, cmap(random()))
    #sim.add_group(g[i], position, destination, cmap(random()))


########## ANIMATE ############
def plt_axis(x):
    plt.ylim(-x, x)
    plt.xlim(-x, x)

fig = plt.figure(1)

ax = fig.add_subplot(1, 1, 1)

def animate(i):

    print(str(i)+"/"+str(FRAMES), end="\r")
    sim.step(dt)
    
    plt.subplot(121)
    plt.cla()
    plt.title(str(sim.amount_agents)+" Agents - "+str(N_GROUPS)+" Groups")
    plt_axis(18)

    # display_text = "Frame: " + str(i) + "/" + str(FRAMES) +"\n"+ "       "+str(round(i*dt,2)) + " s"
    # plt.text(-3, -12, display_text, bbox=dict(facecolor='red', alpha=0.5))

    for group in sim.get_groups():    
        #Group Destination    
        plt.gcf().gca().add_artist(plt.Circle(
            (group.destination[0], group.destination[1]), 0.2*len(group.agents), color=group.color, alpha = 0.2))
        
        #Group Radius
        plt.gcf().gca().add_artist(plt.Circle(
            (group.center_mass()[0], group.center_mass()[1]), group.radius(), color=group.color, alpha = 0.2))

    
    for agent in sim.get_agents():
            #Agent Trails
            ax.plot(agent.x_trail[:i+2], agent.y_trail[:i+2], linewidth=1, color = agent.color, alpha = 0.2)

            #Agent Head
            plt.gcf().gca().add_artist(plt.Circle(
                (agent.position[0], agent.position[1]), agent.radius, color=agent.color))

            #Agent Direction
            plt.arrow(agent.position[0], agent.position[1],agent.direction[0]/2,agent.direction[1]/2,fc=agent.color, ec=agent.color)



    #FUNDAMENTAL DIAGRAM
    plt.subplot(122)
    plt.title("Fundamental diagram")


    plt.ylim(0, 1.4)
    plt.xlim(0, 6)
    v = 0

    density = len(sim.get_agents())/(sim.radius()**2)

    for agent in sim.get_agents():
        v+= np.linalg.norm(agent.velocity)/len(sim.get_agents())

    #if len(sim.get_groups()) > 2:
    if i > 2:
        if not np.all(np.isclose(agent.position, agent.destination, atol=((len(agent.group.agents))*AGENT_RADIUS))):
            plt.scatter(density, v,color="midnightblue", s=5, marker="x")

    plt.xlabel(r"Density $1/m^{2}$")
    plt.ylabel(r"Average velocity $m/s$")


ani = animation.FuncAnimation(
    fig, animate, frames=FRAMES, interval=1, repeat=False)

#ani.save(str(sim.amount_agents)+"A_"+str(N_GROUPS)+"G"+str(np.random.randint(1,5000))+".gif", writer='imagemagick')

plt.show()

# Write simulation into 2 CSV Files.
#sim.write_to_CSV(FRAMES)