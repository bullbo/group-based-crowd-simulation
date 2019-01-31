import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from random import random, seed
import csv
from Utilities import random_circle
from SFModel import SF_Model


plt.style.use("ggplot")
cmap = matplotlib.cm.get_cmap('Accent')
seed(5)

N_AGENTS = 2
RADIUS = 5
SCALE = 1.5
FRAMES = 150

dt = 1


sim = SF_Model()

sim.add_wall(-5, 0, -1, 0)
sim.add_wall(0, 2, 2, 0)
sim.add_group(5, [8, -5], [-1, 8], cmap(random()))

for i in range(N_AGENTS):
    circle = random_circle(RADIUS, SCALE)
    position = circle[0]
    destination = circle[1]
    sim.add_group(1, position, destination, cmap(random()))


########## ANIMATE ############
def plt_axis(x):
    plt.ylim(-x, x)
    plt.xlim(-x, x)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

def animate(i):
    sim.step(dt)
    plt.cla()
    plt_axis(15)

    display_text = "Frame: " + str(i) + "/" + str(FRAMES)
    plt.text(-3, -10, display_text, bbox=dict(facecolor='red', alpha=0.5))

    for wall in sim.get_walls():
        plt.plot(wall.get_x(), wall.get_y(), color="black")

    for group in sim.get_groups():
        for agent in group.get_agents():
            #Agent Trails
            ax.plot(agent.x_trail[:i+2], agent.y_trail[:i+2], linewidth=1, color = agent.color, alpha = 0.2)

            #Agent Head
            plt.gcf().gca().add_artist(plt.Circle(
                (agent.position[0], agent.position[1]), agent.radius, color=agent.color))

            #Agent Direction
            plt.arrow(agent.position[0], agent.position[1],agent.direction[0]/2,agent.direction[1]/2,fc=agent.color, ec=agent.color)

            #Agent ID
            #plt.text(agent.position[0], agent.position[1], agent.id)
    
        #Group Destination    
        plt.gcf().gca().add_artist(plt.Circle(
            (group.destination[0], group.destination[1]), 0.6, color=group.color, alpha = 0.2))
        
        #Group Radius
        plt.gcf().gca().add_artist(plt.Circle(
            (group.center_mass()[0], group.center_mass()[1]), group.radius(), color=group.color, alpha = 0.2))
    

ani = animation.FuncAnimation(
    fig, animate, frames=FRAMES, interval=1, repeat=False)


""" Save animation in either mp4 or gif. """
# ani.save('im.mp4', fps=30,  dpi=400, bitrate=-1)
#ani.save('numpy.gif',  dpi=80, writer='imagemagick')
plt.axis('equal')
plt.show()

# Write simulation into 2 CSV Files.
#sim.write_to_CSV(FRAMES, dt)