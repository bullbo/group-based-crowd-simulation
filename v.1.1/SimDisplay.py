import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from random import random, seed
import csv
from Utilities import random_circle
from Simulation import Simulation


plt.style.use("ggplot")
cmap = matplotlib.cm.get_cmap('nipy_spectral')
seed(5)

N_AGENTS = 2
RADIUS = 5
SCALE = 1.5
FRAMES = 200

dt = 1


sim = Simulation()

sim.add_wall(-5, 0, -1, 0)
sim.add_wall(0, 2, 2, 0)
sim.add_group(5, [8, -5], [-1, 8], cmap(random()))

for i in range(N_AGENTS):
    circle = random_circle(RADIUS, SCALE)
    position = circle[0]
    destination = circle[1]
    sim.add_agent(position, destination, cmap(random()))


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
    plt_axis(15)

    display_text = "Frame: " + str(i) + "/" + str(FRAMES)
    plt.text(-3, -10, display_text, bbox=dict(facecolor='red', alpha=0.5))

    for wall in sim.get_walls():
        plt.plot(wall.get_x(), wall.get_y(), color="black")

    for agent in sim.get_agents():
        ax.plot(agent.x_trail[:i+1], agent.y_trail[:i+1],
                linewidth=1, color=agent.color, alpha=0.3)

        # head
        plt.gcf().gca().add_artist(plt.Circle(
            (agent.x_trail[i], agent.y_trail[i]), agent.radius, color=agent.color))

        # Goal
        if agent.group_id == -1:
            plt.gcf().gca().add_artist(plt.Circle(
                (agent.destination[0], agent.destination[1]), agent.radius*4, color=agent.color, alpha = 0.3))

    for group in sim.get_groups():
        plt.gcf().gca().add_artist(plt.Circle(
            (group.destination[0], group.destination[1]), 0.6, color=group.color, alpha = 0.3))


ani = animation.FuncAnimation(
    fig, animate, frames=FRAMES, interval=1, repeat=False)


""" Save animation in either mp4 or gif. """
# ani.save('im.mp4', fps=30,  dpi=400, bitrate=-1)
#ani.save('numpy.gif',  dpi=80, writer='imagemagick')
plt.axis('equal')
plt.show()

# Write simulation into 2 CSV Files.
#sim.write_to_CSV(FRAMES, dt)




########## PLOT INSTANT ###########
# for agent in sim.get_agents():
#     plt.gcf().gca().add_artist(plt.Circle((agent.x_trail[i], agent.y_trail[i]), agent.radius, color=agent.color))
#     plt.plot(agent.x_trail, agent.y_trail, linewidth=1, color=agent.color)
# for wall in sim.get_walls():
#     plt.plot(wall.get_x(), wall.get_y(), color = "black")