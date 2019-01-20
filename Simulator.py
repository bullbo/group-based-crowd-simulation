import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import random
from helper import *
import numpy as np
from Agent import *
from Simulation import Simulation
from Constants import *
from Wall import Wall
import csv
plt.style.use("ggplot")
cmap = matplotlib.cm.get_cmap('nipy_spectral')

sim = Simulation()

dt = 1

random.seed(1)

sim.add_wall(
    Wall(3, 3, 5, 5))

sim.add_wall(
    Wall(0, 0, 1, 1))

for i in range(N_AGENTS):
    circle = random_circle(RADIUS, SCALE)
    position = circle[0]
    destination = circle[1]
    sim.add_agent(Agent(position, destination, cmap(random.random())))

sim.add_group(2, [8, -5], [-1, 8], cmap(random.random()))


for i in range(FRAMES):
    sim.step(dt)

########## ANIMATE ############
def plt_axis(x):
    plt.ylim(-x, x)
    plt.xlim(-x, x)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


def animate(i):
    plt.cla()
    plt_axis(20)

    for wall in sim.get_walls():
        plt.plot(wall.get_x(), wall.get_y(), color = "black")

    for agent in sim.get_agents():
        ax.plot(agent.x_trail[:i+1], agent.y_trail[:i+1],
                linewidth=1, color=agent.color)
        plt.gcf().gca().add_artist(plt.Circle(
            (agent.x_trail[i], agent.y_trail[i]), agent.radius, color=agent.color))


ani = animation.FuncAnimation(
    fig, animate, frames=FRAMES, interval=1, repeat=False)


""" Save animation in either mp4 or gif. """
# ani.save('im.mp4', fps=30,  dpi=400, bitrate=-1)
#ani.save('im_with_weights.gif',  dpi=80, writer='imagemagick')


########## PLOT INSTANT ###########
# for agent in sim.get_agents():
#     plt.gcf().gca().add_artist(plt.Circle((agent.x_trail[i], agent.y_trail[i]), agent.radius, color=agent.color))
#     plt.plot(agent.x_trail, agent.y_trail, linewidth=1, color=agent.color)
# for wall in sim.get_walls():
#     plt.plot(wall.get_x(), wall.get_y(), color = "black")

plt.axis('equal')
plt.show()

# Write simulation into 2 CSV Files. 
sim.write_to_CSV(FRAMES, dt)
